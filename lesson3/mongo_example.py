from pprint import pprint

from bson import ObjectId
from pymongo import MongoClient

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "posts"
MONGO_COLLECTION = "news_posts"


def print_mongo_objects(cursor):
    for item in cursor:
        pprint(item)


with MongoClient(MONGO_HOST, MONGO_PORT) as client:
    post_doc = {
        "title": "New weather record",
        "rating": 255,
        "_id": ObjectId("60eb3f09d234c048bcf5cdcc")
    }
    post_docs = [
        {
            "title": "News political",
            "rating": 11,
        },
        {
            "title": "New weather record",
            "rating": 255,
        },
        {
            "title": "COVID-19",
            "rating": 7,
        }
    ]

    db = client[MONGO_DB]
    news = db[MONGO_COLLECTION]

    # 1. Create
    # news.insert_one(post_doc)
    # news.insert_many(post_docs)

    # 2. Read

    # cursor = news.find({})

    # cursor = news.find({
    #     "title": "New weather record"
    # })
    #
    # cursor = news.find({
    #     "rating": {"$gt": 10}
    # })
    # cursor = news.find({
    #     "$or": [
    #         {"rating": {"$gt": 10}},
    #         {"rating": {"$lte": 11}},
    #     ]
    # }).limit(2)
    # cursor = news.find({
    #     "$or": [
    #         {"rating": {"$gt": 10}},
    #         {"rating": {"$lte": 11}},
    #     ]
    # }).sort("rating", direction=-1).limit(2)

    # 3. Update
    # my_filter = {
    #     "title": "New weather record"
    # }
    # my_update = {
    #     "$set":
    #         {
    #             "rating": 17,
    #         }
    #     }
    #
    # news.update_one(my_filter, my_update)

    # news.drop()
    # client.drop_database(MONGO_DB)

    cursor = news.find({})
    # data = []
    # for doc in cursor:
    #     data.append(doc)

    data = list(cursor)

    print(len(data))

    # print_mongo_objects(cursor)
