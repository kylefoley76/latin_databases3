import subprocess
from abbreviations import *
import very_general_functions as vgf






def from_rtf2lst(file):
    with open(f'{file}.rtf', 'r') as file:
        text = file.read()
    return text



def from_txt2lst(file, str_only=False, skipex=0):
    if not bool(re.search(r'(txt|rtf|html|\.py)$',file)):
        file += '.txt'
    files_used.add(file)
    try:
        lst = [line for line in open(file, 'r')]
    except:
        lst = [line for line in open(file, 'r+', encoding="latin-1")]

    for e, x in en(lst):
        if x[-1] == '\n':
            lst[e] = x[:-1]

    lst = vgf.del_last_empty_rw(lst)
    if not str_only:
        for e, x in en(lst):
            try:
                lst[e] = int(x)
            except:
                try:
                    lst[e] = float(x)
                except:
                    lst[e] = x.replace(' %%% ', "\n")
                    pass
    else:
        lst = [x.replace(' %%% ', "\n") for x in lst]

    if skipex:
        lst = [x for x in lst if x and x[0] != '!']

    return lst




def from_lst2txt_tab_delim(lst1, name, no_perc=False, make_copy=True):
    if make_copy:
        lst = jsonc(lst1)
    else:
        lst = lst1
    if not name.endswith('txt'):
        name += '.txt'

    with open(name, 'w+', encoding='utf8') as f:
        for x in lst:
            assert type(x) == list
            for e, z in en(x):
                # if :
                #     z = ""

                z = str(z)

                if z and z[-1] == '\n':
                    z = z[:-1]
                if no_perc:
                    z = z.replace("\n", ' ')
                else:
                    z = z.replace("\n", ' %%% ')
                x[e] = z

            str1 = "\t".join(x)
            f.write(str1 + "\n")

    return



def from_txt2lst_tab_delim(file, str_only=0,skipex=1):
    if not file.endswith('.txt'):
        file += '.txt'
    files_used.add(file)

    try:
        lst = [line for line in open(file, 'r')]
    except:
        lst = [line for line in open(file, 'r+', encoding="latin-1")]

    if not lst:
        return lst

    for e, x in en(lst):
        if e == 21:
            bb = 8

        x = x.replace(' %%% ', '\n')

        if x and x[-1] == '\n':
            x = x[:-1]
        x = x.split("\t")
        if not str_only:
            lst[e] = vgf.convert_nums(x)
        else:
            lst[e] = x
    if skipex:
        lst1 = []
        found = 0
        for x in lst:
            if found:
                lst1.append(x)
            elif type(x[0]) == str and x[0][0] == '!':
                pass
            else:
                lst1.append(x)
                found = 1
        lst = lst1

    return vgf.del_last_empty_lst(lst)




def from_lst2txt(lst, file_name, has_slash_n=False, ofile=False):
    '''
    has_slash_n == 2 means that each line is followed by /n
    and it does not replace the /n which are already in the text
    '''

    if file_name.endswith('.rtf'):
        pass
    elif not file_name.endswith('txt'):
        file_name += '.txt'
    with open(file_name, 'w+') as f:
        for x in lst:
            x = str(x)
            assert ' %%% ' not in x, 'you cant have %%% in a file'
            if has_slash_n == 2:
                f.write(x + '\n')
            elif has_slash_n:
                f.write(x)
            else:
                x = x.replace('\n', ' %%% ')
                f.write(x + '\n')

    if ofile:
        p = subprocess.call(['open', file_name])




def from_txt2dct_1d(file):
    lst = from_txt2lst_tab_delim(file)
    return {x[0]: x[1] for x in lst}





