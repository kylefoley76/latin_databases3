import pickle, os
from abbreviations import *



def save_pickle(obj, name, any_name=True):
    if not any_name:
        name = mdir + 'pickles/' + name
    elif any_name == 'hi':
        name = mdir + 'hi_pickles/' + name
    elif any_name == 'hit':
        name = mdir + 'pickles/hieroglyphs/tests/' + name


    if not name.endswith(".pkl"):
        name += ".pkl"
    temp = open(name, "wb")
    pickle.dump(obj, temp)
    temp.close()




def open_pickle(name, any_folder=True, warn=True):
    if "DS_Store" in name: return []

    if not name.endswith(".pkl"):
        name += ".pkl"
    if not any_folder:
        name = mdir + 'pickles/' + name
    elif any_folder == 'hi':
        name = mdir + 'hieroglyphs/hi_pickles/' + name
        # name = f'{os.getcwd()}/{name}'

    files_used.add(name)
    pkl_file = open(name, 'rb')
    obj = pickle.load(pkl_file)
    pkl_file.close()

    return obj




