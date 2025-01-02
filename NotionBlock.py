from pprint import pprint

class NotionBlock:
    def __init__(self, content, url):
        self.block_type = None
        self.content = content
        self.url = url

    def update(self, block_type, content, url):
        self.block_type = block_type
        self.content = content
        self.url = url

    def bookmark(self, url):
        return {
            "object": "block",
            "type": "bookmark",
            "bookmark": {
                "caption": [],
                "url": url
            }
        }    
    def breadcrumb(self):
        return {
            "object": "block",
            "type": "breadcrumb",
            "breadcrumb": {}
        }
    
    def bulleted_list_item(self, text):
        return {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": text,
                        "link": None
                    }
                }],
                "color": "default",
                "children": [{
                    "type": "paragraph"
                    # ..other keys excluded
                }]
            }
        }
    
    def callout(self, text):
        return {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": text,
                        "link": None
                    }
                    # ..other keys excluded
                    }],
                    "icon": {
                        "emoji": "⭐"
                    },
                    "color": "default"
            }
        }
    
    def child_database(self, title):
        return {
            "object": "block",
            "type": "child_database",
            # ..other keys excluded
            "child_database": {
                "title": title
            }
        }


    def child_page(self, title):
        return {
            "object": "block",
            "type": "child_page",
            # ..other keys excluded
            "child_page": {
                "title": title
            }
        }

    def code(self, text, language):
        return {
            "object": "block",
            "type": "code",
            "code": {
                "caption": [],
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": text
                    }
                }],
                "language": language
            }
        }

    def column_list_and_column(self, text):
        '''存在问题'''
        return {
            "object": "block",
            "type": "column_list",
            #...other keys excluded
            "column_list": {}
            }

    def divider(self):
        return {
            "object": "block",
            "type": "divider",
            "divider": {}
        }
    
    def embed(self, url):
        return {
            "object": "block",
            "type": "embed",
            "embed": {
                "url": url
            }
        }

    def equation(self, expression):
        return {
            "object": "block",
            "type": "equation",
            "equation": {
                "expression": expression
            }
        }
    
    def file(self, url):
        return {
            "object": "block",
            "type": "file",
            "file": {
                "caption": [],
                "type": "external",
                "external": {
                    "url": url
                },
                "name": "None"
            }
        }

    def heading(self, level:int, text, link=None):
        return {
            "object": "block",
            "type": f"heading_{level}",
            f"heading_{level}": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": text,
                        "link": link
                    }
                }],
                "color": "default",
                "is_toggleable": False
            }
        }

    def image(self, url):
        return {
            "object": "block",
            "type": "image",
            "image": {
                "type": "external",
                "external": {
                    "url": url
                }
            }
        }

    def mention(self):
        pass

    def numbered_list_item(self, text):
        return {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": text,
                        "link": None
                    }
                }],
                "color": "default",
                "children": [{
                    "type": "paragraph"
                    # ..other keys excluded
                }]
            }
        }
    
    def paragraph(self, text, link=None):
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": text,
                            "link": None
                        }
                    },
                ],
                "color": "default"
            }
        }
    
    def pdf(self, url):
        return {
            "object": "block",
            "type": "pdf",
            "pdf": {
                "type": "external",
                "external": {
                    "url": url
                }
            }
        }
    
    def quote(self, text):
        return {
            "object": "block",
            "type": "quote",
            "quote": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": text,
                        "link": None
                    }
                }],
                "color": "default"
            }
        }
    
    def synced_block(self):
        pass

    def table(self, content):
        pass

    def table_of_contents(self):
        return {
            "object": "block",
            "type": "table_of_contents",
            "table_of_contents": {}
        }

    def video(self, url):
        return {
            "object": "block",
            "type": "video",
            "video": {
                "type": "external",
                "external": {
                    "url": url
                }
            }
        }
    
def main():
    notionblock = NotionBlock("", "")
    block = []
    notionblock.update("paragraph", "Lacinato kale", "")
    block.append(notionblock.paragraph("Lacinato kale"))
    notionblock.update("heading", "Lacinato kale", "")
    block.append(notionblock.heading(1, "Lacinato kale"))
    pprint(block)
    
if __name__ == "__main__":
    main()