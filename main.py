from config_loader import config_loader
from NotionClient import NotionClient
from NotionBlock import NotionBlock
from RssHandler import RSSHandle

from pprint import pprint
import yaml

def main():
    notionclient = NotionClient(*config_loader())
    result = notionclient.get_choose_rss_sources()
    page_id = [item["id"] for item in result]
    feed_url = [item["properties"]["Feed Url"]["url"] for item in result]
    icon_url= [item["icon"]["custom_emoji"]["url"] for item in result]
    rss_handle = RSSHandle("")
    for i in range(len(page_id)):
        rss_handle.update(feed_url[i])
        feed_info = rss_handle.get_feed_info()
        if feed_info:
            notionclient.update_rss_status(page_id[i], "Active")
            notionclient.update_database_feed(page_id[i], feed_info["title"], feed_info["link"], feed_info["description"])
            
            articles = rss_handle.get_articles()
            for article in articles:
                # article["content"] = []   # test for empty content
                notionclient.cre_in_database_paper(icon_url[i], article["title"], article["published"], article["link"], article["content"], page_id[i])

                print(f"Article {article['title']} uploaded")

        else:
            notionclient.update_rss_status(page_id[i], "Error")
        
if __name__ == "__main__":
    main()