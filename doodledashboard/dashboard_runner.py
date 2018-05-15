import itertools
import logging
import time


class Dashboard:
    def __init__(self, interval, display, data_feeds, notifications):
        self._interval = interval
        self._display = display
        self._data_feeds = data_feeds
        self._notifications = notifications

    def get_interval(self):
        return self._interval

    def get_display(self):
        return self._display

    def get_data_feeds(self):
        return self._data_feeds

    def get_notifications(self):
        return self._notifications


class Notification:
    def __init__(self, handler):
        self._handler = handler
        self._filter_chain = None
        self._logger = logging.getLogger("doodledashboard")

    def set_filter_chain(self, filter_chain):
        self._filter_chain = filter_chain

    def handle_entities(self, display, messages):
        filtered_entities = self._filter_entities(messages)

        self._logger.debug("Entities before filters: %s", [messages])
        self._logger.debug("Entities after filters: %s", [filtered_entities])

        self._handler.update(filtered_entities)
        self._handler.draw(display)

    def _filter_entities(self, entities):
        if self._filter_chain:
            return self._filter_chain.filter(entities)
        else:
            return entities

    def __str__(self):
        return "Displays entities using: %s" % str(self._handler)


class DashboardRunner:
    def __init__(self, dashboard):
        self._logger = logging.getLogger("doodledashboard.Dashboard")
        self._dashboard = dashboard

    def run(self):
        entities = []
        for notification in itertools.cycle(self._dashboard.get_notifications()):

            if self._is_at_beginning(notification):
                self._logger.info("At beginning of notification cycle, will poll data sources")
                entities = self._collect_all_entities(self._dashboard.get_data_feeds())
                self._logger.info("%s entities collected" % len(entities))

            notification.handle_entities(self._dashboard.get_display(), entities)
            time.sleep(self._dashboard.get_interval())

    def _is_at_beginning(self, notification):
        return notification is self._dashboard.get_notifications()[0]

    @staticmethod
    def _collect_all_entities(repositories):
        entities = []
        for repository in repositories:
            entities += repository.get_latest_entities()

        return entities
