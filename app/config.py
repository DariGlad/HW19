class Config:
    DEBUG = True  # Режим DEBUG
    SECRET_HERE = '249y823r9v8238r9u'  # секрет здесь
    JSON_AS_ASCII = False  # Отключение ASCII
    SQLALCHEMY_DATABASE_URI = "sqlite:///movies.db"  # Путь к базе данных
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSONIFY_PRETTYPRINT_REGULAR = True  # Построчное отображение json данных
    RESTX_JSON = {"ensure_ascii": False}
