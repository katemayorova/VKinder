class User:
    def __init__(self,
                 user_id: str,
                 name: str,
                 surname: str,
                 city: str,
                 sex: str,
                 relation: str,
                 top_photos=None
                 ):
        if top_photos is None:
            top_photos = []
        self.id = user_id
        self.name = name
        self.surname = surname
        self.top_photos = top_photos
        self.city = city
        self.sex = sex
        self.relation = relation
