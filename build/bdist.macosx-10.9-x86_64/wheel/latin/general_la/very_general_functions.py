
import os, sys

import Levenshtein as lvn
import sys, subprocess, zipfile
from PIL import ImageFont
from abbreviations import *


######### timers



def open_txt_file(file):
    if "." not in file[-4:]:
        file += '.txt'
    p = subprocess.call(['open', file])


def sort_lst_by_len(lst, long_first=0):
    dct = {x: len(x) for x in lst}
    if long_first:
        dct = sort_dct_val_rev(dct)
    else:
        dct = sort_dct_val(dct)

    return list(dct.keys())




def get_arguments():
    arguments = sys.argv
    try:
        arg1 = arguments[1]
    except:
        arg1 = ""
    try:
        arg2 = arguments[2]
    except:
        arg2 = ""
    try:
        arg3 = arguments[3]
    except:
        arg3 = ""
    try:
        arg4 = arguments[4]
    except:
        arg4 = ""
    try:
        arg5 = arguments[5]
    except:
        arg5 = ""

    return [1, arg1, arg2, arg3, arg4, arg5]


def del_last_empty_rw(lst):
    if lst:
        while type(lst[-1] == str) and not reg(r'\S', lst[-1]):
            del lst[-1]
    return lst



def pycharm():
    if 'kylefoley' in sys.argv[0] and len(sys.argv) == 1:
        return 1


def largest_member(dct, tie=0):
    # values must be integers or floats
    dct = sort_dct_val_rev(dct)
    if len(dct)>1 and tie:
        s = dct_idx(dct)
        t = dct_idx(dct,1,'v')
        if s == t:
            return (s,t)

    return dct_idx(dct)



def get_between_sline(s, ld='<', add_com=0):
    on = 0
    if ld == '<':
        rd = '>'
    elif ld == '[':
        rd = ']'
    elif ld == '{':
        rd = '}'
    t = ""
    for x in s:
        if x == ld:
            on = 1
        elif x == rd:
            on = 0
            if add_com:
                t += ','
            else:
                t += ' '
        elif on:
            t += x
    return t.strip()


def sort_dct_by_dct(to_be_ordered, orderer):
    dct2 = {}
    orderer = sort_dct_val_rev(orderer)
    for k,v in orderer.items():
        dct2[k] = to_be_ordered[k]
    return dct2





def convert_nums(x):
    for e, z in en(x):
        try:
            z = int(z)
            x[e] = z
        except ValueError:
            try:
                z = float(z)
                x[e] = z
            except ValueError:
                pass

    return x




def from_dct_sum2perc(dct):
    '''
    the dict must have integers as values
    this will convert the integers into percentages of a
    whole
    '''
    tot = 0
    for k,v in dct.items():
        tot += v
    dct1 = {}
    for k,v in dct.items():
        dct1[k] = int((v/tot)*100)
    return dct1





def inside(s, l, r):
    if s.count(l) != 1 or s.count(r) != 1:
        return ""
    t = lambda s, l, r: s[s.index(l) + 1:s.index(r)]
    return t(s,l,r)




def del_last_empty_lst(lst):
    try:
        while len(lst[-1]) == 1 and not reg(r'\S', lst[-1][0]):
            del lst[-1]
        return lst
    except:
        while not lst[-1]:
            del lst[-1]
        return lst




def outside(s, l, r):
    if s.count(l) != 1 or s.count(r) != 1:
        return ""

    if s[0] == l:
        return s[s.index(r) + 1:].strip()
    elif s[-1] == r:
        return s[:s.index(l):].strip()
    else:
        return ""



def strip_n_split(str1, char=" "):
    lst = str1.split(char)
    return [x.strip() for x in lst]




def dct_idx(dct, idx=0, kv='k'):
    if not dct:
        return {}

    if kv == 'k':
        return list(dct.keys())[idx]
    elif kv == 'i':
        return list(dct.items())[idx]
    else:
        return list(dct.values())[idx]



def err_idx(num, lst):
    if num > len(lst):
        return len(lst)
    return num




def end_list(lst, num):
    try:
        c = lst[num]
        return num
    except:
        return len(lst)



def beg_list(lst,num):
    try:
        c = lst[num]
        return num
    except:
        return 0


def get_text_size(text, font_size=18, font_name='Times New Roman'):
    font = ImageFont.truetype(font_name, font_size)
    size = font.getsize(text)
    return size

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def print_intervals(number, interval, fork=None, total=0):
    if number > 0 and number % interval == 0 and number >= interval:
        if total:
            printProgressBar(number, total)
            # per = int((number / total) * 100)
            # number = f"{per}%"

        # if fork == None:
        #     p(number)
        # else:
        #     p(number)
        # else:
        #     p(f"fork {fork} - {number}")
        return


def unzip(path_to_zip_file, directory_to_extract_to):
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)

