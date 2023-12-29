def insert_into_mongodb(groups, collection):
    for group in groups:
        collection.update_one({'id': group['id']}, {'$set': group}, upsert=True)


def retrieve_from_mongodb(collection, group_id, before_time):
    query = {
        'group_id': group_id,
    }
    if before_time != None:
        query['created_at'] = {'$gt': before_time}

    groups_cursor = collection.find(query)
    return list(groups_cursor)