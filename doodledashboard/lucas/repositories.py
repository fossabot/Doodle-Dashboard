import logging

from requests.exceptions import ConnectionError


class MessageModel:
    def __init__(self, text):
        self._text = text

    def get_text(self):
        return self._text


class Repository:
    def __init__(self):
        pass

    def get_latest_messages(self):
        raise NotImplementedError('Implement this method')


class SlackRepository(Repository):
    _channel = None

    def __init__(self, client, channel_name):
        Repository.__init__(self)
        self._client = client
        self._channel_name = channel_name
        self._logger = logging.getLogger('raspberry_pi_dashboard.SlackRepository')
        self._connected = False
        self._connected_previously = False

    def get_latest_messages(self):
        if not self._connected:
            self._connected = self._try_connect()

        if not self._channel:
            self._channel = self._try_find_channel(self._channel_name)

        if not self._test_connection():
            self._logger.info('Failed to connect to Slack, will try again next time around')
            self._connected = False
            return []

        events = self._client.rtm_read()
        events = SlackRepository._filter_events_by_channel(self._channel, events)
        events = SlackRepository._filter_events_by_type(events, 'message')
        events = SlackRepository._filter_events_with_text(events)

        return [MessageModel(event['text']) for event in events]

    def _test_connection(self):
        try:
            self._client.api_call("api.test")
            return True
        except ConnectionError:
            return False

    def _try_connect(self):
        connected = self._client.rtm_connect(with_team_state=False)
        if connected:
            self._logger.info('Connected to Slack. Huzzah!')
            self._connected_previously = True
        else:
            if self._connected_previously:
                message = 'Failed to connect to Slack. I\'ve connected before so likely the internet is just down.'
            else:
                message = 'Failed to connect to Slack. Is the Slack token correct?'

            self._logger.info(message)

        return connected

    def _try_find_channel(self, channel_name):
        channel = None
        try:
            channel = self._find_channel(channel_name)
            if not channel:
                self._logger.info(
                    "Failed to find Slack channel '%s'. Have you provided created it?" % self._channel_name)
        except ConnectionError:
            pass

        return channel

    def _find_channel(self, channel_name):
        channel_list = self._client.api_call("channels.list", exclude_archived=1)
        return next(iter([c for c in channel_list['channels'] if c['name'] == channel_name]), None)

    @staticmethod
    def _filter_events_with_text(events):
        return [e for e in events if 'text' in e]

    @staticmethod
    def _filter_events_by_type(events, type):
        return [e for e in events if e['type'] == type]

    @staticmethod
    def _filter_events_by_channel(channel, events):
        return [e for e in events if 'channel' in e and e['channel'] == channel['id']]