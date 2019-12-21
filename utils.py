def assert_click_data(data):
    if "name" not in data or type(data["name"]) is not str:
        raise Exception("name must be of type String")
    if "comment" in data and type(data["comment"]) is not str:
        raise Exception("comment is not of type String?")
