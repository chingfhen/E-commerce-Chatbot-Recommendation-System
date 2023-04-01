from scipy.sparse import save_npz, load_npz
from numpy import save, load 
import os
import pickle


"""
Load SAR model
"""
def sar_load(model, directory):
    model.user_affinity = load_npz(file = os.path.join(directory,"sar_user_affinity.npz"))
    model.item_similarity = load(file = os.path.join(directory,"sar_item_similarity.npy"))
    model.item_frequencies = load(file = os.path.join(directory,"sar_item_frequencies.npy"))
    with open(os.path.join(directory,"sar_user2index.pkl"), "rb") as f:
        model.user2index = pickle.load(f)
    with open(os.path.join(directory,"sar_index2item.pkl"), "rb") as f:
        model.index2item = pickle.load(f)
    with open(os.path.join(directory,"sar_index2user.pkl"), "rb") as f:
        model.index2user = pickle.load(f)
    with open(os.path.join(directory,"sar_item2index.pkl"), "rb") as f:
        model.item2index = pickle.load(f)
    with open(os.path.join(directory,"sar_n_items.pkl"), "rb") as f:
        model.n_items = pickle.load(f)
   
"""
Save SAR model
"""
def save_sar(model, directory, model_name):
    model_directory = os.path.join(directory, model_name)
    os.makedirs(model_directory, exist_ok=True)
    save_npz(file = os.path.join(model_directory, "sar_user_affinity.npz"), 
             matrix = model.user_affinity, 
             compressed=True)
    save(file = os.path.join(model_directory, "sar_item_similarity.npy"),
         arr = model.item_similarity)
    save(file = os.path.join(model_directory, "sar_item_frequencies.npy"),
         arr = model.item_frequencies)
    with open(os.path.join(model_directory, "sar_user2index.pkl"), "wb") as f:
        pickle.dump(model.user2index, f)
    with open(os.path.join(model_directory, "sar_index2item.pkl"), "wb") as f:
        pickle.dump(model.index2item, f)
    with open(os.path.join(model_directory, "sar_index2user.pkl"), "wb") as f:
        pickle.dump(model.index2user, f)
    with open(os.path.join(model_directory, "sar_item2index.pkl"), "wb") as f:
        pickle.dump(model.item2index, f)
    with open(os.path.join(model_directory, "sar_n_items.pkl"), "wb") as f:
        pickle.dump(model.n_items, f)
        
   
# """
# Helper function to convert numpy keys in a dictionary to raw values
# """
# def convert_numpy_keys_to_raw(d):
#     non_numpy_keys = list(map(int,d.keys()))
#     non_numpy_values = list(map(int,d.values()))
#     return dict(zip(non_numpy_keys,non_numpy_values))  