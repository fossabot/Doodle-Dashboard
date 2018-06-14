Feature: Configuration loads external displays

    Scenario: Config printed showing display added to static loader
      Given I load an external display
      And I have the configuration
         """
         interval: 0
         display: test-display
         """
      When I call 'start --once config.yml'
      Then the status code is 0
      And the output is
         """
         Interval: 0
         Display loaded: test-display
         0 data sources loaded
         0 notifications loaded
         Dashboard running...

         """

    Scenario: Display without functionality required by notification causes error
      Given I load an external display
      And I have the configuration
         """
         interval: 0
         display: test-display
         notifications:
         - title: Dummy Handler
           handler: text-handler
         """
      When I call 'start --once config.yml'
      Then the status code is 1
      And the output is
         """
         Error reading configuration file 'config.yml':
         Display 'test-display' is missing the following functionality required by the notification 'Displays entities using: Text handler':
          - CanWriteText
         Aborted!

         """