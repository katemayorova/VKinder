from dataclasses import dataclass


@dataclass
class User:
    vk_id: str
    name: str
    surname: str
    city: str
    sex: str
    relation: str
    top_photos = None
