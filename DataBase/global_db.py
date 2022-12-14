from pymongo import MongoClient
LOGIN = ''
PASSWORD = ''
cluster = MongoClient(
    f'mongodb+srv://{LOGIN}:{PASSWORD}@cluster0.h3myb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
)


def check_db():
    try:
        cluster.server_info()
        return True
    except Exception as exc:
        print(exc)
        return False


DB_GAME = cluster.Goodie.economic
DB_SERVER_SETTINGS = cluster.Goodie.settings
DB_IDEA_MEMBERS = cluster.Goodie.idea
ONLINE = cluster.Goodie.online_players
LOGS_ERROR = cluster.Goodie.logs
