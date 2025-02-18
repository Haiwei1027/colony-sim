from json import dumps, loads

def save_map(data : dict, filename : str) -> None:
    with open(f"output/{filename}.map","w+",encoding="utf-8") as file:
        file.write(dumps(data))
        pass
    pass

def load_map(filename : str) -> dict:
    data = {}
    with open(f"output/{filename}.map","r",encoding="utf-8") as file:
        data = loads(file.read())
        pass
    return data