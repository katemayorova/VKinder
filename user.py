from dataclasses import dataclass


@dataclass
class User:
    SEX_MAPPING = {
        "м": 2,
        "ж": 1
    }
    SEX_MAPPING_REVERSE = {
        1: "ж",
        2: "м"
    }
    vk_id: str
    name: str
    surname: str
    city: str
    sex: str
    relation: str
    top_photos = None
