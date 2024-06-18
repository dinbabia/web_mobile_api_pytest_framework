from global_utils.src.my_utils.api.project_name_api.client.project_request_handler import ProjectRequestHandler
from requests.models import Response


class ProfileResources:
    def __init__(self):
        self.request_handler = ProjectRequestHandler()

    def get_profile(self, profile_email) -> Response:
        return self.request_handler.get(f"/profile/?email={profile_email}")

    def patch_profile(self, payload: dict = {}) -> Response:
        return self.request_handler.patch("/profile/", json=payload)

    def set_request_headers(self, headers) -> None:
        self.request_handler.set_headers(headers)
