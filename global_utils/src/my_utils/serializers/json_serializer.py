import json


def data_json_serializer(data_to_serialize) -> str:
    return json.dumps(data_to_serialize, separators=(",", ":"))
