import time, shutil
from bglobals import *
if not public:
    from other.learn_language import match_words, interlinear_translation
    from other.filter_txt import elim_end_hyphen

'''
"Sḗmĭs."1 ăn,1.1 hǣ́c3.5 ănĭmṓs9 ǣrū́go;4 ‿ēt5 cū́ră6 pĕcū́li;7
Cū́m2 sĕmĕl3 ī́mbŭĕrī́t,;8 spērḗmūs9 cā́rmĭnă12 fī́ngi11
Pṓssĕ10 lĭnḗndă;12 cĕdro;13 ‿ḗt14 lēuī́;16 sēruā́ndă15 cŭprḗsso?17 

in this passage we need an error message for two words with same number

'''


def help():
    p(f"""
    
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
        self.divide_seneca()
        self.shorten_auth_names()
        self.step1()
        self.move_phi()
        self.combine_works()
        # self.get_auth2words()
        # self.get_auth2words2()
        self.word2age()



    def get_atts(self):
        self.auth2work = defaultdict(dict)
        self.auth2num = defaultdict(dict)
        self.auth2words = defaultdict(dict)
        self.auth2date = {}
        self.auth2abb = {}
        self.poetic_lines = []
        self.for_move = defaultdict(list)
        self.unknown_dates = {}
        self.poets = set()
        self.phi_freq = defaultdict(int)
        self.poet2work = defaultdict(dict)
        self.poet2work2 = defaultdict(dict)

    def step1(self):
        poems_w_hyphen = to.from_txt2lst(f'{fold}phi_poems_hyphen')
        b = 0
        for auth in os.listdir(f'{phi_fold}'):
            oauth = auth
            if oauth == 'Publius Ovidius Naso':
                bb=8
            auth = self.auth2abb.get(auth,auth)
            auth3 = auth
            authp = f'{auth}_poet'


            if auth[0] != '.':
                file = f'{phi_fold}{oauth}'
                for work in os.listdir(file):
                    if not work == ds:
                        auth = auth3
                        b += 1
                        work = work[:-4]

                        poem = 0
                        vgf.print_intervals(b, 5, None, 800)
                        file2 = f'{file}/{work}'
                        lst = to.from_txt2lst(file2)
                        self.for_move[oauth].append((auth, work))
                        only_poetry = 0
                        self.auth2work[auth][work] = lst

                        if not auth in self.poets:
                            only_poetry = self.is_poetry(lst, work)

                        auth = self.change_auth.get((work,auth), auth)
                        if work[:-4].lower() in poems_w_hyphen:
                            lst = self.remove_hyphen(lst)
                        if auth in self.poets:
                            perc = self.is_poetry(lst,work,1)
                            if perc > 5:
                                bb=8
                            poetry = lst
                            prose = []
                            poem=1
                        elif '_poet' in auth:
                            poetry = lst
                            prose = []
                            poem=1

                        elif only_poetry:
                            poetry = lst
                            prose = []
                            poem = 1
                        else:
                            poetry, prose = self.divide_poet_prose(lst)
                            prose = self.remove_hyphen(prose)

                        for e, lst in en([prose, poetry]):
                            if lst:
                                if auth in self.poets:
                                    auth2 = auth
                                elif e:
                                    auth2 = authp
                                    poem = 1
                                elif poem:
                                    auth2 = authp
                                elif '_poet' in auth:
                                    auth2 = authp
                                    poem = 1
                                else:
                                    auth2 = auth
                                if poem:
                                    self.poet2work2[auth2][work] = lst

                                dct, total = self.small_normalize(lst, poem)
                                if not total:
                                    bb=8
                                self.auth2num[auth2][work] = total
                                self.auth2words[auth2][work] = dct
                                if poem:
                                    self.poet2work[auth2][work] = total

        self.auth2work = sort_dct_key(self.auth2work)
        self.auth2num = sort_dct_key(self.auth2num)
        self.poet2work = sort_dct_key(self.poet2work)
        return

    def combine_works(self):
        self.auth2words_com = {}
        d = 0
        for auth, works in self.auth2words.items():
            dct = defaultdict(int)
            for work, dct1 in works.items():
                for word, num in dct1.items():
                    dct[word] += num
                    self.phi_freq[word] += num
                    d += num
            self.auth2words_com[auth] = dct
        self.total = sum(self.phi_freq.values())
        tot = vgf.good_numbers(self.total,2)
        pl = set(self.poetic_lines)
        p (f'total words {tot}')
        p (f'total poetic lines {len(self.poetic_lines)}')
        p (f'without repeats {len(pl)}')
        return


    def poetry_database(self): #175
        pass

    def is_poetry(self, lst,name, ratio=0):
        '''
        this algorithm doesnt completely work for those authors
        which are extremely fragmentary since most fragments do
        not have hyphens, but right now we're only worried about
        authors with more than 5000 words
        '''

        titles = ['carmen','tragoediae','palliatae', 'praetexta',
                  'praetextae','carmina','tragoedia','togata','comoed']

        tot = len(lst)
        b=0
        for x in lst:
            if x.endswith('-'):
                b += 1
        perc = vgf.percent(b,tot)
        if ratio:
            return perc


        if perc < 2 and b < 3:
            if len(lst)< 50:
                for tit in titles:
                    if tit in name.lower():
                        return 1
                return 0
            else:
                return 1
        else:
            return 0


    def divide_poet_prose(self, lst):
        poem_indent = chr(160) + chr(160) + chr(160) + chr(160)
        poem_indent2 = chr(160) + chr(160) + chr(160)
        prose = []
        poetry = []
        for x in lst:
            if x.startswith(poem_indent2):
                poetry.append(x)
            else:
                prose.append(x)
        return poetry, prose

    def divide_seneca(self):
        file = f'{fold}seneca_divide'
        lst = to.from_txt2lst_tab_delim(file)
        self.change_auth = {}
        for l in lst:
            work = l[0]
            bool1 = 0
            try:
                bool1 = l[1]
            except:
                pass
            if bool1 == 1:
                self.change_auth[(work[:-4], 'seneca')] = 'seneca_poet'
            elif bool1 == 2:
                self.change_auth[(work[:-4],'seneca')] = 'seneca_pseudo'


        self.poets.add("seneca_pseudo")
        self.poets.add("seneca_poet")


    def small_normalize(self, lst, poem=0):
        words = []
        dct = defaultdict(int)
        for x in lst:
            if x and x[0] == '#':
                pass
            else:
                ox = x
                x = re.sub(r'[^a-zA-ZáéúÁÉÓÍÚíóāēīōūȳăĕĭŏŭўĀĒĪŌŪȲ\s]', '', x)
                x = unidecode(x)
                x = jv.replace(x)
                x = x.lower()
                x = x.strip()
                if x == 'char gl k':
                    bb=8
                if poem:
                    self.poetic_lines.append(x)
                words += x.split()
        for x in words:
            dct[x] += 1
        total = sum(dct.values())
        return dct, total

    def remove_hyphen(self, lst):
        lst = [x for x in lst if not x[0] == '#']
        for e, x in en(lst):
            lst[e] = x.replace(' *', '*')

        for b in range(len(lst) - 1):
            x = lst[b]
            y = lst[b + 1]
            if x and x[-1] == '-':
                y = y.split()
                yu = y[0]
                y = ' '.join(y[1:])
                x = x[:-1] + yu
                lst[b] = x
                lst[b + 1] = y

        return lst

    def get_auth2words(self):
        self.long_works = {}
        for auth, works in self.auth2num.items():
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

    def get_auth2words2(self):
        dct = defaultdict(int)
        for k, v in self.auth2num.items():
            num = 0
            for x, y in v.items():
                num += y
            dct[k] = num
        dct = sort_dct_val_rev(dct)
        self.auth2num2 = dct
        # 99.69, 7.73 million words
        b = 0
        total = 0
        d = 0
        self.focus = set()
        for k, v in dct.items():
            if v > 500:
                self.focus.add(k)
                b += 1
                d += v
            total += v
        p(d, total, d / total)

    def shorten_auth_names(self):
        # u2l = {k.lower(): k for k in self.auth2num.keys()}
        u2l = {k.lower(): k for k in os.listdir(f'{phi_fold}') if k != ds}
        lst1 = to.from_txt2lst_tab_delim(f'{fold}phi_auth2')
        lst = to.from_txt2lst_tab_delim(f'{fold}phi_auth', 0, 1)
        lst2 = []
        for g, x in en(lst1):
            if x[0] == '__stop':
                break
            lst2.append(x)
        lst2 += lst
        # because of the function divide_seneca he is given a special case
        lst2 = [x for x in lst2 if x[0] != 'Lucius Annaeus Seneca iunior']
        miss = set()
        start = g
        done = set()
        for g, l in en(lst2):
            oname = l[0]
            if type(oname) != int:
                if oname.lower() == 'iustinianus':
                    bb = 8
                udate = None
                if oname == 'Publius Ovidius* Naso':
                    bb = 8
                name = oname
                name = name.replace('*', '')
                if name.lower() not in done:
                    done.add(name)
                    if g < start:
                        fname = u2l.get(name)
                        if fname == None:
                            bb = 8
                    else:
                        fname = name
                    birth = None
                    death = None
                    other = None
                    other2 = None
                    try:
                        birth = l[1]
                        death = l[2]
                        other = l[3]
                        other2 = l[4]
                    except:
                        pass
                    if birth and type(birth) == str and "?" in birth:
                        udate = birth.replace('?', "")
                        udate = int(udate)
                        birth = None
                    if birth == '':
                        birth = None
                    if death == '':
                        death = None
                    if other == '':
                        other = None
                    if other2 == '':
                        other2 = None

                    oname2 = oname
                    if type(death) == str:
                        oname2 += f' {death}'
                    if other and other != 'po':
                        oname2 += f' {other}'
                    if '*' in oname2:
                        aname = oname2.split()
                        aname = [x[:-1] for x in aname if '*' in x]
                        aname = ' '.join(aname)
                    else:
                        aname = name
                    aname = aname.lower()
                    if udate != None:
                        self.unknown_dates[aname] = udate
                    if fname not in self.auth2abb:
                        self.auth2abb[fname] = aname
                    if other == 'po' or other2 == 'po':
                        self.poets.add(aname)
                    if death == 'po':
                        self.poets.add(aname)
                        death = None


                    approx = None
                    approx2 = None
                    if birth != None:
                        if type(death) == str:
                            death = None

                        if birth == '_':
                            birth = None
                        if birth != None and death == None:
                            death = birth
                            birth = None

                        if birth != None and death != None:
                            approx = birth + 30
                        elif death != None:
                            if death % 50 == 0:
                                approx = death
                            else:
                                approx = death - 20

                        if approx != None:
                            if approx % 50 == 0:
                                approx2 = approx
                            else:
                                b = approx // 50
                                rem = approx % 50
                                if approx > 0 and rem > 25:
                                    b += 1
                                if approx < 0 and rem > 25:
                                    b += 1

                                approx2 = b * 50
                    if approx2 != None:
                        if aname not in self.auth2date:
                            self.auth2date[aname] = approx2
        assert 'ovidius' in self.auth2date
        assert 'iustinianus' in self.auth2date
        return


    def move_phi(self):
        b = 0
        for k,v in self.for_move.items():
            for z in v:
                b += 1
                vgf.print_intervals(b,5,None,800)
                auth, work = z
                work2 = work.lower()
                fold2 = f'{phi_fold2}{auth}'
                if not os.path.exists(fold2):
                    os.mkdir(fold2)
                src = f'{phi_fold}{k}/{work}.txt'
                dest = f'{phi_fold2}{auth}/{work2}.txt'
                shutil.copy(src, dest)




    def word2age(self):
        self.auth2num2ab = {self.auth2abb[k]: v for k, v in self.auth2num2.items()}
        self.auth2date['cicero']=-75
        self.auth2date['cicero_poet']=-75
        self.age2word = defaultdict(int)
        for x, y in self.auth2date.items():
            obj = self.auth2num2ab.get(x)
            if obj:
                self.age2word[y] += obj
        for x, y in self.age2word.items():
            self.age2word[x] = vgf.good_numbers(y, 2)
        self.age2word = sort_dct_key(self.age2word)
        self.auth2date = sort_dct_val(self.auth2date)
        self.poets = list(self.poets)
        self.poets.sort()

        return


def extract_rearrange(file):
    '''
This will take every line in an _itrans document and put it on a new file so that you can
read the rearrangement with ease.  in the _itrans doc every latin line that ends with ,, is
followed by a rearranged line

    '''

    file1 = f'{dwn_dir}{file}'
    file2 = f'{dwn_dir}{file}'
    t = 'ī́'
    p(ord(t[-1]))

    file2 = file2.replace('_itrans', '') + '_rearr'
    lst = to.from_txt2lst(file1, 1)
    lst1 = []
    for e, x in en(lst):
        if x and x[0].isdigit():
            num = x[:x.index(' ')]

        if x.endswith(',,'):
            s = lst[e + 2]
            s = unidecode(s)
            s = re.sub(r'[\",\.\?]', '', s)
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
    lst = to.from_txt2lst(file1, 1)
    lst1 = vgf.clump_lst(lst, 1)
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
    to.from_lst2txt(nums, file2)
    to.from_lst2txt(lst5, file3)
    to.from_lst2txt(lst6, file4)
    vgf.open_txt_file(file2)
    return


class lasla_pos_txt(phi):
    def __init__(self):
        phi.__init__(self)

    def begin(self):  # 200013
        self.get_atts()
        # self.simplify_old()
        self.any_author()
        self.stats()
        # self.add_elision()
        # self.temp_text()
        self.output()

    def get_atts(self):
        self.lasla_db2 = pi.open_pickle(f'{fold}lasla_db2')
        self.las_freq = pi.open_pickle(f'{fold}las_lem_freq')
        self.co_lemmas4 = pi.open_pickle(f'{fold}co_lemmas4')
        self.llemclem = pi.open_pickle(f'{fold}llem2clem2')
        self.noun2gender = pi.open_pickle(f'{fold}lasla_noun2gen')
        self.lem2forms_rev_ui = pi.open_pickle(f'{fold}lem2forms_rev')
        self.lem2forms_rev_jv = pi.open_pickle(f'{fold}lem2forms_rev_jv')
        self.old_wonum = pi.open_pickle(f'{fold}old_wdef')
        self.old_simple = pi.open_pickle(f'{fold}old_simple')
        self.old_variant = pi.open_pickle(f'{fold}old_var2parent')
        self.miss_def = {}
        self.kind = 'pet'
        self.auth = 'Petronius'
        self.tpos = {
            'C': 'm',
            'X': 'm',
            'B': 'm',
        }

    def research_ui(self):
        self.old_wonum = pi.open_pickle(f'{fold}old_wdef')
        dct = {}
        for k, v in self.old_wonum.items():
            if 'ui' in k and not 'qui' in k:
                dct[k] = v.wmacron
        dct1 = {}
        for k, v in self.old_wonum.items():
            if 'ui' in k and not 'qui' in k:

                if hasattr(v, 'wmacron') and tie in v.wmacron:
                    dct1[k] = v.wmacron

    def simplify_old(self):
        dct = defaultdict(dict)
        for k, z in self.old_wonum.items():
            ku, num = cut_num(k, 1)
            pos = " ".join(z.pos)
            s = f'{z.wmacron} {pos} {z.inflection}'
            t = ''
            for x, y in z.defs.items():
                if y:
                    t += f"{x} {y}"
            dct[ku.lower()][num] = [s, t]

        b = 0
        for k, v in dct.items():
            if len(v) > 1:
                b += 1
        p(b)
        pi.save_pickle(dct, f'{fold}old_simple')
        self.old_simple = dct
        return

    def any_author(self):
        self.lst = []
        self.lidx = ''
        self.bad_pos = set()
        self.tgen = 0
        self.missing = defaultdict(int)
        self.hgen = 0
        self.tmac = 0
        self.gdef = 0
        self.error = []
        self.hmac = 0
        for k, books in self.lasla_db2[self.auth].items():
            self.aut_book = k
            if k == 'PetroniusSatiricon_PetronSa':
                self.books = books
                for e, v in en(books):
                    vgf.print_intervals(e, 500, None, len(books))
                    self.idx = v[3]
                    self.lem = v[1]
                    self.lemu, self.num = cut_num(self.lem, 1)
                    self.lemu = self.lemu.lower()
                    self.cat = v[0]
                    freq = self.las_freq.get(self.lem.lower(), 0)
                    self.get_defn(freq)
                    self.word = v[2]
                    self.word_jv = ''
                    self.gender = self.noun2gender.get(self.lem, '')
                    self.pos = v[4]
                    self.pos2 = ''
                    self.noun_gender()
                    if self.cat != '!' and self.pos not in ['_gr']:
                        self.tmac += 1
                        if self.kind != 'simple':
                            self.add_macrons()
                    if self.lidx != self.idx:
                        self.lst.append([self.idx])
                    if not self.word_jv:
                        self.missing[(self.lem, self.word, self.pos)] += 1
                    if self.pos2:
                        self.pos = self.pos2
                    if not self.word_jv:
                        self.word_jv = self.word + circle
                    v.append(self.word_jv)
                    if self.defn:
                        itm = vgf.dct_idx(self.defn, 0, 'v')
                        self.lst.append(['', self.lem, self.word,
                                         self.word_jv, freq, self.pos,
                                         itm[0], itm[1]])

                        if len(self.defn) > 1:
                            h = 0
                            for g, r in self.defn.items():
                                if h > 0:
                                    self.lst.append(['', '', '', '', '', '', r[0], r[1]])

                                h += 1

                    else:
                        self.lst.append(['', '', self.lem, self.word, self.word_jv, self.pos])
                    self.lidx = self.idx
                if self.kind == 'pet':
                    self.output(1)
        self.missing = sort_dct_val_rev(self.missing)
        self.miss_def = sort_dct_val_rev(self.miss_def)
        return

    def get_defn(self, freq):
        obj = self.old_simple.get(self.lemu)
        if not obj:
            if self.lemu in encs:
                self.gdef += 1
            else:
                obj = self.old_variant.get(self.lemu)
                if not obj and self.num not in ['8', '9']:
                    self.miss_def[self.lemu] = freq
                elif obj:
                    self.gdef += 1
                    lst = []
                    for k, v in obj.items():
                        vu, num = cut_num(v, 1)
                        try:
                            lst.append(self.old_wonum[vu][num])
                        except:
                            self.error.append(self.lemu)
                            pass
                    if lst:
                        self.defn = lst



        else:
            self.defn = obj
            self.gdef += 1

    def temp(self):
        dct8 = {}
        for x, y in dct7.items():
            st = set()
            for k, v in y.items():
                vu = cut_num(v)
                st.add(vu)
            if len(st) > 1:
                dct8[x] = y

    def temp_text(self):
        lin = ''
        lst1 = []
        b = 0
        for e, x in en(self.lst):
            vgf.print_intervals(e, 100, None, len(self.lst))
            if len(x) == 1:
                if e and lin:
                    lst1.append(lin)
                    lin = ''
                num = x[0].strip()
                if num.endswith(',1'):
                    lst1.append('')
                    lst1.append(f'CAPUT {num[:-2]}')
                    lst1.append('')

            else:
                word = x[2]
                if word[0] == el:
                    lin += word
                else:
                    lin += " " + word
            if len(lin) > 50:
                pts, _ = vgf.get_text_size(lin)
                if pts > 467:
                    lst1.append(lin)
                    lin = ''
        file = f'{dwn_dir}petronius_mac'
        to.from_lst2txt(lst1, file)
        vgf.open_txt_file(file)
        return

    def enclitic_stress(self):
        """
        When an enclitic is joined to a word, the accent falls | on the syllable next before the enclitic, whether long or short: as, dĕă'que,\
which words retain the accent of the complete words which have lost a vowel | Certain words which have lost a final vowel retain the accent of the complete words: as, illī'c forillī'ce, prōdū'c for prōdūce, sati'n for sati'sne.\

name two exceptions to accent rules | 1 Certain apparent compounds of faciō retain the accent of the simple verb. 2. In the second declension the genitive and vocative of nouns in -ius and the genitive of those in -ium retain the accent of the nominative\

If the vowel or syllable ending in -m is long by nature, it usually will not be elided (so for instance in Demosthenem the final syllable will always be pronounced, even if it comes before a vowel.

For the most part, a long vowel at the end of a word coming before a vowel at the beginning of the next word is elided; but in the case of o, u and i, it sometimes happens that the result is like the addition of a consonant, v or j:  immo age for instance sounds like “im-mwa-ge.”  See Allen’s Vox Latina for more details.

        """
        pass

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
                itm = self.lem2forms_rev_jv.get(lem_wn + cnum)
                itm2 = self.lem2forms_rev_ui.get(lem_wn + cnum)
                mword = 0
                mword_ui = 0
                if itm:
                    if special:
                        self.infer_pos(itm2, itm)
                    else:

                        words = itm.get(pos2)
                        words_ui = itm2.get(pos2)
                        if words:
                            mword = words
                            mword_ui = words_ui

                        elif vgf.dct_idx(itm) == 'inv':
                            mword_ui = itm2['inv']
                            mword = itm['inv']
                        else:
                            self.bad_pos.add(self.pos)

                if mword_ui:
                    try:
                        idx = mword_ui.index(self.word)
                        self.word_jv = mword[idx]
                        self.hmac += 1
                    except ValueError:
                        pass

        return

    def infer_pos(self, itm, itm_jv):
        '''
        for now we are just going to use one word
        not all of them, same with pos
        '''
        done = 0
        for k, v in itm.items():
            try:
                idx = v.index(self.word)
                if not done:
                    self.word_jv = itm_jv[k][idx]
                    done = 1
                    self.hmac += 1
                self.pos += k + ' '
            except ValueError:
                pass

    def noun_gender(self):
        if self.gender:
            self.pos2 = add_at_i(1, self.pos, self.gender)

    def stats(self):
        num = round(self.hmac / self.tmac, 2)
        gnum = round(self.hgen / self.tgen, 2)
        dnum = round(self.gdef / self.tmac, 2)

        p(f'macrons: {num} gender: {gnum} definition: {dnum}')

    def output(self, kind=0):
        if kind == 1:
            file = f'{lfold}lasla2/{self.aut_book}'
            to.from_lst2txt_tab_delim(self.books, file)

        # file = f'{dwn_dir}petr'
        # for e, x in en(self.lst):
        #     try:
        #         self.lst[e][2] = x[2].replace(el, '')
        #     except:
        #         pass
        #
        # ef.from_lst2book(self.lst, file)
        # ef.open_wb(file)
        return


'''
things we have don't yet for the below class
mid punctuation is still not coded for, so
[ ] < > can appear within a word
for those words which are not matched to phi
if they have a j or v it will be put back on
better to make two texts, one without [ ] < >
C. is getting rendered as C..
should probably replace numbers with words such as III

some quotes can be put on the wrong words


'''


class punctuate_lasla(lasla_pos_txt):
    '''
    the enclitics are not getting printed

    '''

    def __init__(self):
        lasla_pos_txt.__init__(self)

    def begin(self):
        self.get_atts()
        self.normalize_las()
        self.elim_enc()
        self.phi_lst = self.remove_hyphen(self.phi_lst)
        self.normalize_phi()
        self.normalize_phi2()
        self.match_phi2las()
        self.add_punc()
        self.add_elision()
        self.add_paragraphs()

    def get_atts(self):
        self.kind = ''
        if public:
            self.phi_lst = to.from_txt2lst(f'{fold}satyrica')
        else:
            self.phi_lst = to.from_txt2lst(f'{phi_fold2}petronius/satyrica')
        # if self.kind != 'all':
        #     self.lasla_db2 = pi.open_pickle(f'{fold}lasla_db2')
        # self.ltxt = self.lasla_db2['Petronius']['PetroniusSatiricon_PetronSa']
        file = f'{lafold2}PetroniusSatiricon_PetronSa'
        self.ltxt = to.from_txt2lst_tab_delim(file, 1, 0)
        self.normalize_las()
        self.ltxtw = [x[2].strip() for x in self.ltxt]
        self.ltxtw = [x.lower() for x in self.ltxtw]

    def normalize_las(self):
        '''
        get rid of the |st in the j_lasla2 file
        '''

        self.ltxt = [x for x in self.ltxt if x[4] not in ['_rf', "_rp", '_nsp']]
        for e, x in en(self.ltxt):
            if '|st' in x[2]:
                self.ltxt[e][2] = x[2][:-3]
                self.ltxt[e + 1][2] = 'est'
            if '|s' in x[3]:
                self.ltxt[e][2] = x[2][:-1]
                self.ltxt[e + 1][2] = 'es'
        return

    def normalize_phi(self):
        poem_indent = chr(160) + chr(160) + chr(160) + chr(160)
        poem_indent2 = chr(160) + chr(160) + chr(160)
        para_indent = chr(160) + chr(160)
        one = '¹'
        four = '⁴'

        for e, x in en(self.phi_lst):
            x = x.replace(' . . .', '$ ')

            if 'agri iacent' in x:
                bb = 8
            if poem_indent2 in x:
                x += '+'
            if poem_indent in x:
                x = re.sub(r'' + chr(160) + '{4,}', "@", x)

            x = x.replace(poem_indent, '@')
            x = x.replace(poem_indent2, '&')
            x = x.replace(para_indent, '%')
            x = x.replace(" *", '*')
            x = x.replace('—', ', ')
            x = x.replace(', ,', ', ')
            x = x.replace(';', ',')
            x = re.sub(r'[' + one + four + ']', '', x)
            x = re.sub(r'\s{2,}', ' ', x)
            x = x.rstrip()
            self.phi_lst[e] = x.lower()

        return

    def normalize_phi2(self):
        '''
        for bpunc which can be either on the beginning
        of the word or the end, we will have to make it
        such that every odd indexed bpunc character is on the
        left and every even indexed bpunc is on the right

        '''

        punctuation = ',.{}"():!?[]<>†$*@%&+' + "'"
        self.punctuation = punctuation
        lpunc = '{([<@%&'
        rpunc = '})]>*+,.:!?"$'
        assert not set(lpunc) & set(rpunc)
        bpunc = '†"' + "'"
        self.phi_lst2 = []
        for x in self.phi_lst:
            self.phi_lst2 += x.split()

        for e, x in en(self.phi_lst2):
            xo = re.sub(r'[,\.\{\}"\(\):\+!\?\[\]\<\>†\$@&%\'\*]', '', x)
            if not xo:
                if x in lpunc:
                    self.phi_lst2[e + 1] = x + self.phi_lst2[e + 1]
                    self.phi_lst2[e] = ''
                elif x in rpunc or x in bpunc:
                    self.phi_lst2[e - 1] = x + self.phi_lst2[e - 1]
                    self.phi_lst2[e - 1] = ''
        self.phi_lst2 = [x for x in self.phi_lst2 if x]
        self.lpunc_dct = {}
        self.rpunc_dct = {}
        for e, x in en(self.phi_lst2):
            s = ""
            xo = x
            for z in x:
                if z in punctuation:
                    s += z
                else:
                    break
            if s:
                self.lpunc_dct[e] = s

            s = ""
            for z in reversed(x):
                if z == "*":
                    bb = 8

                if z in punctuation:
                    s = f'{z}{s}'
                else:
                    break
            if s:
                self.rpunc_dct[e] = s
                if s == '@' and self.lpunc_dct[e] == '@':
                    bb = 8

            x = re.sub(r'[,\.\{\}"\(\):\+!\?\[\]\<\>†\$@&%\'\*]', '', x)
            x = jv.replace(x)
            if not x:
                bb = 8
            self.phi_lst2[e] = x.lower()

    def elim_enc(self):
        b = len(self.ltxtw) - 1
        b = 0
        olst = copy.deepcopy(self.ltxtw)
        self.idx2enc = {}
        self.idx2enc2 = {}
        while b < len(self.ltxt):
            word = self.ltxt[b][2]
            lem = self.ltxt[b][1]
            if word == 'titulos':
                bb = 8
            lst = self.ltxt[b]
            if word in ['que', 'ue'] or lem == 'ne2':
                self.ltxtw[b - 1] += word
                self.idx2enc[b - 1] = word
                self.idx2enc2[b - 1] = lst
                del self.ltxtw[b]
                del self.ltxt[b]
            else:
                b += 1
            bb = 8
        # c = 0
        # for idx, word in self.idx2enc.items():
        #     word1 = self.ltxtw[idx + c]
        #     self.ltxtw[idx + c] = word1[:-len(word)]
        #     self.ltxtw.insert(idx + 1 + c, word)
        #     bb = 8
        #     c += 1

        return

    def spaced(self, pidx):
        b = self.lword.count(' ')
        if b == 2:
            pnxt3 = " ".join(self.phi_lst2[pidx:pidx + 3])
            if self.lword == pnxt3:
                return pidx + 2
        elif b == 1:
            pnxt2 = " ".join(self.phi_lst2[pidx:pidx + 2])
            if self.lword == pnxt2:
                return pidx + 1

    def isgreek(self, x):
        xu = re.sub(r'[αβψδεφγηιξκλμνοπρστθωςχυζΑΒΨΔΕΦΓΗΙΞΚΛΜΝΟΠΡΣΤΘΩΥΖέἀῖëῖί]', '', x)
        if not xu:
            return 1
        if len(xu) / len(x) > .1:
            self.almost_greek.append(x)
            if not public:
                p(f'almost greek {x}')
            return 2
        self.should_be_greek.append(x)

    def match_phi2las(self):
        self.no_rpunc = []
        self.no_lpunc = []
        self.l2p = {}
        self.p2l = {}
        self.greek = {}
        self.mismatches = 0
        self.almost_greek = []
        self.should_be_greek = []
        pidx = 0
        lidx = 0
        while pidx < len(self.phi_lst2):
            if pidx == 251:
                bb = 8
            self.mirror = 0
            self.pword = self.phi_lst2[pidx].lower()
            self.lword = self.ltxtw[lidx].lower()
            if self.lword == 'etiam si':
                bb = 8
            if self.lword == 'quam ob rem':
                bb = 8
            pidx2 = self.spaced(pidx)
            if pidx2:
                pidx = pidx2
            else:
                if self.lword == 'greek' and self.isgreek(self.pword):
                    self.greek[lidx] = self.pword
                elif self.pword != self.lword:
                    dist = vgf.lvn.distance(self.pword, self.lword)
                    if dist > 2:
                        pidx, lidx = self.match_phi2las2(pidx, lidx)
            if not self.mirror:
                self.l2p[lidx] = pidx
                self.p2l[pidx] = lidx
            pidx += 1
            lidx += 1
        if not public:
            p(self.mismatches)
        return

    def match_phi2las2(self, pidx, lidx):
        '''
        mecum, tecum, secum, vobiscum, nobiscum
        - space in p not in l
        - mirror image
        mēcum
        '''

        pidx3, lidx3 = self.cum_enclit(pidx, lidx)
        if pidx3:
            return pidx3, lidx3
        pidx3, lidx3 = self.pspace(pidx, lidx)
        if pidx3:
            return pidx3, lidx3
        pidx3, lidx3 = self.mimage(pidx, lidx)
        if pidx3:
            return pidx3, lidx3

        nlst = []
        op = pidx
        ol = lidx
        for i in range(10):
            for j in range(10):
                if i == 0 and j == 0:
                    pass
                else:
                    nlst.append((i, j))
        found = 0
        for tpl in nlst:
            b, c = tpl
            pidx2 = pidx + b
            lidx2 = lidx + c
            pnxt3 = " ".join(self.phi_lst2[pidx2:pidx2 + 3]).lower()
            lnxt3 = " ".join(self.ltxtw[lidx2:lidx2 + 3]).lower()
            if pnxt3 == lnxt3:
                found = 1
                break

        if not found:
            p(self.phi_lst2[pidx:pidx + 20])
            p(self.ltxtw[lidx:lidx + 20])
            pidx2 = pidx + 7
            lidx2 = lidx + 7

        oddp = self.phi_lst2[op:pidx2]
        oddl = self.ltxtw[ol:lidx2]
        oddp = ' '.join(oddp)
        oddl = ' '.join(oddl)
        if oddl == 'etiam si':
            bb = 8
        if not oddp and not oddl:
            bb = 8

        if oddp == 'mecum':
            bb = 8

        if not public:
            p(f'p: {oddp} l: {oddl}')
            p('')
        self.mismatches += 1

        return pidx2, lidx2

    def cum_enclit(self, pidx, lidx):
        if pidx == 10718:
            bb = 8

        if self.pword in ['mecum', 'tecum', 'secum',
                          'uobiscum', 'nobiscum']:
            lnxt2 = " ".join(self.ltxtw[lidx:lidx + 2]).lower()
            lnxt2 = lnxt2.replace(' ', '')
            if lnxt2 == self.pword:
                self.no_rpunc.append(pidx)
                self.ltxt[lidx + 1][5] = f'^cum'
                return pidx, lidx + 1
        return 0, 0

    def pspace(self, pidx, lidx):
        if self.lword == 'inuicem':
            bb = 8

        pnxt2 = "".join(self.phi_lst2[pidx:pidx + 2]).lower()
        if pnxt2 == self.lword:
            self.no_rpunc.append(pidx)
            self.no_lpunc.append(pidx + 1)
            return pidx + 1, lidx
        return 0, 0

    def mimage(self, pidx, lidx):
        pnxt2 = " ".join(self.phi_lst2[pidx:pidx + 2]).lower()
        lnxt2 = f'{self.ltxtw[lidx + 1]} {self.ltxtw[lidx]}'
        if pnxt2 == lnxt2:
            self.p2l[pidx] = lidx + 1
            self.p2l[pidx + 1] = lidx - 1
            self.mirror = 1
            return pidx + 1, lidx + 1
        return 0, 0

    def add_punc(self):
        miss = []
        klst = list(self.p2l.keys())
        vlst = list(self.p2l.values())

        for k, v in self.lpunc_dct.items():
            num = self.p2l.get(k)
            if num == None:
                if v in '@&%':
                    bb = 8
                miss.append(k)
            else:
                word = self.ltxt[num][5]
                self.ltxt[num][5] = f'{v}{word}'

        for k, v in self.rpunc_dct.items():
            num = self.p2l.get(k)
            if num == None:
                if v in '+*$':
                    bb = 8
                miss.append(k)
            else:
                word = self.ltxt[num][5]
                self.ltxt[num][5] = f'{word}{v}'
        self.ltxt2 = [x[5] for x in self.ltxt]
        return

    def add_elision(self):
        c = 0
        for x, y in zip(self.ltxt2[:-1], self.ltxt2[1:]):
            try:
                xword = x
                yword = y

                if reg(r'[\?\!\.\*\+\$]', xword) or \
                        reg(r'[@%&]', yword):
                    pass
                elif self.quote(xword, yword):
                    pass
                else:
                    ywordu = unidecode(yword)
                    xwordu = unidecode(xword)
                    if reg(r'[āēīōū]m$', xword):
                        pass
                    else:
                        if ywordu not in ['et', 'o']:
                            if ywordu[0] in 'haeiouy':
                                if xwordu[-1] in 'aeiouy' or \
                                        reg(r'[aeioyu]m$', xwordu):
                                    self.ltxt2[c + 1] = el + yword



            except:
                pass
            c += 1

        return

    def quote(self, x, y):
        """
        if a word begins a quotation then it cannot
        be elided with a word outside the quotation
        """

        if "'" not in x and "'" not in y and \
                '"' not in x and '"' not in y:
            return 0
        for e, z in en(x):
            if z not in self.punctuation:
                xend = x[e:]
                break
        e = len(x) - 1
        for z in reversed(y):
            if z not in self.punctuation:
                ystart = y[:e]
                break
            e -= 1

        if "'" in xend or '"' in xend or \
                "'" in ystart or "'" in ystart:
            return 1

    def add_paragraphs(self):
        for e, x in en(self.ltxt2):
            self.ltxt2[e] = x.replace('$', ' ...')
        lst = []
        s = ''
        poem = 0
        for e, x in en(self.ltxt2):
            x = self.ltxt2[e]
            if x == 'plausor':
                bb = 8

            if "%" in x:
                lst.append(s.rstrip())
                x = x.replace('%', '  ')
                s = x + ' '
            elif "@" in x:
                if s:
                    lst.append(s.rstrip())
                if not poem:
                    lst.append('')
                x = x.replace('@', '    ')
                s = x + ' '
                poem = 1
            elif "&" in x:
                if s:
                    lst.append(s.rstrip())
                if not poem:
                    lst.append('')
                x = x.replace('@', '   ')
                s = x + " "
                poem = 1
            elif '+' in x:
                x = x.replace('+', '')
                s += x
                lst.append(s)
                s = ''
                try:
                    nxt = self.ltxt2[e + 1]
                except:
                    nxt = ''
                if not reg(r'[@&]', nxt):
                    lst.append('')
                    poem = 0
                else:
                    poem = 1
            else:
                s += x + ' '

        # we now erase the space between the
        # cum enclitic
        for e, x in en(lst):
            x = x.replace(' ^', '')
            x = x.replace('*', ' ....')
            x = x.replace(f' {el}', el)
            lst[e] = x

        file = f'{fold}satyrica_w_macrons'
        file2 = f'{phi_fold2}petronius/satyrica'
        to.from_lst2txt(lst, file)
        vgf.open_txt_file(file)
        vgf.open_txt_file(file2)
        return

        #
        #
        # if poem_indent2 in x:
        #     x += '+'
        # x = x.replace(poem_indent, '@')
        # x = x.replace(poem_indent2, '&')
        # x = x.replace(para_indent, '%')

    def observe(self):
        lk = -1
        lv = -1
        for k, v in self.l2p.items():
            if k != lk + 1:
                bb = 8
            if v != lv + 1:
                bb = 8

    def temp18(self):
        lst = []
        str1 = ''
        for x in self.ltxtw:
            str1 += x + ' '
            if len(str1) > 70:
                lst.append(str1[:-1])
                str1 = ' '
        file = f'{dwn_dir}pet_punc'
        to.from_lst2txt(lst, file)
        vgf.open_txt_file(file)
        return


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


class rename_phi:
    def __init__(self):
        pass

    def get_atts(self):
        self.phi_aut = os.listdir(f'{phi_fold}')
        file = f'{fold}phi_auth'
        to.from_lst2txt(self.phi_aut, file)
        vgf.open_txt_file(file)


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
            self.final_lst, self.exc_sh = ins.begin2(file, ';', 0, 'third')
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
            y = [None, self.file, x[0], None, ] + x[1:]
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


'''
6.25 - the models are mostly correct except the amo 
model has two forms one of which removes the "av"



'''


if eval(not_execute_on_import):
    if vgf.pycharm():
        args = [0, 'ph', 'lpt', 'IX', '', 0, 0]
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

    elif args[1] == 'pu':
        ins = punctuate_lasla()
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
