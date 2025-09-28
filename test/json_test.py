from flask import json

from src.utils.resp import default_serializer


class CustomClass02:
    def __init__(self):
        self.data: str = "example"

class CustomClass:
    def __init__(self):
        self.data: dict[str, CustomClass02] = {
            "key1": CustomClass02(),
            "key2": CustomClass02()
        }


if __name__ == '__main__':
    custom_obj = CustomClass()
    payload = {
            "code": 123,
            "message": "dsda",
            "data": custom_obj
        }
    
    print(json.dumps(payload, default=default_serializer, ensure_ascii=False))