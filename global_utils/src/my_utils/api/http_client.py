import requests
from requests.adapters import HTTPAdapter, Retry


class HttpClient:
    def __init__(self, retries=5, backoff_factor=0.5, timeout=40.0):
        self.session = self._create_session(retries, backoff_factor)
        self.timeout = timeout
        self.headers = {}

    def _create_session(self, retries, backoff_factor):
        session = requests.Session()

        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _handle_response(self, response):
        try:
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        return None

    def set_headers(self, headers: dict):
        if headers == {}:
            self.headers.clear()
        else:
            self.headers.update(headers)

    def request(self, method, url, **kwargs):
        try:
            response = self.session.request(
                method,
                url,
                headers=self.headers,
                timeout=self.timeout,
                **kwargs
            )
            return self._handle_response(response)
        except Exception as err:
            print(f"An error occurred: {err}")
            return None
