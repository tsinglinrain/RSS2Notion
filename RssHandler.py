import feedparser
from feedparser import FeedParserDict
from bs4 import BeautifulSoup, NavigableString
from datetime import datetime, timedelta
from pprint import pprint
import requests

from NotionBlock import NotionBlock

class RSSHandle:
    def __init__(self, rss_url):
        self.rss_url = rss_url

    def update(self, rss_url):
        self.rss_url = rss_url

    def fetch_feed(self):
        # 解析 RSS
        feed:FeedParserDict = feedparser.parse(self.rss_url)
        if feed.bozo:
            raise ValueError(f"无法解析 RSS 源: {self.rss_url}")
        return feed

    def get_feed_info(self):
        # 提取订阅源信息
        try:
            feed:FeedParserDict = self.fetch_feed()
            return {
                "title": feed.feed.title,
                "link": feed.feed.link,
                "description": feed.feed.get("description", "无描述")
            }
        except Exception as e:
            print(f"An error occurred {e}")
            return None

    def get_articles(self):
        # 提取文章信息
        feed = self.fetch_feed()
        articles = []
        for entry in feed.entries:
            raw_content = entry.get("content", [{"value": entry.get("description", "无正文")}])[0]["value"]
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "published": self.date_transform(entry.published),
                "content": RSSHandle.clean_html(raw_content)
            })
        return articles
    
    @staticmethod
    def date_transform(date_ori:str, time_zone_offset=8):
        '''将data转换成标准iso86格式
        
        "2020-03-17T19:10:04.968Z 参见
        https://developers.notion.com/reference/database"'''
        # 自己用字符串切片写的,发现有现成的
        date = datetime.strptime(date_ori, "%a, %d %b %Y %H:%M:%S %Z")
        date = date + timedelta(hours=time_zone_offset)
        date = date.strftime("%Y-%m-%dT%H:%M:%SZ")
        return date


    @staticmethod
    def clean_html(html_content):
        """
        Recursively parse HTML content into Notion-compatible blocks.
        """
        notionblock = NotionBlock("", "")
        soup = BeautifulSoup(html_content, "html.parser")
        blocks = []

        def parse_element(element):
            # Handle various HTML elements and convert them into Notion blocks
            if element.name == "p":
                # Process <p> as a single block with its children
                rich_text = []
                annotations_italic = False
                if element.parent.name == "em":
                    annotations_italic = True
                for child in element.children:
                    # print(f"child: {child.name}")   # 添加调试信息
                    if child.name == "a":  # Handle hyperlinks
                        link_text = child.get_text(strip=True)
                        href = child.get("href")
                        if link_text and href:
                            rich_text.append({
                                "type": "text",
                                "text": {"content": link_text, "link": {"url": href}},
                                "annotations": {
                                    "bold": False,
                                    "italic": annotations_italic,
                                    "strikethrough": False,
                                    "underline": True,
                                    "code": False,
                                    "color": "default"
                                }
                            })
                    elif child.name is None:  # Handle plain text
                        text = child.strip()
                        if text:
                            rich_text.append({
                                "type": "text",
                                "text": {"content": text},
                                "annotations": {"bold": False, "italic": annotations_italic}
                            })
                    elif child.name == "strong":
                        text = child.get_text(strip=True)
                        if text:
                            rich_text.append({
                                "type": "text",
                                "text": {"content": text},
                                "annotations": {"bold": True, "italic": annotations_italic}
                            })
                if rich_text:
                    return [{
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": rich_text,
                            "color": "default"
                        }
                    }]   

                # return [notionblock.paragraph(element.get_text(strip=True))]
            elif element.name in ["h1", "h2", "h3"]:
                level = int(element.name[1])  # Extract heading level, e.g. h1 -> 1
                return [notionblock.heading(level, element.get_text(strip=True))]
            elif element.name == "hr":
                return [notionblock.divider()]
            elif element.name == "ul":
                return [
                    notionblock.bulleted_list_item(li.get_text(strip=True))
                    for li in element.find_all("li")
                ]
            elif element.name == "ol":
                return [
                    notionblock.numbered_list_item(li.get_text(strip=True))
                    for li in element.find_all("li")
                ]
            elif element.name == "blockquote":
                return [notionblock.quote(element.get_text(strip=True))]
            elif element.name == "img":
                img_url = element.get("src")
                if img_url:
                    try:
                        response = requests.get(img_url)
                        if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
                            return [notionblock.image(img_url)]
                    except Exception as e:
                        print(f"An error occurred {e}")
                        return []
                    # return [notionblock.image(img_url)]
            
            elif element.name == "audio":
                print("audio block found")
                audio_url = element.get("src")
                if audio_url:
                    print(f"audio src: {audio_url}")
                    return [notionblock.embed(audio_url)]
            
            elif element.name == "figure":
                # Handle figure with image and caption
                blocks = []
                img = element.find("img")
                caption = element.find("figcaption")
                if img:
                    img_block = notionblock.image(img["src"])
                    if caption:
                        img_block["image"]["caption"] = [{"type": "text", "text": {"content": caption.get_text(strip=True)}}]
                    blocks.append(img_block)
                    
                    return blocks # 缩进不能前移不能直接就跑了,要处理里面的元素
            elif element.name == "small":
                rich_text = []
                for child in element.children:
                    print(f"child: {child.name}")   # 添加调试信息
                    if child.name == "a":  # Handle hyperlinks
                        link_text = child.get_text(strip=True)
                        href = child.get("href")
                        if link_text and href:
                            rich_text.append({
                                "type": "text",
                                "text": {"content": link_text, "link": {"url": href}},
                                "annotations": {
                                    "bold": False,
                                    "italic": False,
                                    "strikethrough": False,
                                    "underline": True,
                                    "code": False,
                                    "color": "default"
                                }
                            })
                    elif child.name is None:  # Handle plain text
                        text = child.strip()
                        if text:
                            rich_text.append({
                                "type": "text",
                                "text": {"content": text}
                            })
                    elif child.name == "strong":
                        text = child.get_text(strip=True)
                        if text:
                            rich_text.append({
                                "type": "text",
                                "text": {"content": text},
                                "annotations": {"bold": True}
                            })
                if rich_text:
                    return [{
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": rich_text,
                            "color": "default"
                        }
                    }] 
                # return [notionblock.paragraph(element.get_text(strip=True))]
            elif element.name is None:  # Handle text nodes
                # text = element.strip()
                # if text:
                #     return [notionblock.paragraph(text)]
                pass
            
            try:
                if not isinstance(element, NavigableString) and element.contents and (hasattr(element, 'name') or isinstance(element, str)):
                    result = []
                    for child in element.contents:
                        result.extend(parse_element(child))
                    return result
            except AttributeError:
                pass

            return []

        for element in soup.contents:
            # print(f"Processing element: {element}")  # 添加调试信息
            try:
                blocks.extend(parse_element(element))
            except Exception as e:
                print(f"An error occurred {e}")
                continue
            # blocks.extend(parse_element(element))
            # # 先看效果,超过100会出问题,所以这里先把截断
            blocks = blocks[:100]
        return blocks


def main():
    rss_url = "https://rss.soyet.icu/theinitium/app"
    rss_handler = RSSHandle(rss_url)
    feed_info = rss_handler.get_feed_info()
    articles = rss_handler.get_articles()
    print(feed_info)
    # print(articles)
    with open("content.txt", "w", encoding="utf-8") as file:
        for article in articles:
            file.write(f"{article['title']}\n{article['link']}\n{article['published']}\n{article['content']}\n\n")
            break

def parse_content_file(file_path):
    '''测试本地文件'''
    with open(file_path, "r", encoding="utf-8") as file:
        raw_content = file.read()
    rss_handler = RSSHandle("")
    notion_blocks = rss_handler.clean_html(raw_content)
    return notion_blocks

def test_content_block():
    # 解析 content.txt 并输出结果
    filename1 = "content.txt"
    filename2 = "audio2.txt"
    filename3 = "audio.txt"
    filename4 = "link_text.txt"
    filename5 = "link_text2.txt"
    content_blocks = parse_content_file(filename5)
    with open("link_blocks3.txt", "w", encoding="utf-8") as file:
        for block in content_blocks:
            file.write(f"{block}\n")
            print(block)

if __name__ == "__main__":
    pass
    test_content_block()
    # main()
