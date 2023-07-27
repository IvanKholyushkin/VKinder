import configparser


def get_tokens():
    config = configparser.ConfigParser()
    config.read("config.ini")
    group_token = config["GROUP_TOKEN"]["group_token"]
    user_token = config["USER_TOKEN"]["user_token"]
    db_token = config["DEFAULT"]["DSN"]
    return {"group_token": group_token, "user_token": user_token, "db_token": db_token}
