
from __future__ import annotations
from typing import Dict, Any


class ServiceToBook:

    def __init__(self) -> None:
        self.id = None
        self.price = None
        self.duration = None

    def __call__(self) -> Dict[str, Any]:
        service_to_book_attributes = {
            "id": self.id,
            "price": self.price,
            "duration": self.duration,
        }
        return {key: value for key, value in service_to_book_attributes.items() if (value is not None)}


class ServiceToBookBuilder:
    def __init__(self) -> None:
        self.service = ServiceToBook()

    def set_id(self, id: str) -> ServiceToBookBuilder:
        self.service.id = id
        return self

    def set_price(self, price: str) -> ServiceToBookBuilder:
        self.service.price = price
        return self

    def set_duration(self, duration: int) -> ServiceToBookBuilder:
        self.service.duration = duration
        return self

    def build(self) -> ServiceToBook:
        return self.service


class ServiceToBookDirector:

    def __init__(self, user_profile_id: str) -> None:
        self._user_profile_id = user_profile_id
        self._builder = ServiceToBookBuilder()
        self._get_name_and_id_of_services()

    def _get_name_and_id_of_services(self) -> None:
        # INSERT HERE. GET ALL NAME AND ID OF SERVICES. Possibly from an API.
        pass

    def construct_15(self) -> ServiceToBook:
        service_name_to_book = "15 mins service"
        for name, id in self.name_and_id_of_services.items():
            if name == service_name_to_book:
                self._builder.set_id(id).set_price("5.00").set_duration(15)
                return self._builder.build()

    def construct_30(self) -> ServiceToBook:
        service_name_to_book = "30 mins service"
        for name, id in self.name_and_id_of_services.items():
            if name == service_name_to_book:
                self._builder.set_id(id).set_price("10.00").set_duration(30)
                return self._builder.build()

    def get_duration(self) -> int:
        return self._builder.service.duration
