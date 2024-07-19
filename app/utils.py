import pickle as pkl

def save_object(object, path:str):
    with open(path, "wb") as file:
        pkl.dump(object, file)

def load_object(path: str):
    with open(path, "rb") as file:
        return pkl.load(file)
