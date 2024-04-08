# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from loguru import logger

from .utils import convert_jp_dates, convert_duration


class JpboxPipeline:
    @logger.catch
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # jp_duration (convert to minutes)
        jp_duration = adapter.get("jp_duration")
        if jp_duration is not None:
            adapter["jp_duration"] = convert_duration(jp_duration)
        else:
            adapter["jp_duration"] = None       
    
        # jp_release (convert it to format 'YYYY-MM-DD')
        jp_release = adapter.get("jp_release")
        if jp_release is not None:
            adapter["jp_release"] = convert_jp_dates(jp_release)
        else:
            adapter["jp_release"] = None

        # jp_distributors
        jp_distributors = adapter.get("jp_distributors")
        try:
            jp_distributors = [elem.strip() for elem in jp_distributors]
            adapter["jp_distributors"] = "|".join(jp_distributors)
        except BaseException:
            adapter["jp_distributors"] = None 

        return item
