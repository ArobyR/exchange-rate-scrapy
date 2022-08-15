import pymongo

from scrapy.exceptions import DropItem

from itemadapter import ItemAdapter


class MongoDBPipeline(object):
    def __init__(self, mongo_uri, mongo_db, mongo_coll):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_coll = mongo_coll

    @classmethod
    def from_crawler(cls, crawler):

        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "testing"),
            mongo_coll=crawler.settings.get("MONGO_COLL_RATES", "rate"),
        )
        
    def open_spider(self, spider):
        """Connect to MongoDB when the spider is opened."""
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_coll]        

    def close_spider(self, spider):
        """Close the connection to MongoDB when the spider is closed."""
        self.client.close()
    
    def process_item(self, item, spider):
        item_dict = ItemAdapter(item).asdict()
        self.collection.insert_one(item_dict)
        return item    
    
    # def process_item(self, item, spider):
    #     valid = True
    #     for data in item:
    #         if not data:
    #             valid = False
    #             raise DropItem("Missing {0}".format(data))
    #     if valid:
    #         self.collection.insert(dict(item))
    #         # log.msg("Rate added to MongoDB database!",
    #         #         level=log.DEBUG, spider=spider)
    #     return item
