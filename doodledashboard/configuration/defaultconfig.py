import pkgutil

from doodledashboard.configuration.config import InvalidConfigurationException
from doodledashboard.datafeeds.datetime import DateTimeFeedSection
from doodledashboard.datafeeds.rss import RssFeedSection
from doodledashboard.datafeeds.slack import SlackFeedSection
from doodledashboard.datafeeds.text import TextFeedSection
from doodledashboard.filters.contains_text import ContainsTextFilterSection
from doodledashboard.filters.matches_regex import MatchesRegexFilterSection
from doodledashboard.handlers.image.image import ImageMessageHandlerConfigCreator, FileDownloader
from doodledashboard.handlers.text.text import TextHandlerConfigCreator


class FullConfigCollection:

    def __init__(self, state_storage):
        self._state_storage = state_storage

    def configure(self, dashboard_config):
        dashboard_config.add_available_displays(FullConfigCollection._find_displays())
        dashboard_config.add_data_feed_creators(FullConfigCollection._get_data_feed_creators())
        dashboard_config.add_handler_creators(FullConfigCollection._get_handler_creators(self._state_storage))
        dashboard_config.add_filter_creators(FullConfigCollection._get_filter_creators())

    @staticmethod
    def _find_displays():
        from doodledashboard.displays.consoledisplay import ConsoleDisplay
        displays = [ConsoleDisplay]

        if pkgutil.find_loader("papirus"):
            from doodledashboard.displays.papirusdisplay import PapirusDisplay
            displays.append(PapirusDisplay)

        return FullConfigCollection._validate_displays(displays)

    @staticmethod
    def _validate_displays(displays):
        from doodledashboard.displays.display import Display
        for display in displays:
            if not issubclass(display, Display):
                raise InvalidConfigurationException(
                    "Display loaded does not implement Display base class. Contact the Display's creator"
                )
        return displays

    @staticmethod
    def _get_data_feed_creators():
        return [
            RssFeedSection(),
            SlackFeedSection(),
            DateTimeFeedSection(),
            TextFeedSection()
        ]

    @staticmethod
    def _get_handler_creators(key_value_store):
        return [
            ImageMessageHandlerConfigCreator(key_value_store, FileDownloader()),
            TextHandlerConfigCreator(key_value_store)
        ]

    @staticmethod
    def _get_filter_creators():
        return [
            MatchesRegexFilterSection(),
            ContainsTextFilterSection()
        ]


class DatafeedConfigCollection:

    def __init__(self):
        pass

    def configure(self, dashboard_config):
        dashboard_config.add_data_feed_creators(FullConfigCollection._get_data_feed_creators())

    @staticmethod
    def _get_data_source_creators():
        return [
            RssFeedSection(),
            SlackFeedSection(),
            DateTimeFeedSection(),
            TextFeedSection()
        ]
