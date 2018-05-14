import re

from doodledashboard.configuration.config import MissingRequiredOptionException
from doodledashboard.filters.filter import MessageFilter, FilterConfigCreator


class MessageMatchesRegexFilter(MessageFilter):
    def __init__(self, regex):
        MessageFilter.__init__(self)
        self._regex = re.compile(regex, re.IGNORECASE)

    def do_filter(self, messages):
        return [m for m in messages if self._regex.search(m.get_text())]

    def get_pattern(self):
        return self._regex.pattern


class MessageMatchesRegexTextFilterCreator(FilterConfigCreator):
    def __init__(self):
        FilterConfigCreator.__init__(self)

    def creates_for_id(self, filter_id):
        return filter_id == "message-matches-regex"

    def create_item(self, config_section):
        if "pattern" not in config_section:
            raise MissingRequiredOptionException("Expected 'pattern' option to exist")

        return MessageMatchesRegexFilter(str(config_section["pattern"]))