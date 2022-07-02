import copy
from bglobals import *
if not public:
    from i_scrape_old import old_entry
from j_lasla2 import match_colwlas, bottom_most_la
from c_colat4 import bottom_most_a4


class forms:
    def __init__(self, dct, word):
        for k, v in dct.items():
            setattr(self, k, dct[k])
        self.word = word

    def __repr__(self):
        return self.word


class DefaultDict(dict):
    def __missing__(self, name):
        rval = type(self)()
        self.__setitem__(name, rval)
        return rval


class alt_cls:
    def __init__(self, lemma, parent, oblique):
        self.lemma = lemma
        self.parent = parent
        self.oblique = oblique

    def __repr__(self):
        return self.lemma


class topmost():
    def __init__(self):
        pass

    def get_atts(self, kind=''):
        self.excel = 0
        # self.mod2word = pi.open_pickle(f'{fold}mod2word')
        self.co_lemmas4 = pi.open_pickle(f'{fold}co_lemmas4', 1)
        self.mod2word = defaultdict(list)
        for x, y in self.co_lemmas4.items():
            self.mod2word[y['model']].append(x)
        # self.mlem_num = pi.open_pickle(f'{sfold}mlem_num_ab', 1)
        self.las_freq = pi.open_pickle(f'{fold}las_freq2', 1)
        # self.old_wonum = pi.open_pickle(f'{sfold}old_wonum', 1)
        # self.old_homonyms = pi.open_pickle(f'{sfold}old_homonyms', 1)
        self.ui_models = pi.open_pickle(f'{fold}ui_models')
        self.lem2forms = pi.open_pickle(f'{fold}lem2forms_mem')
        self.llem2clem = pi.open_pickle(f'{fold}llem2clem')
        self.lemma2decl = pi.open_pickle(f'{fold}lemma2decl', 1)
        self.lasla_dct = pi.open_pickle(f'{fold}lasla_dct')
        self.final_pos = pi.open_pickle(f'{fold}final_pos', 1)
        self.las_lem_freq = pi.open_pickle(f'{fold}las_lem_freq')
        self.final_pos_rev = {v: k for k, v in self.final_pos.items()}
        self.mc_ins = match_colwlas()
        self.prop_dct = {}
        self.irregs = pi.open_pickle(f'{fold}irregs_parsed')
        self.law_dct2 = {}
        self.bad_words = pi.open_pickle(f'{fold}ill_formed_words', 1)
        dct = to.from_txt2dct_1d(f"{fold}mispellings_rev")
        self.misspell = {k: v.replace('*', '') for k, v in dct.items() if "*" in v}
        lst = pi.open_pickle(f'{fold}lalems2forms')
        self.lalems2forms = lst[0]
        self.lalems2forms_prop = lst[1]
        self.stem_change = {}
        self.declensions = defaultdict(list)
        self.las_freq3 = defaultdict(int)
        self.las_freq_wnum = defaultdict(int)
        self.las_freq_ab = {}
        self.shared = {}
        self.redund_prop = {}
        self.lalems2forms2 = defaultdict(dict)
        self.lalems2forms3 = defaultdict(dict)
        self.lalems2forms_wprop = defaultdict(dict)
        if kind == 'start':
            self.co_lem_wonum = defaultdict(dict)
            self.las_freq3 = defaultdict(int)
            self.las_freq_wopos = defaultdict(int)
        else:
            self.co_lem_wonum = pi.open_pickle(f'{fold}mac_lemmas_wonum')
            self.las_freq3 = pi.open_pickle(f'{fold}las_freq3')
            self.las_freq_wopos = pi.open_pickle(f'{fold}las_freq_wopos')

        return

    def get_atts_third(self):
        self.lemm2ostem = defaultdict(set)
        self.lemm2ostem2 = {}
        self.lemm2nstem = defaultdict(set)
        self.word2prop_third = {}
        self.third_anomalies = defaultdict(list)
        self.pas_type = {}

    def output(self, kind, obj, file):
        if kind == 1:
            to.from_lst2txt_tab_delim(obj, file)

    def get_ddct(self):
        dct1 = {
            'sv': 'a',
            'sa': 'am',
            'sd': 'ae',
            'sg': ['ae', 'ai'],
            'sb': 'a',
            'pn': 'ae',
            'pv': 'ae',
            'pa': 'as',
            'pg': 'arum',
            'pd': 'is',
            'pb': 'is',
            'sl': 'ae',
            'pl': 'ae',
        }

        dct2 = {
            'sn': 'us',
            'sv': 'e',
            'sa': 'um',
            'sd': 'o',
            'sg': 'i',
            'sb': 'o',
            'pn': 'i',
            'pv': 'i',
            'pa': 'os',
            'pg': 'orum',
            'pd': 'is',
            'pb': 'is',
            'sl': 'i',
            'pl': 'is',
        }

        dct2i = copy.deepcopy(dct2)
        dct2i['sv'] = 'i'
        dct2om = copy.deepcopy(dct2)
        dct2om['sa'] = ['om', 'um']
        dct2q = copy.deepcopy(dct2)
        dct2q['sv'] = ['e', 'r']
        dct2r = copy.deepcopy(dct2)
        dct2r['sv'] = ['e', 'r']

        dct2n = {
            'sn': 'um',
            'sv': 'um',
            'sa': 'um',
            'sd': 'o',
            'sg': 'i',
            'sb': 'o',
            'pn': 'a',
            'pv': 'a',
            'pa': 'a',
            'pg': 'orum',
            'pd': 'is',
            'pb': 'is',
            'sl': 'i',
            'pl': 'is',
        }
        dct2on = copy.deepcopy(dct2n)
        dct2on['sa'] = ['om', 'um']

        dct4 = {
            'sn': 'us',
            'sv': 'us',
            'sa': 'um',
            'sd': 'ui',
            'sg': 'us',
            'sb': 'u',
            'pn': 'us',
            'pv': 'us',
            'pa': 'us',
            'pg': 'uum',
            'pd': 'ibus',
            'pb': 'ibus',
            'sl': 'ui',
            'pl': 'ui',
        }

        dct5 = {
            'sn': 'es',
            'sv': 'es',
            'sa': 'em',
            'sd': 'ei',
            'sg': 'ei',
            'sb': 'e',
            'pn': 'es',
            'pv': 'es',
            'pa': 'es',
            'pg': 'erum',
            'pd': 'ebus',
            'pb': 'ebus',
            'sl': 'es',
            'pl': 'es',
        }
        self.ddct = {
            '1': dct1,
            '2': dct2,
            '2n': dct2n,
            '2i': dct2i,
            '2om': dct2om,
            '2on': dct2on,
            '4': dct4,
            '5': dct5,
        }


class pickled(topmost):
    def __init__(self):
        topmost.__init__(self)

    def wo_num(self):
        for k, v in self.co_lemmas4.items():
            ku, num = cut_num(k, 1)
            self.co_lem_wonum[ku][num] = v
        pi.save_pickle(self.co_lem_wonum, f'{fold}co_lem_wonum')

    def get_las_freq3(self):
        '''
        las_freq3 has no lemma index numbers and no capital letters
        the keys of las_freq is a tuple whose indexes are
            0=lemma without capital letters
            1=word with capital letters (but probably a bad idea)
            2=pos
        '''

        for x, y in self.las_freq.items():
            word = x[0]
            try:
                wo_num = cut_num2(word)
                self.las_freq3[wo_num] += y
                self.las_freq_wnum[word] += y
                self.las_freq_wopos[(x[0].lower(), x[1])] += y
            except IndexError:
                pass

        self.las_freq3 = sort_dct_val_rev(self.las_freq3)
        pi.save_pickle(self.las_freq3, f'{fold}las_freq3')
        pi.save_pickle(self.las_freq_wopos, f'{fold}las_freq_wopos')


class tests(pickled):
    def __init__(self):
        pickled.__init__(self)

    def begin(self):
        pass

    def a_end(self):
        self.totest = defaultdict(dict)
        self.by_ending = defaultdict(dict)
        self.ending = 'a'
        self.declensions['3'] = self.lthird
        self.ignore_proper = 1
        self.tot_words = set()
        self.lemma2word = {}
        self.tot_pairs = defaultdict(int)
        for x, y in self.declensions.items():
            if x in ['1', '2', '3', '4', '5']:
                self.decl = x
                for z in y:
                    self.lem = z
                    z = z.lower()
                    zu, num = cut_num(z, 1)
                    try:
                        self.obj = self.lalems2forms2[zu][num]
                        self.small_loop()
                    except KeyError:
                        pass
        return

    def small_loop(self):
        for pos, dct in self.obj.items():
            self.pos = pos
            for self.word, freq in dct.items():
                if self.word.endswith(self.ending) and self.conditions():
                    tpl1 = (self.word, self.lem)
                    tpl2 = (self.decl, pos)
                    if self.decl in ['1', '2', '3']:
                        self.more_research()
                    if freq > 0:
                        self.totest[tpl2][tpl1] = freq
                        self.tot_pairs[(self.lem.lower(), self.word, self.decl)] += freq
                        self.lemma2word[self.lem.lower()] = self.word
        return

    def more_research(self):
        try:
            end4 = self.word[-4:]
        except:
            end4 = ''

        try:
            end3 = self.word[-3:]
        except:
            end3 = ''
        if self.lem.endswith('9') and self.ignore_proper:
            return

        if end4:
            self.by_ending[end4].setdefault(self.decl, set()).add(self.lem)
        if end3:
            self.by_ending[end3].setdefault(self.decl, set()).add(self.lem)
        self.tot_words.add(self.lem)

    def a_end_research(self):
        to_del = set()
        for x, y in self.by_ending.items():
            if len(x) == 3 and len(y) == 1:
                for k, v in self.by_ending.items():
                    if k.endswith(x) and len(k) == 4:
                        to_del.add(k)
        for x in to_del:
            del self.by_ending[x]

        dct = {}
        for x, y in self.by_ending.items():
            if len(y) == 1:
                key = vgf.dct_idx(y)
                val = vgf.dct_idx(y, 0, 'v')
                dct[(x, key)] = len(val)
        laws = sort_dct_val_rev(dct)
        dct2 = {}
        for x, y in self.by_ending.items():
            for k, v in y.items():
                dct2[(x, k)] = len(v)
        tend = sort_dct_val_rev(dct2)

        dct3 = {}
        dct5 = {}
        for k, v in tend.items():
            if v > 10:
                obj = self.by_ending[k[0]]
                dct3[k[0]] = obj
                tot = 0
                for s, t in obj.items():
                    tot += len(t)
                dct6 = {}
                for s, t in obj.items():
                    dct6[s] = int((len(t) / tot) * 100)
                dct5[k[0]] = dct6

        dct5o = {}
        for k, v in dct5.items():
            num = max([z for z in v.values()])
            if num > 59:
                dct5o[k] = num
        dct5 = vgf.sort_dct_by_dct(dct5, dct5o)
        dct3 = vgf.sort_dct_by_dct(dct3, dct5o)
        dct3 = self.remove_subset(dct3)
        dct5 = self.remove_subset(dct5)
        self.tot_words2 = copy.deepcopy(self.tot_words)
        before = len(self.tot_words2)
        self.tendencies = defaultdict(dict)
        self.make_lists(dct3, dct5)
        self.add_lawless()
        self.print_tendencies()
        p(f'{before - len(self.tot_words2)} obey tendencies {len(self.tot_words2)} do not')
        file = f'{fold}aending'
        if self.excel:
            ef.from_lst2book(self.final_lst, file)

        return

    def print_tendencies(self):
        lst = []
        for x, y in self.tendencies.items():
            for g, h in y.items():
                s = ''
                for k, v in h.items():
                    s += f" {k} {v}%"
                lst.append([x, g, s])
        file = f'{fold}tendencies'
        if self.excel:
            ef.from_lst2book(lst, file)

    def remove_subset(self, dct_word):
        to_del = set()
        for x in dct_word.keys():
            if len(x) == 3:
                for z in dct_word.keys():
                    if z.endswith(x) and z != x:
                        to_del.add(x)
        for x in to_del:
            del dct_word[x]
        return dct_word

    def add_lawless(self):
        dfreq = defaultdict(int)
        for k, v in self.tot_pairs.items():
            word = k[1]
            if word in self.tot_words2:
                dfreq[k[2]] += 1
                defn = self.lasla_dct.get(k[0])
                lst = [word, k[0], v, 'i', k[2], 'i', defn]
                self.final_lst.append(lst)
        self.tendencies['i']['i'] = vgf.from_dct_sum2perc(dfreq)
        return

    def make_lists(self, dct3, dct5):
        lst = []
        tdct = {}
        for k, v in self.tot_pairs.items():
            defn = self.lasla_dct.get(k[0])
            tdct[(k[1], k[2])] = [k[0], v, defn]
        word2lemma = defaultdict(set)
        st5 = set()

        for k, v in self.tot_pairs.items():
            word2lemma[k[1]].add(k[0])
            if len(word2lemma[k[1]]) > 1:
                st5.add(k[1])

        for k, v in dct3.items():
            dct = {x: len(y) for x, y in v.items()}
            v = vgf.sort_dct_by_dct(v, dct)
            b = 0
            for x, y in v.items():
                if not b:
                    self.tendencies[x][k] = dct5[k]
                    lst2 = self.make_lists2(k, x, y, 'r')
                    lst += lst2
                else:
                    lst2 = self.make_lists2(k, x, y, 'e')
                    lst += lst2

                b += 1
        self.final_lst = lst

    def make_lists2(self, k, x, y, kind):
        lst2 = []
        for z in y:
            defn = self.lasla_dct.get(z.lower(), '')
            word = self.lemma2word[z.lower()]
            freq = self.las_freq_wopos[(z.lower(), word)]
            zu = [word, z, freq, kind, x, k, defn]
            lst2.append(zu)
            if z in self.tot_words2:
                self.tot_words2.remove(z)
        lst2 = sort_by_col_rev(lst2, 2)
        return lst2

    def conditions(self):
        if self.ending == 'a':
            if self.pos in ['sv', 'pv', 'inv']:
                return 0
            if len(self.pos) > 2:
                return 0
            if self.decl in ['4', '5']:
                return 0
        return 1


class reg_decl(tests):
    def __init__(self):
        tests.__init__(self)

    def main_loop2(self):  # 2630
        self.errors2 = {}
        self.errors3 = defaultdict(list)
        keyerrors = []
        for k, v in self.declensions.items():
            for word in v:
                self.lem, self.num = cut_num(word, 1)
                self.dec = k
                self.lem = self.lem.lower()
                if self.lem == 'uulgus':
                    bb = 8

                if self.lem + self.num not in self.redund_prop:
                    try:
                        self.obj = self.lalems2forms3[self.lem][self.num]
                        self.get_dec_num()
                        self.research()
                        self.tdct = self.ddct.get(self.tdec)
                        if self.tdct:
                            self.verify()
                    except KeyError:
                        keyerrors.append(self.lem + self.num)

        return

    def det_pos3(self, lst):
        dct = defaultdict(int)
        for k in lst:
            pos = k[1]
            pos2 = self.mc_ins.det_pos(pos)
            dct[pos2] += k[2]

        dct = sort_dct_val_rev(dct)
        return vgf.dct_idx(dct)

    def ui_ends(self):
        dct4 = {}
        for k, v in self.ui_models.items():
            dct = {}
            if 'sim' not in v:
                dct4[k] = v
            else:
                for x, y in v['sim'].items():
                    lst = []
                    for z in y:
                        lst.append(z[2])
                    dct[x] = lst
                v['sim_ends'] = dct
                self.ui_models[k] = v

    def new_reg_decl(self, pos2t, pos2n):
        dct1 = {
            'sg': ['ae', 'ai'],
            'sa': ['im', 'em'],
            'sd': ['i'],
            'sb': ['e', 'i'],
            'pn': ['es', 'is', 'ia', 'a'],
            'pa': ['es', 'is', 'ia', 'a'],
            'pg': ['ium', 'um'],
            'pb': ['ibus'],
            'pd': ['ibus'],
        }
        dct2 = defaultdict(list)
        for x, endings in dct1.items():
            obj = pos2t.get(x)
            if obj:
                found = 0

                for end in endings:
                    done = 0
                    if done:
                        break
                    for word in obj:
                        if word.endswith(end):
                            if end == 'i' and word.endswith('ei'):
                                pass
                            elif end == 'um' and word.endswith('ium'):
                                pass
                            else:
                                found = 1
                                stem = word[:-len(end)]
                                if self.lemma + self.num not in self.word2stems:
                                    self.word2stems[self.lemma + self.num] = defaultdict(int)
                                self.word2stems[self.lemma + self.num][stem] += pos2n[x][word]
                                if end not in dct2[x]:
                                    dct2[x].append(end)
                                if end == 'ia':
                                    done = 1
                            break
                    if done:
                        break
                if not found:
                    if x == 'sa':
                        sa = pos2t.get('sa')
                        ns = pos2t.get('sn')
                        if sa and ns:
                            if self.same_end(sa, ns):
                                dct2['sa'].append('x')
                            else:
                                self.third_anomalies['sa'].append((obj, self.lemma))

                    else:
                        self.third_anomalies[x].append((obj, self.lemma))

        self.word2decl[self.lemma + self.num] = dct2
        self.third_prop_new(dct2)

    def verify(self):
        for pos, lst in self.obj.items():
            if pos not in ['sn', 'inv']:
                target = self.tdct[pos]
                if type(target) == str:
                    target = [target]

                if all(not x.endswith(z) for x in lst for z in target):
                    obj2 = self.lalems2forms2[self.lem][self.num]
                    for x in lst:
                        if x.endswith('.') or x.endswith("'") or \
                                x.endswith('st'):
                            pass

                        else:
                            if all(not x.endswith(z) for z in target):
                                freq = obj2[pos][x]
                                if self.lem + self.num == 'respublica' and pos == 'sb':
                                    bb = 8

                                self.errors2[(self.lem + self.num, pos, x, self.tdec)] = freq

    def get_dec_num(self):
        if len(self.lem) > 3 and self.lem[-3:-1] == 'uu' and self.dec == '2':
            self.tdec = '2o'
            return

        if self.lem.endswith('um') and self.dec == '2':
            self.tdec = '2n'
            return
        if self.lem.endswith('ius') and self.dec == '2':
            self.tdec = '2i'
            return

        if self.lem.endswith('a') and self.dec == '2':
            if all(k[0] == 'p' for k in self.obj.keys()):
                self.tdec = '2n'
                return

        if self.lem.endswith('er'):
            stem = self.obj['sn']
            if len(stem) > 1:
                self.errors3['erm'].append(self.obj)
                return
            else:
                stem = stem[0]
                new_end = stem[-3] + stem[-1]
                tdct = self.ddct['2']
                change = 0
                found = 0
                for k, v in self.obj.items():
                    if k not in ['sn', 'sv']:
                        end = tdct[k]
                        word = v[0]
                        new_end2 = f'{new_end}{end}'
                        if word.endswith(new_end2):
                            if change == -1:
                                found = 1
                            change = 1
                        else:
                            if change == 1:
                                found = 1
                            change = -1
                if not found:
                    if change == -1:
                        self.tdec = '2r'
                    else:
                        self.tdec = '2q'
                else:
                    dct = self.lalems2forms2[self.lem][self.num]
                    self.errors3['rc'].append(dct)

            return

        self.tdec = self.dec

    def del_models(self):
        dct = {}
        on = 0
        self.bad_models = set()
        for x, y in self.ui_models.items():
            if x == 'miles':
                on = 1
            elif x == 'manus':
                on = 0
            if not on:
                dct[x] = y
            else:
                self.bad_models.add(x)
        self.ui_models = dct
        return

    def get_irregs_ui(self):
        '''
        the * means that the lemma pos only has that form
        we have ignored this for now

        '''

        self.irreg_excp = {}
        skip = ['sum', 'deus', 'meus']
        for k, v in self.irregs.items():
            if k not in skip:
                for x, y in v.items():
                    pos2 = self.final_pos.get(x)
                    word = norm_str_jv(y)
                    word = word.replace('*', '')
                    self.irreg_excp[(k, pos2)] = word

    def main_loop_fd(self):
        self.get_irregs_ui()
        self.get_las_w2l()
        # self.ui_ends()
        self.errors4 = defaultdict(dict)
        self.bad_words = set()
        self.tot_pos = defaultdict(dict)
        for k, v in self.lalems2forms2.items():
            for lnum, dct in v.items():
                self.lemma = k + lnum
                if k + lnum not in self.lthird:
                    cnum = self.llem2clem.get(k)
                    if cnum:
                        cnum = cnum.get(lnum)
                        if cnum != None:
                            clem = k + cnum
                            clem_dct = self.co_lemmas4.get(clem)
                            mod = clem_dct['model']
                            self.model = mod
                            if mod == 'inv':
                                pass
                            elif mod in self.bad_models:
                                self.bad_words.add(self.lemma)
                            else:
                                # the magnus model is not working
                                self.main_loop_fd2(dct)

        return

    def main_loop_fd2(self, dct, kind=0):
        mod2 = self.ui_models.get(self.model)
        ends = mod2.get('sim')
        if ends:
            for self.pos, self.dct2 in dct.items():
                if self.pos in ['d', 'inv']:
                    pass
                else:
                    self.tpls = ends.get(self.pos)
                    if self.tpls:
                        self.main_loop_fd3(kind)
                    else:
                        self.errors4['wrong_pos'][self.lemma] = [self.pos, self.dct2, self.model]

    def main_loop_fd3(self, kind):
        found = 0
        errors = 0
        hits = 0
        if self.lemma == 'dies' and self.pos == 'sd':
            bb = 8
        for self.word, freq in self.dct2.items():
            irreg = self.irreg_excp.get((self.lemma, self.pos))
            if irreg and self.word == irreg:
                pass
            else:
                if self.model not in self.tot_pos:
                    self.tot_pos[self.model] = defaultdict(int)
                self.tot_pos[self.model][self.pos] += freq
                alt_ends = set()
                for tpl in self.tpls:
                    end = tpl[2]
                    root = tpl[0]
                    if self.word.endswith(end):
                        found = 1
                        lroot = self.word[:-len(end)]
                        break
                    else:
                        alt_ends.add(self.word[-len(end):])
                if found:
                    if self.model not in self.errors4['correct']:
                        self.errors4['correct'][self.model] = defaultdict(dict)
                    if self.pos not in self.errors4['correct'][self.model]:
                        self.errors4['correct'][self.model][self.pos] = defaultdict(int)
                    self.errors4['correct'][self.model][self.pos][end] += freq



                if not found:
                    if kind:
                        errors += freq
                    else:
                        if self.model not in self.errors4['correct']:
                            self.errors4['correct'][self.model] = defaultdict(dict)
                        if self.pos not in self.errors4['correct'][self.model]:
                            self.errors4['correct'][self.model][self.pos] = defaultdict(int)
                        self.errors4['correct'][self.model][self.pos]['bad'] += freq

                        self.bad_words.add(self.lemma)
                        if self.lemma not in self.errors4['anom']:
                            self.errors4['anom'][self.lemma] = defaultdict(dict)
                        if self.pos not in self.errors4['anom'][self.lemma]:
                            self.errors4['anom'][self.lemma][self.pos] = defaultdict(dict)
                        self.errors4['anom'][self.lemma][self.pos][self.word] = freq
                        for end in alt_ends:
                            if self.model not in self.errors4['wrong_end']:
                                self.errors4['wrong_end'][self.model] = defaultdict(dict)
                                self.errors4['wrong_word'][self.model] = defaultdict(dict)
                            if self.pos not in self.errors4['wrong_end'][self.model]:
                                self.errors4['wrong_end'][self.model][self.pos] = defaultdict(int)
                                self.errors4['wrong_word'][self.model][self.pos] = defaultdict(list)
                            self.errors4['wrong_end'][self.model][self.pos][end] += freq
                            self.errors4['wrong_word'][self.model][self.pos][end].append((self.lemma, self.word))
                elif kind:
                    hits += freq

        if kind:
            lst = self.word2fit[self.lemma][self.model]
            tot = hits + errors
            lst[0] += hits
            lst[1] += tot
            self.word2fit[self.lemma][self.model] = lst
        return

    def anom_by_percent(self):
        '''
        5.16 = 31830
        5.16 = 27954
        5.17 = 27088
        5.17 = 24772
        5.17 = 8864 (without sum)
        5.17 = 7631 (without sum)
        5.18 = 7165
        '''

        dct5 = {}
        self.las_w2l = {}
        self.get_las_w2l()
        self.bad_lemmas = {}
        tot_errors = 0
        for mod, dct in self.errors4['wrong_end'].items():
            if mod == 'sum':
                pass
            else:
                for pos, ends in dct.items():
                    for end, freq in ends.items():
                        if (mod == 'doctus' and len(pos) == 4) or 1:
                            # tot = self.tot_pos[mod][pos]
                            # try:
                            #     perc = percent(freq,tot)
                            # except:
                            #     perc = 0
                            tpl = (mod, pos, end)
                            # dct5[tpl] = perc
                            dct5[tpl] = freq
                            tot_errors += freq

        p(f'total errors {tot_errors}')
        lem2forms2 = defaultdict(dict)
        dct5 = sort_dct_val_rev(dct5)
        dct6 = {}
        dct7 = {}
        for k, v in dct5.items():
            mod = self.ui_models.get(k[0])
            pos = k[1]
            end = k[2]
            words = self.errors4['wrong_word'][k[0]][pos]

            lst5 = words[end]
            for tpl in lst5:
                lem, word = tpl
                if lem not in lem2forms2:
                    lem2forms2[lem] = defaultdict(list)

            lem2forms2[lem][pos].append(word)
            dct7[k] = v
            dct6[k] = [mod, v, words[end]]
        self.lem2forms2 = lem2forms2

        # dct11 = {}
        # for x,y in lem2forms2.items():
        #     dct11[x] = self.co_lemmas5[x]

        return

    def get_las_w2l(self):
        self.las_w2l = {}
        for k, v in self.lalems2forms2.items():
            for num, dct in v.items():
                lem = k + num
                for pos, dct2 in dct.items():
                    for word, freq in dct2.items():
                        if word not in self.las_w2l:
                            self.las_w2l[word] = defaultdict(dict)
                        if lem not in self.las_w2l[word]:
                            self.las_w2l[word][lem] = defaultdict(dict)
                        self.las_w2l[word][lem][pos] = freq

    def best_fit3(self):
        self.llem2clem2 = {}
        for x, y in self.llem2clem.items():
            for k, v in y.items():
                llem = x + k
                clem = x + v
                self.llem2clem2[llem] = clem

        self.lalems2forms4 = defaultdict(dict)
        self.word2fit = {}
        excp = []
        for x, y in self.lem2forms2.items():
            xu, num = cut_num(x, 1)
            self.clem = self.llem2clem2[x]
            cdct = self.co_lemmas4[self.clem]
            for self.model, itms in self.ui_models.items():
                if itms['pos'] == cdct['pos'] and self.model not in ['isaac', 'inv', 'abraham']:
                    # self.temp_mod = copy.deepcopy(cdct)
                    # self.temp_mod['model'] = self.mod_name
                    dct = self.lalems2forms2[xu][num]
                    if self.clem not in self.word2fit:
                        self.word2fit[self.clem] = defaultdict(dict)
                    self.word2fit[self.clem][self.model] = [0, 0]
                    self.main_loop_fd2(dct, 1)
                    lst = self.word2fit[self.clem][self.model]
                    try:
                        perc = percent(lst[0], lst[1])
                    except ZeroDivisionError:
                        perc = 0
                    self.word2fit[self.clem][self.model] = perc

        return

    def best_fit(self):
        self.llem2clem2 = {}
        for x, y in self.llem2clem.items():
            for k, v in y.items():
                llem = x + k
                clem = x + v
                self.llem2clem2[llem] = clem

        self.lalems2forms4 = defaultdict(dict)
        self.word2fit = defaultdict(dict)
        ex_models = ['isaac', 'inv', 'abraham', 'ego', 'tu', 'uos',
                     'nos', 'se','licet','jesus']
        for x in self.bad_words:
            self.lemma = x
            xu, num = cut_num(x, 1)
            dct = self.lalems2forms2[xu][num]
            lst5 = [[0, k, vgf.dct_idx(v, 0, 'v')] for k, v in dct.items()]
            pos = self.det_pos3(lst5)
            if x == 'coruus':
                bb=8

            for self.model, itms in self.ui_models.items():
                if '_pl' in self.model:
                    pass
                elif self.model in ['puer','ager'] and not xu.endswith('er'):
                    pass

                elif pos == itms['pos'] and self.model not in ex_models:
                    # self.temp_mod = copy.deepcopy(cdct)
                    # self.temp_mod['model'] = self.mod_name
                    self.word2fit[x][self.model] = [0, 0]
                    self.main_loop_fd2(dct, 1)
                    lst = self.word2fit[self.lemma][self.model]
                    try:
                        perc = percent(lst[0], lst[1])
                    except ZeroDivisionError:
                        perc = 0
                    self.word2fit[x][self.model] = perc
        return

    def best_fit2(self):
        '''
        word2fit2 are perfect matches of new models
        word2fit3 are imperfect matches
        '''

        b = 0
        self.word2fit2 = {}
        self.word2fit3 = {}
        for x, y in self.word2fit.items():
            xu, num = cut_num(x, 1)
            dct = {k: self.model_popularity.get(k, 0) for k, v in y.items() if v == 100}
            obj = self.errors4['anom'].get(x, '')
            if obj:
                if dct:
                    mod = vgf.largest_member(dct)
                    self.word2fit2[x] = [mod, dct, self.lalems2forms2[xu][num], obj]
                else:
                    self.word2fit3[x] = [sort_dct_val_rev(y), obj]
        self.get_old2new_model()
        return


    def print_models(self):
        lst = []
        for k,v in self.ui_models.items():
            lst.append([f'__{k}'])
            for x,y in v['R'].items():
                lst1 = [x] + list(y)
                lst.append(lst1)
            lst.append(['abs',v['abs']])
            lst.append([ 'suf',v['suf']])
            lst.append(['sufd' ,v['sufd']])
            lst.append(['pos', v['pos']])
            if 'sim' not in v:
                p (k)
            else:
                for x,y in v['sim'].items():
                    lst1 = [x]
                    for z in y:
                        lst1 += list(z)
                    lst.append(lst1)



        file = f'{dwn_dir}adjust_models'
        to.from_lst2txt_tab_delim(lst, file)
        vgf.open_txt_file(file)


    def get_old2new_model(self):
        miss = set()
        self.old2new = {}
        lst5 = []
        dct3 = {}
        dct4 ={}
        for x, y in self.word2fit2.items():
            xu, num = cut_num(x, 1)
            clem = self.llem2clem[xu].get(num)
            if clem==None:
                dct4[x]=y
            elif not clem:
                dct3[x]=y

            else:
                lst5.append([xu+clem, y[0]])




        return


    def temp19(self):
        lst = []
        for x,y in self.old2new.items():
            pass


    def get_model_popularity(self):
        self.model_popularity = {}
        for k, v in self.tot_pos.items():
            self.model_popularity[k] = sum(list(v.values()))
        return

    def analyze(self):  # 138
        '''
        the following words do not fit the current
        declension pattern for all declensions except 3rd
        '''

        self.errors2 = sort_dct_val_rev(self.errors2)
        for x, y in self.errors2.items():
            lem, num = cut_num(x[0], 1)
            dct = self.lalems2forms2[lem][num]
            ins = forms(dct, x[0])
            self.errors2[x] = [y, ins]
        return

    def research(self):
        if self.lem.endswith('ius') and self.dec == '2':
            lst = self.obj.get('sv')
            if lst:  # no counterexamples
                found = 0
                for z in lst:
                    if not z.endswith('i'):
                        found = 1
                if found:
                    dct = self.lalems2forms2[self.lem][self.num]
                    self.errors3['ius'].append(dct['sv'])

        if self.dec == '2' and self.lem[-3:-1] == 'uu':
            lst = self.obj.get('sa')
            if lst:
                found = 0
                for z in lst:
                    if z.endswith('om'):
                        found = 1
                if not found:
                    dct = self.lalems2forms2[self.lem][self.num]
                    self.errors3['om'].append(dct['sa'])
            ## probably obligatory of old latin
            ## but optional for classical, sallustius and martialis
            ## use it, then probably died out

        if self.tdec == '2':
            lst = self.obj.get('pg')
            if lst:
                for z in lst:
                    if reg(r'[^r]um$', z):
                        self.errors3['rum'].append(self.lem)

        if self.tdec == '2q':
            lst = self.obj.get('sv')
            if lst:
                dct = self.lalems2forms2[self.lem][self.num]
                self.errors3['rsv'].append(dct['sv'])

        if self.tdec == '4':
            lst = self.obj.get('sd')
            dct = self.lalems2forms2[self.lem][self.num]
            if lst:
                if all(x.endswith('u') for x in lst):
                    self.errors3['4du'].append(dct['sd'])
                else:
                    self.errors3['4dui'].append(dct['sd'])
            lst = self.obj.get('pa')
            if lst:
                if any(x.endswith('ua') for x in lst):
                    self.errors3['4ua'].append(dct['pa'])
                else:
                    self.errors3['4nua'].append(dct['pa'])
            lst = self.obj.get('pn')
            if lst:
                if any(x.endswith('ua') for x in lst):
                    self.errors3['4pa'].append(dct['pn'])
                else:
                    self.errors3['4npa'].append(dct['pn'])


class memorize_cl(reg_decl):
    def __init__(self):
        reg_decl.__init__(self)

    def build_lasla_dct(self):
        b = 0
        missing = set()
        bad = {}
        no_num = {}
        for x, y in self.lalems2forms.items():
            if x == 'praeceps1':
                bb = 8
            for num, v in y.items():
                if num in ['9', '8']:
                    self.lasla_dct[x + num] = 'proper'
                else:
                    try:
                        cnum = self.llem2clem[x][num]
                        clem = x + cnum
                        cobj = self.co_lemmas4[clem]
                        defn = get_def(cobj, 1, 0, 1)
                        self.lasla_dct[x + num] = defn
                    except:
                        obj2 = self.co_lem_wonum.get(x)
                        if not obj2:
                            self.lasla_dct[x] = ""
                            missing.add(x)
                        else:
                            if len(obj2) == 1:
                                obj2 = vgf.dct_idx(obj2, 0, 'v')
                                self.lasla_dct[x + num] = get_def(obj2, 1, 0, 1)
                                no_num[x] = obj2
                            else:
                                s = get_def_many(obj2)
                                self.lasla_dct[x + num] = s
                                bad[x] = obj2

        p(f'missing {len(missing)}')
        p(f'easy {len(no_num)}')
        pi.save_pickle(self.lasla_dct, f'{fold}lasla_dct')
        return

    def not_in_col(self):
        dct = {}
        for x, y in self.las_freq3.items():
            if x in self.co_lemmas4:
                dct[x] = y
        self.shared = dct

    def abridge_lem2forms(self):
        self.lem2forms = pi.open_pickle(f'{fold}lem2forms')
        self.lem2forms_ab = defaultdict(dict)
        for k, v in self.lem2forms.items():
            kw, num = cut_num(k, 1)
            if k in self.shared:
                self.lem2forms_ab[kw].update({num: v})
        pi.save_pickle(self.lem2forms_ab, f'{fold}lem2forms_mem')
        return

    def normalize_quick(self):  # 151860
        '''
        right now words ending in st are simply lopped off
        though in the future this will have to be fixed
        '''
        self.las_freq = defaultdict(int)
        for k, v in self.lalems2forms.items():
            for x, y in v.items():
                lst = []
                for z in y:
                    if z[0].endswith('st'):
                        z[0] = z[0][:-2]
                    if z[0].endswith("'"):
                        z[0] = z[0][:-1] + 's'
                    if z[0].endswith('.'):
                        pass
                    else:
                        if z[0] == 'Valent':
                            p(z[0])
                            bb = 8
                        z[0] = z[0].lower()
                        if z[0].startswith('v'):
                            z[0] = z[0].replace('v', 'u')
                        z[0] = self.misspell.get(z[0], z[0])
                        lst.append(z)
                        self.las_freq[(k + x, z[0], z[1])] += z[2]
                v[x] = lst
        return

    def parse_lalems(self):
        for x, y in self.lalems2forms_prop.items():
            obj = self.lalems2forms.get(x)
            for k, v in y.items():
                for z in v:
                    z[0] = z[0].lower()
                    z[0] = z[0].replace('v', 'u')
            if obj:
                self.lalems2forms[x] = merge_2dicts(obj, y)
            else:
                self.lalems2forms[x] = y

        return

    def order_lalems(self):
        final_pos = pi.open_pickle(f'{fold}final_pos', 1)
        for k, v in self.lalems2forms.items():
            for num, lst in v.items():
                dct = defaultdict(dict)
                dct4 = defaultdict(list)
                for l in lst:
                    pos = l[1]
                    word = l[0]
                    freq = l[2]
                    dct[pos][word] = freq
                    dct4[pos].append(word)
                dct2 = {}
                dct5 = {}
                for s in final_pos.values():
                    if s in dct:
                        dct2[s] = dct[s]
                        dct5[s] = dct4[s]
                self.lalems2forms_wprop[k + num] = dct2
                # if k + num not in self.ignore_proper:
                #     self.lalems2forms2[k][num] = dct2
                #     self.lalems2forms3[k][num] = dct5
                self.lalems2forms2[k][num] = dct2
                self.lalems2forms3[k][num] = dct5

        return

    def combine_proper2(self):
        for k, v in self.redund_prop.items():
            vu, num = cut_num(v, 1)
            ku, numk = cut_num(k, 1)
            obj = self.lalems2forms2[vu][num]
            objr = self.lalems2forms2[ku][numk]
            for x, y in objr.items():
                pass
                dct = obj[x]
                for s, t in y.items():
                    s = norm_str_jv(s)
                    dct[s] += t
            del self.lalems2forms2[ku][numk]
            del self.lalems2forms3[ku][numk]

        return

    def get_declensions_dct(self):
        self.lthird = set()
        dct = defaultdict(dict)
        for k, v in self.lemma2decl.items():
            if any(t == ('n', '7') for t in v.keys()):
                self.declensions['greek'].append(k)
            else:
                if any(t[0] == 'n' and len(t) > 1 for t in v.keys()):
                    n = 0
                    for t in v.keys():
                        if t[0] == 'n':
                            n += 1
                    if n > 1:
                        self.declensions['many'].append(k)
                        dct['many'][k] = v
                    else:
                        if any(t == ('n', '6') for t in v.keys()):
                            self.declensions['anom'].append(k)
                        elif any(t == ('n', '1') for t in v.keys()):
                            self.declensions['1'].append(k)
                        elif any(t == ('n', '2') for t in v.keys()):
                            self.declensions['2'].append(k)
                        elif any(t == ('n', '4') for t in v.keys()):
                            self.declensions['4'].append(k)
                        elif any(t == ('n', '5') for t in v.keys()):
                            self.declensions['5'].append(k)
                        elif any(t == ('n', '3') for t in v.keys()):
                            self.lthird.add(k.lower())

    def check_w_large_corpus(self):
        lat_freq = pi.open_pickle(f'{fold}latin_freq_all_ui')
        # for k,v in self.word2prop.items():
        #     if 'pgb'


class stem_patterns(memorize_cl):
    def __init__(self):
        memorize_cl.__init__(self)

    def use_review(self):
        '''
        it looks like puberes as pn and pa are adjectives

        cupidon is greek

        '''

        file = f'{fold}third_variants'
        lst = to.from_txt2lst_tab_delim(file)
        self.third_variants = {}
        self.no_stem_change = {}
        for x in lst:
            lem = x[0]
            try:
                obl = x[1]
            except:
                obl = ''
            if lem.startswith('_'):
                if not obl:
                    self.no_stem_change[lem[1:]] = lem[1:]
                else:
                    self.lemm2ostem2[lem[1:]] = obl
                parent = lem[1:]
            else:
                if not obl:
                    self.no_stem_change[lem] = lem
                else:
                    self.lemm2ostem2[lem] = obl

                ins = alt_cls(lem, parent, obl)
                self.third_variants[lem] = ins

        return

    def add2lem2stem(self):
        missing = {}
        for x, y in self.word2stems.items():
            if x not in self.lemm2ostem2 and x not in self.no_stem_change \
                    and x not in self.alt_nom:
                if len(y) > 1:
                    missing[x] = y
                else:
                    b = vgf.dct_idx(y)
                    xu = cut_num(x)
                    if b == xu:
                        self.no_stem_change[x] = xu
                    else:
                        self.lemm2ostem2[x] = b

        return

    def use_more_nom_stems(self):
        file = f'{fold}more_nom_stems'
        lst = to.from_txt2lst_tab_delim(file, 1)
        self.alt_nom = {}
        for l in lst:
            if l[0][0] == '_':
                lem = l[0][1:]
            elif len(l) > 1:
                num = l[1]
                word = l[0]
                if num.endswith('*'):
                    self.alt_nom[lem] = word

        return

    def get_plural_only_thirds(self):
        dctp = {}
        for k, v in self.lalems2forms2.items():
            for x, y in v.items():
                lem = k + x
                if lem in self.lthird:
                    if all(s.startswith('p') for s, t in y.items()):
                        dctp[lem] = y

        self.plural_only_thirds = dctp
        return

    def use_more_third_variant_spellings(self):
        file = f'{fold}more_third_variant_spellings'
        lst = to.from_txt2lst_tab_delim(file)
        for l in lst:
            lem = l[0]
            obl = l[1]
            if lem.startswith('_'):
                lem = lem[1:]
                lemu = cut_num(lem)
                if lemu != obl:
                    self.lemm2ostem2[lem] = obl
                else:
                    self.no_stem_change[lem] = lem
                las_lem = lem
            elif lem.startswith('*'):
                varu = lem[1:]
                varus = cut_num(varu)
                if varus == obl:
                    obl = ""
                ins = alt_cls(varu, las_lem, obl)
                self.third_variants[varu] = ins

    def clem_oblique_stems(self):
        for k, v in self.lemm2ostem2.items():
            pass

    def stem_patterns_fu(self):  # 403
        self.st_patterns = defaultdict(set)
        ## iter, itiner
        ## anceps, ancipit
        to_remove = set()
        remainder = defaultdict(list)
        remainder = []
        for lem, vs in self.lemm2ostem2.items():
            vlst = vs.split(',')
            k, num = cut_num(lem, 1)

            for v in vlst:
                if v != k:
                    if k.endswith('tas') and v.endswith('tat'):
                        self.st_patterns['xtas=xtat'].add((k, v))

                    ### add letter to lemma
                    elif k + 'n' == v:
                        self.st_patterns['xn=x'].add((k, v))
                    elif k + 'd' == v:
                        self.st_patterns['xd=x'].add((k, v))
                    elif k + 's' == v:
                        self.st_patterns['xs=xss'].add((k, v))
                    elif k + 'r' == v:
                        self.st_patterns['xr=x'].add((k, v))
                    elif k + 'l' == v:
                        self.st_patterns['xl=xll'].add((k, v))
                    elif k + 't' == v:
                        self.st_patterns['xt=x'].add((k, v))

                    ## add letter to oblique

                    elif v + 's' == k:
                        self.st_patterns['x=xs'].add((k, v))

                    elif v + 'e' == k:
                        self.st_patterns['x=xe'].add((k, v))

                    elif v + 'a' == k:
                        self.st_patterns['x=xa'].add((k, v))

                    ## add two letters to oblique

                    elif v + 'is' == k:
                        self.st_patterns['x=xis'].add((k, v))
                    elif v + 'ia' == k:
                        self.st_patterns['x=xia'].add((k, v))

                    ### change last two letters

                    elif k[:-2] == v[:-2] and k[-2:] == 'us' and v[-2:] == 'or':
                        self.st_patterns['xus=xor'].add((k, v))
                    elif k[:-2] == v[:-1] and k[-2:] == 'er' and v[-1] == 'r':
                        self.st_patterns['xer=xr'].add((k, v))
                    elif k[:-2] == v[:-2] and k[-2:] == 'en' and v[-2:] == 'in':
                        self.st_patterns['xen=xin'].add((k, v))
                    elif k[:-2] == v and k[-2:] == 'es':
                        self.st_patterns['x=xes'].add((k, v))
                    elif k[:-2] == v[:-2] and k[-2:] == 'es' and v[-2:] == 'it':
                        self.st_patterns['xes=xit'].add((k, v))
                    elif k[:-2] == v[:-2] and k[-2:] == 'es' and v[-2:] == 'id':
                        self.st_patterns['xes=xid'].add((k, v))
                    elif k[:-2] == v[:-2] and k[-2:] == 'us' and v[-2:] == 'er':
                        self.st_patterns['xus=xer'].add((k, v))
                    elif k[:-2] == v[:-2] and k[-2:] == 'is' and v[-2:] == 'er':
                        self.st_patterns['xis=xer'].add((k, v))
                    elif k[:-2] == v[:-2] and k[-2:] == 'ex' and v[-2:] == 'ic':
                        self.st_patterns['xex=xic'].add((k, v))
                    elif k[:-2] == v[:-2] and k[-2:] == 'ur' and v[-2:] == 'or':
                        self.st_patterns['xur=xor'].add((k, v))
                    elif k[:-2] == v[:-2] and k[-2:] == 'ur' and v[-2:] == 'in':
                        self.st_patterns['xur=xin'].add((k, v))
                    elif k[:-2] == v[:-2] and k[-2:] == 'ut' and v[-2:] == 'it':
                        self.st_patterns['xut=xit'].add((k, v))
                    elif k[:-2] == v[:-2] and k[-2:] == 'ex' and v[-2:] == 'ig':
                        self.st_patterns['xex=xig'].add((k, v))

                    ### change last letter

                    elif k[:-1] == v[:-1] and k[-1] == 's' and v[-1] == 'r':
                        self.st_patterns['xs=xr'].add((k, v))
                    elif k[:-1] == v[:-1] and k[-1] == 'o' and v[-1] == 'n':
                        self.st_patterns['xo=xn'].add((k, v))
                    elif k[:-1] == v[:-1] and k[-1] == 'x' and v[-1] == 'c':
                        self.st_patterns['xx=xc'].add((k, v))
                    elif k[:-1] == v[:-1] and k[-1] == 'x' and v[-1] == 'g':
                        self.st_patterns['xx=xg'].add((k, v))
                    elif k[:-1] == v[:-1] and k[-1] == 'x' and v[-1] == 'u':
                        self.st_patterns['xx=xu'].add((k, v))
                    elif k[:-1] == v[:-1] and k[-1] == 's' and v[-1] == 'n':
                        self.st_patterns['xs=xn'].add((k, v))
                    elif k[:-1] == v[:-1] and k[-1] == 's' and v[-1] == 'd':
                        self.st_patterns['xs=xd'].add((k, v))
                    elif k[:-1] == v[:-1] and k[-1] == 's' and v[-1] == 't':
                        self.st_patterns['xs=xt'].add((k, v))

                    ### change last letter of lemma, last two letters of oblique

                    elif k[:-1] == v[:-2] and k[-1] == 'o' and v[-2:] == 'in':
                        self.st_patterns['xo=xin'].add((k, v))
                    elif k[:-1] == v[:-2] and k[-1] == 'x' and v[-2:] == 'ct':
                        self.st_patterns['xx=xct'].add((k, v))

                    elif k[:-1] == v[:-2] and k[-1] == 's' and v[-2:] == 'nt':
                        self.st_patterns['xs=xnt'].add((k, v))

                    ### change last three letters of lemma, last two letters of oblique

                    elif k[:-3] == v[:-2] and k[-3:] == 'eps' and v[-2:] == 'ip':
                        self.st_patterns['xeps=xip'].add((k, v))

                    elif k[:-3] == v[:-2] and k[-3:] == 'eps' and v[-2:] == 'up':
                        self.st_patterns['xeps=xup'].add((k, v))

                    elif k[:-3] == v[:-2] and k[-3:] == 'eps' and v[-2:] == 'it':
                        self.st_patterns['xeps=xit'].add((k, v))

                    ### change several letters

                    elif k[:-3] == v[:-4] and k[-3:] == 'eps' and v[-4:] == 'ipit':
                        self.st_patterns['xeps=xipit'].add((k, v))




                    else:
                        remainder.append([lem, v])

        self.order_st_patterns(remainder)

        return

    def order_st_patterns(self, remainder):
        dct = {k: len(v) for k, v in self.st_patterns.items()}
        self.st_patterns = vgf.sort_dct_by_dct(self.st_patterns, dct)
        to_remove = set()
        for k, v in self.st_patterns.items():
            if len(v) == 1:
                to_remove.add(k)
                for z in v:
                    remainder.append(z)

        for x in to_remove:
            del self.st_patterns[x]

        return

    def get_no_stem_change(self, stem_change_mispelled):
        self.no_stem_change = {}
        for k in self.lthird:
            if k not in self.lemm2ostem2:
                self.no_stem_change[k] = self.las_freq_wnum[k]
        self.no_stem_change = sort_dct_val_rev(self.no_stem_change)

        return

    def check_stem_change(self):
        lst = []
        for k, v in self.no_stem_change.items():
            defn = self.lasla_dct.get(k, '')
            lst.append([k, defn])
            dct = self.lalems2forms_wprop[k]
            for x, y in dct.items():
                lst1 = [x]
                for s, t in y.items():
                    lst1.append(f'{s} {t}')
                lst.append(lst1)
        kind = 0
        if kind:
            ef.from_lst2book(lst, f'{fold}check_stems')
        return


class third_decl(stem_patterns):
    def __init__(self):
        stem_patterns.__init__(self)

    def third_properties(self):
        self.word2decl = defaultdict(list)
        self.word2stems = {}
        missing = set()
        got = set()
        self.mod2word2 = defaultdict(list)
        self.mod2wordemp = defaultdict(list)
        for k, dct in self.lalems2forms3.items():
            if k == 'imperator':
                bb = 8
            self.lemma = k
            for self.num, pos2t in dct.items():
                if k + self.num in self.lthird:
                    got.add(k + self.num)
                    pos2n = self.lalems2forms2[k][self.num]
                    self.new_method(pos2t, pos2n)
        missing = self.lthird - got
        missing = {k: self.las_freq_wnum[k] for k in missing}
        missing = sort_dct_val_rev(missing)
        return

    def new_method(self, pos2t, pos2n):
        dct1 = {
            'sg': ['is'],
            'sa': ['im', 'em'],
            'sd': ['i'],
            'sb': ['e', 'i'],
            'pn': ['es', 'is', 'ia', 'a'],
            'pa': ['es', 'is', 'ia', 'a'],
            'pg': ['ium', 'um'],
            'pb': ['ibus'],
            'pd': ['ibus'],
        }
        dct2 = defaultdict(list)
        for x, endings in dct1.items():
            obj = pos2t.get(x)
            if obj:
                found = 0

                for end in endings:
                    done = 0
                    if done:
                        break
                    for word in obj:
                        if word.endswith(end):
                            if end == 'i' and word.endswith('ei'):
                                pass
                            elif end == 'um' and word.endswith('ium'):
                                pass
                            else:
                                found = 1
                                stem = word[:-len(end)]
                                if self.lemma + self.num not in self.word2stems:
                                    self.word2stems[self.lemma + self.num] = defaultdict(int)
                                self.word2stems[self.lemma + self.num][stem] += pos2n[x][word]
                                if end not in dct2[x]:
                                    dct2[x].append(end)
                                if end == 'ia':
                                    done = 1
                            break
                    if done:
                        break
                if not found:
                    if x == 'sa':
                        sa = pos2t.get('sa')
                        ns = pos2t.get('sn')
                        if sa and ns:
                            if self.same_end(sa, ns):
                                dct2['sa'].append('x')
                            else:
                                self.third_anomalies['sa'].append((obj, self.lemma))

                    else:
                        self.third_anomalies[x].append((obj, self.lemma))

        self.word2decl[self.lemma + self.num] = dct2
        self.third_prop_new(dct2)

    def third_prop_new(self, dct2):
        '''
        ciuitas {'ciuitatum': 80, 'ciuitatium': 21}
        dignitas {'dignitatum': 2, 'dignitatium': 1}
        calamitas {'calamitatum': 4}  - checked in phi
        hereditas {'hereditatum': 8, 'hereditatium': 1}
        nobilitas {'nobilitatum': 1}
        necessitas {'necessitatum': 2}
        utilitas {'utilitatum': 4}
        cupiditas {'cupiditatum': 14, 'cupiditatium': 6}
        aedilitas {'aedilitatum': 1}
        affinitas {'adfinitatum': 2}
        immunitas {'immunitatium': 1}
        '''

        '''
    'em;e;es;es,is;ium,um'
    'em;e;es;es,is;um'
    'em;e;es;es;ium'
    
    these can all be combined if
    mortum 0 mortium 6 in PHI
    infantum 12
    immunitatum 0 but immunitatium 1
    canium 2 in martialis in PHI
    mensium - attested
    sedium - attested    
        '''

        pa = dct2.get('pa')
        pn = dct2.get('pn')
        if pn:
            pn = ','.join(pn)
        else:
            pn = '0'

        if pa:
            pa = ','.join(pa)
            if pa == 'is':
                pa = 'es,is'

        else:
            pa = '0'

        pnpa = f'{pn};{pa}'
        if pnpa == 'es;is':
            pnpa = 'es;es,is'

        lst2 = ['sa', 'sb', 'pg']

        tot = ''
        for x in lst2:
            y = dct2.get(x)
            if not y:
                y = '0'
            else:
                y = ','.join(y)
            if x == 'sb' and y == 'i':
                y = 'e,i'

            if tot:
                tot = f'{tot};{y}'
            else:
                tot = y

            if x == 'sb':
                tot = f'{tot};{pnpa}'

        if '0' in tot:
            self.mod2wordemp[tot].append(self.lemma + self.num)
        else:
            self.mod2word2[tot].append(self.lemma + self.num)

    def convert2modeles4(self):
        pass
        best_repr = {}
        for x, y in self.mod2word2.items():
            dct = {z: self.las_freq_wnum for z in y}

    def infer_empty_prop(self):
        '''
        dct8 and 9 are models which have been manually assigned
        a standard model in the incomplete third sheet
        dct5 models so long as there is no 0  are models
        which have been automatically assigned a standard model


        '''

        dct5 = {}
        dct8 = {}
        dct9 = {}
        for k, v in self.mod2wordemp.items():
            lst = k.split(';')
            dct6 = {}
            dct11 = {}
            for x, y in self.mod2word2.items():
                if k == '0;e;ia;ia;ium' and x == 'x;e,i;ia;ia;ium':
                    bb = 8

                lst1 = x.split(';')
                sim = 0
                diff = 0
                for e, f in zip(lst, lst1):
                    if e == '0':
                        pass
                    elif e == f:
                        sim += 1
                    elif e != f:
                        diff += 1
                if not diff and sim:
                    dct6[x] = len(y)
                else:
                    dct11[x] = sim

            if not dct6:
                dct5[k] = 0
                dct8[k] = v
                if dct11:
                    dct9[k] = vgf.largest_member(dct11)
            else:
                dct5[k] = vgf.largest_member(dct6)
        research = 0
        if research:
            file = f'{fold}incomplete_third'
            lst5 = [[k, v] for k, v in dct9.items()]
            to.from_lst2txt_tab_delim(lst5, file)
            vgf.open_txt_file(file)
        else:
            self.assign_empty_mods(dct5)
        return

    def assign_empty_mods(self, dct5):

        file = f'{fold}incomplete_third'
        lst1 = to.from_txt2lst_tab_delim(file)
        for l in lst1:
            emod = l[0]
            fmod = l[1]
            val = l[2]
            if val == '?':
                lst = self.mod2wordemp[emod]
                self.mod2word2[fmod] = lst
                del self.mod2wordemp[emod]

            else:
                dct5[emod] = fmod

        for k, v in dct5.items():
            lst = self.mod2word2[v]
            elst = self.mod2wordemp[k]
            lst += elst

        return

    def same_end(self, lst, lst2, iss=0):
        st1 = set(x[-2:] for x in lst if len(x) > 2)
        st2 = set(x[-2:] for x in lst2 if len(x) > 2)
        if st1 == st2:
            if iss and st1 == {'is'}:
                return 0
            return 1

    def elim_anomalies2(self):
        '''
        it is probably the case that any noun whose form is
        'em;e;es;es,is;um' is probably 'em;e;es;es,is;ium,um'
        instances of ium in pg exist they just don't appear in the
        texts.
        '''

        dct = {
            'em;e;es;es,is;um': 'em;e;es;es,is;ium,um',  # 3
            'em;e;es;es;ium': 'em;e;es;es,is;ium,um',
        }
        for x, y in dct.items():
            lst = self.mod2word2[x]
            lst1 = self.mod2word2[y]
            lst1 += lst
            del self.mod2word2[x]

        self.word2mod = {z: k for k, v in self.mod2word2.items() for z in v}
        missing = self.lthird - set(self.word2mod.keys())
        return

    def wrong_co_lemma(self):
        lst = []
        for mod, v in self.mod2word2.items():
            mod1 = self.best_repr.get(mod)
            mod1 = cut_num(mod1)
            for z in v:
                c = self.llem2clem2.get(z)
                if c:
                    lst.append([c, mod1])

        file = f'{fold}wrong_model3'
        self.output(1, lst, file)

    def export2modeles4(self):
        del self.mod2word2[0]
        lst2 = []
        dct3 = {k: len(v) for k, v in self.mod2word2.items()}
        self.mod2word2 = vgf.sort_dct_by_dct(self.mod2word2, dct3)

        for k, v in self.mod2word2.items():
            lst = k.split(';')
            pn = lst[2]
            pa = lst[3]
            pn = pn.replace('es', 'ēs')
            pa = pa.replace('es', 'ēs')
            pn = pn.replace('is', 'īs')
            pa = pa.replace('is', 'īs')
            code = f'code:{k}'
            members = f'members: {len(v)}'
            b = 'R:0:0,0'
            c = 'R:1:0,0'
            h = f'des:413:1:ī'
            nm = f'modele:{self.best_repr[k]}'
            if nm.endswith('mare'):
                nm += '1'
            if "x" not in k:
                s = "des:3-12:1:"
                u = f'{lst[0]};is;ī;{lst[1]};{pn};{pa};{lst[4]};ibus;ibus'
                f = 'des:1,2:0:-;-'
            else:
                s = "des:4-12:1:"
                f = 'des:1-3:0:-;-'
                u = f'is;ī;{lst[1]};{pn};{pa};{lst[4]};ibus;ibus'
            g = f'{s}{u}'
            i = 'pos:n'
            lst3 = [nm, b, c, f, g, h, i, code, members, '']
            for r in lst3:
                lst2.append(r)
        lst6 = to.from_txt2lst(f'{fold}modeles4')
        lst6.append('')
        lst6 += lst2
        file = f'{fold}modeles5'
        to.from_lst2txt(lst2, file)

        return

    def get_best_repr(self):
        self.best_repr = {}
        for k, v in self.mod2word2.items():
            z = {x: self.las_freq_wnum[x] for x in v}
            self.best_repr[k] = vgf.largest_member(z)

    def elim_anomalies(self):

        ##  immunitas

        to_elim = {
            ('sors', 'sorti', 'sb'),
            ('seges', 'segeti', 'sb'),  # dubious
            ('silex', 'silici', 'sb'),  # dubious
            ('mors', 'morti', 'sb'),  # not in dictionary
            ('caput', 'capiti', 'sb'),  ## in dictionary, but catullus and ovid
            ## maybe it's a poetic dative
            ('uxor', 'uxori', 'sb'),  ## not in dictionary
            ('nauis', 'nauum', 'pg'),
            ('homo', 'hominis', 'pa'),
            ('cinis', 'cineris', 'pa'),
            ('pectus', 'pectori', 'sb'),
            ('foris1', 'foris', 'pn'),
        }
        for t in to_elim:
            lem, num = cut_num(t[0], 1)

            obj = self.lalems2forms2[lem][num]
            obj1 = self.lalems2forms3[lem][num]
            dct = obj[t[2]]
            lst1 = obj1[t[2]]
            del dct[t[1]]
            lst1.remove(t[1])


class bottom_most(third_decl):
    def __init__(self):
        third_decl.__init__(self)

    def begin(self, kind='ending', kind2=''):
        p('now building lists of data to memorize')
        self.get_atts(kind2)
        kind3 = 1
        if kind3:
            self.normalize_quick()
            if kind2 == 'start':
                self.wo_num()
                self.get_las_freq3()
            self.not_in_col()
            self.parse_lalems()
            self.order_lalems()
            self.elim_anomalies()
            self.combine_proper2()
            # self.build_lasla_dct()
        self.get_declensions_dct()
        if kind in ['ending']:
            self.a_end()
            self.a_end_research()
        if kind in ['reg_decl', 'all']:
            self.get_ddct()
            self.del_models()
            self.main_loop_fd()
            self.anom_by_percent()
            self.get_model_popularity()
            self.best_fit()
            self.best_fit2()
            # self.analyze()
        if kind in ['third', 'all']:
            self.get_atts_third()
            self.third_properties()
            self.infer_empty_prop()
            self.elim_anomalies2()
            self.get_best_repr()
            self.wrong_co_lemma()
            self.export2modeles4()
            self.use_more_nom_stems()
            self.use_review()
            self.use_more_third_variant_spellings()
            self.add2lem2stem()
            self.get_plural_only_thirds()
            self.stem_patterns_fu()
            self.check_stem_change()

        return


def begin2(kind=0):
    if kind in [0, 1]:
        ins = bottom_most_a4()
        ins.begin_fc()
    if kind in [1, 2]:
        ins2 = bottom_most_la()
        ins2.begin_mcl()
    ins3 = bottom_most()
    ins3.begin('reg_decl', 'start')


if eval(not_execute_on_import):
    if vgf.pycharm():
        args = [0, 'tel', 'start', 'IX', '', 0, 0]
        args = [0, 'tes', 'start', 'IX', '', 0, 0]
        args = [0, 'tej', 'start', 'IX', '', 0, 0]
        args = [0, 'third', 'start', 'IX', '', 0, 0]
        args = [0, 'all', 'start', 'IX', '', 0, 0]

    else:
        args = vgf.get_arguments()

    if not args[1]:
        p('wrong argument')
    elif args[1] == 'tes':
        begin2()
    elif args[1] == 'tel':
        begin2(1)
    elif args[1] == 'tej':
        begin2(2)

    else:
        ins = bottom_most()
        ins.begin(args[1], args[2])
