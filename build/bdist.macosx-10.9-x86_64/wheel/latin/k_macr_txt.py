
import pyperclip
from bglobals import *
from other.filter_txt import elim_punctuation
from i_scrape_old import old_entry




class macr_txtcl(fix_collatinus_cl):
    def __init__(self):
        fix_collatinus_cl.__init__(self)

    def begin(self, file=""):
        debug = 0
        self.file = file
        self.get_atts()
        self.count_ambig()
        self.divide_all_words()
        self.macr_test_fu()
        if not debug:
            try:
                self.step1()
            except:
                p('error encountered')
                for x, y in self.dct.items():
                    if type(y) == list:
                        self.dct[x] = ' '.join(y)

                pass
        else:
            self.step1()

        self.resolve_ambiguity()
        self.output()

    def get_atts(self):
        self.certain = pi.open_pickle(f'{fold}macronize_certain', 1)
        self.almost_certain = pi.open_pickle(f'{fold}macronize_less_certain', 1)
        self.macronizer = pi.open_pickle(f'{fold}macronizer_ncaps', 1)
        self.from_excel_wnum = pi.open_pickle(f'{fold}from_excel_wnum', 1)
        self.lat_freq = pi.open_pickle(f'{fold}latin_freq', 1)
        self.from_excel_wonum = pi.open_pickle(f'{fold}from_excel_wonum', 1)
        self.mac_lemmas = {v.macron: v for k, v in self.from_excel_wnum.items()}
        self.fake_enclitics = pi.open_pickle(f'{fold}fake_enclitics', 1)
        self.ambiguities = []
        self.ignored_words = []
        self.word2obj = {}
        self.missing = []
        if not self.kind == 'cl':
            if not self.file:
                self.file = f'{lfold}writings/writings'
            else:
                self.file = f'{lfold}writings/{self.file}'
            self.file2 = self.file + '2'
            self.file3 = self.file + '3'
        self.debug = 0
        lst = to.from_txt2lst_tab_delim(f'{fold}always_dis')
        self.always_dis = {x[0]: x[1] for x in lst}

    def count_ambig(self):
        dct = {}
        for x, y in self.macronizer.items():
            if len(y) > 1:
                dct[x] = y
        # 108,092 ambiguities, 8610 certain disambig
        return

    def macr_test_fu(self):

        # vgf.close_and_save(self.file)
        lst = to.from_txt2lst(self.file, 1)
        lst = self.get_unknowns(lst)
        on = 0
        noz = 1 if all('__start' not in x for x in lst) else 0
        self.dct = {}
        for e, x in en(lst):
            if '__start' in x or noz and e == 0:
                self.dct[e] = x
                on = 1
            elif on:
                self.dct[e] = x.split()
            elif not on:
                self.dct[e] = x
        return

    def elim_dash(self, y):
        e = 0
        while e < len(y):
            z = y[e]
            if reg(r'[^-]-[^-]', z):
                lst = z.split('-')
                y[e] = lst[0]
                y.insert(e + 1, '-')
                y.insert(e + 2, lst[1])
            e += 1
        return y

    def get_unknowns(self, lst):
        on = 0
        b = 0
        for v in lst:
            if v == 'ignored words':
                on = 1
            elif on and not v:
                break
            elif on:
                self.ignored_words.append(v.lower())
            b += 1

        return lst[b:]

    def step1(self):
        self.line = 0
        self.amb = 0
        for x, y in self.dct.items():
            if len(self.ambiguities) > 30:
                for x, y in self.dct.items():
                    if type(y) == list:
                        self.dct[x] = ' '.join(y)
                break

            if type(y) == list:
                y = self.elim_dash(y)
                on = 1
                e = 0
                while e < len(y):
                    self.e = e
                    word = y[e]

                    self.oword = word
                    if word == 'Winnie':
                        bb = 8
                    if self.oword[0] == ';':
                        word = self.oword[1:]
                        y[e] = word
                        self.ignored_words.append(word.lower())

                    elif '(' in word:
                        if ')' not in word:
                            on = 0
                    elif ')' in word:
                        on = 1
                    elif not on:
                        pass
                    elif on:
                        nword = self.step2(word)
                        if ' ' in nword and '#' not in nword:
                            lst3 = nword.split()
                            y[e] = lst3[0]

                            for d, z in en(lst3[1:]):
                                y.insert(e + 1 + d, z)
                            e -= 1
                        else:
                            y[e] = nword
                    e += 1
                if self.kind != 'cl':
                    self.dct[x] = ' '.join(y)
            self.line += 1
        return

    def step2(self, word):  # 27
        self.no_disamb = 0
        if reg(r'[0-9]', word):
            return word
        elif not reg(r'[a-zA-Z]', word):
            return word
        self.capital = 0 if word.lower() == word else 1
        word = word.lower()
        spunc, word, epunc = elim_punctuation(word)
        if word == 'alba':
            bb = 8

        self.word_wo_punc = word
        self.word_wo_punc_ca = word
        if self.capital:
            self.word_wo_punc_ca = self.word_wo_punc.capitalize()

        wordu = unidecode(word)
        if wordu in self.ignored_words:
            return self.oword

        wordiu = norm_str_jv(word)
        obj = self.macronizer.get(wordiu)
        self.obj = obj
        macr = self.certain.get(wordiu)
        if macr:
            self.word2obj[(self.line, self.e)] = self.obj
            if self.capital:
                macr = macr.capitalize()
            star = ''
            if self.kind != 'cl':
                star = '*'

            return f'{spunc}{macr}{star}{epunc}'

        ms = self.always_dis.get(wordiu)
        if ms:
            return f'{spunc}{ms}{epunc}'

        if obj:
            return f'{spunc}{self.step3(obj)}{epunc}'
        else:
            wordiu, enc = enclitics(wordiu, self.fake_enclitics)
            if enc:
                self.word_wo_punc = self.word_wo_punc[:-len(enc)]
                self.word_wo_punc_ca = self.word_wo_punc_ca[:-len(enc)]
                obj = self.macronizer.get(wordiu)
                if obj:
                    return f'{spunc}{self.step3(obj)}{enc}{epunc}'

            l = [self.line, self.e, self.word_wo_punc, wordiu]
            if self.debug:
                return self.oword
            else:
                p(f'mispelled {self.oword}')
                res = self.misspell(l)

                if res == 'i':
                    self.ignored_words.append(self.word_wo_punc)
                    return f'{spunc}{self.word_wo_punc_ca}{epunc}'
                elif res == 'e':
                    return ''
                elif res and ' ' in res:
                    return f'{spunc}{res}{epunc}'
                elif self.no_disamb:
                    return f'{spunc}{self.word_wo_punc_ca}{epunc}'
                else:
                    obj = self.macronizer[self.word_wo_punc.lower()]
                    return f'{spunc}{self.step3(obj)}{epunc}'

    def step3(self, obj):
        if len(obj) == 1:
            self.word2obj[(self.line, self.e)] = obj
            nword = vgf.dct_idx(obj)
            if self.capital:
                return nword.capitalize()
            else:
                return nword
        else:
            self.amb += 1
            s = self.print_line([self.line, self.e], 1)
            if self.kind == 'cl':
                self.ambiguities.append([self.e, s, self.word_wo_punc, obj])
                return self.word_wo_punc_ca

            else:
                self.ambiguities.append([f"{self.amb}", s, self.word_wo_punc, obj])
                return f'#{self.amb} {self.word_wo_punc_ca}'

    def resolve_ambiguity(self):
        if self.kind == 'cl':
            self.disambig = defaultdict(dict)
        else:
            self.disambig = []
        for e, l in en(self.ambiguities):
            idx = l[0]
            sent = l[1]
            word = l[2]
            d = l[3]
            if not self.kind == 'cl':
                self.disambig.append(sent)
                self.disambig.append(idx)
            word = word.lower()
            obj = self.almost_certain.get(word)
            if obj and not self.kind == 'cl':
                p('almost certain')
                obj[0] = f'={obj[0]}'
                self.disambig += obj
            else:
                done = set()
                b = 0
                for wmac, d in d.items():
                    for lem, pos_lst in d.items():
                        ps = ' '.join(pos_lst)
                        cl = self.mac_lemmas[lem]
                        defn = get_def(cl)
                        if self.kind == 'cl':
                            self.disambig[idx][b] = [wmac, lem, ps, defn]
                        elif defn:
                            if len(defn) > 50:
                                for e, x in en(defn[50:]):
                                    if x == ' ':
                                        break
                                defn = defn[:50 + e]

                            if lem not in done:
                                self.disambig.append(f'{wmac} {lem} {ps} {defn}')
                            else:
                                self.disambig.append(f'{wmac} {lem} {ps}')
                        b += 1
            if not self.kind == 'cl':
                self.disambig.append('')
        return

    def resolve_ambiguity2(self):
        for k, v in self.disambig.items():
            for e, z in v.items():
                wmac = z[0]
                lem = z[1]
                pos = z[2]
                defn = z[3]
                lst = [wmac, lem, pos, defn]
                p(e)
                for x in lst:
                    p(x)
                p('')
            s = input('choose: ')
            s = int(s)
            word = self.disambig[k][s][0]
            self.dct[0][k] = word

        return

    def print_pos(self):
        for k, v in self.word2obj.items():
            self.print_defs(0, 'p', v)

        v = vgf.dct_idx(self.dct, 0, 'v')
        v = ' '.join(v)
        pyperclip.copy(v)
        p(v)
        return

    def divide_all_words(self):
        self.word_cat = divide_words(self.macronizer)

    def misspell(self, l):
        wordiu = l[3]
        f = wordiu[0]
        b = len(wordiu)
        lst = [b, b + 1, b - 1, b + 2, b - 2]
        dct = defaultdict(list)
        if not self.kind == 'cl':
            self.print_line(l)
        while 1:
            found = 0
            res = ''
            for ln in lst:
                if ln > 2:
                    if f in self.word_cat:
                        possi = self.word_cat[f].get(ln)
                        if possi:
                            for poss in possi:
                                num = vgf.lvn.distance(wordiu, poss)
                                if num < 4:
                                    dct[num].append(poss)
                                    found = 1

            if found:
                res = self.choose_poss2(dct)
                if res in ['i', 'e']:
                    return res

            if res == 'r' or not found:
                old = wordiu
                p('to make only a one time replacement end word with ;')
                wordiu = input(f'respell word {wordiu} or i or e')
                if wordiu in ['i', 'e']:
                    return wordiu

                if wordiu[-1] == ';':
                    wordiu = wordiu[:-1]
                elif ' ' in wordiu:
                    self.always_dis[old] = wordiu
                    return wordiu

                else:
                    self.always_dis[old] = wordiu

                f = wordiu[0]
                b = len(wordiu)
                lst = [b, b + 1, b - 1, b + 2, b - 2]
            else:
                return

    def print_line(self, k, sv=0):
        line = k[0]
        idx = k[1]
        more = self.forward(idx, self.dct[line])
        c = 0
        lst4 = []
        lst3 = []
        while 1:
            str2 = self.dct[line]
            if type(str2) == list:
                lst2 = str2
            else:
                lst2 = str2.split()
            if not c:
                lst3 = [x for x in lst2]
                lst3 = lst3[:idx + 1]
            else:
                lst3 = [x for x in lst2] + lst3

            if len(lst3) > 20:
                lst3 = lst3[-20:]
                s = ' '.join(lst3) + ' | ' + more
                if not sv:
                    p(s)
                else:
                    lst4.append(s)

                break
            line -= 1
            if line < 0:
                s = ' '.join(lst3) + ' | ' + more
                if not sv:
                    p(s)
                else:
                    lst4.append(s)
                break
            c += 1
            if c > 10:
                bb = 8

        s = "__"
        for x in reversed(lst4):
            s += f' {x}'
        return s

    def forward(self, idx, line):
        rem = len(line) - idx
        if rem > 4:
            return " ".join(line[idx + 1:idx + 4])
        else:
            try:
                str1 = " ".join(self.dct[self.line][idx + 1:])
                c = 0
            except:
                try:
                    str1 = " ".join(self.dct[self.line + 1][:4])
                    c = 1
                except:
                    c = 2
            if c == 1:
                return str1
            elif c == 2:
                return ''

            ad = ""
            n = self.line + 1
            while ad.count(' ') < 4:
                try:
                    te = ' '.join(self.dct[n])
                    b = 0
                    for e, x in en(te):
                        if x == ' ':
                            b += 1
                        if b > 4:
                            break
                    ad += " " + te[:e]
                    n += 1
                except:
                    break
            str1 += " " + ad
            return str1

    def choose_poss2(self, v):
        self.tdct = {}
        self.tnum = 0
        v = sort_dct_key(v)
        for dist, lst in v.items():
            c, lst = self.choose_poss3(lst)
            if c != 'm':
                return c

        return 'i'

    def choose_poss3(self, v, kind='', limit=0):
        if not kind:
            h = {w: self.lat_freq.get(w, 0) for w in v}
            v = sort_dct_val_rev(h)
            v = list(v.keys())

        end = limit + 30
        s_forbid = 0
        if len(v) < limit + 30:
            end = len(v)
            s_forbid = 1

        for e, z in en(v[limit:end]):
            if kind == 'd':
                self.print_defs(z, 'd')
            elif kind == 'p':
                self.print_defs(z, 'p')
            else:
                p(self.tnum, z)
                self.tdct[self.tnum] = z
                self.tnum += 1

        c = 'h'

        while c == 'h':
            # c = 'd'
            c = input("""number, d, m, p, e, i, r, s or h to see what the choices mean """)
            if c == 's' and s_forbid:
                c = 'm'

            if c == 'h':
                p("""
                    num to choose, 
                    d to see definitions and case, 
                    m to see more words which are greater distance
                    p to see just what part of speech it is
                    e to eliminate the word because it's gibberish
                    i to ignore the word and leave as is
                    r to respell the word
                    s to see more words than the 30 listed of the same distance
                """)
            elif c.isdigit():
                if kind in ['d', 'p']:
                    self.no_disamb = 1
                self.word_wo_punc = self.tdct[int(c)]
                self.word_wo_punc_ca = self.word_wo_punc
                if self.capital:
                    self.word_wo_punc_ca = self.word_wo_punc.capitalize()
                return 'x', 0
            elif c == 'd':
                c, v = self.choose_poss3(v, 'd', limit)
            elif c == 'p':
                c, v = self.choose_poss3(v, 'p', limit)
            elif c == 's':
                c, v = self.choose_poss3(v, 's', limit + 30)
            elif c == 'm':
                break

            elif c in ['r', 'i', 'e']:
                v = 0
                break
            else:
                c = 'h'

        return c, v

    def check(self):
        lst = vgf.dct_idx(self.dct, 0, 'v')
        for w in lst:
            self.print_defs(w, 'd')

    def print_defs(self, z, kind='', obj=0):
        if not obj:
            obj = self.macronizer[z]
        for k, v in obj.items():
            if kind == 'd':
                for lem, pos_lst in v.items():
                    lem1 = norm_str_jv(lem)
                    ins = self.from_excel_wnum.get(lem1)
                    if not ins:
                        p(f'missing lemma in excel_wnum {lem}')
                    else:
                        defn = get_def(ins)
                        if defn:
                            p(self.tnum, k, pos_lst, defn)
                            self.tdct[self.tnum] = k
                            self.tnum += 1
                        else:
                            p(f'no definition for {k}')
            elif kind == 'p':
                if v == ['inv']:
                    p(k, v[0])
                else:
                    for lem, pos_lst in v.items():
                        p(self.tnum, k, pos_lst, )
                        self.tdct[self.tnum] = k
                        self.tnum += 1

        return

    def output(self):
        lst = []
        if self.ignored_words:
            lst = ['ignored words'] + self.ignored_words

        lst += list(self.dct.values()) + ['', '']
        to.from_lst2txt(lst, f'{self.file2}')
        to.from_lst2txt(self.disambig, f'{self.file3}')
        vgf.open_txt_file(f'{self.file2}')
        vgf.open_txt_file(f'{self.file3}')
        lst = [[k, v] for k, v in self.always_dis.items()]
        to.from_lst2txt_tab_delim(lst, f'{fold}always_dis')
        return


class macr_txtcl2(macr_txtcl):
    def __init__(self):
        macr_txtcl.__init__(self)

    def begin2(self, file=""):
        # get enclitic exceptions

        self.get_atts2(file)
        self.nums()
        self.replace_nums()
        self.output()

    def get_atts2(self, file):
        try:
            lst = to.from_txt2lst_tab_delim(f'{fold}always_dis')
            self.always_dis = {x[0]: x[1] for x in lst}
        except:
            self.always_dis = {}

        if self.kind != 'cl':
            if not file:
                self.sfile = 'writings'
                file = f'{lfold}writings/writings'
            else:
                self.sfile = file
                file = f'{lfold}writings/{file}'

            try:
                lst = to.from_txt2lst_tab_delim(f'{fold}{self.sfile}already_used')
                self.already_used = {x[0]: x[1] for x in lst}
            except:
                self.already_used = {}

            self.file = file
            self.file2 = self.file + '2'
            self.file3 = self.file + '3'
            self.lst = to.from_txt2lst(self.file2, 1)
            self.dis = to.from_txt2lst(self.file3, 1)
            self.fake_enclitics = pi.open_pickle(f'{fold}fake_enclitics', 1)
            self.lst = [x.replace('*', '') for x in self.lst if x != '__start']

    def command_line(self):
        self.kind = 'cl'
        self.get_atts()
        self.get_atts2("")
        self.count_ambig()
        self.divide_all_words()
        debug = 0
        while 1:
            self.tnum = 0
            self.tdct = {}
            if not debug:
                s = input('input, q to quit: ')
                if s == 'q':
                    break
            else:
                s = 'vis john dicere'
            self.dct = {0: s.split()}
            self.step1()
            self.resolve_ambiguity()
            self.resolve_ambiguity2()
            self.print_pos()
            self.word2obj = {}
            self.ambiguities = []
            self.disambig = defaultdict(dict)

    def nums(self):
        num = ''
        self.dct = {}
        needed = 0
        fword = ''
        error = 0
        for x in self.dis:
            if not x and needed:
                if fword not in self.already_used:
                    p(f'number {num} needs a = sign')
                    error = 1
                    needed = 0
                    fword = ''
                else:
                    self.dct[num] = self.already_used[fword]
                    needed = 0
                    fword = ''

            if x:
                if ' ' in x:
                    fword = x[:x.index(' ')]
                    fword = norm_str_jv(fword)

                if x.startswith('_'):
                    pass

                elif x.isdigit():
                    if x == '16':
                        bb = 8

                    num = f'#{x}'
                    needed = 1
                elif x.startswith("=="):
                    if not num:
                        assert 0
                    x = x[2:x.index(" ")]
                    xu = norm_str_jv(x)
                    self.always_dis[xu] = x
                    self.already_used[xu] = x
                    self.dct[num] = x
                    needed = 0
                elif x.startswith('='):
                    x = x[1:x.index(" ")]
                    self.dct[num] = x
                    self.already_used[norm_str_jv(x)] = x
                    num = ''
                    needed = 0

        if needed and num not in self.dct:
            self.dct[num] = self.already_used[fword]

        if error:
            sys.exit()

        return

    def adjust_hash(self, lst):
        e = 0
        while e < len(lst):
            x = lst[e]
            if '#' in x and not x[0] == '#':
                idx = x.index('#')
                beg = x[:idx]
                end = x[idx:]
                lst[e] = beg
                lst.insert(e + 1, end)
            e += 1
        return lst

    def replace_nums(self):
        lnum = 0
        for f, x in en(self.lst):
            b = 0
            while '#' in x:
                lst2 = x.split()
                lst2 = self.adjust_hash(lst2)
                lst3 = [y for y in lst2 if y[0] == '#']
                for z in lst3:
                    if z not in self.dct:
                        p(f'{z} not disambiguated')
                        assert 0

                for e, y in en(lst2):
                    if y.startswith('#'):
                        if y == '#16':
                            bb = 8

                        nword = self.dct[y]
                        to_replace = lst2[e + 1]
                        capital = 0
                        if to_replace[0].isupper():
                            capital = 1

                        to_replace_iu = norm_str_jv(to_replace)
                        if to_replace_iu == 'salue':
                            bb = 8

                        to_replace_iu, enc = enclitics(to_replace_iu, self.fake_enclitics)
                        st, replacee, end = elim_punctuation(to_replace)
                        if capital:
                            nword = nword.capitalize()

                        lst2[e + 1] = f"{st}{nword}{enc}{end}"
                        del lst2[e]
                        x = ' '.join(lst2)
                        self.lst[f] = x
                        lnum = f
                        break
                b += 1
                if b > 10:
                    p(f'{x} caught in infinite loop at')
                    sys.exit()

        self.lst.insert(lnum + 1, '__start')
        return

    def output(self):
        to.from_lst2txt(self.lst, f'{self.file}2a')
        vgf.open_txt_file(f'{self.file}2a')
        lst = [[k, v] for k, v in self.always_dis.items()]
        to.from_lst2txt_tab_delim(lst, f'{fold}always_dis')
        lst = [[k, v] for k, v in self.already_used.items()]
        to.from_lst2txt_tab_delim(lst, f'{fold}{self.sfile}already_used')


if eval(not_execute_on_import):
    if vgf.pycharm():
        args = [0, 'ch', 'petronius_lat', 'IX', '', 0, 0]
    else:
        args = vgf.get_arguments()

    if args[1] == 'mac':
        ins = macr_txtcl()
        ins.kind = ''
        ins.begin(args[2])

    elif args[1] == 'cl':
        ins = macr_txtcl2()
        ins.command_line()
    elif args[1] == 'ch':
        ins = fix_collatinus_cl()
        ins.begin_fc()
    elif args[1] == 'gfe':
        get_fake_enclitics()
    elif args[1] == 'flf':
        ins = fix_collatinus_cl()
        ins.fix_lem2forms()

    elif args[1] == 'mlp':
        ins = fix_collatinus_cl()
        ins.redundant_by_model(1)
        ins.start_decl()
        ins.get_lem2forms()
        ins.get_lem2forms_pos()
        ins.build_macronizer()
        ins.output()
        bb = 8


    elif args[1] == 'wo':
        ins = fix_collatinus_cl()
        ins.get_atts()
        ins.weed_out_proper()
    elif args[1] == 'dis':
        ins = macr_txtcl2()
        ins.kind = ''
        ins.begin2(args[2])
    elif args[1] == 'help':
        p("""
        doc must be stored in the folder latin/writings

        __start must be placed at the part of the text that you want to
            begin processing

        word to be ignored by the macronizer are put underneath
            the first line which reads 'ignored words'
            words must each occupy one line and code will
            stop collecting words with a blank line

        words between ( ) are not scanned and are notes written
            in english

        words which begin with ; are ignored and placed under the heading
            'ignored words' after the function da (disambiguate)
            is run

        words which are temporarily ignored are proceeded by a / but
            in the future the computer will disambiguate them

        after the text is half disambiguated the text is outputted
            with a suffix to the name of 2
            on a sheet with a suffix of 3 is
            a list of words to be disambiguated at the bottom
            put a + before the word you would like to choose
            and a ++ if you would like to choose that word as
            well as never be asked to disambiguate those words
            in the future

        if a word appears several times in the text and it is
            regularly disambiguated in the same way then
            do not place a + the next time around, the computer
            will assume the same disambiguation

        the computer will also make a file so that should more
            of the text be disambiguated in the future it will
            use the same disambiguations

        words that are more than 98% of the time disambiguated in one
            way are disambiguated in that frequent way and then a *
            is placed after the word on file 2.  If it turns out that
            a word with a star should have been disambiguated against
            the norm, then another * must placed next to the word


        """)

