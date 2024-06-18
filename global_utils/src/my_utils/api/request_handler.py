import time
from my_utils.api.http_client import HttpClient
from requests.models import Response

from my_utils.custom_logger import SingletonLogger

_log = SingletonLogger.get_logger()


class RequestHandler:
    def __init__(self, base_url, http_client=None):
        self.base_url = base_url
        self.http_client = http_client or HttpClient()
        self.debug_mode = False

    def _prepare_url(self, endpoint):
        return f"{self.base_url}{endpoint}"

    def _sleep(self, duration):
        time.sleep(duration)

    def _log_request(self, method, url, kwargs):
        if self.debug_mode:
            _log.info(f"[[[ {method} ]]] | '{url}'")
            _log.info(f"HEADERS: {self.http_client.headers}")
            _log.info(f"DATA: {kwargs}")

    def _log_response(self, response: Response):
        if self.debug_mode:
            _log.info(f"[{response}]")
            _log.info(f"[{response.status_code}]")

    def set_debug_mode(self, debug_mode):
        self.debug_mode = debug_mode

    def set_headers(self, headers):
        self.http_client.set_headers(headers)

    def send_request(self, method, endpoint, sleep_duration, **kwargs):
        url = self._prepare_url(endpoint)
        self._log_request(method, endpoint, kwargs)
        response = self.http_client.request(method, url, **kwargs)

        self._sleep(sleep_duration)
        self._log_response(response)
        return response

    def get(self, endpoint, sleep_duration=5, params=None, **kwargs):
        return self.send_request('GET', endpoint, sleep_duration, params=params, **kwargs)

    def post(self, endpoint, sleep_duration=5, data=None, json=None, **kwargs):
        return self.send_request('POST', endpoint, sleep_duration, data=data, json=json, **kwargs)

    def patch(self, endpoint, sleep_duration=5, data=None, json=None, **kwargs):
        return self.send_request('PATCH', endpoint, sleep_duration, data=data, json=json, **kwargs)

    def put(self, endpoint, sleep_duration=5, data=None, json=None, **kwargs):
        return self.send_request('PUT', endpoint, sleep_duration, data=data, json=json, **kwargs)

    def delete(self, endpoint, sleep_duration=5, **kwargs):
        return self.send_request('DELETE', endpoint, sleep_duration, **kwargs)