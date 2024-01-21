# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from tfmkt_scraper.utils import convert_mv, convert_item_str_to_int

class TfmktScraperPipeline:
    def process_item(self, item, spider):

        return item
