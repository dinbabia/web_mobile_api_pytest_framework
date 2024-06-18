from my_utils.api.request_handler import RequestHandler
from my_utils import variables


class ProjectRequestHandler(RequestHandler):
    def __init__(self):
        super().__init__(base_url=variables.DOMAIN)
        self.set_headers(variables.HEADERS)
        self.set_debug_mode(variables.API_DEBUG_MODE)
