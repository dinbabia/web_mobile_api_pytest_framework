import sys
from requests.models import Response
from requests.structures import CaseInsensitiveDict


class ResponseBaseActions:

    def __init__(self) -> None:
        self._response: Response

    def _get_status(self) -> int:
        return self._response.status_code

    def _get_json(self) -> dict:
        return self._response.json()

    def _get_results(self):
        try:
            return self._response.json()['results']
        except KeyError:
            print(f"[ERROR] {self._response.json()}")
            sys.exit(1)

    def _get_headers(self) -> CaseInsensitiveDict[str]:
        return self._response.headers
