import yaml

def config_loader():
    # 加载 .yaml 文件
    with open("config_private.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    # 获取配置变量
    notion_config = config.get("notion_config", {})
    db_feed_id, db_paper_id, token = (i for i in notion_config.values())

    return db_feed_id, db_paper_id, token