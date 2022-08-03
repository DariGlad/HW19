class DirectorsService:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        """ Возвращает данные всех режиссёров """

        return self.dao.get_all()

    def get_one(self, director_id):
        """ Возвращает данные по id режиссёра """

        return self.dao.get_one(director_id)

    def check_is_dict(self, data):
        """ Проверяем, являются ли данные словарём """

        return self.dao.check_is_dict(data)

    def create(self, data):
        """ Создание данных нового режиссёра """

        return self.dao.create(data)

    def update(self, director_id, data):
        """ Обновление данных режиссёра по id """

        director = self.get_one(director_id)
        director.id = data.get("id")
        director.name = data.get("name")
        return self.dao.update(director)

    def update_partial(self, director_id, data):
        """ Частичное обновление данных режиссёра по id """

        director = self.get_one(director_id)
        if "id" in data:
            director.id = data.get("id")
        if "name" in data:
            director.name = data.get("name")
        return self.dao.update(director)

    def delete(self, director_id):
        """ Удаление данных режиссёра по id """

        self.dao.delete(director_id)
