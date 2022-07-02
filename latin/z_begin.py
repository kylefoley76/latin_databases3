import sys
import os
import shutil
import urllib.request
import requests
vol = os.path.join(os.path.dirname(__file__)) + '/general_la/'
dir2 = os.path.join(os.path.dirname(__file__))
sys.path.append(dir2)
sys.path.append(vol)

from bglobals import *
import c_colat1
import c_colat2
import c_colat3
import c_colat4
import e_pedocerto
from e_pedocerto import pros, vow_marked
if not public:
    import i_scrape_old
    from i_scrape_old import old_entry
import j_lasla
import j_lasla2
import m_stems
import o_memorize
import v_reading


def elim_useless_files():
    to_del = []
    for l in os.listdir(fold):
        file = f'{fold}{l}'
        if file not in files_used:
            dest = f'{bfold}{l}'
            shutil.copy(file, dest)
            to_del.append(file)
    for x in to_del:
        os.remove(x)
    return




def begin():
    ins = c_colat1.get_co_lemmas1()
    ins.begin()
    ins = c_colat2.bottom_most()
    ins.begin()
    ins.kind = 'p'
    ins.begin(1)
    ins = c_colat3.colatinus()
    ins.begin()
    ins = c_colat4.bottom_most_a4()
    if public:
        ins.begin_fc(0,'rs')
    else:
        ins.begin_fc()
    ins = e_pedocerto.pedecerto()
    ins.begin()
    ins = e_pedocerto.long_by_pos()
    ins.begin3()
    ins = e_pedocerto.check_vowels()
    ins.begin_f()
    if not public:
        ins = i_scrape_old.bottom_most()
        ins.begin()
    ins = j_lasla.convert2txt()
    ins.kind = ''
    ins.begin_ct()
    ins = j_lasla2.bottom_most_la()
    ins.begin_mcl(1)
    ins = m_stems.bottom()
    ins.begin_st()
    ins = o_memorize.bottom_most()
    ins.begin('all', 'start')
    ins = v_reading.punctuate_lasla()
    ins.begin()


begin()
first = 0
if first:
    elim_useless_files()
