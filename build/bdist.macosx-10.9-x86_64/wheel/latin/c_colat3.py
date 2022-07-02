from bglobals import *




# authors = ['LS', 'GG', 'GJ', 'Ge', 'FG', 'Lw', 'YO', 'PO', 'WW']


class colatinus():
    def __init__(self):
        '''
        this class uses the definitions of the online latin dictionary
        and combines them with the definitions of collatinus and
        prints all properties of each word to an excel spread sheet

        '''

    def begin(self):
        self.get_atts()
        self.corrupting_alternates()
        self.ad_hoc()
        self.simplify_models()
        self.new_mod_names()
        self.use_wrong_model()
        self.get_pos()
        self.get_short_defs()
        self.get_gender()
        self.get_word2defs()
        pi.save_pickle(self.co_lemmas2, f'{fold}co_lemmas3')
        return




    def get_atts(self):
        p ('opening pickles')
        self.co_lemmas2 = pi.open_pickle(f'{fold}co_lemmas2')
        self.col_dct = pi.open_pickle(f'{fold}col_dct')
        self.mmodels = pi.open_pickle(f'{fold}mmodels')
        self.lem_freq_rank = pi.open_pickle(f'{fold}lem_freq_rank')


    def corrupting_alternates(self):
        '''
        the following eliminates geninf and perf roots which derive from a variant
        spelling
        '''
        file = f'{fold}bogus_alt'
        lst5 = to.from_txt2lst(file)
        for x in lst5:
            if x.startswith('__'):
                lemma = x[2:]
                obj = self.co_lemmas2[lemma]
            if "*" in x:
                if x.startswith('g:'):
                    orig = obj['geninfmjv']
                else:
                    orig = obj['perfmjv']

                s = x[2:]
                l = s.split(',')
                m = [z for z in l if '*' not in z]
                mu = ','.join(m)
                # p (orig, mu)

                if x.startswith('g:'):
                    obj['geninfmjv'] = mu
                else:
                    obj['perfmjv'] = mu

        return




    def new_mod_names(self):
        file = f'{fold}modeles4'
        lst = to.from_txt2lst(file)
        self.omod2newmod = {}
        for x, y in zip(lst[:-1], lst[1:]):
            if x.startswith('modele:') and y.startswith('!;'):
                nmod = x[7:].strip()
                omod = y[2:].strip()
                self.omod2newmod[omod] = nmod
        pi.save_pickle(self.omod2newmod, f'{fold}omod2nmod')
        for k, v in self.co_lemmas2.items():
            v['model'] = self.omod2newmod.get(v['model'], v['model'])


    def use_wrong_model(self):
        file = f'{fold}wrong_model'
        file2 = f'{fold}wrong_model2'
        lst = to.from_txt2lst_tab_delim(file, 1, 1)
        lst1 = to.from_txt2lst_tab_delim(file2, 1, 1)

        for x in lst:
            xu = norm_str_jv(x[0])
            obj = self.co_lemmas2[xu]
            obj['model'] = x[1]
        for x in lst1:
            if x[0][0] != '/':
                xu = norm_str_jv(x[0])
                obj = self.co_lemmas2[xu]
                obj['model'] = 'sono'
        return

    def get_pos(self):
        '''
        the pos should be obtained in the w_convert_models
        do this later
        '''

        dct = {}
        research = 0
        if research:
            for e, x in en(list(self.mmodels.keys())):
                p(e, x)
        e = 0
        for k, v in self.mmodels.items():
            dct[e] = k
            if e == 0:
                v['pos'] = 'o'
            elif e < 58:
                v['pos'] = 'n'
            elif e < 83:
                v['pos'] = 'a'
            elif e < 107:
                v['pos'] = 'p'
            elif e < 136:
                v['pos'] = 'v'
            else:
                v['pos'] = 'd'
            x = self.mmodels[k]
            x['pos'] = v['pos']
            self.mmodels[k] = x
            e += 1

        st = set()
        for k, v in self.co_lemmas2.items():
            try:
                v['pos'] = self.mmodels[v['model']]['pos']
            except:
                st.add(v['model'])

        return



    def purge_chinese(self):
        nums = {
            5: 6,
            2: 4,
            1: 6,
            0: 6,
        }
        for k, v in self.col_dct.items():
            for aut, num in nums.items():
                try:
                    str1 = v[aut][num]
                    if any(w for w in str1 if ord(w) == 65279):
                        pass

                    elif any(w for w in str1 if ord(w) > 10000):
                        v[aut][num] = ''

                except:
                    pass

        return



    def get_short_defs(self):
        '''
        169 words are found in the short defs which
        do not have a lemma but most are heteronyms
        '''

        lst = to.from_txt2lst(f'{fold}lemmes_en_mean')
        self.lemmes_en_mean = {}
        wrong = []
        miss2 = {}

        for x in lst:
            if x and x[0] != '!':
                if x.count(':') == 1:
                    y = x.split(":")
                    key = y[0]
                    key = norm_str_jv(key)
                    # itm = self.by_class.get(key)
                    itm = self.co_lemmas2.get(key)
                    if itm:
                        itm['def_co'] = y[1]

                else:
                    wrong.append(x)
        miss2 = vgf.sort_dct_val(miss2)
        return

    def ad_hoc(self):
        file = f"{fold}bad_macrons"
        dct4 = to.from_txt2dct_1d(file)
        for k, v in dct4.items():
            self.co_lemmas2[k]['macronjv'] = v

        del self.co_lemmas2['cn']
        dct = {
            'nereides': 'nereid',
            'aether2': 'aetheris',
            'philochares2': 'philocharetis',
            'sanguinans': 'sangụinant'
        }
        for k, v in dct.items():
            obj = self.co_lemmas2[k]
            obj['geninfmjv'] = v
        self.co_lemmas2['concustodio']['perfmjv'] = 'concustōdi'



    def simplify_models(self):
        lst = ['lexicon', 'syl', 'spell', 'jv', 'macronjv',
               'perfm', 'geninfm', 'macron', 'geninfmjv', 'perfmjv',
               'operf', 'ogeninf']

        for k, v in self.co_lemmas2.items():
            v['def_co'] = ''
            if 'perfmjv' in v:
                v['perf'] = v['perfmjv']
            if 'geninfmjv' in v:
                v['geninf'] = v['geninfmjv']

            del v['quantity']
            v['lemma'] = v['macronjv']
            # if v['lemma'][-1].isdigit():
            #     p (v['lemma'])
            #     v['lemma'] = v['lemma'][:-1]

            for x in lst:
                if x in v:
                    del v[x]


        return




    def get_gender(self):
        dct = {
            0: 4,
            1: 4,
            2: 3,
            3: 3,
            5: 4,
            6: 6
        }
        errors = defaultdict(dict)
        col_errors = {}
        b = 0
        c = 0
        d = 0
        f = 0
        p (f'now getting the gender of the nouns')
        self.co_lemmas2['bos']['model']='miles'
        self.co_lemmas2['bos']['pos']='n'
        for k, v in self.co_lemmas2.items():
            b += 1
            vgf.print_intervals(b, 1000, None, len(self.co_lemmas2))
            if v['pos'] == 'n':
                itm = self.col_dct.get(k)
                if not itm:
                    col_errors[k]=v
                else:
                    st = set()
                    if k == 'labellum':
                        bb = 8
                    lst = []
                    for x, y in dct.items():
                        found = 1
                        try:
                            s = itm[x][y]
                        except:
                            found = 0
                        if found:
                            ostr = s
                            if hl(s):
                                found = 0
                                for g in ['m', 'n', 'f']:
                                    g1 = f' {g} '
                                    g2 = f' {g}.'
                                    g3 = f'{g}.'
                                    if g1 in s or g2 in s \
                                            or g3 == s:
                                        found = 1
                                        if not st or g not in st:
                                            lst.append(g)
                                        st.add(g)
                                        lst.append(g)

                                if not found:
                                    errors[k][x] = ostr
                                else:
                                    c += 1

                    if st:
                        lst5 = list(st)
                        lst5.sort()
                        v['gender'] = ''.join(lst5)
                        f += 1
                    else:
                        d += 1

        return


    def get_word2defs(self):
        nums = {
            5: 6,
            0: 6,
            2: 4,
            1: 6,
            3: 4,
        }
        self.no_def = set()
        errors = defaultdict(dict)
        for k, cl in self.co_lemmas2.items():
            v = self.col_dct[k]
            found = 1 if cl['def_co'] else 0
            for aut, num in nums.items():
                auth = authors[aut]
                s = f'def_{auth.lower()}'
                cl[s] = ""

            for aut, num in nums.items():
                if aut in [1, 3] and found:
                    pass
                else:
                    try:
                        if len(v[aut]) > num:
                            defn = v[aut][num]
                            if defn:
                                if not ord(defn[0]) > 30_000:
                                    auth = authors[aut]
                                    found = 1
                                    s = f'def_{auth.lower()}'
                                    cl[s] = defn
                    except:
                        errors[k][aut] = self.col_dct[k][num]
            if not found:
                self.no_def.add(k)

        dct7 = {}
        for k in self.no_def:
            j = cut_num(k)
            rank = self.lem_freq_rank.get(j, 99_999)
            dct7[k] = rank
        dct7 = sort_dct_val(dct7)

        return





if eval(not_execute_on_import):
    if vgf.pycharm():
        args = [0, '', '', 'IX', '', 0, 0]
    else:
        args = vgf.get_arguments()

    ins = colatinus()
    ins.begin()


