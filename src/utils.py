import os
import pickle


def save_object(file_path, object):
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    
    with open(file_path, 'wb') as f:
        pickle.dump(object, f)
        
def load_object(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)