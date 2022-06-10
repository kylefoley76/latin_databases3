import add_path
from lglobals import *
from learn_language import match_words, interlinear_translation
import time,os
from filter_txt import elim_end_hyphen

'''
"Sḗmĭs."1 ăn,1.1 hǣ́c3.5 ănĭmṓs9 ǣrū́go;4 ‿ēt5 cū́ră6 pĕcū́li;7
Cū́m2 sĕmĕl3 ī́mbŭĕrī́t,;8 spērḗmūs9 cā́rmĭnă12 fī́ngi11
Pṓssĕ10 lĭnḗndă;12 cĕdro;13 ‿ḗt14 lēuī́;16 sēruā́ndă15 cŭprḗsso?17 

in this passage we need an error message for two words with same number

'''



def help():
    p (f"""
    
    the file must be in downloads and there must be an accompanying
        file ending in _eng
    
    nw - to add new words to the vocab doc located in /latin/vocab
        doc will gather words once __start is found and stop once zzz
        is found.  automatically removes all numbers from words
        words must have ; in them to count
        to add a whole line then put all the words on that line and end
            it with ;;
        
    nw2 - adds news words to vocab but here the words must have @ in them
    
    awi - adds new words but the text is in interlinear format, words
        must have @ in them
        
    
    
    """)




def running_check(file):
    while 1:
        ins = match_words()
        ins.file = file
        ins.loop_til_right(1)
        ins = interlinear_translation()
        ins.file = file
        ins.loop_til_good()
        p('checked')
        time.sleep(60)



class phi:
    def __init__(self):
        pass

    def begin(self):
        self.get_atts()


    def get_atts(self):
        self.auth2work = defaultdict(dict)
        self.auth2num = defaultdict(dict)
        for auth in os.listdir(f'{lfold}phi'):
            if auth[0] != '.':
                file = f'{lfold}phi/{auth}'
                for work in os.listdir(file):
                    file2 = f'{file}/{work}'
                    lst = to.from_txt2lst(file2)
                    self.auth2work[auth][work] = lst
                    b = 0
                    for z in lst:
                        z = re.sub(r'\s{1,}',' ',z)
                        b += z.count(' ')+1
                    self.auth2num[auth][work] = b
        return



    def get_auth2words(self):
        self.long_works = {}
        for auth,works in self.auth2num.items():
            for work, num in works.items():
                self.long_works[(auth, work)] = num

        self.long_works = sort_dct_val_rev(self.long_works)
        self.auth2work = sort_dct_key(self.auth2work)
        b = 0
        tot_words = 0
        for x, y in self.long_works.items():
            tot_words += y
            if y > 5000:
                b += 1
        p (b)


def extract_rearrange(file):
    '''
This will take every line in an _itrans document and put it on a new file so that you can
read the rearrangement with ease.  in the _itrans doc every latin line that ends with ,, is
followed by a rearranged line

    '''

    file1 = f'{dwn_dir}{file}'
    file2 = f'{dwn_dir}{file}'
    t = 'ī́'
    p (ord(t[-1]))

    file2 = file2.replace('_itrans','') + '_rearr'
    lst = to.from_txt2lst(file1,1)
    lst1 = []
    for e, x in en(lst):
        if x and x[0].isdigit():
            num = x[:x.index(' ')]

        if x.endswith(',,'):
            s = lst[e+2]
            s = unidecode(s)
            s = re.sub(r'[\",\.\?]','',s)
            s = s.lower()
            lst1.append(f"{num} {s}")
            lst1.append('')
    to.from_lst2txt(lst1, file2)
    vgf.open_txt_file(file2)


def focus(file, only_list=0):
    '''
this function takes a text in the itrans format in which
there is a number beginning the line of each foreign language
line, followed by rearrangement, then english and so long
as there is a / in the line then it will save that line alone
with the rearrangement and the english and put it on another
file.

    '''

    file1 = f'{dwn_dir}{file}'
    file3 = f'{dwn_dir}{file}a'
    file4 = f'{dwn_dir}{file}b'
    lst = to.from_txt2lst(file1,1)
    lst1 = vgf.clump_lst(lst,1)
    lst3 = []
    lst4 = []
    nums = []
    on = 0
    for x in lst1:
        y = x[0]
        num = y[:y.index(' ')]
        if any('/' in z for z in x):
            nums.append(num)
            lst4.append(x)
            on = 1
        elif x[0][0].isdigit():
            if lst4:
                lst3.append(lst4)
            lst4 = []
            on = 0
        elif on:
            lst4.append(x)

    if lst4:
        lst3.append(lst4)

    if only_list:
        return lst3

    lst5 = []
    lst6 = []
    for x in lst3:
        for z in x:
            for y in z:
                lst5.append(y)
                lst6.append(y)
            lst5.append('')


    file2 = f'{dwn_dir}nums'
    to.from_lst2txt(nums,file2)
    to.from_lst2txt(lst5,file3)
    to.from_lst2txt(lst6,file4)
    vgf.open_txt_file(file2)
    return





class lasla_pos_txt:
    def __init__(self):
        pass

    def begin(self):
        self.get_atts()
        self.any_author()
        self.stats()
        self.output()

    def get_atts(self):
        self.lasla_db2 = pi.open_pickle(f'{fold}lasla_db2')
        self.from_excel_wnum = pi.open_pickle(f'{fold}from_excel_wnum')
        self.llemclem = pi.open_pickle(f'{fold}llem2clem')
        self.noun2gender = pi.open_pickle(f'{fold}lasla_noun2gen')
        self.lem2forms_rev = pi.open_pickle(f'{fold}lem2forms_rev')
        self.kind = 'simple'
        self.auth = 'Horatius'
        self.tpos = {
            'C': 'm',
            'X': 'm',
            'B': 'm',
        }

    def any_author(self):
        self.lst = []
        self.lidx = ''
        self.tgen = 0
        self.hgen = 0
        self.tmac = 0
        self.hmac = 0
        for k, books in self.lasla_db2[self.auth].items():
            if k == 'ArsPoetica_HorArsPo':
                for e, v in en(books):
                    vgf.print_intervals(e, 500, None, len(books))
                    self.idx = v[3]
                    self.lem = v[1]
                    self.cat = v[0]
                    self.word = v[2]
                    self.gender = self.noun2gender.get(self.lem, '')
                    self.pos = v[4]
                    if self.cat != '!':
                        self.tmac += 1
                        if self.kind == 'simple':
                            self.add_macrons()
                            self.basic()
                        self.lidx = self.idx

    def line1(self):
        lst = ['lem', 'word', 'pos']

        dct = {x: vgf.get_text_size(getattr(self, x)) for x in lst}

    def add_macrons(self):
        if len(self.pos) == 2 and self.pos[0] in ['s', 'p']:
            self.tgen += 1
            if self.gender:
                self.hgen += 1

        special = 0
        pos2 = self.pos
        if reg(r'[CBX]', self.pos):
            for x, y in self.tpos.items():
                pos2 = pos2.replace(x, y)
        elif reg(r'[A-Z]', self.pos):
            special = 1

        lem_wn, num = cut_num(self.lem, 1)
        obj = self.llemclem.get(lem_wn)
        if obj:
            cnum = obj.get(num)
            if cnum != None:
                itm = self.lem2forms_rev.get(lem_wn + cnum)
                mword = 0
                if type(itm) == str:
                    mword = itm
                elif itm:
                    if special:
                        mword = self.infer_pos(itm)
                    else:
                        words = itm.get(pos2)
                        if words:
                            mword = words.get(self.word)

                if special and mword:
                    self.word = f'_{mword}_$'
                    self.tmac -= 1
                elif mword:
                    self.word = f'_{mword}_'
                    self.hmac += 1
                else:
                    self.word = f'_{self.word}__'

    def infer_pos(self, itm):
        '''
        for now we are just going to use one word
        not all of them, same with pos
        '''
        dct = {}
        tword =''
        for k, v in itm.items():
            obj = v.get(self.word)
            if obj:
                dct[k] = obj
                tword = obj
                self.pos = k

        if not dct:
            return 0
        else:
            return tword


    def basic(self):
        pos = self.pos
        if self.gender:
            pos = add_at_i(1,self.pos,self.gender)

        sz = f'{self.lem} {pos}'
        pts, _ = vgf.get_text_size(sz)
        space = (220 - pts) / 5
        sp = ' ' * int(space)
        self.lst.append(f'{sz}{sp}_{self.word}_  ')
        if self.idx != self.lidx:
            self.lst.append('')
            self.lst.append(self.idx)

    def petronius(self):
        pass

    def stats(self):
        num = round(self.hmac / self.tmac, 2)
        gnum = round(self.hgen / self.tgen, 2)
        p(f'macrons: {num} gender: {gnum}')

    def output(self):
        to.from_lst2txt(self.lst, f'{fold}{self.auth}_lasla')
        vgf.open_txt_file(f'{fold}{self.auth}_lasla')


class quick_lookup:
    def __init__(self):
        pass

    def begin(self, file):
        self.file = f'{dwn_dir}{file}'
        self.ofile = file
        self.get_atts()
        self.step1()

    def get_atts(self):
        self.def_lemmas = pi.open_pickle(f'{fold}def_lemmas', 1)
        self.macronizer = pi.open_pickle(f'{fold}macronizer_ncaps', 1)
        self.fake_enclitics = pi.open_pickle(f'{fold}fake_enclitics', 1)
        self.lem_freq_rank = pi.open_pickle(f'{fold}lem_freq_crude', 1)
        pass

    def step1(self):
        while 1:
            lst = to.from_txt2lst(self.file, 1)
            lst1 = []
            for x in lst:
                lst1 += x.split()
            for x in reversed(lst1):
                if ';' in x:
                    break
            self.look_up(x)

    def look_up(self, x):
        pass


class new_words:
    def __init__(self):
        pass

    def begin(self, file):
        self.file = file
        self.get_atts(file)
        self.step1()
        self.add2excel()
        self.export()

    def begin2(self, file):
        self.file = file
        self.get_atts(file, 'second')
        self.step1()
        self.add2excel()
        self.export(1)

    def begin_add(self, file):
        self.file = file
        self.get_atts(file, 'third')
        self.step1()
        self.add2excel()
        self.export(1)

    def get_atts(self, file, kind=0):
        self.def_lemmas = pi.open_pickle(f'{fold}co_lemmas5', 1)
        self.macronizer = pi.open_pickle(f'{fold}macronizer_ncaps', 1)
        self.fake_enclitics = pi.open_pickle(f'{fold}fake_enclitics', 1)
        self.lem_freq_rank = pi.open_pickle(f'{fold}lem_freq_crude', 1)
        p('done opening')
        ins = match_words()
        ins.remove_scansion = 1
        if kind == 'second':
            self.final_lst, self.exc_sh = ins.begin2(file, '@', 0, 'second')
        elif kind == 'third':
            self.final_lst, self.exc_sh = ins.begin2(file,';',0,'third')
        else:
            self.final_lst, self.exc_sh = ins.begin2(file)
        return

    def step1(self, divided=1):
        for e, l in en(self.final_lst):
            if divided:
                lword = l[1]
            else:
                lword = l[0]
            if '_' not in lword:
                lwordu = norm_str_jv(lword)
                lwordu, enc = enclitics(lwordu, self.fake_enclitics)
                itm = self.macronizer.get(lwordu)
                if itm:
                    tot_def = []
                    for k, dct in itm.items():
                        for lemma, plst in dct.items():
                            pos = " ".join(plst)
                            lemu = norm_str_jv(lemma)
                            lemmacl = self.def_lemmas.get(lemu)
                            freq = self.lem_freq_rank.get(lemu, -1)
                            if not lemmacl:
                                p(f'missing lemmas {lemu} {l[0]}')
                            else:
                                defn = get_def(lemmacl, 1)
                                tot_def += [k, freq, lemma, pos, defn]
                    if tot_def:
                        l += tot_def
                    self.final_lst[e] = l
                else:
                    p(f'could not find {lwordu}')

        return

    def add2excel(self):
        self.exc_sh = self.exc_sh[1:]
        self.exc_sh = [x[1:] for x in self.exc_sh]

        for e, x in en(self.final_lst):
            y = [None,self.file, x[0], None, ] + x[1:]
            self.final_lst[e] = y
        self.final_lst = self.exc_sh + self.final_lst
        return

    def export(self, add=0):
        # if add:
        file2 = f'{lfold}vocab2'
        # else:
        #     file2 = f'{lfold}vocab'
        ef.from_lst2book(self.final_lst, file2)
        ef.open_wb(file2)


def beautify_packhum(file):
    file = f'{dwn_dir}{file}'
    lst = to.from_txt2lst(file, 1)
    for e, x in en(lst):
        x = x.replace('\t', '')
        lst1 = x.split()
        try:
            lst2 = [z for z in lst1 if not reg(r'[0-9]', z)]
            lst2 = [y.replace(';', ',') for y in lst2]
            lst[e] = ' '.join(lst2)

        except:
            p(f'error in {x}')
    lst = elim_end_hyphen(lst)
    to.from_lst2txt(lst, f'{file}2')
    vgf.open_txt_file(f'{file}2')


def beautify_deoque(file):
    file1 = f'{dwn_dir}{file}'
    # pfold = f'{lfold}poetry/'
    # file1 = f"{pfold}{file}"
    file2 = file + '2'
    lst = to.from_txt2lst(file1, 1)
    lst1 = []
    for x in lst:
        if x.startswith('__'):
            lst1.append(x)
        elif '*' in x:
            lst1.append(x)

        elif 'ERROR' in x:
            pass
        elif 'Attenzione!' in x:
            pass

        elif x.isdigit():
            pass
        elif ha(x):
            lst2 = x.split()
            lst3 = [y for y in lst2 if reg(r'[^SD—\|]', y)]
            lst3 = [y.replace(';', ',') for y in lst3]
            s = ' '.join(lst3)
            lst1.append(s)
    lst1 = [x for x in lst1 if hl(x)]
    to.from_lst2txt(lst1, file2)
    vgf.open_txt_file(file2)


def beautify_doc_in_perseus():
    file = 'horace_ap_eng'
    pfold = f'{lfold}poetry/'
    file1 = f"{pfold}{file}"
    file2 = f"{pfold}{file}2"
    lst2 = to.from_xml2txt(file1)
    to.from_lst2txt(lst2, file2)
    vgf.open_txt_file(file2)


if eval(not_execute_on_import):
    if vgf.pycharm():
        args = [0, 'er', 'horace_ap_itrans', 'IX', '', 0, 0]
    else:
        args = vgf.get_arguments()

    if args[1] == 'nw':
        ins = new_words()
        ins.begin(args[2])
    elif args[1] == 'fo':
        focus(args[2])
    elif args[1] == 'er':
        extract_rearrange(args[2])

    elif args[1] == 'nwa':
        # if we are adding more words but using ;
        ins = new_words()
        ins.begin_add(args[2])

    elif args[1] == 'lpt':
        ins = lasla_pos_txt()
        ins.begin()

    elif args[1] == 'nw2':
        '''
        if there are @ on the foreign text
        '''
        ins = new_words()
        ins.begin2(args[2])

    elif args[1] == 'adi':
        '''
        if there are @ on the itrans text
        '''
        ins = new_words()
        ins.begin_add(args[2])

    elif args[1] == 'rt':
        ins = parse_old()
        ins.begin()
    elif args[1] == 'bp':
        beautify_packhum(args[2])
    elif args[1] == 'ph':
        ins = phi()
        ins.begin()

    elif args[1] == 'bd':
        beautify_deoque(args[2])

    elif args[1] == 'rc':
        running_check(args[2])
