import add_path
from lglobals import *
from striprtf.striprtf import rtf_to_text as r2t

'''
striprtf 0.0.20 throws an error, whereas 0.0.12 does not
'''


old_bottom = chr(8869)
bowtie = chr(8904)
contradictory = chr(390)
neg = chr(172)
lneg = chr(10858)
infer = chr(8680)





class old_entry:
    def __init__(self, uword):
        self.defs = {}
        self.etym = ''
        self.alt_spell = []
        self.exams = {}
        self.forms = []
        self.grammar = ""
        self.uiword = uword
        self.jvword = ""
        self.inflection = ""
        self.pos = []
        self.notes = ""
        self.variant_of = ''
        self.variants = []
        self.two_words = ''
        self.seperable = 0
        self.tmesis = 0
        self.number = ''
        self.wmacron = ''
        self.register = ''
        self.genetive = ''
        self.model = ''
        self.raw = []
        self.oraw = []
        self.compounds = []

    def __repr__(self):
        return self.uiword


class top_most:
    def __init__(self):
        pass

    def get_atts_ll(self):
        '''
        lst = [self.new_variants, self.paren_var, self.equal_var, self.dct10,
        self.variants7, self.variants, self.singular_variants, self.var_dct]
        '''

        self.llem2clem = pi.open_pickle(f'{fold}llem2clem')
        self.variants = pi.open_pickle(f'{fold}old_variants5')
        # self.variants = pi.open_pickle(f'{sfold}old_variants')
        self.lem2participles = pi.open_pickle(f'{fold}lem2participles')
        if public:
            self.old_wonum = pi.open_pickle(f'{fold}old_wonum_public')
        else:
            self.old_wonum = pi.open_pickle(f'{fold}old_wonum5')
        # self.old_wonum = pi.open_pickle(f'{sfold}old_wonum')
        self.var2parent = defaultdict(dict)

    def get_attsad(self):
        self.ad_hoc_code = to.from_txt2lst(f'{fold}ad_hoc_code')
        self.ad_hoc_code = vgf.sort_lst_by_len(self.ad_hoc_code, 1)



    def get_attspv(self):
        self.see_excp = {'Mutinus2', 'Rufus2', 'Sciratae', 'Tutilina',
                         'Indianus', 'Papirius', 'uiresco2'}
        st = set(to.from_txt2lst(f'{fold}see_excp'))
        self.see_comp = set(x[:-1] for x in st if x[-1] == "#")
        self.see_excp |= set(x[:-1] for x in st if x[-1] in [';'])
        self.false_equals2 = to.from_txt2lst(f'{fold}false_equals2')
        self.false_equals2 = set(x[:-1] for x in self.false_equals2 if x[-1] == ';')
        self.var_dct = {x.uiword: x for x in self.variants}
        self.var_dct = {}
        self.prob = {}
        self.missing_words = set()
        self.prob2 = {}
        self.to_del = set()
        self.prob3 = {}
        self.fixes = {}
        for x in self.variants:
            if x:
                self.var_dct[x.uiword] = x
        self.of_excp = {"longisco", "odiossicus",
                        "Oscensis", 'Scaptensula',
                        'scirerytis', 'selinas',
                        'siriasis', 'Theromedon', 'trama',
                        'triophthalmos', 'uiaticum',
                        'zonatim', 'Zoroastres',
                        'accensitus', 'magiriscium',
                        'Maro2', 'pyxidatus', 'castellatim',
                        'dialectos', 'enariste', 'lagonaris'}
        file2 = f'{fold}false_of'
        false_of = set(to.from_txt2lst(file2))
        false_of = set(x[:-1] for x in false_of if x[-1] == ';')
        self.of_excp |= false_of



    def short_cut(self, kind=0):
        if kind == 1:
            self.lst = pi.open_pickle(f'{fold}old_lst', 1)
        elif kind == 2:
            self.word2def = pi.open_pickle(f'{fold}old_word2def', 1)
            self.word2def_orig = pi.open_pickle(f'{fold}old_word2def_orig', 1)
        elif kind == 3:
            self.word2clas = pi.open_pickle(f'{fold}word2clas', 1)
        elif kind == 4:
            self.word2clas = pi.open_pickle(f'{fold}word2clas2', 1)
        elif kind == 5:
            self.variants = pi.open_pickle(f'{fold}variants', 1)
            self.dash_kinds = pi.open_pickle(f'{fold}dash_kinds', 1)
        elif kind == 6:
            self.all_english = []
            self.greek_errors = defaultdict(list)
            self.dash_kinds = defaultdict(set)
            self.english2 = pi.open_pickle('raw_freq_top1m', 0)
            # self.lat_freq = pi.open_pickle(f'{fold}latin_freq_all_ui', 1)
            tpos = to.from_txt2lst(f'{fold}pos_old')
            tpos = set(x for x in tpos if not x[-1] == '*')
            self.tpos = tpos
            self.old2new = {}
            self.variants = []
            self.contractions = {}
            self.all_greek = []
            self.all_greek2 = []
            self.word2clas = {}
            self.aft_et = ['Forms:', 'Orthography:', 'Gender:', 'Prosody:',
                           'Construction:', 'NB:', 'Prosod.:', 'Position:',
                           'Number:', 'Abbreviations:', 'Mood:', 'Note:',
                           'Constructions:', 'Plural:', 'Postulatory:',
                           'Fumitory:', 'Many-rooted:', '(poet.)', '(usu. pl.)']

            self.nlem_mark = ['ablative', 'perfect', 'infinitive', 'superlative',
                              'participle', ' m.', ' n.', 'imperative',
                              'accusative', 'dative', 'genitive', ' sg.', 'vocative',
                              'comparative', 'neut.', 'fem.', 'masc.', 'pl.', 'sg.',
                              'old nominative', 'subjunctive', 'diminutive', ' f. '
                              ]

        elif kind == 7:
            self.lat_freq = pi.open_pickle(f'{fold}latin_freq', 1)
            if public:
                self.lst = to.from_txt2lst(f'{fold}old_public')
            else:
                file = f'{lfold}books/dictionaries/oxford_latin_dct'
                lst = to.from_rtf2lst(file)
                self.lst = lst.split('\n')
                self.lst = self.lst[99_969:]
        elif kind == 8:
            self.has_brackets = pi.open_pickle(f'{fold}old_has_brackets')


class step_one(top_most):
    def __init__(self):
        top_most.__init__(self)


    def apply_check_def(self):
        '''
        fix backslash
        fix defs beginning with -
        fix defs defined by see

        '''

        file = f'{fold}def_check2'
        file2 = f'{fold}def_check3'
        file3 = f'{fold}check_def4'
        lst = to.from_txt2lst_tab_delim(file, 1, 1)
        lst2 = to.from_txt2lst_tab_delim(file2, 1, 1)
        lst4 = to.from_txt2lst_tab_delim(file3, 1, 1)
        dct2 = self.fix_def_check4(lst4)
        lst3 = []
        for x in lst:
            if x[0] == 'zzz':
                break
            else:
                lst3.append(x)

        lst3 += lst2
        dct = {}
        for x in lst3:
            if x[0].isdigit():
                pass
            else:
                try:
                    dct[x[0]] = x[1]
                except:
                    p(x)

        self.parsed_def = merge_2dicts(dct, dct2)
        return

    def fix_def_check4(self, lst):
        dct = {}
        for l in lst:
            k = l[0]
            v = l[1]
            v = v.replace('\\;', '')
            if v.count('\\') > 1:
                p(k)
            dct[k] = v
        return dct

    def check2(self, kind=0):
        '''
        \\'9e=ž
        \\'a0=?
        \\
        file1 = f'{dwn_dir}martinez.mp4'
        file2 = f'{dwn_dir}martinez2.mp4'
        ffmpeg_extract_subclip(file1, 0, 60, targetname=file2)

        '''

        lst5 = to.from_txt2lst(f'{fold}rtfchar')
        lst6 = [x[:-1] if '*' in x else x for x in lst5]
        lst6 = vgf.sort_lst_by_len(lst6, 1)
        elim_rtf = {x: r2t(x) for x in lst6}
        elim_rtf["\\'96"] = '-'
        elim_rtf = merge_2dicts({"\\ulnone": ""}, elim_rtf)
        self.elim_rtf = elim_rtf
        self.elim_rtf['\x9c'] = f'o{tie}e'
        dct11 = {}
        if not kind:
            for k, v in self.parsed_def.items():
                u = v
                for x, y in elim_rtf.items():
                    u = u.replace(x, y)
                dct11[k] = u

            lst8 = [' See ', ' see ', '=', 'lll', 'mmm', 'vvv']

            for k, v in dct11.items():
                if v.count('\\') > 1:
                    p(k)
                elif v.count('\\') == 0 and not k[0] == '-' and all(z not in v for z in lst8):
                    p(f'no slash {k}')
            self.parsed_def = dct11

        return



    def main(self):
        p ('eliminating strange characters')
        for e, x in en(self.lst):
            vgf.print_intervals(e, 100_000,0,len(self.lst))
            self.ln = x
            if self.ln:
                self.elim_spec_char(e)
                self.lst[e] = self.ln

        return

    def elim_heading(self):
        lst1 = []
        lst2 = []
        self.all_greek = []
        e = 0
        while e < len(self.lst):
            x = self.lst[e]
            if 'Glare, P. G. W.' in x:
                del lst1[-1]
                e += 7
            else:
                lst1.append(x)
            e += 1
        self.lst = lst1

        return

    def elim_spec_char(self, e):

        '''
        check \\i0  \\b0  \i\b
        diphthong chr is 865
        fontsizes: 24 28 36 22
        old_bottom = chr(8869)
        bowtie = chr(8904)
        contradictory = chr(390)
        neg = chr(172)
        lneg = chr(10858)
        infer = chr(8680)
        '''

        if 'V5' in self.ln:
            bb = 8

        self.ln = self.ln.replace('\\uc0\\u865 ', chr(865))
        self.ln = self.ln.replace('\\u865 ', chr(865))
        self.ln = self.ln.replace('\\f0\\b0', '@')
        self.ln = self.ln.replace('\\b0', '@')
        self.ln = self.ln.replace('\\f2\\b', '#')
        self.ln = self.ln.replace('\\f1\\i', '$')
        self.ln = self.ln.replace('\\f0\\i0', '^')
        if 'partightenfactor' in self.ln:
            self.ln = old_bottom
        self.ln = self.ln.replace('\\uc0\\u8229', '..')
        self.ln = self.ln.replace('\\uc0\\u9654', contradictory)
        self.ln = self.ln.replace('\\cf0', '')
        self.ln = self.ln.replace('\\uc0', '')
        self.ln = self.ln.replace('\\i0\\b', '^#')
        self.ln = self.ln.replace("\\\'a1\\\'b4", '<')
        self.ln = self.ln.replace("\\\'a1\\\'b5", '>')
        self.ln = self.ln.replace('\\super ', '')
        self.ln = self.ln.replace('\\nosupersub ', '')
        self.ln = self.ln.replace("\\\'97", ' ')
        self.ln = self.ln.replace("\\\'92", "'")
        self.ln = self.ln.replace("\\\'91", "'")
        self.ln = self.ln.replace('\\fs', bowtie)
        self.ln = self.ln.replace('\\u972 ', "ó")
        self.ln = self.ln.replace('\\u973 ', chr(973))
        self.ln = self.ln.replace('\\u974 ', chr(974))
        self.ln = re.sub(r'\\' + r'f\d', ' ', self.ln)
        for k, v in self.elim_rtf.items():
            self.ln = self.ln.replace(k, v)

        if self.ln[-1] == '\\':
            self.ln = self.ln[:-1]

        c = re.findall(r'\\u\d{3,}\s', self.ln)
        for l in c:
            nums = re.sub(r'[^0-9]', '', l)
            self.ln = self.ln.replace(l, chr(int(nums)))

        self.ln = self.ln.replace("\'", "'")  # not working
        self.ln = self.ln.replace("ë", "ĕ")  # not working
        if 'ë' in self.ln:
            bb = 8
        lst7 = ['a2', 'a3', 'a4']
        '''
        some greek letters were represented as a2, a3 etc
        in the rtf code and i'm not sure this error was
        every fixed
        '''

        if any(x in self.ln for x in lst7):
            for x in lst7:
                if x in self.ln:
                    self.greek_errors[x].append(self.ln)










class ad_hoc(step_one):
    def __init__(self):
        step_one.__init__(self)

    def begin_ad(self):
        # self.word2clas = lst[0]
        # self.err = lst[1]
        # self.err2 = lst[2]
        # self.variants = lst[3]

        self.get_attsad()
        self.get_ad_lst()
        self.handle_delf()
        self.step1ad()
        self.compounds()
        self.main_loop()
        self.handle_iivv()
        self.implement_del()
        return


    def get_ad_lst(self):
        lst1 = to.from_txt2lst_tab_delim(f'{fold}ad_hoc_bracket')
        lst2 = to.from_txt2lst_tab_delim(f'{fold}ad_hoc_bracket2')
        lst3 = []
        self.first = set()
        for x in lst1:
            if x[0] == 'zzz':
                break
            else:
                lst3.append([x[0], [x[1]]])
                self.first.add(x[0])

        on = 0
        for x in lst2:
            if x[0] == 'zzz':
                on = 1
            elif on:
                lst4 = x[1].split('|')
                for e, z in en(lst4[:-1]):
                    if e < 10:
                        lst4[e] = z[:-1]
                    else:
                        lst4[e] = z[:-2]

                lst3.append([x[0], lst4])
        self.ad_lst = lst3



    def handle_delf(self):
        self.del_dct = {}
        self.ad_dct = {}
        for l in self.ad_lst:
            word = l[0]
            for line in l[1]:
                if reg(r'delf\d+', line):
                    num = line[line.index('delf') + 4:line.index('delf') + 6]
                    num = num.strip()
                    try:
                        num = int(num)
                    except:
                        p(f'bad number in {word}')
                    self.del_dct[word] = num

    def implement_del(self):
        for x, y in self.del_dct.items():
            obj = self.word2clas.get(x)
            if not obj:
                obj = self.var_dct.get(x)
                if not obj:
                    p(f'missing {x}')

            if obj:
                for i in range(y - 1):
                    if ha(obj.raw[i]):
                        p(x, obj.raw[i])
                    obj.raw[i] = ''
        return

    def step1ad(self):
        self.dct = defaultdict(list)
        self.non_lemmas2 = []
        for x in self.ad_lst:
            key = x[0]
            for z in self.ad_hoc_code:
                if key.startswith(z):
                    if z == 'nnll':
                        self.non_lemmas2.append(x)
                    else:
                        key1 = key[len(z):]
                        self.dct[z].append([key1, x[1]])
                        break

    def handle_iivv(self):
        lst2 = ['iivv', 'ssww', 'cc']

        for m in lst2:
            for l in self.dct['iivv']:
                word = l[0]
                obj = self.word2clas.get(word)
                if obj:
                    for e, line in en(l[1]):
                        if '=' in line and m == 'iivv':
                            idx = line.index('=')
                            s = line[idx + 1:].strip()
                            if ' ' in s:
                                s = s[:s.index(' ')]
                            vari = re.sub('[\.,;]', '', s)
                            self.add_ins2(vari, word, 1)
                            if m + word in self.first:
                                self.get_idx({0: vari}, obj.raw, word)
                            else:
                                obj.raw[e - 1] = ''
                        elif 'ometimes written' in line and m == 'ssww':
                            line2 = line.strip()
                            if line2.endswith('written'):
                                vari = l[1][e + 1].strip()
                                p(word, obj.raw[e - 1])
                                p(word, obj.raw[e])
                                obj.raw[e - 1] = ''
                                obj.raw[e] = ''

                            else:
                                idx = line.index('written') + len('written')
                                vari = line[idx:] + 1
                                vari = vari.strip()
                                vari = vari[:vari.index(' ')]
                                p(word, obj.raw[e - 1])
                                obj.raw[e - 1] = ''

                            self.add_ins(vari, word, 1)

        for l in self.dct['nnvv']:
            word = l[0]
            obj1 = old_entry(word)
            for e, line in en(l[1]):
                if '{' in line:
                    self.handle_brace(e, line, obj1, word, 1)

    def get_props(self, s, key):
        dct = {
            'i': 'inflection',
            'infl': 'inflection',
            'ge': 'genetive',
            'v': 'variant_of',
            'hv': 'variants',
            'n': 'number',
            'r': 'register',

        }
        ins2 = old_entry('hey')
        attrib = set(x for x in ins2.__dict__)

        dct1 = {}
        t = s[s.index('{') + 1:s.index('}')]
        if t.count('=') > 1 and t.count('=') == t.count(',') + 1:
            lst = vgf.strip_n_split(t, ',')
        else:
            lst = [t]

        for x in lst:
            y = vgf.strip_n_split(x, '=')
            itm = dct.get(y[0], y[0])
            if itm == y[0] and itm not in attrib:
                p(f'missing {y[0]} in {key}')

            if itm:
                if itm == 'variant_of':
                    val = re.sub(r'[\.,;]', '', y[1])
                else:
                    val = y[1]

                dct1[itm] = val

        return dct1



    def main_loop(self):
        for l in self.ad_lst:
            word = l[0]
            if word in ['pendeo', 'cado', 'Calchedonensis']:
                bb = 8
            obj = self.word2clas.get(word)
            if obj:
                if word[0] == ';' or ';;' in l[1][-1]:
                    self.short_infl(obj, 'i', word)
                elif '::' in l[1][-1]:
                    self.short_infl(obj, 'p', word)

                for e, line in en(l[1]):
                    if 'ddd' in line:
                        p(word, obj.raw[e - 1])
                        obj.raw[e - 1] = ''
                    # elif '(intr.)' in line:
                    #     obj.
                    #     obj.pos += ' intr.'
                    #     obj.raw[e] = ''
                    elif '{' in line:
                        self.handle_brace(e - 1, line, obj, word)
        return

    def handle_brace(self, e, line, obj, word, vari=0):
        dct = self.get_props(line, word)
        for s, t in dct.items():
            val = getattr(obj, s)
            val += t
            setattr(obj, s, val)
        if word in self.first and not vari:
            num = self.get_idx(dct, obj.raw, word)
            # if not num:
            #     p(f'{word} no connection')
        elif not vari:
            # p (word, obj.raw[e])
            obj.raw[e] = ''

    def get_idx(self, dct, lst, word):
        st1 = set(dct.values())
        c = 0
        for e, z in en(lst):
            st = set(z.split())
            if any(s in self.tpos for s in st):
                c += 1
            else:
                zu = re.sub(r'[\]\.,\(\);:]', '', z)
                st = set(zu.split())
                if st & st1:
                    lst[e] = ''
                    c += 1
            if len(st1) == c:
                # break
                return 1
        p('getidx', word, dct)

    def compounds(self):
        for l in self.dct['cc']:
            word = l[0]
            obj = self.word2clas.get(word)
            if obj:
                for e, z in en(obj.raw):
                    if '~' in z:
                        obj.compounds.append(z.strip())
                        obj.raw[e] = ''
                        break
                    else:
                        # p(obj.raw[e])
                        obj.raw[e] = ''

    def short_infl(self, obj, att, word):
        for e, x in en(obj.raw):
            if ha(x):
                if att == 'i':
                    obj.inflection += " " + x.strip()
                elif att == 'p':
                    obj.pos.append(x.strip())
                p(word, obj.raw[e])
                obj.raw[e] = ''
                break

    def add_ins2(self, w, parent, kind=0):
        wu = unidecode(w)
        ins = old_entry(wu)
        ins.wmacron = w
        ins.variant_of = unidecode(parent)
        self.var_dct[wu] = ins
        return ins


class parse_variants(ad_hoc):
    def __init__(self):
        ad_hoc.__init__(self)



    def begin_pv(self):
        self.get_attspv()
        self.get_variants() # interval loop
        self.parsevl()
        self.parse_of()
        self.parse_equals()
        self.parse_see()

    def isolate_bracket(self):
        self.defect_bracket = {}
        for x, y in self.word2clas.items():
            if x == 'abstulo':
                bb = 8
            for e, z in en(y.raw):
                if '[' in z:
                    pre = ''
                    for f, t in en(z):
                        if t == '[':
                            s = z[f:]
                            if f > 0:
                                pre = z[:f]
                            break
                    y.raw[e] = ''
                    post = ''
                    if ']' in s:
                        post = s[s.index(']') + 1:].strip()
                        mid = s[:s.index(']') + 1]
                    else:
                        mid = s
                        g = e
                        while g < len(y.raw):
                            g += 1
                            n = y.raw[g]
                            if ']' in n:
                                y.raw[g] = ''
                                mid += f' {n[:n.index("]") + 1]}'
                                post = n[n.index(']') + 1:]
                                break
                            elif old_bottom in n:
                                self.defect_bracket[x] = y.oraw
                                break
                            else:
                                mid += f' {n}'
                                y.raw[g] = ''
                    if ha(post):
                        y.raw.insert(e + 1, post)
                    y.raw.insert(e + 1, mid)
                    if ha(pre):
                        y.raw.insert(e + 1, pre)
                    break
        return

    def get_variants(self):
        # cacabus not getting inflection
        # don't see why necerim is getting included
        # get the ad-hoc exceptions later
        ad_hoc = ['aroscit', 'Āsōpiadēs', 'ciprus',
                  'Collīnus2', 'cēuentinābiliter', 'Corcȳraeus',
                  'Dardanus2', 'Diespiter', 'Āpis2']
        lst7 = ['see also', 'see the']

        vl_exc = {'Mīnōs', 'Orestēs1'}
        # must begin the etymology
        to_del = set()
        file = f'{fold}false_equals'
        file1 = f'{fold}false_variants'
        fals_equals = to.from_txt2lst_tab_delim(file)
        fals_var = to.from_txt2lst_tab_delim(file1)

        self.synonyms = {}
        false_equals2 = set()
        synon = set()
        for x in fals_equals:
            w = unidecode(x[0][1:])
            w = w.replace('?', '')
            if x[0][0] == "#":
                false_equals2.add(w)
            elif x[0][0] == '*':
                synon.add(w)
        for x in fals_var:
            if x[0][0] == ";":
                false_equals2.add(x[0][1:])
            elif x[0][0] == '*':
                synon.add(x[0][1:])

        fe = 0
        sy = 0
        self.vl = {}
        self.equalb = {}
        self.equals = {}
        self.con_var = {}
        self.variants2 = {}
        self.variants3 = {}
        self.variants4 = {}
        self.variants5 = {}
        self.form_var = {}
        self.see_also = {}
        tmes = ['inversion', 'tmesis', 'separated']
        self.see = {}
        seperable2 = to.from_txt2lst_tab_delim(f'{fold}seperable')
        not_seperable = []
        seperable = {}
        for x in seperable2:
            if '**' in x[1]:
                not_seperable.append(x[0])
            else:
                seperable[x[0]] = x[1]
        self.see2 = {}
        lst1 = ['late spelling of', 'old spelling of',
                'contraction of ', ' v.l. for ',
                'variants of', 'variant reading for',
                'var. spelling of', 'forms of', 'var. of', 'form of', 'Form of']

        for x, z in self.word2clas.items():
            if x == 'Ceuenna':
                bb = 8
            new = 0
            nx = 0
            if x in false_equals2:
                fe += 1
                pass
            elif x in synon:
                sy += 1
                self.synonyms[x] = z

            elif x in ad_hoc:
                pass
            else:
                for e, y in en(z.raw):
                    if 'contracted for ' in y:
                        self.con_var[x] = y
                        to_del.add(x)
                        break
                    elif 'v.l.' in y and 's.v.l' not in y \
                            and x not in vl_exc:
                        self.vl[x] = y
                        to_del.add(x)
                        break
                    elif 'two words' in y and x not in not_seperable:
                        z.seperable = 1
                        if any(r in y for r in tmes):
                            z.tmesis = 1
                        itm = seperable[x]
                        if "<" in itm:
                            z.raw[e] = re.sub(r'<.*>', '', itm)
                        else:
                            z.raw[e] = ''


                    elif 'Also' in y:
                        break
                    elif not y:
                        new = 1

                    elif old_bottom in y:
                        break

                    elif reg(r'(S|s)ee\salso', y):
                        self.see_also[x] = y
                        break
                    elif (reg(r'\s+(S|s)ee\s', y) \
                          or reg(r'^(S|s)ee\s', y) or reg(r'\((S|s)ee\s', y)) \
                            and not 'ee quotat' in y \
                            and all(u not in y for u in lst7) \
                            and x not in self.see_excp:
                        to_del.add(x)
                        if '[' in y:
                            self.see2[x] = y
                        else:
                            self.see[x] = y
                            z.raw[e] = ''

                        break
                    elif any(t in y for t in lst1) and \
                            x not in self.of_excp:

                        self.form_var[x] = y
                        to_del.add(x)
                        break

                    elif '=' in y and x not in self.false_equals2:
                        if '[' in y:
                            self.equalb[x] = y
                        else:
                            self.equals[x] = y
                        to_del.add(x)
                        break
                    if nx:
                        break

                    if '[' in y:
                        nx = 1

        return

    def parsevl(self):
        odd = {}
        for x, y in self.vl.items():
            if x == 'mantichoras':
                bb = 8
            s = y
            if 'v.l. for' in y:
                t = s[s.lower().index('v.l. for') + len('v.l. for'):].strip()
            else:
                t = s[s.lower().index('v.l.') + 4:].strip()

            if not ha(unidecode(t)):
                t = self.nxt_line(x, y)

            if ha(unidecode(t)):
                self.variant_exists(t, 0, y, x)
            else:
                self.prob[x] = y
        return

    def parse_see(self):
        excp = ['aedoeon', 'potami', 'uerse', 'deque']
        odd = {}
        for x, y in self.see.items():
            s = y
            t = s[s.lower().index('see') + 4:].strip()
            if x in excp:
                bb = 8

            if ha(unidecode(t)):
                com = 1 if x in excp else 0
                self.variant_exists(t, com, y, x)
            else:
                odd[x] = y

        return

    def parse_of(self):
        non_lemmas = ['fictus2']
        # lagonaris has =

        of_dct = {
            'quoiquoimodi': 'cuicuimodi',
            'quoiuismodi': 'cuiuismodi',
            'quoius1': 'cuius',
            'quoiusmodi': 'cuiuismodi',
            'parret': 'paret'

        }

        lst1 = ['late spelling of', 'old spelling of',
                'contraction of ', ' v.l. for ',
                'variants of', 'variant reading for',
                'var. spelling of', 'forms of', 'var. of',
                'form of', 'Form of',
                'mistake for,', 'old form of pl. of',
                ]
        lst1 = vgf.sort_lst_by_len(lst1, 1)
        old = ['old', 'archaic', 'early', 'earlier', 'original',
               'primitive']
        colloquial = ['plebian', "rustic", 'colloquial', 'popular',
                      'dialect', 'illiterate']
        late = ['later']
        poetic = ['poetic']
        lst5 = [old, colloquial, late, poetic]
        lst6 = ['old', 'colloquial', 'late', 'poetic']
        rdct = {}
        for x, y in zip(lst5, lst6):
            for z in x:
                rdct[z] = y

        for x, y in self.form_var.items():
            if x == 'aberceo':
                bb = 8

            for z in lst1:
                if z in y:
                    yu = y[y.index(z) + len(z):].strip()
                    beg = y[:y.index(z)]
                    reg = ''
                    for s, t in rdct.items():
                        if s in beg.lower():
                            reg = t
                    parent = of_dct.get(x)

                    if parent:
                        obj = self.word2clas[x]
                        obj.variant_of = parent
                        self.var_dct[x] = obj
                    else:
                        if not ha(yu):
                            # p (x,y)
                            yu = self.nxt_line(x, y)
                            yu = yu.strip()
                            # p (yu)

                        if ha(yu):
                            obj = self.variant_exists(yu, 0, y, x)
                        else:
                            self.prob[x] = y
                    if reg and obj:
                        obj.register = reg
                    break
        return

    def nxt_line(self, x, y):
        z = self.word2clas[x]
        for e, l in en(z.raw):
            if l == y:
                return z.raw[e + 1]
        assert 0

    def parse_equals(self):
        excp = set()
        dct = {}
        for x, y in self.equals.items():
            s = y
            t = s[s.lower().index('=') + 1:].strip()
            if ha(t):
                self.variant_exists(t, 0, y, x)
            else:
                dct[x] = y
        return

    def variant_exists(self, t, compound, y, x):
        t = self.elimv2(t)
        t = re.sub(r'[\$#\*]', '', t)
        t = t.replace('#', '').strip()
        if compound:
            pass
        else:
            if ' ' in t:
                t = t[:t.index(' ')]
        t = re.sub(r'[\]\.,\(\);:]', '', t)
        if '-' in t:
            self.fixes[x] = y
            return 0
        else:
            tu = unidecode(t)

            found = self.word2clas.get(tu)
            if not found:
                tobj = self.var_dct.get(tu)
                if not tobj:
                    self.prob2[x] = y
                    self.missing_words.add(tu)
                    return 0
                else:
                    self.prob3[x] = y
                    # obj = self.word2clas.get(tobj.variant_of)
                    # if not obj:
                    #     return 0
                    # else:
                    #     tu = obj.uiword
                    return 0

            else:
                obj = self.word2clas[x]
                obj.variant_of = tu
                self.var_dct[x] = obj
                self.to_del.add(x)
        return obj


class handle_also(parse_variants):
    def __init__(self):
        parse_variants.__init__(self)

    def begin_ha(self):
        self.variants7 = {}
        self.use_manual_variants3()
        by_lst = self.main_ha()
        just_tilde = self.handle_also2(by_lst)
        self.bad_dash = {}
        self.mid_dash = {}
        self.parse_jtilde(just_tilde)
        self.prep_bad_dash()
        self.parse_dash2()
        self.parse_dash(0)

        # new_variants = vgf.split_dct(self.variants, totv, len(self.variants))
        # self.test_also(new_variants)
        return

    def convert_dcts(self, ):
        self.two_words = to.from_txt2lst_tab_delim(f'{fold}also_two_words', 0, 1)
        self.also_sg = to.from_txt2lst_tab_delim(f'{fold}also_sg', 0, 1)
        self.also_other = to.from_txt2lst_tab_delim(f'{fold}also_other', 0, 1)
        to_del = []
        for e, x in en(self.also_other):
            if len(x) == 6:
                del x[-1]
                to_del.append(e)
                self.two_words.append(x)
            elif len(x) == 5 and x[4] == 'c':
                del x[-1]
                to_del.append(e)
                self.two_words.append(x)
        for x in reversed(to_del):
            del self.also_other[x]

        self.unusual = []
        self.elim_two_words()
        self.elim_also(self.also_sg)
        self.elim_also(self.also_other, 1)
        self.implement_unusual()
        return

    def elim_two_words(self):
        for l in self.two_words:
            try:
                obj = self.word2clas[l[0]]
                obj.two_words = l[2]

                if len(l) > 4:
                    if l[4] == 't':
                        obj.tmesis = 1
                    else:
                        obj.pos.append(l[4])

                if len(l) > 3 and l[3] == '*':
                    self.unusual.append(l[0])
                else:
                    obj.raw = self.del_lst(obj.raw)
            except:
                if not public:
                    assert 0

        return

    def elim_also(self, lst, kind=0):
        self.non_lemmas = []
        lword = ''
        for l in lst:
            try:
                obj = self.word2clas[l[0]]
                if not kind:
                    obj.number = 'mostly plural'

                if len(l) > 2:
                    nword = l[1]
                limit = 2
                if len(l) > 3:
                    limit = l[3]
                if limit == '[':
                    obj.raw = self.del_lst(obj.raw)
                elif lword == l[0]:
                    pass
                elif limit == '*':
                    self.unusual.append(l[0])
                else:
                    obj.raw = self.del_lst(obj.raw, limit)
                if l[0] == 'bigae':
                    bb = 8
                try:
                    if l[2]:
                        self.new_sg(obj, l)
                except:
                    pass

                lword = l[0]
            except:
                if not public:
                    assert 0

        return

    def new_sg(self, obj, olst):
        if len(olst) == 2:
            return
        oword = olst[0]
        nword = olst[2]
        if ' ' not in nword:
            nwordu = unidecode(nword)
            ins = old_entry(nwordu)
            nword2u = nword
            ins.variant_of = oword
            ins.wmacron = nword
            ins.raw = obj.raw
        else:
            lst = nword.split()
            nword2 = lst[0]
            infl = ''
            if '~' in lst[1]:
                infl = ' '.join([x for x in lst if '~' in x])
            pos = ''
            for x in lst:
                if '.' in x:
                    pos = x
                    break
            if not infl:
                for x in lst[1:]:
                    if not '.' in x:
                        infl += " " + x
            nword2u = unidecode(nword2)
            ins = old_entry(nword2u)
            ins.wmacron = nword2
            ins.inflection = infl
            ins.pos.append(pos)
            ins.variant_of = oword
            if len(olst) == 5:
                if olst[4] in ['nonl', 'non-lemma']:
                    self.non_lemmas.append(olst[0])
                elif olst[4] in ['archaic']:
                    ins.register = 'archaic'
                elif '.' in olst[4]:
                    ins.pos.append(olst[4])

        self.singular_variants[nword2u] = ins



    def implement_unusual(self):
        file = f'{fold}also_unusual'
        lst7 = to.from_txt2lst_tab_delim(file)
        for l in lst7:
            word = l[0]
            try:
                obj = self.word2clas[word]
                for f, x in en(obj.raw):
                    if 'Also' in x:
                        break
                raw = l[1]
                raw = raw.split('|')
                on = 0
                for t in raw:
                    if t == '{':
                        on = 1
                    elif t == '}':
                        on = 0
                    elif t == '|' and on:
                        p(f'error in {word}')

                for e, z in en(raw):
                    s = re.sub(r'\{.*\}', "", z)
                    obj.raw[e] = s
                    if s != z:
                        break
            except:
                if not public:
                    assert 0

        return

    def del_lst(self, lst, limit=0):
        f = 0
        found = 0
        for e, x in en(lst):
            if 'Also' in x:
                if limit and limit != '[':
                    for f, z in en(lst[e:e + limit]):
                        lst[e + f] = ''
                    return lst

                found = 1
                if '[' in x:
                    lst[e] = x[x.index('['):]
                    return lst
                else:
                    lst[e] = ''
            elif '[' in x and found:
                lst[e] = x[x.index('['):]
                return lst
            elif found:
                lst[e] = ''
            if found:
                f += 1
            if f == 4:
                return lst
        return lst

    def main_ha(self):
        # assipio does not fit the pattern
        self.singular_variants = {}
        self.convert_dcts()

        by_lst2 = to.from_txt2lst_tab_delim(f'{fold}by_lst', 1)
        by_lst3 = {}
        for l in by_lst2:
            found = 0
            if l[0].isdigit():
                pass
            else:
                g = []
                for z in l[1:]:
                    if "**" in z:
                        g.append(z.replace('**', ''))
                        found = 1
                        break
                    else:
                        g.append(z)
                if found:
                    by_lst3[l[0]] = g

        by_lst = {}
        for x, y in self.word2clas.items():
            if x == 'Tomis2':
                bb = 8
            if x in by_lst3:
                by_lst[x] = by_lst3[x]
            else:

                for e, z in en(y.raw):
                    zu = re.sub(r'[\^@\.\(\)]', '', z)
                    zu = zu.strip()
                    # if zu.count(' ')>3:
                    if old_bottom in zu:
                        break

                    if zu == 'Also':
                        y.raw[e] = ''
                        f = e + 1
                        lst6 = []
                        while f < len(y.raw):
                            s = y.raw[f]
                            st = re.sub(r'[@\$\^]', '', s)
                            st = st.strip()
                            if st in self.tpos:
                                y.raw[f] = ''
                                lst6.append(st)
                            elif any(t in s for t in self.aft_et):
                                break

                            elif self.is_english(s) or '..' in s or old_bottom in s:
                                break

                            elif '.' in s or '[' in s:
                                u = 200
                                i = 200
                                if '.' in s:
                                    u = s.index('.') + 1
                                if '[' in s:
                                    i = s.index('[')
                                if u < i:
                                    idx = u
                                else:
                                    idx = i
                                t = s[:idx]
                                if ha(t):
                                    lst6.append(t)
                                y.raw[f] = s[idx:]
                                break
                            else:
                                y.raw[f] = ''
                                lst6.append(s)

                            f += 1
                        by_lst[x] = lst6



        return by_lst

    def use_manual_variants3(self):
        manual_variants = to.from_txt2lst_tab_delim(f'{fold}manual_variants3', 1, 1)
        self.more_variants = []
        for l in manual_variants:
            child = l[0]
            parent = l[1]
            self.add_ins(child, parent)

    def handle_also2(self, by_lst):
        '''
        passiolus - var.
        Cerialia - see.
        (f.
        forms of caerefoliom, chaerephyllum
        '''

        ignore = {'(deponent).', 'forms of caerefolium.', '(in quotation, as two words).'}
        prob_dash = {}
        also_errors = to.from_txt2lst_tab_delim(f'{fold}also_errors', 1, 1)
        also_irreg = to.from_txt2lst_tab_delim(f'{fold}also_irreg', 1, 1)
        ignore_key = []
        for l in also_irreg:
            if len(l) == 1:
                ignore_key.append(l[0])
            else:
                try:
                    obj = self.word2clas[l[0]]
                    setattr(obj, 'forms', l[2])
                except:
                    if not public:
                        assert 0

        temp_pos = set()
        to_replace = {}
        ldist = set()
        for x in also_errors:
            if len(x) == 1:
                if x[0][0] == '#':
                    temp_pos.add(x[0][1:])
                elif not x[0][0] == '/':
                    ignore.add(x[0])
                else:
                    ldist.add(x[0][1:])
            else:
                to_replace[x[0]] = x[1]

        new = set()
        self.tpos |= temp_pos
        for x in self.tpos:
            x = x.replace('.', '')
            new.add(x)
        self.tpos |= new

        new_ins = {}
        has_com = {}
        deps = {}
        two = {}
        ins = 0
        nid = defaultdict(list)
        di = []
        did = {}
        just_tilde = {}
        pos_errors = {}
        totv = len(self.variants)
        eng = ['spelling', 'sometimes']
        if 'confluens' in by_lst:
            bb = 8

        for x, y in by_lst.items():
            obj = self.word2clas[x]
            self.temp_raw = y
            dep = 0
            infl = ""
            instances = []
            if x == 'confluens':
                bb = 8

            for z in y:
                z = re.sub(r'[#@\$]', '', z)
                z = z.strip()
                zu = unidecode(z)
                if zu and zu[0] == '(':
                    zu = zu[1:]

                zu = to_replace.get(zu, zu)

                if z in ignore or zu in ignore:
                    pass
                elif z in self.tpos or zu in self.tpos:
                    if zu in self.tpos and z not in self.tpos:
                        z = zu

                    if not instances:
                        pos_errors[x] = y
                    else:
                        for r in instances:
                            r.pos.append(z)
                            if infl:
                                ins.inflection = infl

                    infl = ""
                    # if ni:
                    #     nid[ni].append([x, y])
                    #     ni = 0
                elif not z or not ha(zu):
                    pass
                elif zu in ['and', 'or', 'etc.']:
                    pass
                elif any(t in z for t in eng):
                    pass
                elif 'two words' in z:
                    two[x] = y
                elif '~' in z or '~' in zu:
                    if '~' in zu and '~' not in z:
                        z = zu

                    infl += " " + z
                    infl = infl.strip()

                elif '-' in z or '-' in zu:
                    if '-' not in z:
                        z = '-' + z


                    if ' ' in z:
                        prob_dash[x] = y
                    nword = f"{obj.wmacron} {z}"
                    ins = self.add_variant(x, nword)
                    if instances:
                        for r in instances:
                            r.inflection = infl
                    instances = [ins]
                    infl = ""
                else:
                    if reg(r'[a-zA-Z],\s[a-zA-Z]', zu):
                        instances = self.var_comma(x, z)
                    else:
                        d = vgf.lvn.distance(zu, x)
                        if d > 3 and zu not in ldist: #todo make into errors
                            p(f'large distance {x} {zu}')
                        if '(' in z:
                            instances = self.elim_paren(x, z)
                        else:
                            ins = self.add_variant(x, z)
                            instances = [ins]

            if infl and instances:
                for r in instances:
                    r.inflection = infl
                    self.variants7[r.uiword] = r
            elif infl and not instances:
                just_tilde[x] = [infl, self.temp_raw]


        return just_tilde

    def var_comma(self, x, y):
        lst = vgf.strip_n_split(y, ',')
        lst1 = []
        for z in lst:
            ins = self.add_variant(x, z)
            lst1.append(ins)
        return lst1

    def add_variant(self, x, z, kind=0):
        if 'polliceor' in x:
            bb = 8

        z = re.sub(r'[\.,]', '', z)
        zu = unidecode(z)
        ins = old_entry(zu)
        ins.wmacron = z
        ins.variant_of = x

        if kind == 2:
            self.variants7[z] = ins
        else:
            self.variants7[zu] = ins
        if not kind:
            ins.traw = self.temp_raw

        return ins

    def elim_paren(self, x, z):
        wop = re.sub(r'\(.+\)', '', z)
        wp = re.sub(r'[\(\)]', '', z)
        ins1 = self.add_variant(x, wop)
        ins = self.add_variant(x, wp)
        return [ins, ins1]

    def parse_dash(self, research=0):
        got = 0
        ngot = defaultdict(set)
        ngot2 = defaultdict(list)
        mid = defaultdict(list)
        self.new_variants = {}
        self.paren_var = {}
        self.dct10 = {}
        self.equal_var = {}
        self.tie_rep = defaultdict(list)
        self.dash_errors = {}
        self.dash_errors3 = []
        self.dash_errors2 = defaultdict(list)

        for x, y in self.variants7.items():
            if '-' in x:
                if y.wmacron in self.bad_dash:
                    self.use_bad_dash(x, y)
                else:
                    if 'ar(i)' in x:
                        bb = 8

                    fix = x[x.index(' ') + 1:]
                    fix2 = y.wmacron[y.wmacron.index(' ') + 1:]
                    word = x[:x.index(' ')]
                    wordwm = y.wmacron[:y.wmacron.index(' ')]
                    word, num = cut_num(word, 1)
                    wordwm, num = cut_num(wordwm, 1)
                    obj = self.dash_kinds.get(fix)
                    found = 0
                    if obj and len(obj) == 1:
                        key = list(obj)[0]
                        if x.startswith(key):
                            if not research:
                                diff = len(key) - len(fix[:-1])
                                if diff < 0:
                                    tnum = f'-{diff}'
                                elif diff == 0:
                                    tnum = ''
                                elif diff > 0:
                                    tnum = f'+{diff}'

                                self.parse_dash3(fix, tnum, wordwm, y, x, num, 2)
                            found = 1
                            got += 1
                    if not found:
                        if fix.count('-') == 2:
                            if not research:
                                self.use_mid(wordwm, x, y, fix2)
                            else:
                                mid[fix2].append(wordwm)
                        else:
                            if fix[0] == '-':
                                repl = word[-(len(fix) - 1):]
                            elif fix[-1] == '-':
                                repl = word[:len(fix) - 1]
                            if research:
                                ngot[fix].add(repl)
                                ngot2[(fix, repl)].append(word)
                            else:
                                obj = self.replacement.get((fix, repl))

                                if obj:
                                    self.parse_dash3(fix, obj[0], wordwm, y, x, num)
                                else:
                                    self.dash_errors2[(fix, repl)].append(x)

        if research:
            file1 = f'{fold}also_dash_lstm'
            lst3 = []
            found = 0
            for x, y in ngot2.items():
                lst4 = [x[0], x[1], '', ', '.join(y)]
                lst3.append(lst4)
            lst3 = sort_by_col(lst3, 0)
            to.from_lst2txt_tab_delim(lst3, file1)
            vgf.open_txt_file(file1)

        return

    def parse_dash3(self, rep, num, word, ins, key, idx, kind=0):
        err = 0
        nword = ''
        if tie in word:
            tidx = word.index(tie)
            if rep[-1] == '-' and tidx < len(rep) - 1:
                self.tie_rep[rep].append(word)
            elif rep[0] == '-' and tidx > len(word) - len(rep):
                self.tie_rep[rep].append(word)

        if "(" in rep:
            nrep, rep, tnum = self.has_paren(num, rep)
            self.parse_dash3(nrep, tnum, word, ins, key, idx, 1)

        if '.' in num:
            return

        if '=' in num:
            num, rep = self.has_equal(num, rep, word)
            kind = 3

        if rep[0] == '-':
            if not num:
                b = len(rep) - 1
            elif num == '0':
                nword = f'{word}{rep[1:]}'
                err = 1

            elif num.startswith('--'):
                b = len(rep) - 1 - int(num[2:])
            elif num.startswith('+'):
                b = len(rep) - 1 + int(num[1:])
            elif num.startswith('-'):
                b = int(num[1:])
            else:
                self.dash_errors[key] = ins
                err = 1
            if not err:
                nword = f'{word[:-b]}{rep[1:]}'

        else:
            if not num:
                b = len(rep) - 1


            elif num.startswith('--'):
                b = len(rep) - 1 - int(num[2:])
            elif num.startswith('+'):
                b = len(rep) - 1 + int(num[1:])
            else:
                self.dash_errors[key] = ins
                err = 1
            if not err:
                nword = f'{rep[:-1]}{word[b:]}'

        if nword:
            if reg(r'\d$', nword):
                bb = 8
            if kind == 3:
                self.equal_var[key] = [nword + idx, ins]
            elif kind == 2:
                self.dct10[key] = [nword + idx, ins]
            elif kind:
                self.paren_var[key] = [nword + idx, ins]

            self.new_variants[key] = [nword + idx, ins]

    def has_equal(self, num, rep, word):
        lst = num.split(',')
        lst2 = []
        for x in lst:
            lst1 = x.split('=')
            lst2.append([len(lst1[0]), lst1[0], lst1[1]])
        lst2 = vgf.sort_by_col(lst2, 0)
        found = 0
        for l in reversed(lst2):
            fix = l[1]
            if rep[0] == '-':
                if word.endswith(fix):
                    rep = f'-{l[2]}'
                    found = 1
                    break
            elif rep[-1] == '-':
                if word.startswith(fix):
                    rep = f'{l[2]}-'
                    found = 1
                    break
        if not found:
            assert 0

        diff = len(fix) - len(rep[:-1])
        if diff < 0:
            tnum = f'-{diff}'
        elif diff == 0:
            tnum = ''
        elif diff > 0:
            tnum = f'+{diff}'
        return tnum, rep

    def has_paren(self, num, rep):
        u = 0
        on = 0
        for e, f in en(rep):
            if f == '(':
                on = 1
            elif f == ')':
                on = 0
            elif on:
                u += 1
        nrep = re.sub(r'\(.*\)', '', rep)
        rep = re.sub(r'[\(\)]', '', rep)
        if not num:
            tnum = '+1'
        elif num == '0':
            tnum = '0'
        elif num.startswith('--'):
            tnum = int(num[1:]) + u
            if not tnum:
                tnum = ''
            else:
                tnum = f'-{str(tnum)}'
        elif num.startswith('+'):
            tnum = int(num[1:]) + u
            tnum = f'+{tnum}'
        else:
            assert 0
            # tnum = int(num) + u
            # if not tnum:
            #     tnum = ''
            # else:
            #     if tnum<0:
            #         tnum = f''
            #
            #     tnum = str(tnum)
        return nrep, rep, tnum

    def use_bad_dash(self, x, y):
        obj = self.bad_dash[y.wmacron]
        for w in obj[1:]:
            self.new_variants[x] = [w, y]

    def use_mid(self, wordwm, x, y, fix2):
        repl = self.mid_dash.get(fix2)
        if not repl:
            self.dash_errors3.append(fix2)
        else:
            nword = wordwm.replace(fix2[1:-1], repl)
            self.new_variants[x] = [nword, y]

    def prep_bad_dash(self):
        file3 = f'{fold}bad_dash'
        file5 = f'{fold}mid_dash'
        file4 = f'{fold}bad_dash2'
        lst8 = to.from_txt2lst(file3, 1)
        lst7 = to.from_txt2lst_tab_delim(file5, 1)
        lst9 = to.from_txt2lst(file4, 1)
        for x, y in zip(lst8, lst9):
            lst = y.split(' ')
            self.bad_dash[x] = lst
        for x in lst7:
            if x[1] != '.':
                self.mid_dash[x[0]] = x[1]

    def parse_dash2(self):
        file1 = f'{fold}also_dash_lst'
        file2 = f'{fold}also_dash_lst2'

        lst = to.from_txt2lst_tab_delim(file1, 1)
        lst1 = to.from_txt2lst_tab_delim(file2, 1)

        lst3 = []
        found = 0
        for x in lst:
            if x[0] == 'zzz':
                found = 1
            elif found:
                lst3.append(x)
        lst4 = []
        for x in lst1:
            if '-ar(i)arius' in x[0]:
                bb = 8

            if x[0] == 'zzz':
                break
            else:
                lst4.append(x)
        lst4 += lst3
        lst5 = [x for x in lst4 if x[2] != '.']
        self.dot_errors = [x[0] for x in lst4 if x[2] == '.']
        self.replacement = {}
        repeats = {}
        repeats2 = {}
        done = set()
        for l in lst5:
            tpl = (l[0], l[1])
            tpl2 = (unidecode(l[0]), l[1])
            if tpl2 in done:
                repeats[tpl] = [l[2], l[3]]
            else:
                done.add(tpl2)
            if '=' in l[2]:
                bb = 8

            self.replacement[tpl] = [l[2], l[3]]

        return



    def parse_jtilde(self, dct):
        del dct['Aegoceros']
        del dct['abstergeo']

        nos = {}
        for x, y in dct.items():
            infl = y[0]
            traw = y[1]
            found = 0
            if x == 'polliceor':
                bb = 8

            if not ' ' in infl:
                suff = infl
                word = x
                infl = ''

            elif infl[0] == '~':
                idx = infl.index(' ')
                suff = infl[:idx]
                suff = suff.replace(',', '')
                infl = infl[idx:].strip()
                word = x
            else:
                idx = infl.index(' ')
                word = infl[:idx]
                infl = infl[idx + 1:]
                if ' ' in infl:
                    idx = infl.index(' ')
                    suff = infl[:idx]
                    suff = suff.replace(',', '')
                    infl = infl[idx:].strip()
                else:
                    found = 1

            if not found:
                suff = suff.replace('~', '-')
                z = f'{word} {suff}'
                ins = self.add_variant(x, z, 2)
                ins.inflection = infl
                ins.traw = traw
            else:
                ins = self.add_variant(x, word)
                ins.inflection = infl

        return














    def ad_hoc_adj(self):
        '''
        the pattern of quotation is interrupted in the list
        and the following fixes those departures from the pattern
        '''

        lst = [36866, 217197, 338057, 364054, 1066418, 1659626,
               1751856, 1902230, 1942497, 2204697, 2572542,
               2621805, 2752861]
        for num in lst:
            if public and num > len(self.lst):
                pass
            else:
                self.lst[num] = self.lst[num].replace(bowtie + '22', '')
                for i in range(4):
                    del self.lst[num - 4]

    def first_line(self):
        p('separating entries')
        lst5 = []  # abdō. absegmen
        lword = ""
        self.word2def = {}
        self.word2def_orig = {}
        self.suffixes = {}
        let_fol = 0
        b = 0
        for x, y, z in zip(self.lst[2:-2], self.lst[1:-1], self.lst):
            vgf.print_intervals(b, 50_000,None,len(self.lst))
            b += 1
            if b == 2424752:
                bb = 8

            if b > 2_300_000 or 1:

                if 'ābaetō' in x:
                    p('hey')
                    bb = 8
                if bowtie in lword:
                    bb = 8

                t = y.replace(' ', '')
                xl = x.lower()
                if x and len(x) > 3 and x[-3] == ' ' and xl[-2] == xl[-1] and \
                        not xl[-1].isdigit():
                    lword = self.first_line2(lst5, lword, t, x)
                    lst5 = []
                    lword = ""
                    let_fol = 1

                elif not y and reg(r'^#\s+([0-9]{1,2}|[a-zA-Z]{1})$', x):
                    lst5.append(x)
                ## on one occasion the ? appears in the wrong place
                elif (not y or t == '?') and x[0] == '#' and b not in [1453893]:
                    # if lword and let_fol:
                    #     lword=0
                    #     let_fol=0
                    if lword and lword[0] == '-':
                        self.suffixes[lword] = lst5
                        lword = x[1:].strip()

                    else:
                        if let_fol:
                            lword = ""
                            let_fol = 0
                        else:
                            lword = self.first_line2(lst5, lword, t, x)

                    lst5 = []
                else:
                    lst5.append(x)

        self.word2def[lword] = lst5
        self.word2def_orig[lword] = copy.deepcopy(lst5)

        # for k, v in self.word2def.items():
        #     p(k)

        return

    def elimv(self):
        dct7 = {}
        for k, v in self.word2def.items():
            if k[0] == 'V' and len(k) > 2 and k[1:3] == chr(32) + chr(772):
                g = 'Ū' + k[3:]
                dct7[g] = v
                self.old2new[k] = g
            elif k[0] == 'V':
                g = k.replace('V', 'U')
                dct7[g] = v
                self.old2new[k] = g
            else:
                dct7[k] = v
        self.word2def = dct7

    def elimv2(self, k):
        if k[0] == 'V' and len(k) > 2 and k[1:3] == chr(32) + chr(772):
            g = 'Ū' + k[3:]

        elif k[0] == 'V':
            g = k.replace('V', 'U')
        else:
            g = k
        return g

    def handle_dashes(self):
        lst9 = to.from_txt2lst_tab_delim(f'{fold}dash_words', 1, 1)
        dct12 = {x[0]: x[1] for x in lst9 if not '*' in x[1]}
        typos = {x[0]: x[1][:-1] for x in lst9 if '*' in x[1]}
        self.add_ins('adamos', 'adamās')
        try:
            self.prefixes['Foro-'] = self.word2def['Foro-']
            self.prefixes['endo-'] = self.word2def['endo-']
            self.prefixes['uae-'] = self.word2def['uae-']
            self.word2def['frūdo'] = ['archaic form of # fraudo @']
            self.word2def['adamās ~antis'] = self.word2def['adamās ~antis (-os)']
            del self.word2def['adamās ~antis (-os)']
            del self.word2def['frūd-']
            del self.word2def['Foro-']
            del self.word2def['endo-']
            del self.word2def['uae-']
        except:
            pass

        new = {}
        for k, v in self.word2def.items():
            if k in typos:
                # p (f'typos {k}')
                n = typos[k]
                new[n] = v
                self.old2new[k] = n

            elif k in dct12:
                # p (k)
                s = k[:k.index(',')]
                var = dct12[k]
                self.add_ins(var, s)
                new[s] = self.word2def[k]
                self.old2new[k] = s
            else:
                new[k] = v

        check = {}
        for k, v in new.items():
            if '-' in k:
                if public:
                    pass
                else:
                    assert 0
                    check[k] = v

        self.word2def = new

    def add_ins(self, w, parent):
        wu = unidecode(w)
        ins = old_entry(wu)
        ins.wmacron = w
        ins.variant_of = unidecode(parent)
        self.variants.append(ins)
        return ins

    def handle_etc(self):
        etc = {}
        dct7 = {}
        try:
            self.word2def[f'hērōi{tie}on'] = self.word2def['(hērōion) (trisyllabic)']
            del self.word2def['(hērōion) (trisyllabic)']
        except:
            if not public:
                assert 0
        self.inferred = set()

        for k, v in self.word2def.items():
            if 'etc.' in k:
                etc[k] = v
                ku = k.replace(' etc.', '')
                dct7[ku] = self.word2def[k]
                self.old2new[k] = ku
            elif k[0] == '(':
                ku = re.sub(r'[\s\(\)\?]', '', k)
                dct7[ku] = self.word2def[k]
                self.old2new[k] = ku
                self.inferred.add(ku)
            else:
                dct7[k] = v
        self.word2def = dct7

    def manual_variants(self):
        lst = to.from_txt2lst_tab_delim(f'{fold}manual_variants', 1, 1)
        spacev = to.from_txt2lst_tab_delim(f'{fold}space_variants', 1, 1)
        lst += spacev
        lst1 = to.from_txt2lst_tab_delim(f'{fold}rename_entry', 1, 1)
        lst2 = to.from_txt2lst(f'{fold}to_del', 1, 1)
        for l in lst:
            self.add_ins(l[0], l[1])

        for x in lst1:
            try:
                self.old2new[x[0]] = x[1]
                obj = self.word2def[x[0]]
                self.word2def[x[1]] = obj
                del self.word2def[x[0]]
            except:
                if not public:
                    assert 0

        for x in lst2:
            try:
                del self.word2def[x]
            except:
                if not public:
                    assert 0

    def elim_false_spaces(self):
        spacew = to.from_txt2lst(f'{fold}space_words', 1, 1)
        self.rspacew = set(x for x in spacew if "*" not in x and "#" not in x)
        obj = self.word2def['Aegos flumen, Aegos potamī']
        del self.word2def['Aegos flumen, Aegos potamī']
        self.word2def['Aegos flumen'] = obj
        self.rspacew.add('Aegos flumen')
        self.odd_infl = {}
        for x in spacew:
            try:
                if '*' in x:
                    if x == 'Āfer Afra, Afrum*j':
                        s = 'Āfer'
                    elif not ',' in x:
                        s = x[:x.index(' ')]
                    else:
                        s = x[:x.index(',')]
                    self.old2new[x] = s
                    self.odd_infl[s] = x
                elif '#' in x:
                    y = x[:-1]
                    lst = vgf.strip_n_split(y, ',')

                    for z in lst[1:]:
                        self.add_ins(z, lst[0])

                    obj = self.word2def[y]
                    self.old2new[x] = lst[0]
                    self.word2def[lst[0]] = obj
                    del self.word2def[y]
            except:
                if not public:
                    assert 0



        for x, y in self.odd_infl.items():
            try:
                obj = self.word2def[y[:-2]]
                del self.word2def[y[:-2]]
                self.word2def[x] = obj
            except:
                if not public:
                    assert 0

        err = {}
        for x, y in self.word2def.items():
            if x in self.rspacew:
                pass
            elif ' ' in x and "~" not in x:
                err[x] = y
        return

    def elim_strange_char(self):
        dct = {
            'ü': 'ŭ',
            'ï': 'ĭ',
            'ë': 'ĕ',
            "'": '',
            '?': '',
        }
        st = set()
        b = 0
        done = set()
        while b < 2:
            err = {}
            for x, y in self.word2def.items():
                if x == 'canāle?':
                    bb = 8

                if x in self.rspacew:
                    pass
                elif '~' in x and b == 0:
                    pass
                elif reg(r'[^\,0-9a-zA-ZāēīōūȳĀĒĪŌŪȲ' + tie + ']', x) and x not in done:
                    err[x] = y

            if b == 0:
                self.inflection1()

            for x, y in err.items():
                x1 = x
                for k, v in dct.items():
                    x1 = x1.replace(k, v)

                x1 = both_long_short(x1)
                x1 = remove_hats_diph(x1, 0, 0, 1)
                self.old2new[x] = x1
                self.change_entry(x1, x, y)
                done.add(x1)
            b += 1

        err = {}
        for x, y in self.word2def.items():
            if x in self.rspacew:
                pass
            elif reg(r'[^0-9a-zA-ZāēīōūȳĀĒĪŌŪȲîâêôûÂÊÎÔÛ' + tie + ']', x):
                err[x] = y

        return

    def handle_comma(self):
        # 'haliāetos'2 dashes
        lst = to.from_txt2lst(f'{fold}to_del2')
        for x in lst:
            try:
                del self.word2def[x + ',']
            except:
                p(x)

        lst = to.from_txt2lst_tab_delim(f'{fold}del_raw')
        lst1 = to.from_txt2lst_tab_delim(f'{fold}manual_variants2')
        for x in lst1:
            self.add_ins(x[0], x[1])

        dr = {x[0] + ',': x[1] for x in lst}
        for x, y in dr.items():
            try:
                self.word2def[x] = self.word2def[x][y:]
            except:
                if not public:
                    assert 0

        infl = {}
        var = {}
        non_var = {}
        unfound = {}
        rem = {}
        dash = {}
        dash2 = {}
        to_del = set()
        b = 0
        for x, y in self.word2def.items():
            # for x, y in err.items():
            if 'Baccha' in x:
                bb = 8

            if ',' in x:
                b += 1
                s = ""
                found = 0
                for e, z in en(y):
                    u = re.sub(r'[@\$]', '', z)
                    u = u.strip()
                    if z.strip() == "@":
                        pass
                    elif not ha(z):
                        pass

                    elif '~' in z:
                        s += ' ' + z[1:]
                    elif 'see ' in z:
                        break

                    elif u in self.tpos:
                        break
                    elif '[' in z or not z or 'Also' in z \
                            or old_bottom in z:
                        break
                    else:
                        found = 1
                        t = z[1:].strip()
                        t = t.replace(',', '')
                        x1 = x.replace(',', '')
                        if '-' in z:
                            dash[x1] = z[1:].strip()
                            dash2[x1] = y[e + 1:]
                            self.word2def[x] = y[e + 1:]
                        else:
                            g = z[1:].strip()
                            g = g.replace(',', '')
                            self.add_ins(g, x1)
                            self.word2def[x] = y[e + 1:]
                            var[x1] = y[e + 1:]
                        to_del.add(x)
                        break
                if s:
                    q = x.replace(',', '')
                    self.word2infl[q] = s.strip()
                    infl[q] = s.strip()
                if not found:
                    to_del.add(x)
                    unfound[x] = y
        for x in to_del:
            x1 = x.replace(',', '')
            self.change_entry(x1, x)

        first = 0
        if first:
            lst3 = []
            for x, y in dash.items():
                lst3.append([x, y])
            file = f'{fold}dash_words2'
            to.from_lst2txt_tab_delim(lst3, file)
            vgf.open_txt_file(file)

        return

    def implement_dash(self, kind=0):
        '''
        not some of these variations include only
        a difference in vowel length.  i havent
        coded for that
        '''

        if not kind:
            lst = to.from_txt2lst_tab_delim(f'{fold}dash_words2')
        else:
            lst = to.from_txt2lst_tab_delim(f'{fold}dash_words3')

        for l in lst:
            rep = l[1]
            if kind:
                try:
                    oword = self.word2clas[l[0]].wmacron
                except:
                    if not public:
                        assert 0
            else:
                oword = l[0]

            word, enum = cut_num(oword, 1)

            try:
                m = int(l[2])
            except:
                if kind and len(l) == 3 and l[2] in ['x', '~']:
                    m = 'x'
                else:
                    m = 0

            try:
                n = int(l[3])
            except:
                n = 0

            if m == 'x':
                pass
            else:
                if rep.count('-') == 2:
                    if n:
                        nword = f'{word[:m]}{rep[1:-1]}{word[n:]}'
                    else:
                        nword = f'{word[:m]}{rep[1:-1]}{word[m + len(rep) - 2:]}'

                elif rep[0] == '-':
                    if not m:
                        e = -len(rep) + 1
                    else:
                        e = m
                    nword = f'{word[:e]}{rep[1:]}'
                    beg = word[e:]
                    self.dash_kinds[rep].add(beg)

                else:
                    if not m:
                        b = len(rep) - 1
                    else:
                        b = m

                    nword = f'{rep[:-1]}{word[b:]}'
                    beg = word[:b]
                    self.dash_kinds[rep].add(beg)

                nwordu = unidecode(nword).lower()
                final = f'{nword}{enum}'
                self.add_ins(final, oword)

        # self.analyze_dash_kind()
        return lst




    def build_class(self):
        new2old = {y: x for x, y in self.old2new.items()}
        got = set()
        dct = defaultdict(int)
        self.word2clas = {}
        d = 0
        for x, y in self.word2def.items():
            orig = self.word2def_orig.get(x, [])
            if not orig:
                ol = new2old.get(x)
                if ol:
                    d += 1
                    orig = self.word2def_orig.get(ol)

            xu = unidecode(x)
            ins = old_entry(xu)
            ins.wmacron = x
            ins.raw = y
            ins.oraw = orig
            obj = new2old.get(x)
            if obj:
                ins.parsed_def = obj
                got.add(x)
            dct[xu] += 1
            if xu in self.word2clas:
                self.word2clas[f'{xu}1'] = ins
            else:
                self.word2clas[xu] = ins

        missing = set(new2old.keys()) - got
        for x, y in self.parsed_def.items():
            if x in missing:
                if ' ' in x:
                    g = x[:x.index(' ')]
                    g = g.replace(',', '')
                else:
                    g = x
                g = g.replace('?', '')
                g = unidecode(g)
                ins = self.word2clas[g]
                ins.parsed_def = y

    def inflection1(self):
        self.word2infl = {}
        lst = list(self.word2def.keys())
        for x in lst:
            if x in self.rspacew:
                pass
            elif '~' in x:
                x1 = x[:x.index(' ')]
                infl = x[x.index(' ') + 1:]
                x1 = x1.replace(',', '')
                x1u = unidecode(x1)
                self.old2new[x] = x1u
                self.word2infl[x1u] = infl
                self.change_entry(x1, x)
        return

    def attach_infl(self):
        for k, v in self.word2infl.items():
            ku = unidecode(k)
            self.word2clas[ku].inflection = v

    def last_dash(self):
        lst = self.implement_dash(1)
        for l in lst:
            if len(l) == 3 and l[2] == '~':
                try:
                    obj = self.word2clas[l[0]]
                    for e, z in en(obj.raw):
                        if l[2] in z:
                            obj.raw[e] = z.replace('-', '~')
                except:
                    if not public:
                        assert 0

            elif len(l) == 3 and l[2] == 'x':
                pass
            else:
                try:
                    obj = self.word2clas[l[0]]
                    for e, z in en(obj.raw):
                        if l[1] in z:
                            obj.raw = obj.raw[e + 1:]
                            break
                except:
                    if not public:
                        assert 0
        return



    def handle_inflection2(self):
        minfl = {}
        minflr = {}
        minfl2 = {}
        minfl2r = {}
        dash = {}
        minfl3 = {}
        for x, y in self.word2clas.items():
            found = 0
            isadverb = 0
            if x == 'Bublos':
                bb = 8

            for z in y.raw:
                t = re.sub(r'[@\$]', '', z)
                t = t.strip()
                if 'adv.' in z:
                    isadverb = 1
                elif t in self.tpos:
                    found = 1
                elif 'Also' in t:
                    break
                elif '[' in z:
                    break
                elif old_bottom in z or not z:
                    break
                elif '~' in z:
                    if isadverb:
                        minfl3[x] = y
                    elif not found:
                        minfl[x] = y
                        minflr[x] = y.raw
                    else:
                        minfl2[x] = y
                    break

        if 'absentiuos' in minfl3 or \
                'absentiuos' in minfl or \
                'absentiuos' in minfl2:
            bb = 8

        self.infl_adv(minfl3)
        self.standard_infl(minfl)
        self.filter_adj(minfl2)

        return

    def infl_adv(self, minfl3):
        pre_def = {}
        for k, v in minfl3.items():
            pos2 = ''
            lst2 = []
            for e, z in en(v.raw):
                t = re.sub(r'[@\$]', '', z)
                if '[' in z:
                    break
                elif 'Also' in z:
                    break
                elif old_bottom in z:
                    break
                elif t in self.tpos:
                    pos2 += " " + t
                    pos2 = pos2.strip()
                elif '~' in z:
                    v.inflection = z[1:]
                    v.raw[e] = ""
                else:
                    lst2.append(z)
            pre_def[k] = lst2
            v.raw = v.raw[e:]
            v.pos.append(pos2)
        return

    def standard_infl(self, minfl):
        self.usual_infl = defaultdict(int)
        self.usual_infl['dative'] = 5
        self.usual_infl['ablative'] = 5
        self.scored = []
        self.not_infl = {}
        rem = {}
        research = 0
        c = 0
        while c < 2:
            for k, v in minfl.items():
                to_del = []
                found = 0
                if k == 'Bublos':
                    bb = 8

                for e, z in en(v.raw):
                    z = z.strip()
                    zu = unidecode(z)
                    y = re.sub(r'[@\$#]', '', z)
                    y = y.strip()
                    if not ha(zu):
                        pass
                    elif 'Also' in z or '[' in z:
                        break
                    elif old_bottom in z or not z:
                        break
                    elif any(t in z for t in self.aft_et):
                        break
                    elif y in self.tpos:
                        v.pos.append(y)
                        v.raw[e] = ''
                        found = 1
                    elif '..' in z or reg(r'\d', z):
                        break

                    elif '~' in z:
                        if c == 1:
                            if not research:
                                bool1 = self.stan_infl2(k, y, 1)
                                if bool1:
                                    # p (y)
                                    v.inflection += " " + y
                                    v.inflection = v.inflection.strip()
                                    v.raw[e] = ""
                            else:
                                self.stan_infl2(k, y, 1)

                        else:
                            if found:
                                pass

                            else:
                                pass
                                self.com_infl(y)
                            found = 2
                rem[k] = to_del
            c += 1
        if research:
            self.order_scored(self.scored)
        return

    def stan_infl2(self, k, y, kind=0):
        u = re.sub(r'[\)\(,\.#]', '', y)
        lst = u.split()
        lst1 = []
        for z in lst:
            num = self.usual_infl.get(z, 0)
            if num > 5:
                lst1.append(3)
            elif z[0] == '~':
                lst1.append(3)
            else:
                lst1.append(0)
        sm = sum(lst1)
        score = round(sm / len(lst1), 1)
        exp = ['tundo', 'infero', 'confero']
        if kind:
            if k in exp or score > 1.5:
                return 1
            elif score <= 8:
                return 0
            elif y.count(',') > 1:
                return 1
            else:
                return 0
        else:
            self.scored.append([k, y, score])

    def order_scored(self, scored):
        self.scored = sort_by_col(self.scored, 2)
        dct7 = defaultdict(list)
        for x in self.scored:
            dct7[x[2]].append(x)

        lst5 = [x for x in self.scored if x[2] == .7]
        lst4 = defaultdict(list)
        lst6 = []
        com2 = []
        com = []
        lst7 = []
        half = []
        half_com = []
        for x in self.scored:
            if x[2] == .8:
                if x[1].count(',') > 1:
                    com2.append(x)
                else:
                    com.append(x)
            # elif x[2] == 1.5:
            #     if x[1].count(',') == 0:
            #         half.append(x)
            #     else:
            #         half_com.append(x)

    def com_infl(self, y):
        y = re.sub(r'[\)\(,\.#]', '', y)
        lst = y.split()
        for z in lst:
            self.usual_infl[z] += 1

    def filter_adj(self, minfl2):
        minfl4 = {}
        minfl5 = {}
        for x, y in minfl2.items():
            if x == 'Abantius':
                bb = 8
            found = 0
            for e, z in en(y.raw):
                if reg(r'^#\s+~', z):
                    y.inflection = z[1:].strip()
                    # p (y.inflection)
                    for g in y.raw[:e]:
                        s = re.sub(r'[\$\@#]', '', g).strip()
                        if s in self.tpos:
                            y.pos.append(s)
                        elif ha(g):
                            y.notes += ' ' + g
                            y.notes = y.notes.strip()
                    found = 1
                    y.raw = y.raw[e + 1:]
                    break
                elif 'Also' in z or '[' in z:
                    break
                elif old_bottom in z or not z:
                    break
                elif any(t in z for t in self.aft_et):
                    break
                elif '..' in z or reg(r'\d', z):
                    break

            if not found:
                minfl5[x] = y.raw
        return

    def change_entry(self, x1, x, obj=0):
        if not obj:
            obj = self.word2def[x]
        self.word2def[x1] = obj
        del self.word2def[x]





    def get_prefixes(self):  # 36,3
        '''
        dia-, ēmi, prē
        all prefixes except the three above have 'prefix'
        written in 0 or 1 of their list
        '''

        to_del = set()
        lst4 = ['dia-', 'ēmi-', 'prē-']
        self.prefixes = {}
        for x, y in self.word2def.items():
            if x in lst4:
                self.prefixes[x] = y
                to_del.add(x)
            elif 'prefix' in y[0] or 'prefix' in y[1]:
                self.prefixes[x] = y
                to_del.add(x)

        for x in to_del:
            del self.word2def[x]

    def is_english(self, s):
        s = s.lower()
        lst = s.split()
        u = [x for x in lst if not reg(r'\d', x) and not '.' in x]
        s = ' '.join(u)
        s = re.sub(r'[^a-z\s]', '', s)
        s = s.strip()
        lst3 = ['a ', 'the ', 'of ', 'an ']
        if any(s.startswith(z) for z in lst3):
            return 1
        lst = s.split()
        lst2 = []
        for x in lst:
            lst2.append(self.english2.get(x, 0))
        sm2 = 0
        if len(lst2) > 3:
            sm2 = round(sum(lst2) / len(lst2), 0)

        if sm2 > 70_000_000:
            return 1
        return 0

    def parse_pos(self):
        ad_hoc = ['confuturus', 'medius', 'nȳ', 'ollaner', 'sequō', 'pinnus']
        dct = {}
        only2 = {}
        dword = {}
        pos = defaultdict(list)
        st = set()
        found = 0
        err = {}
        for x, y in self.word2clas.items():
            if x == 'calco':
                bb = 8

            found = 0

            for e, z in en(y.raw[:7]):
                g = re.sub(r'[@\$]', '', z).strip()

                # if 'dub. word' in z:
                #     dword[x] = y
                #     break

                if 'Also' in z:
                    break
                    pass
                elif '[' in z or reg(r'\d', z) or '..' in z:
                    break

                elif old_bottom in z:
                    break
                elif g in self.tpos:
                    y.pos.append(g)
                    found = 1
                    y.raw[e] = y.raw[e].replace(g, '')
            if not found:
                err[x] = y.raw
        return

    def first_line2(self, lst5, lword, t, x, var=0):
        if lword:

            self.word2def[lword] = lst5
            self.word2def_orig[lword] = copy.deepcopy(lst5)
            lword = x[1:].strip()


        else:
            lword = x[1:].strip()
        if lword == 'var. of absinthītēs.':
            bb = 8

        if t == '?':
            lword += '?'

        if lword == 'dōnec':
            bb = 8

        return lword



    def check_bra(self):
        '''
        this function makes sure that everything before
        a bracket has been categorized.
        for those that have not they are placed in the
        err dict


        '''

        p('now checking for errors before the first bracket')
        err = {}  # 119
        err2 = {}  # 854
        headers = {}
        pos_err = {}  # 12
        two_words = {}
        br = {}
        non_lemmas = {}
        wrong_num_brack = {}
        eng_def = ['A ', 'An ', 'The ', 'Of ']
        d = 0
        b = 0
        self.has_brackets = {}
        self.has_brackets2 = {}

        for x, y in self.word2clas.items():
            b += 1
            y.def_start = -1
            vgf.print_intervals(b, 1000)
            if not y.oraw:
                y.oraw = [''] * len(y.raw)
            err1 = 0
            err20 = 0
            for e, z in en(y.raw):
                z = re.sub(r'[@\$\^]', '', z)
                z = z.strip()
                try:
                    f = e + 4
                    u = y.raw[f]
                except:
                    f = len(y.raw)

                if '[' in z:
                    if not z[0] == '[':
                        t = z[:z.index('[')]
                        t = t.replace('dub.', '')
                        if ha(t):
                            if 'two words' in t:
                                two_words = [y.raw[:f], y.oraw]
                            else:
                                br[x] = [y.raw[:f], y.oraw]
                    else:
                        if not z.count('[') == 1 and z.count(']') == 1:
                            wrong_num_brack[x] = y.raw
                        else:
                            self.has_brackets[x] = y
                            self.has_brackets2[x] = z

                    break
                elif old_bottom in z:
                    break
                elif '(dub.)' in z:
                    pass
                elif 'ee quotation' in z:
                    break
                elif any(z.startswith(t) for t in eng_def):
                    d += 1
                    y.def_start = e
                    break
                elif any(f'{t} of' in z for t in self.nlem_mark):
                    non_lemmas[x] = [y.raw[:f], y.oraw]
                    break
                elif z in self.tpos:
                    pos_err[x] = [y.raw[:f], y.oraw]
                    break
                elif any(t in z for t in self.aft_et):
                    headers[x] = [y.raw, y.oraw]
                    break
                elif ha(z):
                    if self.is_english(z):
                        pass
                    else:
                        err[x] = y.raw[:f]
                        err2[x] = y.oraw
                    break
        self.err = sort_dct_key(err)
        self.err2 = sort_dct_key(err2)

        return

    def parse_bra(self):
        '''
        if there is a non_lemma marking without a + sign, then it is a non-lemma


        '''

        greek_etym = {}
        languages = ['Armenian', 'Umbrian', 'Sanskrit', 'Oscan', 'Celtic', 'Old High German',
                     'Old Irish', 'Cornish', 'Middle Irish', 'Old Norse', 'Old Bulgarian',
                     'Irish', 'Old Icelandic', 'Etruscan', 'Welsh', 'Thracian',
                     'Anglo-Saxon', 'Persian', 'Russian', 'Ital.', 'Old Polish',
                     'Engl.', 'Gallic', 'Lithuanian', 'Middle High German', 'Czech',
                     'Gothic', 'Avestan', 'Indo-European']
        hedge = ['probably', 'apparently', 'possibly', 'perhaps']

        lst = [[x, y] for x, y in self.has_brackets.items()]
        # file = f'{sfold}old_brackets'
        # to.from_lst2txt_tab_delim(lst, file)
        # vgf.open_txt_file(file)
        non_lemmas3 = {}
        plus = []
        no_plus = []
        self.parse_plus = {}
        self.success = [0, 0, 0]
        self.lem2participles = pi.open_pickle(f'{fold}lem2participles')
        for k, v in self.has_brackets.items():
            self.lemma = k
            if k == 'blandiloquens':
                bb = 8

            for t in v.raw:
                if '[' in t:
                    z = get_between(t, '[', ']')

                    if z == '[dub.]':
                        pass

                    elif any(t in z or t.capitalize() in z for t in self.nlem_mark) and not '+' in z:
                        # self.non_lemmas[k] = z
                        non_lemmas3[k] = z
                    elif '+' in z:
                        # plus.append([k,z])
                        self.get_parse_plus(k, z)

                    else:
                        no_plus.append([k, z])
                        z = z.strip()
                        zu = z[1:-1]
                        if reg(r'\(cf\..*\)', zu):
                            zu = re.sub(r'\(cf\..*\)', '', zu)
                    break

        self.parse_plus = sort_dct_val_rev(self.parse_plus)
        b = 0  # 390
        for k, v in self.parse_plus.items():
            if v > 5:
                b += 1

        p(b, self.success)  # 103, 411, 32, 3

        file = f'{fold}old_brackets4'
        to.from_lst2txt_tab_delim(plus, file)
        # vgf.open_txt_file(file)

        lst1 = []
        for k, v in non_lemmas3.items():
            lst1.append([k, v])
        file = f'{fold}old_brackets2'
        to.from_lst2txt_tab_delim(lst1, file)
        # vgf.open_txt_file(file)
        return



    def get_parse_plus(self, lemma, z):
        if z[-1] == '+':
            return
        if z[0] == '+':
            z = z[1:]
        oz = z
        z = re.sub(r'[\$\^]', '', z)
        z = unidecode(z)
        z = self.parse_participles(z)

        '''
        ; or ( represents end of division,
        but sometimes () can split a division
        * represents a hypothetical headword
        words between $ and ^ have no entry the others do
        '''
        z = re.sub(r'\(.*?\)', '', z)
        '''
        the following will happen if the only + is between ()
        '''
        if not '+' in z:
            return

        f = z.index('+')
        space1 = 0
        space2 = 0
        lett = 0
        for i in range(f - 1, -1, -1):
            l = z[i]
            if l != ' ':
                lett = 1
            elif not lett and l == ' ':
                pass
            elif lett and l == ' ':
                break
        start = i
        add = 0
        nword = 1
        nplus = 0
        if oz.count('+') > 1:
            bb = 8

        if lemma == 'abhinc':
            bb = 8

        for e, l in en(z[f:]):
            if l == '*':
                pass
            elif l in [';', '(', ',']:
                break

            elif l == '+':
                nplus = 0
                nword = 1
            elif l == ' ':
                if not nword:
                    nplus = 1
            elif nplus:
                break
            else:
                nword = 0

        else:
            add = 1
        stop = e + f + add
        lemu = re.sub(r'[0-9]', '', lemma)
        div = z[start:stop]

        divu = re.sub(r'[\s\-0-9\+\*]', '', div)
        dis = vgf.lvn.distance(lemu, divu)
        self.parse_plus[(lemma, div, divu, oz)] = dis


    def parse_participles(self, z):
        #        lst = [303,201,339]

        dct = {'present participle of': 201, 'participle of': 303, 'gerundive of': 339}
        for x, y in dct.items():
            if x in z:

                idx = z.index(x) + len(x) + 1
                zo = z[idx:]
                try:
                    word = zo[:zo.index(' ')]
                except:
                    word = zo
                word = re.sub(r'[0-9]', '', word)
                lst = self.lem2participles.get(word)
                if lst:
                    self.success[0] += 1
                    if len(lst) > 1:
                        pass

                    dct1 = lst[0]
                    if dct:
                        if y not in dct1:
                            y = 201
                        if 201 not in dct1:
                            self.success[2] += 1
                            return z
                        part = dct1[y]
                        z = z.replace(word, part)
                        z = z.replace(x, '')
                else:
                    self.success[1] += 1
                break
        return z



    def remove_num_word2clas(self):  # 34705, 144
        dct = defaultdict(dict)
        for x, y in self.word2clas.items():
            y.olemma = x
            x, num = cut_num(x,1)
            y.number = num
            if x[0].isupper():
                x = x.lower()
                y.capital = 1
            else:
                y.capital = 0
            y.uiword = x
            dct[x][num] =y
        self.old_wonum = dct
        # diff_macrons = defaultdict(set)
        # for x, y in dct.items():
        #     if len(y) > 1:
        #         for w in y:
        #             if w.capital == 0:
        #                 diff_macrons[x].add(w.wmacron)
        # dct7 = {x: y for x, y in diff_macrons.items() if len(y) > 1}

        # pi.save_pickle(dct7, f'{sfold}old_homonyms', 1)
        return






    def single_def(self):
        '''
        not currently being used but might use in the future

        '''

        # rechere\\\'9, Boa\\f6tes,  \\\f4

        file2 = f'{fold}period2'
        period = to.from_txt2lst(file2, 1)
        period = [x.strip() for x in period if x]
        pdct = {}
        dct4 = {}
        dct3 = {}
        dct = {}
        dct2 = {}
        quotes = {}
        vari = {}
        for x in period:
            l = x.split()
            if '.' in l[0]:
                pdct[l[0]] = l[0].replace('.', '®')
        pdct['e.g.'] = 'e®g®'
        pdct['i.e.'] = 'i®e®'
        pdct['etc.'] = 'etc®'
        pdct['fin.'] = 'fin®'

        for x, y in self.word2clas.items():
            if not y.defs:
                if 'see quotation' in y.pre.lower():
                    quotes[x] = y.pre
                elif ' var. of ' in y.pre:
                    vari[x] = y
                elif ']' in y.pre[:-1]:
                    idx2 = vgf.rindex(y.pre[:-1], ']')
                    dct3[x] = y.pre[idx2 + 1:].strip()
                else:
                    str1 = re.sub(r'[\,;\(\)]]', ' ', y.pre)
                    if str1[-1] == '.':
                        str1 = str1[:-1]

                    lst7 = str1.split()
                    lst7 = [pdct.get(x, x) for x in lst7]
                    str1 = ' '.join(lst7)
                    if "." in str1:
                        idx = vgf.rindex(str1, '.')
                        # str1 = str1.replace('®', '.')
                        dct3[x] = y.pre[idx + 1:].strip()
                    elif "^" in y.pre[:-1]:
                        # idx = vgf.rindex(y.pre[:-1], '^')
                        dct[x] = y.pre
                        # dct[x] = y.pre[idx + 1:]
                    else:
                        dct2[x] = y.pre.strip()

        lst5 = []
        e = 0
        low = {}
        dct9 = {}
        noy = {}
        good = {}
        for x, y in dct3.items():

            obj = self.word2clas[x]
            if not y:
                noy[x] = obj.pre

            elif y.count(')') != y.count('('):
                dct9[x] = obj.pre
                lst5.append([x, obj.pre])

            elif y and reg(r'[A-Z\(=]', y[0]):
                good[x] = y
                pass
            elif y[0].islower():
                lst5.append([x, obj.pre])

                dct9[x] = obj.pre

            if len(lst5) % 100 == 0:
                lst5.append([len(lst5), ""])

        on = 0
        lst6 = []
        for x, y in dct9.items():
            if x == 'Gela':
                on = 1
            elif on:
                idx = 0
                idx1 = 0
                if '^' in y:
                    idx = vgf.rindex(y, '^')
                if '@' in y:
                    idx1 = vgf.rindex(y, '@')

                if idx1 and idx1 > idx:
                    idx = idx1
                if idx:
                    y = add_at_i(idx + 1, y, '\\')
                lst6.append([x, y])

        file = f'{fold}def_check3'
        to.from_lst2txt_tab_delim(lst6, file)
        vgf.open_txt_file(file)





class parse_definition(handle_also):
    def __init__(self):
        handle_also.__init__(self)


    def parse_definition_fu(self):
        '''
        if the word has only one meaning and there are no aft_et phrases between
        the last bracket and old bottom then the definition if the first set
        of words after the closed bracket

        after the first old bottom the next line should be # 1 if there are
            multiple definitions
        if the definition has subsenses then the first sense labeled 'a' can be ignored


        '''
        p ('now numbering definintions')

        self.derrors = defaultdict(dict)
        self.success = [0, 0]
        r = 0
        d = 0
        for x, y in self.word2clas.items():
            if x:
                # if r > 11500:
                #     p(x)
                etym = 0
                ob = 0
                if x == 'immerito':
                    bb = 8
                ae = 0
                r += 1
                self.lemma = x
                # if len(self.derrors['5'])>20:
                #     break
                vgf.print_intervals(r, 500, None, len(self.word2clas))
                self.rlst = y.raw

                for e, z in en(y.raw):
                    if '[' in z and not etym:
                        etym = e + 1
                    elif old_bottom in z and not ob:
                        ob = e + 1
                        break

                    elif any(t in z for t in self.aft_et):
                        dct = {}
                        for g in self.aft_et:
                            if g in z:
                                dct[g] = z.index(g)
                        j = vgf.largest_member(dct)
                        for c, s in en(z):
                            if s == '.':
                                break

                defs = {}
                if not ob:
                    b = etym if etym else 0
                    s = ''
                    for e, z in en(y.raw[b:]):
                        # p (e)
                        if hl(z):
                            s = f'{s} {z} '
                    s = self.clean_str(s)
                    defs['1'] = s
                    y.defs = defs

                else:
                    num = 1
                    num2 = 97
                    num4 = 65
                    state = 'defs'
                    d += 1
                    i = ob
                    s = i
                    while i < len(y.raw):
                        z = y.raw[i]
                        if i == 161:
                            bb = 8
                        zu = z.replace(' ', '')
                        if hl(z):
                            if zu == '?':
                                pass
                            elif zu.startswith(f'{bowtie}22{contradictory}'):
                                state = 'examples'
                            elif state == 'examples':
                                if old_bottom in zu:
                                    state = 'defs'
                                elif zu == f'#{num + 1}' or zu == f'#{num2 + 1}':
                                    n = vgf.err_idx(3, self.rlst[i:])
                                    self.derrors['3'][x] = [i, y.raw[i - 3:i + n], y.raw]
                                    break

                            elif state == 'defs':
                                if f'{bowtie}22' in zu:
                                    n = vgf.err_idx(3, self.rlst[i:])
                                    self.derrors['6'][x] = [i, y.raw[i - 3:i + n], y.raw]
                                    break

                                elif zu == f'#{num}':
                                    num += 1
                                    num2 = 97
                                    num3 = f'{chr(num)}'
                                elif zu == f"#{chr(num4)}":
                                    num3 = f'{chr(num4)}'
                                    num4 += 1
                                elif num2 == 97 and zu == '#b':
                                    num2 = 99
                                    num3 = f'{chr(num)}b'
                                elif num2 == 97 and zu == '#a':
                                    num2 = 98
                                    num3 = f'{chr(num)}a'
                                elif zu == f'#{chr(num2)}':
                                    num2 += 1
                                    num3 = f'{chr(num)}{chr(num2)}'
                                elif zu == f'#{num + 1}':
                                    num2 = 97
                                    num3 = f'{chr(num + 1)}'
                                    n = vgf.err_idx(3, self.rlst[i:])
                                    num += 2
                                    self.derrors['8'][x] = [i, y.raw[i - 3:i + n], y.raw]
                                elif zu == f'#{chr(num2 + 1)}':
                                    num3 = f'{chr(num)}{chr(num2 + 1)}'
                                    num2 += 2
                                    n = vgf.err_idx(3, self.rlst[i:])
                                    self.derrors['9'][x] = [i, y.raw[i - 3:i + n], y.raw]
                                else:
                                    n = vgf.err_idx(3, self.rlst[i:])
                                    self.derrors['5'][x] = [i, y.raw[i - 3:i + n], y.raw]
                                    break
                                i, defn = self.def_line(i)
                                if i == 0:
                                    break
                                defs[num3] = defn
                        i += 1
                        s += 1
                        if s > len(self.rlst) + 50:
                            break
                    if i == len(y.raw):
                        self.success[0] += 1
                        y.defs = defs
                    else:
                        self.success[1] += 1
        rem = len(self.word2clas) - d
        p(f'{d} {rem} {self.success}')
        return

    def clean_str(self, s):
        s = re.sub(r'[@\$\^#]', '', s)
        s = re.sub(r'\s{2,}', ' ', s)
        return s

    def def_line(self, i):
        z = ""
        t = ''
        while z != old_bottom and not self.condition2(z, t) and i < len(self.rlst) + 1:
            if i == len(self.rlst):
                self.derrors['7'][self.lemma] = [i, self.rlst[i - 5:], self.rlst]
                return 0, 0

            t = self.rlst[i]
            if t == old_bottom:
                break
            elif t.startswith(f'{bowtie}22{contradictory}'):
                n = vgf.err_idx(2, lst[i:])
                self.derrors['4'][self.lemma] = [i, self.rlst[i - 3:i + n], y.raw]
                return 0, 0
            else:
                z += f'{t} '
            i += 1
        if self.condition2(z, t):
            i -= 1
        if i > len(self.rlst):
            self.derrors['10'][self.lemma] = [i, self.rlst[i - 6:], y.raw]

        z = z.replace('$', '{')
        z = z.replace('^', '}')
        z = z.replace('@', ' ')
        z = re.sub(r'\s{2,}', ' ', z)
        return i, z

    def condition2(self, z, t):
        if '@   $ ~' in z and not hl(t):
            return 1



class link2lasla(parse_definition):
    def __init__(self):
        parse_definition.__init__(self)

    def begin_ll(self):
        self.get_atts_ll()
        self.add_variants()
        self.rev_participles()
        self.ll_fu()
        self.quick_fix()
        self.use_assimil()
        self.use_col()



    def remove_nums_old(self):
        dct = defaultdict(dict)
        for x, y in self.word2clas.items():
            y.wmacron = cut_num2(y.wmacron)
            y.olemma = x
            x, num = cut_num(x,1)
            if x[0].isupper():
                x = x.lower()
                y.capital = 1
            else:
                y.capital = 0
            dct[x][num] = y
        self.old_wonum = dct




    def add_variants(self):
        # this step was done in feb
        #         lst = [self.new_variants, self.paren_var, self.equal_var, self.dct10,
        #        self.variants7, self.variants, self.singular_variants, self.var_dct]

        all_variants = {}
        self.missing_var = {}
        self.space_word = {}
        self.error = defaultdict(dict)

        for e, obj in en(self.variants):
            if e in [5]:
                for l in obj:
                    ku = l.uiword.lower()
                    l.uiword = ku
                    if ku in self.old_wonum and l.number in self.old_wonum[ku]:
                        self.error['1'+str(e)][ku] = l
                    else:
                        self.old_wonum[ku][l.number] = l
                        all_variants[ku+l.number] = l
                    l.variant_of = l.variant_of.lower()
                    self.var2parent[ku][l.number] = l.variant_of.lower()
                    lu = cut_num(l.variant_of).lower()

                    if lu not in self.old_wonum:
                        self.missing_var[ku] = lu


            elif e in [0,3]:
                for t, itm in obj.items():
                    v = itm[1]
                    k = itm[0]
                    k, num = cut_num(k, 1)
                    if k[0].isupper():
                        cap = 1
                    else:
                        cap = 0
                    ku = k.lower()
                    kuw = norm_str_jv(ku)
                    ins = old_entry(kuw)
                    ins.wmacron = ku
                    ins.capital = cap
                    ins.number = num
                    ins.variant_of = v.uiword
                    v.variant_of = v.variant_of.lower()
                    vu = cut_num(v.variant_of).lower()
                    if vu not in self.old_wonum:
                        self.missing_var[kuw] = vu

                    if kuw in self.old_wonum and num in self.old_wonum[kuw]:
                        self.error['1'+str(e)][k] = v
                    else:
                        self.old_wonum[kuw][num] = ins
                        all_variants[kuw+num] = v
                        self.var2parent[kuw][num] = v.variant_of


            elif e in [4,2,3,6,7]:
                for k, v in obj.items():
                    found = 0
                    if e == 2:
                        v = v[1]



                    if '-' not in k:
                        found = 1
                    elif k.count('-') > 1:
                        self.error['3'+str(e)][k]=v
                    else:
                        l = k.split(' ')
                        left, right = l[0], l[1]
                        leftu, num = cut_num(left, 1)
                        b = len(right) - 1
                        if right[-1] == '-':
                            k = right[:-1] + left[b:]
                            found = 1
                        elif right[0] == '-':
                            k = leftu[:-b] + right[1:]
                            found = 1
                        else:
                            self.error['2'+str(e)][k] = v

                    if found:
                        if e == 6:
                            v.variant_of = v.variant_of.lower()

                        ku,num = cut_num(k,1)
                        if ku[0].isupper():
                            v.capital=1
                        else:
                            v.capital = 0
                        ku = ku.lower()
                        v.wmacron = ku
                        ku = norm_str_jv(ku)
                        if e != 2:
                            v.number = num
                        v.uiword = ku
                        if ' ' in ku:
                            bb=8

                        if ku in self.old_wonum and num in self.old_wonum[ku]:
                            self.error["1" + str(e)][k] = v
                        else:
                            self.old_wonum[ku][num] = v
                            all_variants[ku+num] = v
                            self.var2parent[ku][num] = v.variant_of.lower()

                        vu = cut_num(v.variant_of).lower()
                        if vu not in self.old_wonum:
                            self.missing_var[ku] = vu #10


        return










    def ll_fu(self):  # 1294
        self.missing = {}
        is_part = {}
        for k, v in self.llem2clem.items():
            if k in self.old_wonum:
                pass
            else:
                self.missing[k] = v

    def get_participles(self):
        # participle of, gerundive of, present participle of

        # 303 passive participle
        # 201 activie participle
        # 203 activie oblique
        ## 339 gernundive
        lst = [303, 201, 339]
        lem2participles = defaultdict(list)
        for k, v in lem2forms.items():
            ku = cut_num(k)
            dct = {}
            for x in lst:
                try:
                    obj = v[x]
                    word = obj[0][0]
                    dct[x] = norm_str_jv(word)
                except:
                    pass
            if dct not in lem2participles[ku]:
                lem2participles[ku].append(dct)
            else:
                p('hey')

    def rev_participles(self):
        '''
        this needs fixing, because participles are linked to more
        than one lemma
        '''
        self.lem2part_rev = defaultdict(list)
        for k, v in self.lem2participles.items():
            if k in self.old_wonum:
                for l in v:
                    for y in l.values():
                        if y not in self.old_wonum:
                            ins = old_entry(y)
                            ins.defs = {'1':f'participle of {k}'}
                            self.old_wonum[y] = ins


    def quick_fix(self):
        to_remove = set()
        for k, v in self.missing.items():
            self.quick_fix2(k, to_remove)

        for k in to_remove:
            del self.missing[k]
        p(len(self.missing)) # 925
        return

    def quick_fix2(self, k, to_remove):
        if k.endswith('or') and k[:-1] in self.old_wonum:
            to_remove.add(k)
        elif k.endswith("um") and f'{k[:-1]}s' in self.old_wonum:
            to_remove.add(k)
        elif k.endswith("e") and f'{k[:-1]}is' in self.old_wonum:
            to_remove.add(k)
        elif k.endswith("e") and f'{k[:-1]}us' in self.old_wonum:
            to_remove.add(k)
        elif k.endswith("i") and f'{k[:-1]}us' in self.old_wonum:
            to_remove.add(k)
        elif k.endswith("i") and f'{k[:-1]}is' in self.old_wonum:
            to_remove.add(k)
        elif k.endswith("a") and f'{k[:-1]}um' in self.old_wonum:
            to_remove.add(k)
        elif k.endswith("a") and f'{k[:-1]}us' in self.old_wonum:
            to_remove.add(k)
        elif k.endswith("ae") and f'{k[:-2]}a' in self.old_wonum:
            to_remove.add(k)


    def use_assimil(self):
        '''
        Is in OLD but not my database
        diues, coniux, connexus, praebeo, sponte, iunior
        materies, proprius
        Not in OLD
        nocte, iamdudum (under dudum)
        intelligens in C, intellegens in OLD

        '''

        lst = to.from_txt2lst(f'{fold}assimilations')
        self.asimil = [x for x in lst if x[0] != '!']
        dct = {}
        dct1 = {}
        for x in self.asimil:
            y = x
            y = unidecode(y)
            lst = x.split(':')
            dct[lst[0]] = lst[1]
            lst = y.split(':')
            dct1[lst[0]] = lst[1]
        to_remove = set()
        for x in self.missing.keys():
            for k, v in dct1.items():
                if x.startswith(k):
                    new_word = v + x[len(k):]
                    if new_word in self.old_wonum:
                        to_remove.add(x)
                        break
                    else:
                        self.quick_fix2(new_word,to_remove)
                        break

        for k in to_remove:
            del self.missing[k]



        return

    def use_col(self):
        self.ml_wonum = pi.open_pickle(f'{fold}mac_lemmas_wonum')
        b = 0
        dct = {}
        for k,v in self.ml_wonum.items():
            if k in self.missing:
                s = ''
                c = 0
                for g,h in v.items():
                    t = get_def(h,1,1,1)
                    t = ' '.join(t)
                    s = f"#{c} {s} {t}"
                    b +=1
                    c += 1
                p (f'{k} {s}')
                dct[k] =  s



class bottom_most(link2lasla):
    def __init__(self):
        link2lasla.__init__(self)


    def output(self, kind):
        if not public:
            p ('you went in the output')
            db()
            if kind == 1:
                pi.save_pickle(self.lst, f'{fold}old_lst', 1)
            elif kind == 2:
                pi.save_pickle(self.word2def, f'{fold}old_word2def', 1)
                pi.save_pickle(self.word2def_orig, f'{fold}old_word2def_orig', 1)
            elif kind == 3:
                pi.save_pickle(self.word2clas, f'{fold}word2clas', 1)
                pi.save_pickle(self.variants, f'{fold}variants', 1)
            elif kind == 4:
                pi.save_pickle(self.old_wonum, f'{fold}old_wonum', 1)
            elif kind == 5:
                pi.save_pickle(self.word2clas, f'{fold}old_wdef')
            elif kind == 6:
                pi.save_pickle(self.var2parent, f'{fold}old_var2parent')



    def begin(self,kind =0):
        if kind < 2:
            self.apply_check_def()
            self.check2()
            self.short_cut(6)
            self.short_cut(7)
            self.main()
            self.elim_heading()
            self.output(1)
        if kind < 3:
            if kind > 1:
                self.short_cut(1)
            self.ad_hoc_adj()
            self.first_line()
            self.output(2)

        if kind < 4:
            if kind > 2:
                self.short_cut(2)
            self.get_prefixes()
            self.elimv()
            self.handle_dashes()
            self.handle_etc()
            self.manual_variants()
            self.elim_false_spaces()
            self.elim_strange_char()
            self.handle_comma()
            self.implement_dash()
            self.build_class() ## put in interval loop
            self.isolate_bracket()
            self.attach_infl()
            self.last_dash()
            self.handle_inflection2() ## put in interval loop
            self.output(3)

        if kind < 5:
            if kind > 3:
                self.short_cut(5)
                self.short_cut(3)
            self.begin_pv()
            self.parse_pos()
            self.begin_ha()
            self.parse_pos()
            self.begin_ad()
            self.remove_num_word2clas()
            self.output(4)

        if kind < 6:
            if kind > 4:
                self.short_cut(6)
                self.short_cut(5)
                self.short_cut(4)
            self.parse_definition_fu()
            self.output(5)

        if kind < 7:
            self.begin_ll()
            self.output(6)

        if kind < 8:
            self.check_bra()

        if kind < 9:
            if kind > 7:
                self.short_cut(8)
            self.parse_bra()
        return






if eval(not_execute_on_import):
    if vgf.pycharm():
        args = [0, '0', '', 'IX', '', 0, 0]
    else:
        args = vgf.get_arguments()

    if args[1] == 'ma':
        ins = scrape_old()
        ins.main()
    else:
        ins = bottom_most()
        num = 0 if not args[1] else int(args[1])
        ins.begin(num)

