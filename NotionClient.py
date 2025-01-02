import os
from notion_client import Client
import feedparser
import yaml
from pprint import pprint


class NotionClient:
    def __init__(self, db_feed_id, db_paper_id, token):
        self.client = Client(auth=token)
        self.db_feed_id = db_feed_id
        self.db_paper_id = db_paper_id

    def get_choose_rss_sources(self):
        """读取订阅源数据库中所有checbox为True 的订阅源
        
        如果数据库包含超过 100 条数据，需要分页获取所有数据"""
        results = []
        next_cursor = None
        while True:
            response = self.client.databases.query(
                database_id=self.db_feed_id,
                filter={"property": "Checkbox", "checkbox": {"equals": True}},
                sorts=[{"property": "Feed Name", "direction": "ascending"}],
                start_cursor=next_cursor
            )
            results.extend(response["results"])
            next_cursor = response.get("next_cursor")
            if not next_cursor:
                break
        
        # pprint(results)
        # return [{"id": item["id"], "url": item["properties"]["Feed Url"]["url"]} for item in results["results"]]
        return results

    def update_rss_status(self, page_id, status):
        """更新订阅源的状态"""
        try:
            self.client.pages.update(
                page_id = page_id, properties={"Status": {"select": {"name": status}}}
            )
            print("Update status successfully!")
        except Exception as e:
            print(e)
            # return

    def update_database_feed(self, page_id, Feed_Name, ori_url, description):
        """更新细节至database_feed"""
        try:
            self.client.pages.update(
                page_id = page_id, properties={
                    "Feed Name": {"title": [{"text": {"content": Feed_Name}}]},
                    "Ori Url": {"url": ori_url},
                    "Description": {"rich_text": [{"text": {"content": description}}]}
                }
            )
            print("Update details successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")

    def cre_in_database_paper(self, icon_url, title, pubDate, url_paper, blocks: list, database_feed_page_id=None):
        """添加文章至database_paper"""
        try:
            self.client.pages.create(
                icon = {
                    "external": {
                        "url": icon_url  # 使用上传文件的 URL 作为图标
                    }
                },
                parent = {"database_id": self.db_paper_id},
                properties = {
                    "Title": {"title": [{"text": {"content": title}}]},
                    "Link": {"url": url_paper},
                    "PubDate": {"date": {"start": pubDate}},
                    "From": {"relation": [{"id": database_feed_page_id}]}
                },
                children=blocks,
            )
            print("Create paper successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.client.pages.create(
                # icon = {"type": "emoji", "emoji": "🇩🇪"},
                # icon = {
                #     "type": "custom_emoji",
                #     "custom_emoji": {
                #         'id': '12d99f72-bada-802e-9688-007a0c387d8d',
                #         'name': 'lianhezaobao'}
                # },
                icon = {
                    "external": {
                        "url": icon_url  # 使用上传文件的 URL 作为图标
                    }
                },
                parent = {"database_id": self.db_paper_id},
                properties = {
                    "Title": {"title": [{"text": {"content": title}}]},
                    "Link": {"url": url_paper},
                    "PubDate": {"date": {"start": pubDate}},
                    "From": {"relation": [{"id": database_feed_page_id}]}
                },
                children=[],
            )
    def cre_in_database_paper_copy(self, title, pubDate, url_paper, blocks: list, database_feed_page_id=None):
        """添加文章至database_paper"""
        self.client.pages.create(
            icon = {"type": "emoji", "emoji": "🇩🇪"},    # Deutschland
            # icon = {
            #     "type": "custom_emoji",
            #     "custom_emoji": {
            #         'id': '12d99f72-vivo-vo50-9688-007vivo50d8d',
            #         'name': 'lianhezaobao'}
            # },
            # icon = {
            #     "external": {
            #         "url": icon_url  # 使用上传文件的 URL 作为图标
            #     }
            # },
            parent = {"database_id": self.db_paper_id},
            properties = {
                "Title": {"title": [{"text": {"content": title}}]},
                "Link": {"url": url_paper},
                "PubDate": {"date": {"start": pubDate}},
                # "From": {"relation": [{"id": database_feed_page_id}]}
            },
            children=blocks,
        )

    def image_save(self):
        with open("image.png", "rb") as file:
            file_content = file.read()
        
        response = self.client.files.upload(
            file=file_content,
            type="image/png"
        )
        # 获取上传后的 URL
        file_url = response["file"]["url"]


def config_loader():
    # 加载 .yaml 文件
    with open("config_private.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    # 获取配置变量
    notion_config = config.get("notion_config", {})
    db_feed_id, db_paper_id, token = (i for i in notion_config.values())

    return db_feed_id, db_paper_id, token

def block_generator1():
    blocks = [
        {
            "object": "block",
            "heading_2": {"rich_text": [{"text": {"content": "Lacinato kale"}}]},
        },
        {
            "object": "block",
            "paragraph": {
                "rich_text": [
                    {
                        "text": {
                            "content": "Lacinato kale is a variety of kale with a long tradition in Italian cuisine, especially that of Tuscany. It is also known as Tuscan kale, Italian kale, dinosaur kale, kale, flat back kale, palm tree kale, or black Tuscan palm.",
                            "link": {
                                "url": "https://en.wikipedia.org/wiki/Lacinato_kale"
                            },
                        },
                    }
                ],
                "color": "default",
            },
        },
        {
            "object": "block",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "equation",
                        "equation": {
                            "expression": "E = mc^2"
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        },
                        "plain_text": "E = mc^2",
                        "href": None
                        }
                ]
            }
        },
        {
            "object": "block",
            "paragraph": {
                "rich_text": [
                    {
                    "type": "mention",
                    "mention": {
                        "type": "database",
                        "database": {
                        "id": "a1d8501e-1ac1-43e9-a6bd-ea9fe6c8822b"
                        }
                    },
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default"
                    },
                    "plain_text": "Database with test things",
                    "href": "https://www.notion.so/a1d8501e1ac143e9a6bdea9fe6c8822b"
                    }
                ]
            }
        },
    ]
    return blocks

def block_generator2():
    blocks = [
        {
            "type": "image",
            "image": {
                "type": "external",
                "external": {
                    # "url": "https://cn.bing.com/th?id=OHR.CANYE24_ZH-CN3884754296_UHD.jpg"
                    # "url": "https://app.theinitium.com/wp-content/uploads/sites/1104/2024/12/62460/f33dcea87154d38119443c9d71dc33b4--birds-02_a56cd6.jpg"                }
                    "url": "https://pixiv.rsshub.app/img-original/img/2024/12/04/18/05/58/124891165_p0.jpg"
            }
        }}
    ]
    return blocks

def block_generator3():
    '''embed'''
    blocks = [
                {
        "type": "embed",
        "embed": {
            "url": "https://cn.bing.com/th?id=OHR.CANYE24_ZH-CN3884754296_UHD.jpg"
        }
        }
    ]
    return blocks



def main():

    notionclient = NotionClient(*config_loader())
    results = notionclient.get_choose_rss_sources()
    pprint(results[0]["properties"]["Feed Url"]["url"])

    # ID = results[0]["properties"]["ID"]["unique_id"]["number"]
    # print(ID)
    page_id = results[0]["id"]
    print(page_id)
    notionclient.update_rss_status(page_id, "Active")


def cus_emoji_get_test():

    notionclient = NotionClient(*config_loader())
    results = notionclient.get_choose_rss_sources()
    icon = [item["icon"] for item in results]
    pprint(icon)
    # with open("image_json.txt", "wb") as file:
    #     for item in icon:
    #         file.write(item)
    #         file.write(b"\n")
        


def add_paper_test():
    notionclient = NotionClient(*config_loader())
    # blocks = block_generator1()
    blocks = block_generator2()
    # blocks = block_generator3()
    notionclient.cre_in_database_paper_copy(
        "pixiv_test_img", "2025-01-01", "https://pixiv.rsshub.app/img-original/img/2024/12/04/18/05/58/124891165_p0.jpg", blocks
    )


def relation_test():
    notionclient = NotionClient(*config_loader())
    results = notionclient.get_choose_rss_sources()
    # pprint(results[0]["properties"]["Feed Url"]["url"])

    # ID = results[0]["properties"]["ID"]["unique_id"]["number"]
    # print(ID)
    print(len(results))
    page_detail = [item["properties"]["Feed Name"]["title"][0]["plain_text"] for item in results]
    print(page_detail)
    # page_id = results[2]["id"]
    # print(page_id)

    # blocks = block_generator1()
    # notionclient.add_to_database_paper(
    #     "relation_test2", "2024-12-27", "https://en.wikipedia.org", blocks, page_id
    # )

if __name__ == "__main__":
    pass
    # main()
    add_paper_test()

    # cus_emoji_get_test()
    # relation_test()