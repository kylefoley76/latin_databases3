from bglobals import *

lvow = {
    'a': 'ā',
    'e': 'ē',
    'i': 'ī',
    'o': 'ō',
    'u': 'ū',
    'y': 'ȳ'
}
bvow = {
    'a': 'ă',
    'e': 'ĕ',
    'i': 'ĭ',
    'o': 'ŏ',
    'u': 'ŭ',
    'y': 'ў'
}

dctabb = {
    'a-': 'ă',
    'e-': 'ĕ',
    'i-': 'ĭ',
    'o-': 'ŏ',
    'u-': 'ŭ',
    'v-': 'ŭ',
    'y-': 'ў',
    'a+': 'ā',
    'e+': 'ē',
    'i+': 'ī',
    'o+': 'ō',
    'u+': 'ū',
    'v+': 'ū',
    'y+': 'ȳ',
}



class pros:
    def __init__(self, lst, ped=0, ucons_dct={}):
        self.name = lst[0].lower()
        self.raw = lst[1]
        if self.raw == 'qui+nque-iu-go':
            bb = 8

        self.wmac = lst[1]
        self.vowels = lst[2]
        self.tot = int(lst[4])
        self.ratio = int((int(lst[3]) / self.tot) * 100)
        if ped:
            self.macronize(ucons_dct)

    def macronize(self, ucons_dct):
        s = self.wmac
        for x, y in dctabb.items():
            s = s.replace(x, y)

        if len(s) > 2:
            te = jv.replace(unidecode(s))
            idx = ucons_dct.get(te)
            if idx:
                # p (te)
                s = replace_at_i(idx, s, conu)

            lvow = last_vowel(unidecode(s))
            sec = s[lvow:]
            fir = s[:lvow]
            s = self.restore_jv(fir) + sec

        self.wmac = s
        self.jv_no_mac = unidecode(self.wmac)
        self.iu = jv.replace(self.jv_no_mac)
        return

    def restore_jv(self, fir):
        dct2 = {
            'ē': 'e',
            "ū": 'u'
        }
        if not fir:
            return ''
        b = 0
        if fir[0] == 'i':
            fir = replace_at_i(0, fir, 'j')

        for x, y in zip(fir[:-1], fir[1:]):
            xl = x
            for s, t in dct2.items():
                xl = xl.replace(s, t)
            if y == 'i' and xl not in 'eu':
                fir = replace_at_i(b + 1, fir, 'j')
            elif y == 'u' and xl not in 'qae':
                bb = 8
            b += 1
        return fir

    def __repr__(self):
        return self.iu


class pedecerto:
    '''
    this class must be run before macronizer_cl, since the latter
    weeds out its words based on whether or a word exists in
    the prosodic file
    '''

    def __init__(self):
        pass

    def begin(self):
        self.get_atts()
        self.make_class()
        # self.researchj()
        self.output_p()
        # self.weed_out()

    def begin2(self):
        self.get_atts(1)

    def get_atts(self, second=0):
        if not second:
            self.macronizer = pi.open_pickle(f'{fold}macronizer_new', 1)
            self.prosodic = to.from_txt2lst(f'{fold}prosodic')
            self.word2stats = {}
            self.prosodic_stats = defaultdict(list)
            self.prosodic_stats_jv = defaultdict(list)

        else:
            self.macronizer_pc = pi.open_pickle(f'{fold}macronizer_pc', 1)
            self.pros_stats = pi.open_pickle(f'{fold}pros_stats', 1)
        return

    def output_p(self):
        pi.save_pickle(self.prosodic_stats, f'{fold}prosodic_stats_new', 1)



    def make_class(self):
        '''
        in order to use the ucons dict the macronizer has to be run
        first, it replace u with a u consonant, either that
        or we need to build a ucons dict or perhaps infer
        that if u follows q,g,s and it is not marked then
        it is a consonant
        '''

        b = 0
        p (f"""
        now converting the pedocerto database into a list
        of python classes
""")

        for x in self.prosodic:
            lst = vgf.strip_n_split(x, ";")
            ins = pros(lst, 1)
            self.prosodic_stats[ins.iu].append(ins)
            self.prosodic_stats_jv[ins.jv_no_mac].append(ins)
            b += 1
            vgf.print_intervals(b, 5000, None, len(self.prosodic))
            # if b > 10_000:
            #     break
        return

    def researchj(self):
        '''
        there are mistakes in my algorithm, omnia is turning out
        omnja yet omnja has zero hits
        :return:
        '''

        lst = []
        dct = defaultdict(int)
        for k, v in self.prosodic_stats_jv.items():
            dct[v.iu] += 1

        dct2 = {k: v for k, v in dct.items() if v > 1}
        dct3 = {}
        for k, v in self.prosodic_stats_jv.items():
            if v.iu != v.jv_no_mac and dct2.get(v.iu) and dct[v.iu] > 1:
                itm = self.prosodic_stats.get(v.iu)
                if itm:
                    dct3[v.iu] = [v.jv_no_mac, v.ratio, v.tot, v.iu, itm.ratio, itm.tot]

        return

    def weed_out(self):
        dct = {}
        self.ncol = {}
        for x, y in self.word2stats.items():
            if x not in self.macronizer:
                self.ncol[x] = y.tot
        self.ncol = sort_dct_val_rev(self.ncol)
        for x, y in self.macronizer.items():
            if x in self.word2stats:
                dct[x] = y
        self.macronizer = dct
        pi.save_pickle(self.ncol, f"{fold}macron_pc", 1)







class vow_marked:
    def __init__(self, x, split, y):
        self.original = x
        self.marked = y
        self.code = ''
        self.split = split

    def __repr__(self):
        return self.original


class long_by_pos:
    def __init__(self):
        """
        this class does not save any new object but just tests
        to see if our understanding of long by position is
        correct
        """
        pass

    def begin3(self):
        self.get_atts4(2)
        self.get_atts2()
        self.step2()
        self.test()
        self.mf_diph()
        self.output()
        return



    def get_atts4(self, pede=0):
        self.ucons_dct = {}
        if not pede:
            self.lemmes = to.from_txt2lst(f'{fold}lemmes', 1)
        elif pede == 2:
            self.macronizer = pi.open_pickle(f'{fold}macronizer_new', 1)
            self.prosodic_stats = pi.open_pickle(f'{fold}prosodic_stats_new', 1)
        else:
            self.prosodic = to.from_txt2lst(f'{fold}prosodic')
            self.macronizer = pi.open_pickle(f'{fold}macronizer_new', 1)
            self.prosodic_stats = {}
        return

    def output(self):
        st = set(v[0].iu for k, v in self.still_wrong.items())
        to.from_lst2txt(st, f'{fold}col_ped_diff')



    def research_ui(self):
        dct1 = {}
        dct2 = {}
        for x,y in self.prosodic_stats.items():
            if 'ui' in x:
                if reg(r'u\+i[^\+\-]', y.raw) or reg(r'u\+i$', y.raw):

                    dct1[x] = y.raw
                else:
                    dct2[x] = y


    def special_prefixes(self):
        lst, _ = prefixes()
        liquids = 'bcdgpt'
        exp = ['post', 'amb', 'red', 'sed']
        self.sprefix = [x for x in lst if x[-1] in liquids and x not in exp]

    def temp12(self):

        lst7 = [x for x, y in wrong.items() if any(x.startswith(z) for z in self.sprefix)]
        dct4 = {x: wrong[x] for x in lst7}

    def test(self):
        error = {}
        for x, z in self.prosodic_stats.items():
            for y in z:
                coll = self.macronizer.get(y.iu)
                if coll:
                    wmacu = unidecode(y.wmac)
                    st = set()
                    for k, v in coll.items():
                        k1 = unidecode(k)
                        st.add(k1)
                    col2 = vgf.dct_idx(coll)
                    if wmacu not in st:
                        error[(y.wmac, col2)] = [y, coll]
        self.error = error
        return

    def mf_diph(self):
        dct = {}
        dct2 = {}
        still_wrong = {}
        for k, v in self.error.items():
            ped = k[0]
            col = k[1]
            found = 0
            pedu = unidecode(ped)
            for y in ['ui', 'ei']:
                if y in pedu and 'j' in col:
                    cidx = [e for e, w in en(col) if w == 'j']
                    pidx = pedu.index(y)
                    if ped[pidx + 1] in 'īĭ':
                        pass

                    elif pidx + 1 in cidx:
                        if not pedu.count(y) == 1:
                            found = 1
                            dct2[k] = v
                            break
                        else:
                            found = 1
                            dct[k] = v
                            break
            if not found:
                still_wrong[k] = v
        self.still_wrong = still_wrong

        return

    def get_atts2(self):
        self.ncons = 'aeiouyăĕĭŏŭўāēīōūȳh_'
        singles = ['ch', 'ph', 'th', 'qu']
        singles += [x + 'l' for x in 'bcdgpt']
        singles += [x + 'r' for x in 'bcdgpt']
        self.singles = singles
        self.special_prefixes()
        self.wrong = []

    def step2(self):
        self.wrong = []  # should be 58
        self.single = 0
        self.fdiph = []
        self.sdiph = []
        self.gcons = []
        self.hasj = []
        self.jlong = []
        self.jshort = []
        self.gfl_tot = 0
        self.gfl_rat = 0
        b = 0
        p (f"""
        now distinguishing between syllables which are
        long by position and those that are not
""")

        for k, lst in self.prosodic_stats.items():
            b += 1
            # if b > 10_000:
            #     break

            vgf.print_intervals(b, 500,None,len(self.prosodic_stats))
            for self.ins in lst:
                x = self.ins.wmac
                self.is_heavy(x)
                if len(self.wrong) > 100:
                    bb = 8

        return

    def is_heavy(self, x, kind=""):
        xo = x
        self.syllables = []
        for s in self.singles:
            x = x.replace(s, s[0] + '_')
        y = unidecode(x)

        for s in self.singles:
            y = y.replace(s, s[0] + '_')
        idx = len(x)
        if kind == 'p':
            idx = last_vowel(y)
            x = x[:idx]

        i = 0
        while i < idx:
            xl = x[i]
            xlu = unidecode(xl)
            try:
                x0 = x[i - 1]
            except:
                x0 = ""

            try:
                xl1 = x[i + 1]
            except:
                xl1 = ""
            try:
                xl2 = x[i + 2]
            except:
                xl2 = ""
            combo = xl + xl1
            combo2 = xl1 + xl2
            combo2u = unidecode(combo2)
            combou = unidecode(combo)

            if xl == 'u' and x0 == 'g' and self.quantified(xl1):
                if not self.single:
                    self.gcons.append(x)

            elif combou in diph and conu not in combo:
                if self.single:
                    x, i = self.is_diph(x, i, combo, kind)
                else:
                    if self.quantified(xl1):
                        if not self.quantified(xl):
                            if not self.single:
                                self.add2wrong(x, xl)
                                break
                        else:
                            i += 1

                    elif xl in 'ăĕĭŏŭў':
                        if not self.quantified(xl1):
                            if not self.single:
                                self.fdiph.append([self.ins, x, xl])
                                i += 1
                                break
                        else:
                            if not self.single:
                                self.sdiph.append([self.ins, x, xl])
                            i += 1
                    elif self.has_macron(xl):
                        i += 1
                    elif not self.has_macron(xl):
                        if not self.single:
                            self.add2wrong(x, xl)
                            break


                    bb=8


            elif xlu in 'aeiouy':
                if combo2 in ['fl', 'fr']:
                    if not self.single:
                        self.gfl_tot += self.ins.tot
                        if self.islong(xl):
                            self.gfl_rat += int(self.ins.tot * (self.ins.ratio * .01))

                elif xl1 in ['x', 'z']:
                    if self.single:
                        x = self.underscore(x, i)

                    elif not self.islong(xl):
                        self.add2wrong(x, xl)
                        break

                elif len(combo2) > 1 and \
                        not reg(r'[' + self.ncons + r']', combo2u):
                    if self.single:
                        x = self.underscore(x, i)

                    elif not self.islong(xl):
                        self.add2wrong(x, xl)
                        break

            i += 1
        return x, xo

    def is_diph(self, x, i, combo, kind):
        '''
        kind: c
        the words from the macronizer indicate a diphthong by being
        absent of macrons and breves and belonging to one of the six
        two letter combinations
        kind: p
        the words from prosodic indicate diphthongs by marking the
        first letter as long and not marking the second
        here, if it is a diphthong then the first letter is long and
        the second is an _
        '''
        found = 0
        if kind in ['c','a']:
            if not self.quantified(combo[0]) and not self.quantified(combo[1]):
                x = self.make_long(x, i)
                found = 1
        else:
            if self.islong(combo[0]) and not self.quantified(combo[1]):
                found = 1
        if found:
            return self.underscore(x, i + 1), i + 1
        return x, i

    def underscore(self, x, i):
        # if self.kind == 'a':
        #     return replace_at_i(i, x, '+')
        # else:
        return replace_at_i(i, x, '_')

    def add2wrong(self, x, xl):
        self.wrong.append([self.ins, x, xl, self.ins.ratio, self.ins.tot])

    def quantified(self, x):
        if x in 'āēīōūȳ' + 'ăĕĭŏŭў':
            return 1

    def has_macron(self, x):
        if x in 'āēīōūȳ':
            return 1

    def islong(self, x):
        if x == chr(1263):
            bb = 8

        if x in 'āēīōūȳ' + chr(1263):
            return 1
        return 0

    def isshort(self, x):
        if x in 'ăĕĭŏŭў':
            return 1

    def make_long(self, x, i):
        uvow = unidecode(x[i])
        if not uvow in 'aeiouy':
            return x
        l = lvow[uvow]
        return replace_at_i(i, x, l)

    def make_short(self, x, i):
        uvow = x[i]
        l = bvow[uvow]
        return replace_at_i(i, x, l)


class check_vowels(long_by_pos):
    '''
    the following determines to what extent authors agree
    on the length of vowels

    '''

    def __init__(self):
        long_by_pos.__init__(self)

    def begin(self):
        self.get_atts()
        self.get_atts2()
        self.unambig_words()
        self.mark_long()
        self.evaluate()
        return

    def begin_e(self):
        self.get_atts()
        self.get_atts2()


        self.unambig_words()
        self.mark_long(1)
        #self.by_author() currently has bugs
        return



    def begin_f(self):
        '''
        for reasons that utterly escape i cannot get the obj
        self.prosodic_stats to open a second time.  for this
        reasons i've had to combine long_by_pos.begin3 with
        check_vowels.begin_f

        '''

        self.get_atts4(2)
        self.get_atts2()
        self.get_atts()
        self.step2()
        self.test()
        self.mf_diph()
        self.output()
        self.unambig_words()
        self.mark_long(1)




    def begin_ac(self):
        self.get_atts2()
        self.kind = 'a'
        self.single = 1
        self.lem2forms_jv = pi.open_pickle(f'{fold}lem2forms')
        # self.test_ac()
        self.get_accent()


    def get_atts(self):
        # self.macronizer = pi.open_pickle(f'{fold}macronizer_new', 1)
        self.splits = pi.open_pickle(f'{fold}splits', 1)
        # self.prosodic_stats = pi.open_pickle(f'{fold}prosodic_stats', 1)
        # self.col_ed_diff = set(to.from_txt2lst(f'{fold}col_ped_diff'))

    def unambig_words(self):
        '''
        the following divides words into those which only belong
        to one lemma 'unambig' and those that don't 'ambig'
        those that are unambiguous can be used to determine
        correctness of vowel quantity

        '''

        p (f'''
        now determining which words have no ambiguities
        in their vowel length
''')

        self.unambig = {}
        self.ambig = {}
        errs = defaultdict(list)
        b = 0
        for k, v in self.macronizer.items():
            if len(v) == 1:
                word = vgf.dct_idx(v)
                tpl = self.splits.get(word)
                if tpl:
                    self.unambig[k] = tpl[0]
                else:
                    errs[k].append(word)
            else:
                st = set()
                for x, y in v.items():
                    sp = self.splits.get(x)
                    if sp:
                        st.add(sp[0])
                    else:
                        errs[k].append(x)
                if len(st) == 1:
                    self.unambig[k] = list(st)[0]
                else:
                    self.ambig[k] = v
            b += 1
            vgf.print_intervals(b,20_000,None,len(self.macronizer))

        return

    def by_author(self):
        '''
        the following determines the extent to which each author's
        vowel lengths aggree with the pedecerto database
        '''

        self.macronizer_each = pi.open_pickle(f'{fold}macronizer_each', 1)
        self.single = 1
        auth2wrong = {}
        a2perc = {}
        p (f"""
        we now use the pedecerto database to determine if
        a dictionary author has correctly indicated vowel length
""")

        for auth, dct in self.macronizer_each.items():
            b = 0
            p (f"""
            now evaluating the extent to which the following author: 
            {auth}
            agrees with the others in terms of syllable length
            """)
            self.unambig2 = {}
            for k, v in dct.items():
                x = self.unambig.get(k)
                b += 1
                if x:
                    kind = 'c'
                    marked, orig = self.is_heavy(x, kind)
                    vgf.print_intervals(b, 1000,None,len(dct))
                    v = vow_marked(k, x, marked)
                    code, locs = self.get_code(marked, kind)
                    v.nature = code
                    self.unambig2[k] = v

            auth2wrong[auth], perc = self.evaluate()
            a2perc[auth] = perc
            p (f'{auth} has a success ratio of {perc}')

        return



    def mark_long(self, only_pro=0, lst2=[]):
        self.single = 1
        self.single = 0 # usually 1
        if lst2:
            lst = [self.prosodic_stats, self.unambig]
        else:
            lst = lst2

        self.unambig2 = {}
        p(f"""
        now seeing if we correctly understand how
        pedecerto determines a long syllable 
        """)

        for e, dct in en(lst):
            b = 0
            if e> 0:
                if only_pro and e:
                    break
                for k, v in dct.items():
                    if e == 0:
                        x = v.wmac
                        kind = 'p'
                    else:
                        x = v # v is the first half of a split
                        kind = 'c'
                    marked, orig = self.is_heavy(x, kind) # marked has only the short and long vowels, string
                    if marked != orig:
                        bb=8
                    b += 1
                    vgf.print_intervals(b, 1000, None, len(dct))
                    if e == 0:
                        v.marked = marked
                    else:
                        v = vow_marked(k, v, marked) # k is an unmacronized full word string
                    code, locs = self.get_code(marked, kind)
                    v.nature = code
                    if e:
                        self.unambig2[k] = v
        return

    def test_ac(self):
        self.get_accent2( 'achaeīssimum')


    def get_accent(self):
        for k,v in self.lem2forms_jv.items():
            for pos,y in v.items():

                lst = []
                for z in y[0]:
                    word = self.get_accent2(z)
                    lst.append(word)
                y[0] = lst
                done = 1
                v[pos] = y
        return


    def get_accent2(self, x):
        marked, orig = self.is_heavy(x,'a')  # marked has only the short and long vowels, string
        code, locs = self.get_code(marked,'a')
        if len(code)>2:
            if code[-2] == '+':
                sloc = locs[-2]+1
            else:
                sloc = locs[-3]+1
            x = add_at_i(sloc,x,ac)

        return x




    def get_code(self, x, kind):
        code = ""
        locs = []
        for e,y in en(x):
            if y == '+':
                code += '+'
                locs.append(e)
            elif self.isshort(y) and kind == 'p':
                code += '-'
                locs.append(e)
            elif kind in ['c','a'] and y in 'aeiouy':
                code += '-'
                locs.append(e)
            elif self.islong(y):
                code += '+'
                locs.append(e)

        return code, locs

    def evaluate(self):
        tot = 0
        right = 0
        wrong = {}
        rightd = {}
        for x, y in self.prosodic_stats.items():
            if y.ratio == 100 and y.iu not in self.col_ed_diff:
                ins = self.unambig2.get(x)
                if ins:
                    self.temp_conu(y, ins)
                    tot += 1
                    if len(y.nature) < len(ins.nature):
                        shorter = y.nature
                        longer = ins.nature
                    else:
                        shorter = ins.nature
                        longer = y.nature

                    if longer.startswith(shorter):
                        right += 1
                        rightd[x] = [y.marked, ins.marked, y, ins]
                    else:
                        wrong[x] = [y.marked, ins.marked, y, ins]

        return wrong, right / tot

    def temp_conu(self, pro, col):
        if hasattr(pro, 'marked'):
            if 'u' in pro.marked:
                idx = pro.marked.index('u')
                if len(col.marked) >= idx:
                    col.marked = replace_at_i(idx, col.marked, '_')
                    col.nature,_ = self.get_code(col.marked, 'c')
        return







if eval(not_execute_on_import):
    if vgf.pycharm():
        args = [0, 'all', '', 'IX', '', 0, 0]
    else:
        args = vgf.get_arguments()

    if args[1] == 'lbp':
        ins = long_by_pos()
        ins.begin3()
    elif args[1] == 'cv':
        ins = check_vowels()
        ins.begin()
    elif args[1] == 'cve':
        ins = check_vowels()
        ins.begin_e()
    elif args[1] == 'pc':
        ins = pedecerto()
        ins.begin()

    elif args[1] == 'acc':
        ins = check_vowels()
        ins.begin_ac()

    elif args[1] == 'all':
        ins = long_by_pos()
        ins.begin3()
        ins = check_vowels()
        ins.begin_e()
