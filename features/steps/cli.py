from behave import given, when, then, Then
from click.testing import CliRunner
from sure import expect

from doodledashboard.cli import view, start, list


@given("I have the configuration called '{config_filename}'")
def _given_i_have_the_configuration_x(context, config_filename):
    if "dashboard_local_configs" not in context:
        context.dashboard_local_configs = {}

    context.dashboard_local_configs[config_filename] = context.text


@given("I have the remote configuration")
def _given_i_have_the_remote_configuration_x(context):
    context.file_host.host_file(context.text)


@Then("I stop all servers")
def _i_stop_all_servers(context):
    for server in context.dashboard_remote_config_servers:
        server.stop()


@when("I call 'list {arguments}'")
def _when_i_call_list_x(context, arguments):
    arguments = arguments.split(" ")

    runner = CliRunner()
    context.runner_result = runner.invoke(list, arguments, catch_exceptions=False)


@when("I call 'start {arguments} {configs}'")
def _when_i_call_start_x_x(context, arguments, configs):
    _i_call_x_x_config_yml(context, start, arguments, configs)


@when("I call 'view {arguments} {configs}'")
def _when_i_call_view_x_x(context, arguments, configs):
    _i_call_x_x_config_yml(context, view, arguments, configs)


def _i_call_x_x_config_yml(context, cli_command, arguments, configs):
    if "file_host" in context:
        urls = " ".join(context.file_host.get_all_urls())
        configs = configs.replace("%REMOTE_URLS%", urls)

    configs = configs.split(" ")
    arguments = arguments.split(" ")
    arguments += configs

    runner = CliRunner()
    with runner.isolated_filesystem():
        for filename in configs:
            if "dashboard_local_configs" in context and filename in context.dashboard_local_configs:
                with open(filename, "w") as f:
                    f.write(context.dashboard_local_configs[filename])

        context.runner_result = runner.invoke(cli_command, arguments, catch_exceptions=False)


@then('the output is')
def _the_output_is_x(context):
    cli_output = context.runner_result.output
    expect(cli_output).should_not.be.different_of(context.text)


@then('the status code is {code:d}')
def _the_status_code_is_x(context, code):
    cli_exit_code = context.runner_result.exit_code
    expect(cli_exit_code).should.equal(code)
