
import pdb, json, re
from operator import itemgetter


p = print

en = enumerate

db = pdb.set_trace
conditional = chr(8594)
ds = ".DS_Store"
ds1 = '._.DS_Store'

# vol = '/users/kylefoley/'
#
# fdir = vol + 'documents/'
# fdir2 = vol + 'documents/'
# mdir = vol + 'documents/codes/'
files_used = set()
# pdir = fdir + 'pcode/'
# base_dir = '/Users/kylefoley/documents/pcode/'
# dwn_dir = '/users/kylefoley/downloads/'

dia = 'àáäâèéêëìíïîòóöôùúûüçßñ'
diau = 'ÀÁÄÂÈÉÊËÌÍÏÎÒÓÖÔÙÚÛÜÇÑ' + dia

open_apost = chr(8220)

closed_apost = chr(8221)

large_dash = chr(8212)

upside_down_q = chr(191)

ellip = chr(8230)

obje = chr(65532)

letter_2numbers = "abcdefghijklmnopqrstuvxyz"

letters = "abcdefghijklmnopqrstuvxyz"

dsstore = '.DS_Store'

not_execute_on_import = '__name__ == "__main__"'

sort_dct_key = lambda x: from_tpl2dct(sort_dct_key_tpl(x))

sort_dct_key_tpl = lambda x: sorted(x.items(), key=itemgetter(0))

ujsonc = lambda x: json.loads(json.dumps(x))

sort_dct_val_rev = lambda x: from_tpl2dct(sort_dct_val_rev_tpl(x))

sort_dct_val = lambda x: from_tpl2dct(sort_dct_val_tpl(x))

sort_by_col_rev = lambda lst, col: sorted(lst, key=itemgetter(col), reverse=True)

sort_dct_val_rev_tpl = lambda x: sorted(x.items(), key=itemgetter(1), reverse=True)

sort_by_col = lambda lst, col: sorted(lst, key=itemgetter(col))

hl = lambda x: bool(re.search(r'\S', x))  # has non-characters

ha = lambda x: bool(re.search(r'[a-zA-Z]', x))  # has alphabetic characters

reg = lambda x, y: bool(re.search(x, y))

sort_dct_val_tpl = lambda x: sorted(x.items(), key=itemgetter(1))

from_tpl2dct = lambda x: {z[0]: z[1] for z in x}

get_between = lambda sent, l, r: sent[sent.index(l) + 1:sent.index(r)]

percent = lambda x, tot: int(round(x / tot, 2) * 100)

add_at_i = lambda idx, sent, char: sent[:idx] + char + sent[idx:]

replace_at_i = lambda idx, sent, char: sent[:idx] + char + sent[idx + 1:]

merge_2dicts = lambda x, y: {**x, **y}

delete_at_i = lambda x, sent: sent[:x] + sent[x + 1:]

jsonc_lam = lambda x: json.loads(json.dumps(x))

def jsonc(obj):
    if type(obj) == dict:
        for x, y in obj.items():
            if type(x) == int:
                try:
                    obj = ujsonc(obj)
                except:
                    obj = jsonc_lam(obj)
                return {int(k): v for k, v in obj.items()}
            else:
                break
    try:
        obj = ujsonc(obj)
    except:
        obj = jsonc_lam(obj)
    return obj