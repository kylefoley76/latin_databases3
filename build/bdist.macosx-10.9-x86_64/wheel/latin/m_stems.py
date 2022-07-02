from bglobals import *


def help():
    p('''
    
    the purpose of this model is to find the roots of latin words
    since if you know the roots you can easily infer the forms of
    child words.
    we divide words into the following categories:
    
    alternates: alternate spellings
    
    bachelors: words to which no suffix or prefix is ever added
        and are not compound
    
    parents: words which do not contain a prefix or suffix but prefixed
        and suffixes are added to them
    
    children: words which contain a parent
    
    we now divid the children into categories:
    orphans: words composed of prefixes and/or suffixes but the
        parent nolonger exists in the language.  each orphan
        however must be similar in meaning to its sibling orphans
    
    we perform this in broad strokes as follows.
    1) there are 4 text files where we manually went through and weeded
    out children from non-children.  these text files are: stem_lst, check_doubles
    check_reals, check_fakes.  How the files are parsed is explained on
    the file themselves
    
    2) we then put each child into a dict called word2morph whose key is the word
        and whose value is the divisions of this word
    
    3) we then use the technique of cutting off prefixes and a few
        very famous words which often end words such as facio and dico
    
    4) we then divide the potential children into two categories, real and fake
        the reals contain morphemes which we know to be bonafide children,
        the fakes do not.  the fakes are put into the method
        temp_word2morph
    
    we have not yet formed this step but once the oxford latin dictionary
        is fully parsed we will go through the and weed out the
        children from the non-children
        
    
    
    
    
    
    ''')




class top:
    def __init__(self):
        pass

    def get_atts(self):
        self.not_compound = set()
        self.not_compound2 = set()
        self.popular = set()
        self.not_stem = set()
        self.umorphemes = defaultdict(set)
        self.word2morph = defaultdict(set)
        self.failed_fakes = set()
        self.all_stems = set()
        self.no_final = {}
        self.dubious = set()
        self.double2prefix = {}
        self.isalt = {}
        self.not_morpheme = set()
        self.dimin = {}
        # self.def_lemmas = pi.open_pickle(f'{fold}def_lemmas', 1)
        self.co_lemmas4 = pi.open_pickle(f'{fold}co_lemmas4', 1)
        # self.mmodels = pi.open_pickle(f'{fold}mod_vow2', 1)
        self.mmodels = pi.open_pickle(f'{fold}mmodels', 1)
        self.mod2word = pi.open_pickle(f'{fold}mod2word', 1)
        self.lem_freq_crude = pi.open_pickle(f'{fold}lem_freq_crude')
        self.declinable = {}
        self.alt_morph = {}
        self.manual = {}
        self.initials = defaultdict(set)
        self.endings2 = defaultdict(list)
        lst = to.from_txt2lst(f'{fold}check_reals', 1, 1)
        lst1 = to.from_txt2lst(f'{fold}check_fakes', 1, 1)
        self.real_check = lst + lst1
        self.irr_notes = {}
        self.isproper = set()
        self.ie_root = []
        self.non_lemma = set()
        self.word2end = {}
        self.iwords = set()
        self.owords = set()
        self.bachelors = set()
        self.true_fake_stem = set()
        self.temp_word2morph = defaultdict(set)
        self.suffixes = {'faci', 'fact', 'fic', 'fici', 'dic'}

    def cut_off_suffix(self, word, suff):
        if suff == 0:
            l = self.word2end.get(word)
            if not l:
                return word, ''
            return l[0], l[1]
        elif not suff:
            return word

        return word[:-len(suff)]

    def get_suffix(self, word, beg):
        return word[len(beg):]

    def cut_off_prefix(self, word, pre):
        return word[len(pre):]



    def model_by_end(self):
        ends = set()
        for k, v in self.mmodels.items():
            if k == 'miles':
                bb = 8
            for num, lsts in v['des'].items():
                if num == 12:
                    bb = 8
                for l in lsts:
                    for z in l[1]:
                        if z:
                            z = unidecode(z)
                            z = re.sub(r'[0-9]', "", z)
                            ends.add(z)

            if k == "clio_g":
                break
        self.end2 = ends
        return






class use_prefixes(top):
    def __init__(self):
        top.__init__(self)

    def begin_up(self):
        # self.longest_words()
        self.get_pref()
        self.fix_double_cons_prefix()
        self.get_more_real_stems()
        self.rank_lemmas()
        self.popular_words()
        self.get_failed_fakes()
        self.check_spell()
        self.del_ambig_split()
        self.research_failed_fakes()

    def chop_stem(self, w):
        if w.endswith('ior'):
            w = w[:-3]
        elif w.endswith('or'):
            w = w[:-2]
        elif w in ['pesco']:
            w = w[:-1]

        elif reg(r'(e|i)sco$', w):
            w = w[:-4]
        else:
            w = w[:-1]

        if len(w) < 1:
            bb = 8

        return w

    def detach_prefix(self, word, prefix, stem, end):
        c = 0
        if len(word) > len(prefix) + 1 and prefix in self.pref2 \
                and word[len(prefix)] == word[len(prefix) + 1]:
            c = 1
            prefix = prefix + word[len(prefix) + 1]
            stem = stem[len(prefix):]

        else:
            stem = self.cut_off_prefix(stem, prefix)

        if prefix == 'o' and not word[:2] == 'ob' and not c:
            self.owords.add(word)

        if prefix == 'i':
            self.iwords.add(word)
            if len(word) < 3:
                return 0
            elif word[1] == 'g':
                pass
            elif word[1] == word[2] and word[2] in 'lr':
                pass
            else:
                return 0

        if stem in self.not_stem:
            return 0

        if stem in self.true_fake_stem or \
                stem + end in self.popular:
            self.temp_real_stem = (prefix, stem)
        else:
            self.temp_fake_stem = (prefix, stem)

        return 1

    # def longest_words(self):
    #     dct = {}
    #     for x, y in self.stem2lemma.items():
    #         dct[x] = len(x)
    #     self.longest = sort_dct_val_rev(dct)
    #     self.stem2lemma = {k: self.stem2lemma[k] for k, v in self.longest.items()}

    def get_pref(self):
        self.pref, self.pref2 = prefixes()
        self.pref2.append('i')
        self.pref['su'] = 'su'
        self.pref['o'] = 'o'
        self.pref['i'] = 'i'

    def fix_double_cons_prefix(self):
        '''
        here we fix the problem where in praecolligo, for example,
        with ll one l is in the prefix the other in the stem
        '''

        to_de = []
        to_add = {}
        for k, v in self.double2prefix.items():
            if v[1][0] == v[1][1] and (v[0][-1] in self.pref2 or \
                                       v[0][-2:] in self.pref2):

                pre = v[0] + v[1][0]
                stem = v[1][1:]
                _, end = self.word2end.get(k, (k, ''))
                stem = self.cut_off_suffix(stem, end)
                to_de.append(k)
                to_add[k] = (pre, stem, end)
            else:
                _, end = self.word2end.get(k, (k, ''))
                stem = v[1]
                pre = v[0]
                stem = self.cut_off_suffix(stem, end)
                self.double2prefix[k] = (pre, stem, end)
                # p(pre, stem, end)

        for x in to_de:
            del self.double2prefix[x]
        self.double2prefix = merge_2dicts(self.double2prefix, to_add)
        return


    def conditions(self, x):
        if x in self.not_compound:
            return 0
        if x in self.dimin:
            return 0
        if x in self.double2prefix:
            return 0
        if x in self.word2morph:
            return 0
        return 1

    def ad_hoc(self):
        self.word2end['redux'] = ['redux', '']
        self.word2end['res'] = ['res', '']

    def get_failed_fakes(self):
        b = 0
        self.ad_hoc()
        self.all_stems = set(y[0] for x, y in self.word2end.items())
        for x in self.declinable.keys():
            if self.conditions(x):
                if x == 'paratio':
                    bb = 8

                s = x
                stem, end = self.word2end.get(x, (None, None))
                if not stem:
                    # todo all words should have an ending
                    pass
                else:
                    b += 1
                    if b == 38:
                        bb = 8
                    vgf.print_intervals(b, 50)

                    found = 0
                    for z in self.suffixes:
                        if stem.endswith(z) and stem != z:
                            found = 1
                            pref = self.cut_off_suffix(stem, z)
                            stem = self.cut_off_prefix(stem, pref)
                            self.temp_real_stem = (pref, stem)
                            break

                    if not found:
                        self.temp_real_stem = ''
                        self.temp_fake_stem = ''
                        tpref = ""
                        for z in self.pref:
                            if s.startswith(z) and stem > z:
                                found = self.detach_prefix(s, z, stem, end)
                                if found:
                                    tpref += z
                                    break

                    if not found:
                        self.bachelors.add(x)
                    else:
                        self.add2dcts(end, x)

        return

    def check_spell(self):
        dct = {}
        for k, v in self.word2morph.items():
            for tpl in v:
                tpl = [re.sub(r'[0-9]', '', x) for x in tpl]
                s = ''.join(tpl)
                if s != k:
                    dct[k] = v
        if dct:
            assert 0
        return

    def del_ambig_split(self):
        '''
        our code is set up such that a word can be split in different
        ways, ultimately there can only be one way
        '''
        dct = {}
        b = 0
        for k, v in self.word2morph.items():
            if len(v) > 1:
                b += 1
                obj = self.manual.get(k)
                if obj:
                    self.word2morph[k] = obj
                else:
                    dct[k] = v
            else:
                tpl = list(v)[0]
                self.word2morph[k] = tpl
        if dct:
            assert 0

    def get_more_real_stems(self):
        for k, v in self.manual.items():
            vu = self.parse_morpheme(v[1])
            if vu not in self.pref:
                self.true_fake_stem.add(v[1])
        for k, v in self.double2prefix.items():
            vu = self.parse_morpheme(v[1])
            if vu not in self.pref:
                self.true_fake_stem.add(v[1])
        for k, v in self.word2end.items():
            vu = self.parse_morpheme(v[1])
            if vu not in self.pref and k not in self.dimin:
                self.true_fake_stem.add(v[1])

    def parse_morpheme(self, w):
        return re.sub(r'0-9', '', w)


    def rank_lemmas(self):
        dct = sort_dct_val_rev(self.lem_freq_crude)
        b = 0
        dct1 = {}
        for k,v in dct.items():
            dct1[k] = b
            b += 1
        for k,v in self.declinable.items():
            ku = cut_num(k)
            v['rank'] = dct1.get(ku,99_000)


    def popular_words(self):
        for k, v in self.declinable.items():
            if v['rank'] < 8_000:
                self.popular.add(norm_str_jv(v['lemma']))

    def large_endings(self):
        dct = defaultdict(dict)
        for i in range(2, 5):
            dct1 = defaultdict(set)
            dct2 = defaultdict(int)
            for k, v in self.word2end.items():
                s = v[0]
                if len(s) > i + 1:
                    suff = s[-i:]
                    dct1[suff].add(k)
                    dct2[suff] += 1
            dct2 = sort_dct_val_rev(dct2)
            dct3 = {}
            for k in dct2.keys():
                dct3[k] = dct1[k]
            dct[i] = dct3

    def research_failed_fakes(self):
        # 11711 - fake 17638
        # 12559 - fake 16790
        # fake stems - 2481, real words = 12559
        # fake stems - 1497, real words = 18040
        error = {}
        dct = defaultdict(int)
        for k, v in self.temp_word2morph.items():
            v = list(v)[0]
            mid = v[1]
            dct[mid] += 1
            self.temp_word2morph[k] = v

        c = 0
        for k, v in dct.items():
            if v > 1 and reg(r'[aeiouy]', k):
                c += 1
        p(c, len(self.word2morph))

        for k, v in self.temp_word2morph.items():
            mid = v[1]
            if dct[mid] > 1:
                self.word2morph[k] = v
            else:
                self.failed_fakes.add(k)
                self.bachelors.add(k)

        return


    def add2dcts(self, end, word):
        if self.temp_real_stem:
            tpref = self.temp_real_stem[0]
            stem = self.temp_real_stem[1]
            self.word2morph[word].add((tpref, stem, end))

        elif self.temp_fake_stem:
            tpref = self.temp_fake_stem[0]
            stem = self.temp_fake_stem[1]
            self.temp_word2morph[word].add((tpref, stem, end))
        if tpref + stem + end != word:
            bb = 8

    def get_non_stems(self):
        '''
        this is an ad hoc list of stems and non-stems,
        i forget where it came from but currently it works
        as a good filter
        '''

        lst = to.from_txt2lst_tab_delim(f'{fold}stems', 1, 1)
        for l in lst:
            if l[0][0] == ';':
                self.not_stem.add(l[0][1:])
            elif l[0][0] == '#':
                s = l[0][1:]
                l2 = vgf.strip_n_split(s, '+')
                x = l2[0]
                y = l2[1]
                if x in self.declinable:
                    self.isalt[y] = x
                elif y in self.declinable:
                    self.isalt[x] = y
            elif len(l) > 1:
                w = l[0]
                w = self.chop_stem(w)
                self.true_fake_stem.add(w)
            else:
                w = l[0]
                w = self.chop_stem(w)
                self.true_fake_stem.add(w)

        return


class process_stem_lst(top):
    def __init__(self):
        top.__init__(self)

    def main_loop(self, kind='', lst=[]):
        lst1 = []
        if kind == 's':
            lst = to.from_txt2lst(f'{fold}stem_lst', 1, 1)
            lst1 = to.from_txt2lst(f'{fold}manual_stems')
            lst += lst1
        elif kind == 'd':
            lst = to.from_txt2lst(f'{fold}check_doubles', 1, 1)

        self.pre = 1
        self.on = 0
        self.kind = kind
        self.strong = 0
        self.medium = 0
        self.word = ''
        self.is_stem = 0
        self.root_wo_num = ''
        self.no_end = set()

        '''
        removing the * at the end of a word since it does't mean
        anything and is hard to code
        '''
        for e, x in en(lst):
            if '* -- ' in x:
                idx = x.index('*')
                lst[e] = delete_at_i(idx, x)

        for e, x in en(lst):
            if 'paratio' in x:
                bb = 8
            self.end2 = ''

            if x == 'zzz':
                '''
                on the stem_lst sheet the roots before zzz the words end with the root
                after zzz the words start with the root
                '''
                self.pre = 0

            elif x[0] == '/':
                pass
            elif x in lst1:
                # these are the ad hoc manual divisions
                self.word = x
                self.use_slash()

            elif x.isdigit():
                pass

            elif self.kind == 'r' and x.startswith('__') \
                    and x.endswith('#'):
                self.on = 0
                self.not_morpheme.add(x[2:-1])

            elif x.startswith('__'):
                # if it goes in here then it is a root
                if x.endswith('$'):
                    x = x[:-1]
                elif x.endswith('%'):
                    x = x[:-1]
                    self.ie_root.append(x[2:-1])

                elif x.endswith('__') and not self.kind == 'd':
                    x = x[:-2]

                elif x.endswith(')'):
                    idx = x.index(' ')
                    ot = x[idx:].strip()
                    x = x[:idx]
                    self.irr_notes[x[2:]] = ot

                if '=' in x:
                    lst2 = x.split('=')
                    self.alt_morph[lst2[0][2:]] = lst2[1]
                    x = lst2[0]

                self.on = 1
                if not self.is_stem and e > 1 and not self.kind == 'd':
                    self.not_stem.add(self.root.replace('__', ''))

                self.is_stem = 0
                x = x[2:]
                self.strong = 0
                self.medium = 0
                if x.endswith('*'):
                    self.strong = 1
                    x = x[:-1]

                elif x.endswith('>'):
                    x = x[:-1]
                    self.medium = 1
                    self.dubious.add(x)

                elif not self.kind == 'r':
                    self.on = 0
                    self.not_stem.add(x.replace('__', ''))  # 382
                if self.kind == 'd':
                    x = x[:-2]

                self.root = x
                self.root_wo_num = self.root
                if self.root[-1].isdigit():
                    self.root_wo_num = self.root[:-1]


            elif x[-1] == '@':
                # below here we handle words
                self.word = x[:x.index(' ')]
                self.non_lemma.add(self.word)

            elif x[-1] == '#':
                self.word = x[:x.index(' ')]
                self.not_compound.add(self.word)

            elif reg(r'^[a-z//]*\s--', x):
                self.word = x[:x.index(' ')]
                if self.word == 'credulus':
                    bb = 8

                if x.endswith('cc'):
                    self.isproper.add(self.word)  # 1

                elif not self.conditions_psl(self.word):
                    pass

                elif not self.on and self.kind == 'r':
                    self.not_compound.add(self.word)


                elif self.kind == 'd' and (x[-1] == '$' or self.strong):
                    suff = self.word[len(self.root):]
                    self.double2prefix[self.word] = (self.root, suff)

                elif '/' in self.word:
                    self.use_slash()

                elif not self.on and '/' not in self.word:
                    pass
                else:
                    self.is_stem = 1
                    self.num = ''
                    self.tstrong = -1
                    if x[-1].isdigit():
                        self.num = x[-1]
                    elif x[-1] == ')':
                        pass
                    elif x[-1] == '*':
                        self.tstrong = 1
                    elif x[-1] == '>':
                        self.tstrong = 0
                        if x[-2].isdigit():
                            self.num = x[-2]

                    if x[-1] == '?':
                        # these are words that we're
                        # unsure of if they contain a morpheme
                        # i think at the moment nothing is going in here
                        self.add2umorphemes()
                    else:
                        self.divide_word()


        lst = ['no_end', 'root_wo_num']
        for x in lst:
            delattr(self, x)
        return

    def conditions_psl(self, w):
        w = w.replace('/', '')
        if w in self.dimin:
            return 0
        if w in self.isalt:
            return 0
        if w not in self.declinable:
            return 0
        return 1

    def get_end(self):
        self.end2 = self.word2end.get(self.word)
        if self.end2 == None:
            self.no_end.add(self.word)
            self.end2 = ''
        else:
            self.end2 = self.end2[1]




    def use_slash(self):
        '''
        if self.medium = 1 then the final is a mere suffix
        whereas if self.strong = 1 then the final is a stand alone word

        '''

        triple = 0
        mid = ''
        lsuf = ''
        quad = 0
        lst = self.word.split('/')
        if self.word.count('/')>2:
            quad = 1

        elif self.word.count('/') > 1:
            triple = 1
        self.initial = f'{lst[0]}'

        if quad:
            self.initial = lst[0]
            mid = f'{lst[1]}'
            self.final = f'{lst[2]}'
            self.end2 = f'{lst[3]}'

        elif triple:
            mid = f'{lst[1]}'
            self.final = f'{lst[2]}'
        else:
            self.final = f'{lst[1]}'

        self.word = self.word.replace('/', '')
        if not quad:
            self.get_end()
            if self.end2:
                self.final = self.cut_off_suffix(self.final, self.end2)

        if quad:
            self.word2morph[self.word].add((self.initial, mid, self.final, self.end2))

        elif triple:
            self.word2morph[self.word].add((self.initial, mid, self.final, self.end2))
        else:
            self.word2morph[self.word].add((self.initial, self.final, self.end2))

        if self.medium:
            self.endings2[self.final[1:]].append(self.word)
        self.add2manual(mid)


    def add2manual(self, mid):
        if mid:
            self.manual[self.word] = (self.initial, mid, self.final, self.end2)
        else:
            self.manual[self.word] = (self.initial, self.final, self.end2)


    def add2umorphemes(self):
        '''
        these are morphemes that i'm not very certain of
        '''
        pass
        # self.umorphemes[self.initial + "-"].add(self.word)

    def divide_word(self):
        '''
        some very bad code.  the problem with this method is that i did
        not have a system going when i built the sheets stem_lst, check_reals etc
        if the word begins with a root then it is relatively easy to divide the word
        but if the word does not begin with a root then it is quite hard
        in some cases the root contains the ending of the word
        in other cases there are some letters between the root and the ending
        in other cases the root + the ending compose the end of the word
        '''

        self.get_end()
        lsuf = ''
        if self.word.startswith(self.root_wo_num):
            rest = self.get_suffix(self.word, self.root_wo_num)
            final2 = self.cut_off_suffix(rest, self.end2)
            final = final2
            initial = self.root_wo_num
            initial2 = self.root
        else:
            initial = self.word[:self.word.index(self.root_wo_num)]
            initial2 = initial
            s = self.root_wo_num + self.end2
            su = initial + s

            if su == self.word:
                # in this case the word is already properly divided
                final = self.root_wo_num
            else:
                if len(su) > len(self.word):
                    # here the root and the ending overlap
                    mid = self.word[len(initial):-len(self.end2)]
                    lsuf = self.get_suffix(mid, self.root_wo_num)
                    final = self.root_wo_num

                    v = initial + mid + lsuf
                    if v == self.word:
                        # here the ending was not obtained
                        vnew = self.cut_off_suffix(v, self.end2)
                        if vnew == self.end2:
                            # here the root + lsuf = end of the word
                            if not lsuf:
                                if self.num:
                                    assert 0
                                else:
                                    final = self.cut_off_suffix(self.root_wo_num, self.end2)
                            else:
                                assert 0
                        else:
                            if vnew == self.root_wo_num:
                                final = self.root_wo_num
                            else:
                                lsuf = self.get_suffix(vnew, self.root_wo_num)

                    else:
                        if initial + mid + lsuf + self.end2 == self.word:
                            final = mid
                        else:
                            assert 0
                else:
                    if not self.end2 and not self.word.endswith(self.root_wo_num):
                        # here the ending is not obtained and the word does not end with the root
                        v = initial + self.root_wo_num
                        lsuf = self.get_suffix(self.word, v)
                        final = self.root_wo_num
                    else:
                        # here there are some letters between the root and the ending
                        mid = self.word[len(initial):-len(self.end2)]
                        lsuf = self.get_suffix(mid, self.root_wo_num)
                        final = self.root_wo_num

            final2 = final + self.num

        if not final:
            self.no_final[self.word] = (initial, self.end2)
            return

        if self.word != f"{initial}{final}{lsuf}{self.end2}":
            bb = 8

        self.word2morph[self.word].add((initial2, final2, lsuf, self.end2))



class stems(process_stem_lst, use_prefixes):
    def __init__(self):
        process_stem_lst.__init__(self)
        use_prefixes.__init__(self)

    def change_spelling(self):
        '''
        this changes the macrons on a few words but this step will
        soon be obsolete anyway since we will soon use more
        sophisticated methods to determine vowel length

        '''

        self.spell_change = {}
        lst = to.from_txt2lst_tab_delim(f'{fold}mispellings', 1, 1)
        for l in lst:
            self.spell_change[l[0]] = l[1]

        for x, y in self.spell_change.items():
            self.co_lemmas4[x]['lemma'] = y

        # for x, ins in self.def_lemmas.items():
        #     if ins.pos == 'v' and ins.macron[-1] == 'o':
        #         ins.macron = f'{ins.macron[:-1]}ō'
        #     elif reg(r'o\d$', ins.macron):
        #         ins.macron = replace_at_i(len(ins.macron) - 2, ins.macron, 'ō')

        return

    def get_declinable(self):
        '''
        we are now only interested in finding the roots of
        declinable words, nouns, verbs and adjectives, ignoring adverbs for now.
        we also ignore some words that belong to specific modules
        '''

        for x, y in self.co_lemmas4.items():
            if y['model'] in ['eo', 'fio', 'do', 'aio', 'duo', 'deni']:
                pass
            elif y['pos'] in ['n', 'v', 'a'] and not y['capital']:
                self.declinable[x] = y



    def cut_off_ending(self):
        '''
        we here separate the ending from the rest of the word.
        we are not here concerned with large endings such as -mentum
            in the word argumentum, rather just the um part.
        the verbs are rather straightforward.

        some nouns are a little hard to deal with.  for most we
        take the latters in the nominative singular which undergo
        change in the other declensions.  for some nouns this does
        not work. in this case we take the number in des key in the
        model dictionary, the first member and subtract one from it,
        that is how many letters we cut off at the end.  this algorithm
        works find for

        our algorithm works fine for: pulcher, corpus, animal, miser
            miles_ium+, puer, infans

        for reasons unknown to me, the number for the following models was wrong though
            they still decline correctly

            for facilis, fortis, civis_um, civis3, civis2, civis4, acer, miles_s the last 2 letters are cut off

        for those we substract the last two letters.

        for miles we had to find the stem in an ad hoc manner

        there are a few words in civis where the final letters can be
        cut off but not many.  ignore these for now
        todo find stems in the civis model

        '''

        dct = defaultdict(list)
        for k, v in self.co_lemmas4.items():
            if k.startswith('maximus2'):
                bb = 8

            if not v['capital'] and v['pos'] in ['a', 'v', 'n']\
                    and v['model'] not in ['prcum','se']:
                mod = self.mmodels[v['model']]
                w = cut_num(k)
                if v['pos'] == 'v':
                    found = 1
                    l2 = w[-2:]
                    l1 = w[-1]
                    if l2 == 'or':
                        stem = w[:-2]
                        end = 'or'
                    elif l1 == 't':
                        stem = w[:-2]
                        end = w[-2:]
                    elif l1 in ['o', 'i']:
                        stem = w[:-1]
                        end = l1

                    elif l1 == 'm':
                        stem = w
                        end = ""
                    else:
                        '''only a few haplaxes go in here'''
                        found = 0

                else:
                    if '_pl' in v['model'] or v['model'] in ['nos','uos']:
                        lst = mod['des'][7]
                    elif v['pos'] == 'a':
                        lst = mod['des'][13]
                    else:
                        lst = mod['des'][1]
                    found = 0
                    should = 0
                    for t in lst:
                        for x in t[1]:
                            if x:
                                should = 1
                                xu = unidecode(x)
                                if v['lemma'].endswith(xu):
                                    stem = w[:-len(xu)]
                                    end = xu
                                    found = 1
                                    break
                            else:
                                found = 1
                                if v['model'] == 'miles':
                                    stem, end = self.stem_miles(w)

                                elif t[0] == '0':
                                    stem = w
                                    end = ''
                                elif v['model'] in ['uetus', 'plus', 'miles_g', 'civis']:
                                    stem = w
                                    end = ''


                                elif v['model'] in ['facilis', 'fortis', 'civis_um', 'civis3', 'civis2', 'civis4', 'acer',
                                                 'miles_s']:
                                    stem = w[:-2]
                                    end = w[-2:]
                                else:
                                    stem = w[:-(int(t[0]) - 1)]
                                    end = w[-(int(t[0]) - 1):]
                                break

                        if not found and should:
                            dct[v['model']].append(v)
                if found:
                    if end and not v['lemma'].endswith(end):
                        bb = 8

                    self.word2end[w] = [stem, end]

        return

    def stem_miles(self, w):
        try:
            l3 = w[-3:]
        except:
            l3 = ''
        try:
            l2 = w[-2:]
        except:
            l2 = ""
        try:
            l4 = w[-4:]
        except:
            l4 = ""

        if l4 in ['tudo', 'trix']:
            return w[:-4], l4

        if l3 in ['tio', 'tor', 'tas', 'fex']:
            return w[:-3], l3

        if l2 in ['io', 'or']:
            return w[:-2], l2

        return w, ""

    def elim_diminutives1(self):
        '''
        todo code for ittus
        -lus
            -ulus, -ula, -ulum, e.g. globulus (globule) from globus (globe).
    -culus, -cula, -culum, e.g. homunculus (so-small man) from homo (man)
    -olus, -ola, -olum, e.g. malleolus (small hammer) from malleus (hammer)
    -ellus, -ella, -ellum, e.g. libellus (little book) smaller than librulus (small book) from liber (book)
    -ittus, -itta, -ittum (hypocoristic, a doublet of -itus)
        '''

        dct = {
            'uncula': ['o'],
            'unculus': ['o'],
            'ellus': ['er', 'a', 'us', 'ulus'],
            'ellum': ['rum'],
            'ella': ['a'],
            'icula': ['us', 'a'],
            'ulum': ['um', 'a', 'e'],
            'olus': ['us'],
            'olum': ['um'],
            'ola': ['a'],
            'ole': ['um'],
            'ulus': ['us', 'a', 'e', 'o'],
            'ula': ['a', 'e'],
        }
        dct1 = {
            'uncula': 'a',
            'unculus': 'us',
            'ellus': 'us',
            'ellum': 'um',
            'ella': 'a',
            'icula': 'a',
            'ulum': 'um',
            'olus': 'us',
            'olum': 'um',
            'ola': 'a',
            'ole': 'e',
            'ulus': 'us',
            'ula': 'a',
        }

        self.dimin = {}
        for k, v in self.declinable.items():
            found2 = 0
            for x, y in dct.items():
                if found2:
                    break
                if k.endswith(x):
                    for t in y:
                        ku = k[:-len(x)] + t
                        if ku in self.co_lemmas4:
                            if k == 'naulum':
                                bb = 8

                            found2 = 1
                            initial = self.cut_off_suffix(k, x)
                            end = dct1[x]
                            lsuf = self.cut_off_suffix(x, end)
                            self.word2morph[k].add((initial, lsuf, end))
                            self.dimin[k] = ku
                            break

        return

    def elim_diminutives2(self):
        '''
        todo further split diminutives
        do this later, some diminutives can be further split

        '''

        for k, v in self.dimin.items():
            obj = self.word2morph.get(v)
            parent = self.word2morph.get(v)
            if parent:

                to_add = []


        return




class bottom(stems):
    def __init__(self):
        stems.__init__(self)

    def begin_st(self):
        p ('now dividing words into morphemes')
        '''
        the methods get_endings, ana_homop and permutations might
            still be useful

        '''

        self.kind = 'l'
        self.get_atts()
        self.change_spelling()
        self.get_declinable()
        self.cut_off_ending()
        self.get_non_stems()
        self.elim_diminutives1()
        self.main_loop('d')
        self.main_loop('s')
        self.main_loop('r', self.real_check)
        self.begin_up()
        self.elim_diminutives2()
        self.output()
        return

    def output(self, kind=0):
        '''
        work must still be done on diminutives
        the manual attribute represents words which have
        been already verified
        the not_compound attribute contains words that are not compound
            but of course contain an ending
        the double prefix contains all words  which contain
            a double prefix

        '''
        pi.save_pickle(self.word2morph, f'{fold}word2morph')
        pi.save_pickle(self.double2prefix, f'{fold}double2prefix')





        return


    def contains_prefix(self):
        for k,v in self.word2morph.items():
            pass






if eval(not_execute_on_import):
    if vgf.pycharm():
        args = [0, 'me', '', 'IX', '', 0, 0]
    else:
        args = vgf.get_arguments()

    if args[1] == 'me':
        ins = bottom()
        ins.begin_st()
    elif args[1] == 'psl':
        ins = process_stem_lst()
        ins.main_loop()
