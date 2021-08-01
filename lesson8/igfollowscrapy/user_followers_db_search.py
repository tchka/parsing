from pymongo import MongoClient

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "ig"
MONGO_COLLECTION = "user_follow"


def user_follow_search(username, status):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        data = []
        cursor = collection.find({
            "username": username,
            "status": status,
        })
        for doc in cursor:
            data.append(doc)

    return data


if __name__ == '__main__':

    username = input("Введите имя пользователя: ")
    data_following = user_follow_search(username, "following")
    data_follower = user_follow_search(username, "follower")
    print(f"Подписки ({len(data_following)}): ")
    for user in data_following:
        print(user["follow_username"], end=", ")
    print(' ')
    print(f"Подписчики:  ({len(data_follower)})")
    for user in data_follower:
        print(user["follow_username"], end=", ")
