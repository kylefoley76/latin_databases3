from collections import ChainMap
from bglobals import *
if not public:
    from i_scrape_old import old_entry
from j_lasla import convert2txt
from c_colat4 import bottom_most_a4


'''
occido3 = occidoō
sallio,salio = to salt, is missing though it might have been deleted because it has the same form
in salio2 it gets conjugated as saliio

about 10 of the lemmas in lasla are capitalized
unabbreviate words
enclose aux in ( )
unenclose non aux
remove < >
remove space words
some lines have two spaces
put aux on a different line
add ft.sg and locative adjectives
add more lemmas
change -um adjectives to -us
handle abbreviated s
handle bogus pos
perhaps replace numbers with spoken
handle alternative spellings
handle greek words
insert punctuation
research disagreement in conjugation
'''


def uncommon_lems():
    st = set()
    st2 = set()
    for x in self.all_lems:
        y, num = cut_num(x, 1)
        if num in ['8', '9']:
            st2.add(x)
        elif y not in self.lem2forms:
            st.add(y)


def is_proper2(word):
    if len(word) > 1 and word[0] in ['N', 'A']:
        if word[1].isupper():
            if len(word) > 2:
                word = word[1:]

    return word


def lasla_non_bad_hash_words(hash_words):
    '''
    to determine if the words whose pos is marked # or 0 we compare
    them to the words whose pos is actually marked.
    the list is not entirely accurate because words with <>
    in them got counted twice
    '''
    las_freq = pi.open_pickle(f'{fold}las_freq', 1)
    dct = defaultdict(int)
    for k, v in las_freq.items():
        word = k[1]
        word = re.sub(r'<.*>', '', word)
        word = word.strip()
        word = is_proper2(word)
        dct[word] += v
    dct1 = {}
    for k in hash_words:
        k = is_proper2(k)
        dct1[k] = dct.get(k, 0)

    dct1 = sort_dct_val_rev(dct1)
    illegit_words = []
    legit_words = []
    for k, v in dct1.items():
        if v < 4:
            illegit_words.append(k)
        else:
            legit_words.append(k)
    to.from_lst2txt(legit_words, f'{fold}lasla_legit_words', 1)
    to.from_lst2txt(illegit_words, f'{fold}lasla_illegit_words', 1)

    for k, v in self.las_freq_old.items():
        if k[1] == 'NCereris':
            p(k[0])


def fake_enclitics_lasla():
    lem2forms_pos = pi.open_pickle(f'{fold}lem2forms_pos_ab', 1)
    enclit = to.from_txt2lst(f'{fold}reference/enclitics')
    enclit.remove('st')
    enclit.remove('ue')
    fake_enclitics = defaultdict(dict)
    b = 0
    for x, y in lem2forms_pos.items():
        b += 1
        vgf.print_intervals(b, 100, len(lem2forms_pos))
        for pos, dct in y.items():
            for lem, dct2 in dct.items():
                dct2 = dct2[0]
                for num, lsts in dct2.items():
                    pos = lsts[1]
                    words = lsts[0]
                    for word in words:
                        wordu = norm_str_jv(word)
                        if reg(r'[aeioum]st$', wordu):
                            fake_enclitics['st'].setdefault(wordu, []).append((x, pos))
                        else:
                            for en in enclit:
                                if word.endswith(en):
                                    fake_enclitics[en].setdefault(wordu, []).append((x, pos))

    for en, words in fake_enclitics.items():
        for word, lst in words.items():
            dct = defaultdict(list)
            for x in lst:
                dct[x[0]].append(x[1])
            fake_enclitics[en][word] = dct

    pi.save_pickle(fake_enclitics, f'{fold}fake_enclitics_lasla', 1)


class topmost:
    def __init__(self):
        pass

    def get_atts_mcl(self, kind=0):
        if kind < 1:
            p('opening pickles')
            # self.lem2forms = pi.open_pickle(f'{sfold}lem2forms_ab', 1)
            # self.lem2forms_pos = pi.open_pickle(f'{sfold}lem2forms_pos_ab', 1)
            self.lem2forms_pos = pi.open_pickle(f'{fold}lem2forms_pos', 1)
            self.co_lemmas4 = pi.open_pickle(f'{fold}co_lemmas4', 1)
            # self.mlem_num = pi.open_pickle(f'{sfold}mlem_num_ab', 1)
            self.las_freq = pi.open_pickle(f'{fold}las_freq', 1)
            self.fake_enclitics = pi.open_pickle(f'{fold}fake_enclitics', 1)
            self.lemma2decl = pi.open_pickle(f'{fold}lemma2decl', 1)
            if public:
                self.old_wonum = pi.open_pickle(f'{fold}old_wonum_public', 1)
            else:
                self.old_wonum = pi.open_pickle(f'{fold}old_wonum', 1)
            self.old_homonyms = pi.open_pickle(f'{fold}old_homonyms', 1)
            self.old_variants = pi.open_pickle(f'{fold}old_variants')

            p('done opening')
            self.num_lems = defaultdict(dict)
            self.all_lalems = defaultdict(dict)
            self.prop_lalems = defaultdict(dict)
            self.llem2clem = defaultdict(dict)
            self.extra_llems = defaultdict(list)
            self.redundant_map = {}
        if kind < 2:
            self.extra_clems = defaultdict(list)
            self.cambig_nl_by_hand = []
        self.llem2clem_old = pi.open_pickle(f'{fold}llem2clem')
        self.clem_errors = defaultdict(dict)
        self.fixm_lems = pi.open_pickle(f'{fold}fixm_lems')
        self.shared_forms = pi.open_pickle(f'{fold}shared_forms')
        self.missing5 = set(to.from_txt2lst(f'{fold}missing5'))
        self.missing6 = set(to.from_txt2lst(f'{fold}missing6'))
        self.still_missing = set(to.from_txt2lst(f'{fold}still_missing'))
        del self.lem2forms_pos['fides']['n']['2']
        self.noun2gender = {}
        self.lem2forms_rev = {}
        self.wrong_pos = {}
        self.ui_models = pi.open_pickle(f'{fold}ui_models')

    def get_atts_sm(self):
        self.forms = defaultdict(dict)
        self.lem2forms_pos = pi.open_pickle(f'{fold}lem2forms_pos', 1)
        self.old_wonum = pi.open_pickle(f'{fold}old_wonum', 1)
        self.old_wdef = pi.open_pickle(f'{fold}old_wdef', 1)
        self.old_homonyms = pi.open_pickle(f'{fold}old_homonyms', 1)
        self.old_variants = pi.open_pickle(f'{fold}old_var2parent', 1)
        self.missing_old_lemmas = pi.open_pickle(f'{fold}missing_old_lemmas', 1)
        self.all_lalems = pi.open_pickle(f'{fold}all_lalems', 1)
        self.clemmas = pi.open_pickle(f"{fold}clemmas", 1)
        self.alt_spellings = pi.open_pickle(f"{fold}alternative_spellings", 1)
        self.found = set()
        self.lem2forms_set = pi.open_pickle(f'{fold}lem2forms_set')
        self.missing = to.from_txt2lst(f'{fold}still_missing')
        '''
        for some reason the still_missing were not being included into
        the missing
        
        '''
        return

    def get_atts_pm(self):
        self.lasla_db2 = pi.open_pickle(f'{fold}lasla_db2', 1)
        self.las_freq_old = pi.open_pickle(f'{fold}las_freq', 1)
        self.llem2clem = pi.open_pickle(f'{fold}llem2clem', 1)

    def short_cut(self, kind=0):
        if kind == 0:
            lst = pi.open_pickle(f'{fold}match_colwas_atts')
            lst1 = ['lemma2decl', 'lem2forms_pos', 'ambig_lalems', 'lalems_pos',
                    'done_la', 'llem2clem', 'all_lalems', 'done_co', 'mlem_num',
                    'old_homonyms', 'unambig_lalems']
            for x, y in zip(lst, lst1):
                setattr(self, y, x)
            self.get_atts_mcl(1)

    def output(self, kind=0):
        if kind == 2:
            lst = []
            for k, v in self.word2nmod.items():
                b = ''
                c = ''
                if k in self.final_roots:
                    b = self.final_roots[k].get('1', '')
                    c = self.final_roots[k].get('2', '')

                lst1 = [k, v, b.lower(), c.lower()]
                lst.append(lst1)
            file = f'{fold}new_mods4colat'
            to.from_lst2txt_tab_delim(lst, file)
            vgf.open_txt_file(file)

        if kind == 5:
            lst = [self.all_lalems, self.prop_lalems]
            pi.save_pickle(lst, f'{fold}lalems2forms')
            # pi.save_pickle(self.lalems2forms2, f'{sfold}lalems2forms2')
            # pi.save_pickle(self.lalems2forms3, f'{sfold}lalems2forms3')
        if kind == 7:
            pi.save_pickle(self.llem2clem, f'{fold}llem2clem', 1)

        if kind == 6:
            pi.save_pickle(self.las_freq, f'{fold}las_freq2', 1)

        if kind == 9:
            ## figure out why # is in the lemmas

            p('saving pickles')
            pi.save_pickle(self.llem2clem, f'{fold}llem2clem')
            pi.save_pickle(self.noun2gender, f'{fold}lasla_noun2gen', 1)
            pi.save_pickle(self.lem2forms_rev, f'{fold}lem2forms_rev')
            pi.save_pickle(self.lem2forms_rev_jv, f'{fold}lem2forms_rev_jv')
            pi.save_pickle(self.las_freq, f'{fold}las_freq2')
            pi.save_pickle(self.las_lem_freq, f'{fold}las_lem_freq')
            pi.save_pickle(self.miss_col_pos, f'{fold}miss_col_pos')
            pi.save_pickle(self.missing_proper2, f'{fold}missing_proper2')

        if kind == 10:
            pi.save_pickle(self.found, f'{fold}fixm_lems')
            pi.save_pickle(self.shared_forms, f'{fold}shared_forms')


class get_all_variants(topmost):
    def __init__(self):
        topmost.__init__(self)

    def begin_gv(self):
        pass

    def get_variants_fu(self):
        self.lem2alt = {}
        for k, v in self.lalems_pos_rev.items():
            for pos, dct in v.items():
                for num, pdct in dct.items():
                    clem = self.llem2clem[l][num]
                    cobj = self.co_lemmas4.get(clem)
                    mod = cobj['model']
                    for pos2, tpls in pdct.items():
                        root = 0
                        root2freq = defaultdict(int)
                        endings = []
                        for tpl in tpls:
                            word = tpl[0]
                            freq = tpl[1]
                            for end in endings:
                                if word.endswith(end):
                                    beg = word[:-len(end)]
                                    root2freq[(root, beg)] += freq


class handle_still_missing(get_all_variants):
    def __init__(self):
        get_all_variants.__init__(self)

    def begin_fm(self, kind=0):
        '''
        all of these words are found in lasla but not in collatinus
        as such after their meanings are found, their models
        will be calculated
        '''

        self.get_atts_sm()
        self.get_ass()
        self.use_wonum()
        self.use_old_variants()
        self.use_pre_participle()
        delattr(self, 'lem2forms_pos')
        self.use_assmilation()
        self.quick_fix()
        if kind == 2:
            self.link2parent()
        else:
            self.use_distance()
            self.output(10)

    def use_pre_participle(self):
        c = 0
        d = 0
        self.verb2slemma = {}
        self.plural_of = {}
        for x, y in self.lem2forms_pos.items():
            for k, v in y.items():
                if k == 'v':
                    for t, dct in v.items():
                        dct1 = dct[0]
                        for i in [213, 219, 225, 261, 267, 303, 339, 309]:
                            word = dct1.get(i)
                            if word:
                                word = word[0][0]
                                wordu = norm_str_jv(word)
                                if wordu in self.missing:
                                    self.forms['subverb'][wordu] = [x, i]
                                    self.missing.remove(wordu)
                                    self.found.add(wordu)
                                    c += 1
                                else:
                                    wordu2 = self.assimil2(wordu, self.missing)
                                    if wordu2:
                                        self.missing.remove(wordu2)
                                        self.forms['subverb2'][wordu2] = [x, i]
                                        self.found.add(wordu2)
                                        c += 1
                elif k == 'n':
                    for t, dct in v.items():
                        dct1 = dct[0]
                        word = dct1.get(7)
                        if word:
                            word = word[0][0]
                            wordu = norm_str_jv(word)
                            if wordu in self.missing:
                                self.forms['plural_of'][wordu] = x
                                d += 1
                                self.missing.remove(wordu)
                                # self.verb2slemma[x] = wordu
                                self.found.add(wordu)
                                break
        p(c)
        p(f'{d} plurals')
        return

    def get_alt_lems(self):
        dct7 = pi.open_pickle(f'{fold}mac_lemmas_new', 1)
        st = set()
        alt_lemmas = defaultdict(list)
        for x, y in dct7.items():
            if y['quantity']:
                lst = y['quantity'].split()
                for z in lst:
                    zu = norm_str_jv(z, 1)
                    if zu != y['wo_num']:
                        alt_lemmas[zu].append(y)
                    st.add(zu)
            else:
                st.add(y['wo_num'])
        pi.save_pickle(st, f'{fold}clemmas', 1)
        pi.save_pickle(alt_lemmas, f'{fold}alternative_spellings', 1)

    def get_ass(self):
        dct7 = {x: 1 for x in self.missing_old_lemmas}
        old_wonum_cm = ChainMap(self.old_wonum, dct7)
        self.all_old = set(old_wonum_cm.keys())
        self.in_old_wonum = {}
        self.old_wonum_cm = old_wonum_cm

        self.to_assimilate = {}
        lst = to.from_txt2lst(f'{fold}assimilations')
        ass = {x.split(":")[0]: x.split(":")[1] for x in lst if x[0] != '!'}
        ass = {unidecode(k): unidecode(v) for k, v in ass.items()}
        ass2 = {v: k for k, v in ass.items()}
        self.ass = merge_2dicts(ass, ass2)

    def use_assmilation(self):
        to_del = []
        c = 0
        for k in self.missing:
            nword = self.assimil2(k, self.clemmas)
            if nword:
                self.forms['ass'][k] = nword
                to_del.append(k)
                self.found.add(k)
                c += 1
        p(c)
        for x in to_del:
            self.missing.remove(x)

        return

    def assimil2(self, k, target):
        if len(k) > 3:
            for i in range(4, 1, -1):
                beg = k[:i]
                if len(k) > i and beg in self.ass:
                    s = self.ass[beg]
                    nword = f'{s}{k[i:]}'
                    if nword in target:
                        return nword
        return

    def quick_fix(self):
        b = 0
        to_remove = set()
        for x in self.missing:
            self.quick_fix2(x, to_remove)
            b += 1
        p(f'removed {len(to_remove)} using quick fix')
        for x in to_remove:
            self.found.add(x)
            self.missing.remove(x)
        return

    def quick_fix2(self, k, to_remove):
        if k.endswith('or') and k[:-1] in self.all_old | self.clemmas:
            to_remove.add(k)
            self.forms['_or'][k] = k[:-1]
        elif k.endswith("um") and f'{k[:-1]}s' in self.all_old | self.clemmas:
            to_remove.add(k)
            self.forms['_um_us'][k] = f'{k[:-1]}s'

        elif k.endswith("e") and f'{k[:-1]}is' in self.all_old | self.clemmas:
            to_remove.add(k)
            self.forms['_e'][k] = f'{k[:-1]}is'


        elif k.endswith("e") and f'{k[:-1]}us' in self.all_old | self.clemmas:
            to_remove.add(k)
            self.forms['_e2'][k] = f'{k[:-1]}us'


        elif k.endswith("i") and f'{k[:-1]}us' in self.all_old | self.clemmas:
            to_remove.add(k)
            self.forms['_i'][k] = f'{k[:-1]}us'

        elif k.endswith("i") and f'{k[:-1]}is' in self.all_old | self.clemmas:
            to_remove.add(k)
            self.forms['_i2'][k] = f'{k[:-1]}is'

        elif k.endswith("a") and f'{k[:-1]}um' in self.all_old | self.clemmas:
            to_remove.add(k)
            self.forms['_a'][k] = f'{k[:-1]}um'

        elif k.endswith("a") and f'{k[:-1]}us' in self.all_old | self.clemmas:
            to_remove.add(k)
            self.forms['_a2'][k] = f'{k[:-1]}us'

        elif k.endswith("ae") and f'{k[:-2]}a' in self.all_old | self.clemmas:
            to_remove.add(k)
            self.forms['_ae'][k] = f'{k[:-1]}a'

    def link2parent(self):
        llem2clem = pi.open_pickle(f"{fold}llem2clem2", 1)

        miss = set()
        miss2 = set()
        miss3 = set()
        misso = set()
        dct3 = defaultdict(set)
        self.child2parent = {}
        for form, dct in self.forms.items():
            for child, parent in dct.items():

                if form == 'old_var':
                    vals = list(parent.values())
                    s = ';'.join(vals)
                    form2 = form
                elif form == 'old':
                    vals = []
                    for x, y in parent.items():
                        vals.append(y.olemma)
                    s = ';'.join(vals)
                    form2 = form


                else:
                    if form == 'subverb2':
                        num = parent[1]
                        s = parent[0]
                        form2 = f'{form}_{num}'

                    elif form == 'subverb':
                        num = parent[1]
                        s = parent[0]
                        form2 = f'{form}_{num}'
                    else:
                        form2 = form
                        s = parent
                    obj = llem2clem.get(s)
                    if obj:
                        lst2 = []
                        for s, t in obj.items():
                            pass

                    else:
                        miss.add(s)
                        if s not in self.all_old:
                            miss2.add(s)
                            if s not in self.clemmas:
                                miss3.add(s)

                self.child2parent[child] = [form2, s]
        return

    def use_distance(self, kind=0):
        unused_old = self.all_old - self.found
        unused_col = self.clemmas - self.found
        unused_col = unused_col - unused_old
        word2di = {}
        shares = defaultdict(set)
        p('now using the distance method')
        b = 0
        for k in self.missing:
            dct = {}
            words = set()
            forms = self.all_lalems[k]
            for s, t in forms.items():
                for u in t:
                    words.add(u[0].replace(' ', ''))
            got = 0
            for x in unused_old:
                if x.startswith(k[0]) or k[0] in ['aeiou'] and x.startswith('h'):
                    d = vgf.lvn.distance(k, x)
                    if d < 3:
                        dct5 = self.lem2forms_set.get(x)
                        if dct5:
                            for f, st in dct5.items():
                                if words & st:
                                    got = 1
                                    shares[k].add(x + f)

                        if not got:
                            dct[x + '*'] = d
            got = 0
            for x in unused_col:
                if x.startswith(k[0]) or k[0] in ['aeiou'] and x.startswith('h'):
                    d = vgf.lvn.distance(k, x)
                    if d < 3:
                        dct5 = self.lem2forms_set.get(x)
                        if dct5:
                            for f, st in dct5.items():
                                if words & st:
                                    got = 1
                                    shares[k].add(x + f)

                        if not got:
                            dct[x] = d
            if dct:
                word2di[k] = dct

            b += 1
            vgf.print_intervals(b, 5, None, len(self.missing))

        word2di = {x: y for x, y in word2di.items() if x not in shares}

        lst = []
        b = 0
        for k, v in word2di.items():
            lst.append([b])
            lst.append([f'__{k}'])
            v = sort_dct_val(v)
            for s, t in v.items():
                lst.append([s, t])
            b += 1

        self.shared_forms = shares
        lst11 = [x for x in self.still_missing if x not in self.found and x not in self.shared_forms]

        if kind:
            file = f'{fold}match_miss_lasla'
            to.from_lst2txt_tab_delim(lst, file)
            vgf.open_txt_file(file)

        return

    def typical_endings(self):
        '''
        see permutations in def2excel

        '''

        total = self.all_old | self.clemmas
        unused = total - (set(self.all_lalems) | self.found)
        lst = ['us', 'a', 'o', 'um', 'is', 'ae', 'i', 'es', 'os',
               'ium', 'eo', 'io']
        remainder = total - self.missing
        lst_sort = vgf.sort_lst_by_len(lst, 1)
        possib = defaultdict(list)
        for x in self.missing:
            for z in lst_sort:
                if x.endswith(z):
                    short = x[:-len(z)]
                    for t in lst_sort:
                        nword = f'{short}{t}'
                        if nword in remainder:
                            possib[x].append(nword)

    def use_wonum(self):

        to_del = []
        c = 0
        for x in self.missing:
            obj = self.old_wonum_cm.get(x)
            if obj:
                self.forms['old'][x] = obj
                self.found.add(x)
                to_del.append(x)
                c += 1
        for x in to_del:
            self.missing.remove(x)

        p(f'found {c} using OLD')

    def use_old_variants(self):
        to_del = set()
        self.is_old_variant = {}
        for x in self.missing:
            obj = self.old_variants.get(x)
            if obj:
                self.forms['old_var'][x] = obj
                to_del.add(x)
                self.found.add(x)
        p(f'removed {len(to_del)} using OLD variants')
        for x in to_del:
            self.missing.remove(x)
        return

    def used_spelled_wrong_technique(self):
        '''
        if a sublemma appears in more than 2 lemmas
        and one of the two lemmas is barely used, then
         it is probably a typo
        '''
        self.las_freq = pi.open_pickle(f'{fold}las_freq', 1)
        child2parent = defaultdict(list)
        lem_freq = defaultdict(int)
        for x, y in self.all_lalems.items():
            for num, lsts in y.items():
                for lst in lsts:
                    child2parent[lst[0]].append(x)
                    tpl = (x + num, lst[0], lst[1])
                    freq = self.las_freq.get(tpl)
                    if freq:
                        lem_freq[x] += freq
                    else:
                        p(f'missing {tpl}')

        lem_freq = {}
        # for x in


class prelim_match(handle_still_missing):
    def __init__(self):
        handle_still_missing.__init__(self)

    def begin_pm(self, kind=0):
        self.kind = kind
        self.get_atts_pm()
        self.new_las_freq()
        if not self.kind:
            self.output(6)

    def conditions(self, cat, lem, word, pos):
        # todo blank pos should not exist
        if cat == '!':
            self.onums['dupl'] += 1
            return 0
        if word == 'GREEK':
            self.onums['greek'] += 1
            return 0
        if not lem or lem in ['#', '0']:
            self.onums['hash'] += 1
            return 0
        if "_" in pos or pos in ['#', '']:
            '''
            
            these are words which lasla failed to understand not me
            they are used in printing the text but not for understanding
            latin, later a pos can be assigned to them if spelled
            correctly
            '''
            self.onums['unanalyzable'] += 1
            return 0
        if pos in ['m']:
            self.onums['numbers'] += 1
            return 0
        return 1

    def new_las_freq(self):
        '''

        dupl 7075
        numbers 17230
        split 491
        hash 415
        greek 642
        unanalyzable 220
        unprocessed tokens 18356
        odd lems 98
        all lems 25002
        unique old 29
        unique new 453
        lemma pos tokens 151860
        lemma pos tokens old 164652
        old words 126398
        new words 120898
        '''

        self.las_freq = defaultdict(int)
        all_lems = set()
        odd_lems = set()
        all_words = set()
        self.onums = defaultdict(int)
        b = 0
        for auth, works in self.lasla_db2.items():
            for work, infos in works.items():
                b += 1
                p(b)
                for e, rw in en(infos):
                    cat = rw[0]
                    lem = rw[1]
                    word = rw[2]
                    # todo perhaps find a better place to elim space
                    word = word.replace(' ', '')
                    pos = rw[4]
                    self.una = 0
                    if self.conditions(cat, lem, word, pos):
                        if "_" in lem:
                            self.onums['split'] += 1
                            odd_lems.add(lem)
                        else:
                            all_lems.add(lem)
                            all_words.add(word)
                            self.las_freq[(lem, word, pos)] += 1

        old_lems = set()
        old_words = set()
        for x, y in self.las_freq_old.items():
            old_lems.add(x[0])
            old_words.add(x[1])
        unique_old = old_lems - all_lems
        unique_new = all_lems - old_lems
        unique_old = set(x for x in unique_old if len(x) > 1 and x[-1] not in ['8', '9'])
        unique_new = set(x for x in unique_new if len(x) > 1 and x[-1] not in ['8', '9'])

        unprocessed = 0
        for x, y in self.onums.items():
            if x not in ['dupl', 'greek']:
                unprocessed += y
            p(x, y)

        p(f'unprocessed tokens {unprocessed}')
        p(f'odd lems {len(odd_lems)}')
        p(f'all lems {len(all_lems)}')
        p(f'unique old {len(unique_old)}')
        p(f'unique new {len(unique_new)}')
        p(f'lemma pos tokens {len(self.las_freq)}')
        p(f'lemma pos tokens old {len(self.las_freq_old)}')
        p(f'old words {len(old_words)}')
        p(f'new words {len(all_words)}')

        return

    def rough_preliminary(self):
        p('now checking collatinus against lasla')
        '''
        feb 17 - 53%
        feb 18 - 77%  
        april 30 - 80%
        may 2 - 90%
        bad lemmas: 0.04
        unmatched: 0.03
        bad_word: 0.03
        bad_pos: 0.00
        code_error: 0.000
        unprocessed: 0.0106
        found: 0.90
        total: 1739218      
        '''

        if not self.kind:
            self.lem2forms_rev = pi.open_pickle(f'{fold}lem2forms_rev', 1)
            self.llem2clem = pi.open_pickle(f'{fold}llem2clem', 1)
            self.las_freq = pi.open_pickle(f'{fold}las_freq2', 1)
        else:
            self.las_freq = pi.open_pickle(f'{fold}las_freq2', 1)

        code_errors = set()
        bad_lemmas = defaultdict(int)
        bad_words = {}
        bad_pos_dct = {}
        bad_pos_dct2 = {}
        unprocessed = 18356
        total = 0
        total += unprocessed
        for x, freq in self.las_freq.items():
            total += freq

        found = 0
        bad_word = 0
        bad_pos = 0
        bad_lemma = 0
        miss_pos = set()
        unmatched = 0
        unmatched_dct = {}
        code_error = 0
        encs2 = {'que', 'ue', 'ne'}
        b = 0
        for x, freq in self.las_freq.items():
            b += 1
            vgf.print_intervals(b, 5000, None, len(self.las_freq))
            lem = x[0]
            if lem in encs2:
                total += freq
                found += freq

            else:
                word = x[1].lower()
                word = word.replace(' ', '')
                pos = x[2]
                if x == ('non', 'non', 'd'):
                    bb = 8

                lem, num = cut_num(lem, 1)
                itm = self.llem2clem.get(lem, None)
                if itm != None:
                    clem = itm.get(num)
                    if clem != None:
                        tclem = lem + clem
                        pos2words = self.lem2forms_rev.get(tclem)
                        if not pos2words:
                            code_errors.add(tclem)
                            code_error += freq
                        else:
                            if len(pos2words) == 1 or type(pos2words) == str:
                                # todo if str then not getting macrons

                                found += freq
                            else:
                                if pos == 'd' and 'd' not in pos2words and 'inv' in pos2words:
                                    pos = 'inv'

                                macron_dct = pos2words.get(pos)
                                if not macron_dct:
                                    bad_pos += freq

                                    bad_pos_dct[(tclem, x[1], x[2])] = freq
                                    bad_pos_dct2[(tclem, x[1], x[2])] = [pos, pos2words]

                                else:
                                    if word in macron_dct:
                                        found += freq
                                    else:
                                        bad_word += freq
                                        bad_words[(tclem, x[1], x[2])] = [macron_dct, pos2words]


                    else:
                        unmatched_dct[lem + num] = itm
                        unmatched += freq
                else:
                    bad_lemma += freq
                    bad_lemmas[lem] += freq

        b = round(bad_lemma / total, 3)
        c = round(unmatched / total, 3)
        d = round(bad_word / total, 3)
        e = round(bad_pos / total, 5)
        f = round(found / total, 3)
        h = round(code_error / total, 4)
        g = round(unprocessed / total, 4)
        p(f'bad lemmas: {b}')
        p(f'unmatched: {c}')
        p(f'bad_word: {d}')
        p(f'bad_pos: {e}')
        p(f'found: {f}')
        p(f'code_error: {h}')
        p(f'unprocessed: {g}')
        p(f'total: {total}')
        # unmatched_dct = sort_dct_val_rev(unmatched_dct)
        # bad_pos_dct2 = vgf.sort_dct_by_dct(bad_pos_dct2, bad_pos_dct)
        bad_lemmas = vgf.sort_dct_val_rev(bad_lemmas)

        if code_errors:
            to.from_lst2txt(code_errors, f'{fold}code_errors')
            vgf.open_txt_file(f'{fold}code_errors')
        if bad_lemmas:
            bad_lemmas = sort_dct_val_rev(bad_lemmas)
            bad_lemmas = list(bad_lemmas.keys())

            to.from_lst2txt(bad_lemmas, f'{fold}bad_lemmas')
            vgf.open_txt_file(f'{fold}bad_lemmas')
        return


class word2model(prelim_match):
    def __init__(self):
        prelim_match.__init__(self)

    def short_cut_w2m(self):
        self.miss_col_pos2 = pi.open_pickle(f'{fold}missing_proper2')
        self.miss_col_pos = pi.open_pickle(f'{fold}miss_col_pos')
        self.miss_col_pos = [x for x in self.miss_col_pos if '_' not in x[0]]
        self.miss_col_pos += self.miss_col_pos2
        self.final_pos = pi.open_pickle(f'{fold}final_pos')
        self.las_lem_freq = pi.open_pickle(f'{fold}las_lem_freq')
        self.llem2clem = pi.open_pickle(f'{fold}llem2clem')
        self.co_lemmas4 = pi.open_pickle(f'{fold}co_lemmas4')
        self.fpos_rev = {v: k for k, v in self.final_pos.items()}
        ins = bottom_most_a4()
        ins.build_ui_models(1)
        self.ui_models = ins.ui_models

    def begin_w2m(self):
        self.get_mod2pos()
        self.get_mod_freq()
        self.use_w2m_hand()
        self.word2model_fu()
        self.output(2)

    def get_mod2pos(self):
        self.mod2pos = {}
        for k, v in self.co_lemmas4.items():
            vp = v['pos']
            vp = 'a' if vp == 'p' else vp
            self.mod2pos[v['model']] = vp
            if len(self.mod2pos) > 141:
                break

    def get_mod_freq(self):
        self.mod2freq = defaultdict(int)
        for k, v in self.llem2clem.items():
            for x, y in v.items():
                llem = k + x
                lfreq = self.las_lem_freq.get(llem)
                clem = k + y
                mod = self.co_lemmas4.get(clem)
                if mod and lfreq:
                    self.mod2freq[mod['model']] += lfreq

    def use_w2m_hand(self):
        file = f'{fold}new_mods_by_hand'
        file2 = f'{fold}new_mods_by_hand2'
        lst = to.from_txt2lst_tab_delim(file, 1)
        lst2 = to.from_txt2lst_tab_delim(file2, 1)
        lst += lst2
        self.lem2mod_hand = {}
        for x in lst:
            s = x[0]
            if s.startswith('__'):
                lem = s[2:]
            elif '*' in s:
                s = s.replace('*', '')
                self.lem2mod_hand[lem] = s

    def weed_out_fake_lemmas(self):
        lst = []
        b = 0
        for k in self.miss_col_pos:
            lem = k[0]
            b += 1
            for x, y in k[2].items():
                lem2 = lem + x
                if self.las_lem_freq[lem2] < 10:
                    if b % 10 == 0:
                        lst.append([b])
                    lst.append([f'__{lem}{x}'])
                    for z in y:
                        lst.append(z)

        file = f'{fold}pos_fake_lems'
        to.from_lst2txt_tab_delim(lst, file)
        vgf.open_txt_file(file)

    def word2model_fu(self):
        ## plerique in col should be a noun
        ## potis has two lemmas in it

        word2rat = {}  # 34
        word2rat2 = {}  # 34
        '''
        potis has two lemmas, potissimum and potis, pote
        also potissimus
        dominans should be an adjective
        '''

        dct5 = {x[0]: x for x in self.miss_col_pos}

        self.word2nmod = {}
        props = 90
        final_roots = {}
        b = 0
        for k in self.miss_col_pos:  # 243
            b += 1
            if len(self.miss_col_pos) > 500:
                vgf.print_intervals(b, 100, None, len(self.miss_col_pos))
            lem = k[0]
            if lem == 'uolux':
                bb = 8

            lem_pos = k[1]
            lem_pos2 = lem_pos
            if lem_pos == 'x':
                props = 49
                lem_pos = ['n', 'a']
            else:
                lem_pos = [lem_pos]

            for idx, lsts in k[2].items():
                hand = self.lem2mod_hand.get(lem + idx)
                if ('d' in lem_pos or lem_pos2 == 'x') and all(y[1] in ['d', 'inv'] for y in lsts):
                    self.word2nmod[lem + idx] = 'inv'
                    p(lem + idx, 'inv')
                elif 'n' in lem_pos and all(y[1] in ['sn'] for y in lsts):
                    self.word2nmod[lem + idx] = 'lupus'
                else:
                    mod_freq = {}
                    mod_root = defaultdict(int)
                    for mod, dct in self.ui_models.items():
                        mod_pos = self.mod2pos.get(mod)
                        if mod_pos in lem_pos:
                            mod_freq[mod] = [0, 0]

                    for lst in lsts:
                        word = lst[0]
                        pos2 = lst[1]
                        freq = lst[2]
                        for mod, dct in self.ui_models.items():
                            mod_pos = self.mod2pos.get(mod)

                            if mod_pos in lem_pos:
                                mod_freq[mod][0] += freq
                                if mod == 'lupus_g' and pos2 == 'sa':
                                    bb = 8

                                num = self.fpos_rev[pos2]
                                obj = dct['des'].get(num)
                                if obj:
                                    endings = [g for f in obj for g in f[1]]
                                    ## the line belowed does not work all the time but we won't worry about it for now
                                    root = obj[0][0]
                                    for end in endings:
                                        if not end:
                                            if pos2 == 'sn':
                                                mod_freq[mod][0] -= freq
                                            else:
                                                bool1 = self.no_end(pos2, lsts, word)
                                                if bool1 == 2:
                                                    mod_freq[mod][0] -= freq
                                                elif bool1:
                                                    mod_freq[mod][1] += freq


                                        elif word.endswith(end):
                                            if root in ['1', '2']:
                                                mid = dct['R'][root][1]
                                                beg = word[:-(len(end) + len(mid))]
                                                # capitalized words beginning with u are changed to v
                                                beg = norm_str_jv(beg)

                                                if lem + idx not in mod_root:
                                                    mod_root[lem + idx] = {}
                                                if mod not in mod_root[lem + idx]:
                                                    mod_root[lem + idx][mod] = {}
                                                if root not in mod_root[lem + idx][mod]:
                                                    mod_root[lem + idx][mod][root] = defaultdict(int)

                                                mod_root[lem + idx][mod][root][beg] += freq
                                            mod_freq[mod][1] += freq
                                            break

                    if mod_freq:
                        mod_freq2 = {}
                        for x, y in mod_freq.items():
                            try:
                                perc = percent(y[1], y[0])
                            except ZeroDivisionError:
                                perc = 0
                            mod_freq[x] = perc
                            mod_freq2[x] = y[0]
                        mod_freq = sort_dct_val_rev(mod_freq)
                        lval = vgf.dct_idx(mod_freq, 0, 'v')
                        # with proper nouns the threshold is 50% otherwise 90%
                        # a proper noun is determined by have the x pos in lem_pos2
                        if lval > props or hand:
                            if not hand:
                                dct5 = {x: self.mod2freq[x] for x, y in mod_freq.items() if y == lval}
                                modc = vgf.largest_member(dct5)
                                self.word2nmod[lem + idx] = modc
                            else:
                                modc = hand

                            if lem + idx in mod_root and modc in mod_root[lem + idx]:
                                dct4 = {d: vgf.largest_member(c) for d, c in mod_root[lem + idx][modc].items()}
                                final_roots[lem + idx] = dct4

                        else:
                            mod_freq3 = {s: [t, mod_freq2[s]] for s, t in mod_freq.items()}
                            word2rat[lem + idx] = [mod_freq3, lsts]
                            word2rat2[lem + idx] = vgf.dct_idx(mod_freq, 0, 'v')

        word2rat2 = vgf.sort_dct_val_rev(word2rat2)
        word2rat = vgf.sort_dct_by_dct(word2rat, word2rat2)

        lst5 = []
        for k, v in word2rat.items():
            mods = v[0]
            decl = v[1]
            modscore = vgf.dct_idx(mods, 0, 'v')[0]
            mods2 = {x: y for x, y in mods.items() if y[0] > modscore - 10}
            lst5.append(["__" + k])
            for mod, score in mods2.items():
                lst5.append([mod] + score)
            for l in decl:
                lst5.append(l)

        if not props:
            self.word2nmod = merge_2dicts(self.word2nmod, self.lem2mod_hand)
        self.final_roots = final_roots

        research = 0
        if research:
            file = f'{fold}new_mods_by_hand3'
            to.from_lst2txt_tab_delim(lst5, file)
            vgf.open_txt_file(file)

        return

    def g_and_p_stems(self):
        # here we get which pos # are geninf stems and which are p stems
        self.gp_stems = defaultdict(list)
        for k, v in self.ui_models['amo']['des'].items():
            if v[0][0] == '1':
                posn = self.final_pos[k]
                self.gp_stems['1'].append(posn)
            elif v[0][0] == '2':
                posn = self.final_pos[k]
                self.gp_stems['2'].append(posn)

    def no_end(self, pos2, lsts, word):
        dct = defaultdict(list)
        for x in lsts:
            dct[x[1]].append(x[0])

        dct1 = {
            'pn': 'pa',
            'pa': 'pn',
            'sa': 'sn',
            'sg': 'sn'

        }

        opp = dct1.get(pos2)
        if opp:
            lst = dct.get(opp)
            if lst:
                if word in lst:
                    return 1
                else:
                    return 0
            else:
                return 2
        else:
            return 2


class match_colwlas(word2model):
    def __init__(self):
        word2model.__init__(self)

    def build_colat5(self):
        file = f'{fold}new_mods4colat_prop'
        file1 = f'{fold}new_mods4colat2'
        colem = pi.open_pickle(f'{fold}co_lemmas4')
        p(f'number of lemmas before {len(colem)}')
        llem2clem = pi.open_pickle(f'{fold}llem2clem2')
        lst = to.from_txt2lst_tab_delim(file, 1)
        lst1 = to.from_txt2lst_tab_delim(file1, 1)
        lst1 += lst
        for l in lst1:
            d = {}
            lwnum = l[0]
            word, num = cut_num(lwnum, 1)
            d['lemma'] = word
            d['word'] = l[0]
            d['model'] = l[1]
            d['geninf'] = l[2]
            d['perf'] = l[3]
            d['pos'] = ''
            if num in ['8', '9']:
                d['capital'] = 1
            else:
                d['capital'] = 0

            d['def_co'] = ''
            d['def_lw'] = ''
            d['def_ls'] = ''
            d['def_gj'] = ''
            d['def_gg'] = ''
            d['def_ge'] = ''
            if lwnum in colem:
                assert num not in ['8', '9']
                if not num:
                    num = '0'
                num2 = int(num) + 1
                lwnum2 = f'{word}{num2}'
                while lwnum2 in colem:
                    num2 += 1
                    lwnum2 = f'{word}{num2}'
                num2 = str(num2)
            else:
                num2 = num

            colem[word + num2] = d
            if num == '0':
                num = ''
            assert num2 != '0'
            llem2clem[word][num] = num2
        p(f'number of lemmas after {len(colem)}')

        assert 'musa1' in colem
        pi.save_pickle(colem, f'{fold}co_lemmas5')
        pi.save_pickle(llem2clem, f'{fold}llem2clem2')

    def use_fake_lemmas(self):
        file = f'{fold}pos_fake_lems'
        lst = to.from_txt2lst(file, 1)
        self.fake_lems = set()
        for x in lst:
            if '#' in x:
                bb = 8
            if x.startswith('__') and ';' in x:
                s = x[2:].replace(';', '').strip()
                self.fake_lems.add(s)
        if '#' in self.fake_lems:
            bb = 8
        if 'm' in self.fake_lems:
            bb = 8
        return

    def use_match_miss(self):
        lst = to.from_txt2lst_tab_delim(f'{fold}match_miss_lasla', 1)
        self.lem2variants = defaultdict(list)
        self.lem2constituents = {}
        self.unknown = []
        self.bogus_lems = set(x for x in self.missing5 if '*' in x)
        self.missing5 = set(x for x in self.missing5 if '*' not in x)

        found = 0
        lemma = ''
        for l in lst:
            if l[0].isdigit():
                pass
                if not found and not lemma:
                    if not public:
                        p(f'you didnt hand select {lemma} in the match_miss_lasla sheet')
                found = 0
            elif l[0].startswith('__'):
                lemma = l[0][2:]
                if '|' in lemma:
                    lst1 = lemma.split('|')
                    lemma = lemma.replace('|', '')
                    self.lem2constituents[lemma] = lst1
                    found = 1
                if '?' in lemma:
                    self.unknown.append(lemma.replace('?', ''))
                    found = 1

            elif l[1].endswith('#'):
                word = l[0]
                word = word.replace('*', '')
                self.lem2variants[lemma].append(word)
                found = 1
        self.handlems = set(self.lem2constituents.keys()) | set(self.lem2variants.keys()) | set(self.unknown)
        self.handlems |= set(self.fixm_lems)
        ## todo roughly 13 of the still missing still have not been found
        self.handlems |= set(self.still_missing)
        self.missing5 = self.missing5 - self.still_missing

    def elim_pos_in_col(self):
        '''
        here we change some nouns to adjectives
        '''
        error = 0
        for x, y in self.lem2forms_pos.items():
            new = {}
            to_del = []
            for k, v in y.items():
                if k == 'o':
                    new['d'] = v
                    to_del.append(k)
                elif k == 'p':
                    to_del.append(k)
                    if len(v) > 1:
                        p(f'two rare pos {x}')
                        error = 1
                    for m, n in v.items():
                        dct = n[0]
                        val = vgf.dct_idx(dct, 0, 'v')
                        val = val[1]
                        pos = self.det_pos(val)
                        new[pos] = v
                        # p(f'changed {x} to {pos}')
                        if pos not in ['n', 'a']:
                            error = 1
                            p(f'error {x}')
                        break

                    new['a'] = v
            for k, v in new.items():
                obj = y.get(k)
                if not obj:
                    y[k] = v
                else:
                    self.lem2forms_pos[x][k] = merge_2dicts(obj, v)
            for t in to_del:
                del self.lem2forms_pos[x][t]
        if error:
            assert 0

        return

    def get_num_lems(self):
        '''
        here we make a dictionary where it is determined which pos each numbered
        lemma has.
        '''
        dct4 = defaultdict(list)
        for k in self.missing5:
            ku, num = cut_num(k, 1)
            dct4[ku].append(num)
        self.miss5_dct = dct4

        for t, f in self.las_freq.items():
            lem, num = cut_num(t[0], 1)
            if lem in self.handlems:
                '''
                these are words which are not found in collatinus so there is no point
                in trying to match them to the collatinus database
                '''
                pass
            elif num in ['8', '9']:
                self.prop_lalems[lem].setdefault(num, []).append([t[1], t[2], f])
            else:
                self.all_lalems[lem].setdefault(num, []).append([t[1], t[2], f])
        self.num_lems2 = {k: v for k, v in self.all_lalems.items() if len(v) > 1}
        self.lem2forms_pos = {x: y for x, y in self.lem2forms_pos.items() if x in self.all_lalems}
        return



    def get_lalems_pos(self):
        '''
        here we assign lemma indexes to parts of speech
        so 'lego' has two lemmas which are both verbs, hence
        they will fall under lego[v]
        '''

        self.lalems_pos = defaultdict(dict)
        self.lalems_pos_rev = defaultdict(dict)
        self.lalems_pos_rev2 = defaultdict(dict)
        self.lalems_pos_rev3 = defaultdict(dict)
        self.pos_anom = defaultdict(dict)
        errors = defaultdict(dict)
        # for k, v in self.num_lems2.items():
        p('building lalems_pos')
        b = 0
        for k, v in self.all_lalems.items():
            b += 1
            if k == 'cum':
                bb = 8
            vgf.print_intervals(b, 2000, None, len(self.all_lalems))
            for num, lst in v.items():
                pos, dct, dct2, dct4 = self.det_pos2(lst, k, num)
                if k not in self.lalems_pos:
                    self.lalems_pos[k] = {}
                    self.lalems_pos_rev[k] = {}
                    self.lalems_pos_rev2[k] = {}
                    self.lalems_pos_rev3[k] = {}
                if pos not in self.lalems_pos[k]:
                    self.lalems_pos[k][pos] = {}
                    self.lalems_pos_rev[k][pos] = {}
                    self.lalems_pos_rev2[k][pos] = {}
                    self.lalems_pos_rev3[k][pos] = {}
                if num not in self.lalems_pos[k][pos]:
                    self.lalems_pos[k][pos][num] = []
                    self.lalems_pos_rev[k][pos][num] = []
                    self.lalems_pos_rev2[k][pos][num] = []
                    self.lalems_pos_rev3[k][pos][num] = []
                self.lalems_pos[k][pos][num] = lst
                self.lalems_pos_rev[k][pos][num] = dct
                self.lalems_pos_rev2[k][pos][num] = dct2
                self.lalems_pos_rev3[k][pos][num] = dct4

        return

    def det_pos2(self, lst, k, num):
        dct = defaultdict(list)
        for x in lst:
            tpl = (k + num, x[0], x[1])
            freq = self.las_freq[tpl]
            if not freq:
                bb = 8
            dct[x[1]].append((x[0], freq))

        dct2 = defaultdict(set)
        dct4 = {}
        for x, y in dct.items():
            dct3 = {b[0]: b[1] for b in y}
            dct4[x] = vgf.largest_member(dct3)
            for t in y:
                dct2[x].add(t[0])

        prob = defaultdict(int)

        for b, c in dct.items():
            dpos = self.det_pos(b)
            o = 0
            for t in c:
                o += t[1]

            prob[dpos] += o
        prob = sort_dct_val_rev(prob)
        total = sum(prob.values())
        top = vgf.dct_idx(prob, 0, 'v')

        # try:
        rat = round(top / total, 4)
        # except ZeroDivisionError:
        #     rat = 0

        if len(prob) > 1:
            self.pos_anom[k][num] = [rat, prob, dct]

        # if all(l[0] == 'd' for l in lst):
        #     return 'd', dct, dct2, dct4  ## formerly o
        # elif any(l[0] in ['ac', 'as'] for l in lst):
        #     return 'd', dct, dct2, dct4

        pos = vgf.dct_idx(prob, 0)
        return pos, dct, dct2, dct4

    def det_pos(self, s):
        if s == 'inv':
            return 'd'  ## formerly o
        if s in ['su', 'sup']:
            return 'v'
        if '.' in s:
            return 'v'
        if s in ['d', 'ac', 'as']:
            return 'd'
        if len(s) == 2:
            return 'n'
        else:
            return 'a'

    def lasla_pos_anomalies(self):
        '''
        the following looks for contradictions where the same lemma exists as
        two parts of speech which cannot happen.
        there are many nouns which appear once as an invariant, of the few
        i looked up they are mistakes.  delete these temporarily
        until more research is done
        #todo verify invariants are really invariant

        '''

        to_del = []
        exam = defaultdict(dict)
        level = {}

        for k, v in self.pos_anom.items():
            for num, info in v.items():
                if info[0] > .98:
                    to_del.append((k, num))
                else:
                    exam[k][num] = info

        return

    def elim_redundant_lasla(self):
        '''
        this step could probably be deleted since match_lambig
        does the same thing but since it already works it has
        been left as is

        '''

        b = 0
        for k, v in self.lalems_pos.items():
            b += 1
            # vgf.print_intervals(b, 1000, None, len(self.lalems_pos))
            for pos, dct in v.items():
                if len(dct) > 1:
                    rev = self.lalems_pos_rev3[k][pos]
                    diff = self.ambig_by_form(rev)
                    if not diff:
                        dct4 = self.elim_redundant_lasla2(rev, k, dct)
                        self.lalems_pos[k][pos] = dct4
        return

    def remove_proper_l2f(self):
        self.lem2forms_posco = defaultdict(dict)
        self.lem2forms_pospr = defaultdict(dict)
        for k, v in self.lem2forms_pos.items():
            for pos, dct in v.items():
                for num, lst in dct.items():
                    obj = self.co_lemmas4[k + num]
                    if obj['capital'] == 1:
                        if k not in self.lem2forms_pospr:
                            self.lem2forms_pospr[k] = defaultdict(dict)
                        if pos not in self.lem2forms_pospr[k]:
                            self.lem2forms_pospr[k][pos] = defaultdict(dict)
                        self.lem2forms_pospr[k][pos][num] = lst
                    else:
                        if k not in self.lem2forms_posco:
                            self.lem2forms_posco[k] = defaultdict(dict)
                        if pos not in self.lem2forms_posco[k]:
                            self.lem2forms_posco[k][pos] = defaultdict(dict)
                        self.lem2forms_posco[k][pos][num] = lst

    def four_categories(self):
        self.miss_col_pos = []
        cambig = []  # 183
        lambig = []
        bambig = []
        for k, v in self.lalems_pos.items():
            for pos, ldct in v.items():
                cdcts = self.lem2forms_posco.get(k)
                if not cdcts:
                    self.miss_col_pos.append([k, pos, ldct])
                else:
                    cdct = cdcts.get(pos)
                    if not cdct:
                        self.miss_col_pos.append((k, pos, ldct))
                    else:
                        if len(cdct) == 1 and len(ldct) == 1:
                            clem = vgf.dct_idx(cdct)
                            llem = vgf.dct_idx(ldct)
                            if k in self.llem2clem and llem in self.llem2clem[k]:
                                pass
                                bb = 8
                            else:
                                self.llem2clem[k][llem] = clem
                        elif len(ldct) == 1 and len(cdct) > 1:
                            cambig.append([k, pos, cdct, ldct])
                        elif len(ldct) > 1 and len(cdct) == 1:
                            lambig.append((k, pos, cdct, ldct))
                        elif len(ldct) > 1 and len(cdct) > 1:
                            bambig.append((k, pos, cdct, ldct))

        self.match_bambig(bambig)
        self.match_cambig_nl(cambig)
        self.match_lambig(lambig)

        return

    def temp15(self):
        dct = {}
        for l in self.miss_col_pos:
            for x, y in l[2].items():
                lem = l[0] + x
                dct[lem] = self.las_lem_freq[lem]
        dct = sort_dct_val_rev(dct)

    def match_lambig(self, lambig):
        for l in lambig:
            word = l[0]
            cdct = l[2]
            clem = vgf.dct_idx(cdct)
            ldct = l[3]
            for k in ldct.keys():
                if word in self.llem2clem and k in self.llem2clem[word]:
                    pass
                else:
                    self.llem2clem[word][k] = clem

    def ambig_by_form(self, rev):
        forms = defaultdict(dict)
        for num, dct in rev.items():
            for pos, word in dct.items():
                forms[pos][num] = word

        diff = {}
        for pos, dct2 in forms.items():
            st = set(dct2.values())
            if len(st) > 1:
                diff[pos] = dct2
            else:
                bb = 8

        return diff

    def elim_redundant_lasla2(self, dct, k, dct4):
        dct2 = {}
        for num in dct.keys():
            dct2[num] = self.las_lem_freq[k + num]

        to_del = []
        lnum = vgf.largest_member(dct2)
        for num in dct.keys():
            if num != lnum:
                self.redundant_map[k + num] = k + lnum
                to_del.append(num)

        for num in to_del:
            del dct4[num]
        return dct4

    def use_wrong_lpos(self):
        lst = to.from_txt2lst_tab_delim(f'{fold}wrong_lasla_pos', 1)
        for l in lst:
            lem = l[0]
            word = l[1]
            wpos = l[2]
            rpos = l[3]
            self.wrong_pos[(lem, word, wpos)] = (lem, word, rpos)

    def handle_shared_forms(self):
        '''
        the fixm lemmas are variants using several techniques found in the
        fix mistakes class
        the shared_forms are composed of lem2variants and lem2constituents

        '''

        all_lems = set(self.las_lem_freq.keys())
        have = set()
        for k, v in llem2clem2.items():
            for x, y in v.items():
                have.add(k + x)

        not_have = all_lems - have
        known_miss = self.missing6 | self.missing5 | self.fixm_lems | self.handlems | set(self.shared_forms.keys())
        unknown_miss = not_have - known_miss
        unknown_common = set(x for x in unknown_miss if not x[-1] in ['8', '9'])

        llem2clem2 = pi.open_pickle(f'{fold}llem2clem2')
        llems = set(self.all_lalems.keys())
        st = set(self.shared_forms.keys()) & self.missing6
        st = self.handlems - (self.missing6 | self.missing5)
        for k, v in self.shared_forms.items():

            if k in self.missing6:
                pass

    def use_la_fake_ambigs(self):
        '''
        todo we still haven't coded for the > sign in this file
        which respells words
        '''

        lst = to.from_txt2lst_tab_delim(f'{fold}la_fake_ambigs', 1)
        self.bogus2true = to.from_txt2dct_1d(f'{fold}wrong_lemmas')
        lemma = ''
        base_idx = None
        bogus = []
        for l in lst:

            if l[0].startswith('__'):
                if lemma == 'quisquis':
                    bb = 8

                if lemma and base_idx != None:
                    true = lemma + base_idx
                    for y in bogus:
                        self.bogus2true[lemma + y] = true

                lemma = l[0][2:]
                base_idx = None
                bogus = []
            else:
                freq = l[3]
                idx = l[1]

                if freq.endswith('#'):
                    base_idx = idx
                else:
                    bogus.append(idx)

        return

    def use_wrong_lasla_lemma(self):
        lst = to.from_txt2lst_tab_delim(f'{fold}wrong_lasla_lemma')
        self.wrong_lemma = {}
        for l in lst:
            tpl = (l[0], l[1], l[2])
            word = l[3]
            self.wrong_lemma[tpl] = word

    def use_typos(self):
        lst = to.from_txt2lst_tab_delim(f'{fold}lasla_typos3')
        self.wrong_word = {}
        for l in lst:
            tpl = (l[0], l[1], l[2])
            word = l[3]
            self.wrong_word[tpl] = word

    def fix_las_freq(self):
        ###  genus, generest sb
        '''
        todo in the sum1 lemmas in pos 3.pr.in.ac there are a lot
        of words with the enclitic st
        exter, bene, prodest
        '''

        dct = defaultdict(int)
        rem = 0
        exc = {'post'}
        dct4 = {'meliust': 'melius',
                'bonust': 'bonus',
                'bonast': 'bonas'}
        rem_dct = defaultdict(set)
        for k, v in self.fake_enclitics.items():
            st = set()
            for x in v:
                if x == 'inv':
                    st.add('d')
                else:
                    st.add(x)
            self.fake_enclitics[k] = st

        for x, y in self.las_freq.items():
            lem = x[0]
            word = x[1]
            pos = x[2]
            if lem == 'genus' and word == 'generest' \
                    and pos == 'sb':
                bb = 8
            if word in ['prodest', 'bene', 'exter']:
                bb = 8

            itm = self.wrong_word.get((lem, word, pos))
            if itm:
                word = itm
            itm = self.wrong_lemma.get((lem, word, pos))
            if itm:
                lem = itm

            word = word.replace(' ', '')
            wordu = word.lower()

            itm = self.wrong_pos.get((lem, word, pos))
            if itm:
                pos = itm[2]

            if '.' in word or "'" in word or '_' in lem or lem in self.fake_lems or \
                    not lem:
                pass
            else:
                lem = self.bogus2true.get(lem, lem)
                lemu = cut_num(lem)
                obj = self.fake_enclitics.get(lemu)

                if obj or not obj and lemu in self.lem2forms_pos:
                    if obj and pos in obj:
                        pass
                    else:
                        # if wordu in dct4:
                        #     word = dct4[wordu]
                        if wordu.endswith('st') and word != 'st':
                            word = word[:-2]
                        # for enc in encs:
                        #     if wordu.endswith(enc) and word != enc:
                        #         word = word[:-len(enc)]
                        #         rem += 1
                        #         rem_dct[enc].add((lemu,wordu,pos))
                        #         break

                dct[(lem, word, pos)] += y
        self.las_freq = dct

        return

    def delete_bogus_pos(self):
        '''
        here we delete parts of speech which appear less
        than 2% of the time in lasla, however this is just
        a preliminary purge until we obtain a better method
        for deleting bogus pos

        '''

        dct = self.lemma2decl
        dct2 = {}
        b = 0
        for k, v in dct.items():
            b += 1

            to_del = []
            sm = sum(v.values())
            for x, y in v.items():
                if y / sm < .02:
                    to_del.append(x)
            for x in to_del:
                # p(f'deleted pos {x[0]} in lemma {k}')
                del v[x]
            if len(v) > 1:
                dct2[k] = v

        return

    def combine_proper(self):  # anom 220
        '''
        currently there is a weakness in this algorithm
        if a proper name is has, say, sv and the common noun does not
        then it is anomalous and it should not be

        '''

        anom = defaultdict(dict)
        self.redund_prop = defaultdict(dict)
        self.missing_proper = set()
        self.missing_proper = set()
        anom2 = {}
        anom2a = {}
        anom4 = {}
        anom5 = {}
        c = 0
        for k, v in self.prop_lalems.items():
            for u, obj in v.items():
                found = 0
                try:
                    if u == '8':
                        found = 1
                        nouns2 = self.lalems_pos_rev2[k].get('a')
                        nouns3 = self.lalems_pos_rev2[k].get('d')
                        if nouns2 and nouns3:
                            nouns2 = merge_2dicts(nouns2, nouns3)
                        elif not nouns2 and nouns3:
                            nouns2 = nouns3
                        elif not nouns2 and not nouns3:
                            anom4[k] = obj
                            found = 0

                    else:
                        nouns2 = self.lalems_pos_rev2[k]['n']
                        found = 1
                except:
                    # p (f'error {k}')
                    pass

                if not found:
                    if u == '9':
                        anom2[k] = obj
                    elif u == '8':
                        anom4[k] = obj

                else:
                    cor = 0
                    tot = 0
                    agree = {}
                    for num, dct in nouns2.items():
                        for lst in obj:
                            w = norm_str_jv(lst[0])
                            pos = lst[1]
                            freq = lst[2]

                            st = dct.get(pos)
                            if st:
                                tot += freq
                                if w in st:
                                    cor += freq
                        if not tot:
                            agree[num] = 0
                        else:
                            agree[num] = int((cor / tot) * 100)
                    if not agree or not tot:
                        if u == '9':
                            anom2[k] = obj
                        else:
                            anom4[k] = obj

                    else:
                        agree = sort_dct_val_rev(agree)
                        llem = vgf.largest_member(agree)
                        perc = vgf.dct_idx(agree, 0, 'v')
                        if perc == 94:
                            self.redund_prop[k][u] = llem
                            if u == '8':
                                c += 1

                        else:
                            if u == '9':
                                anom2[k] = obj
                                anom[k]['9'] = [llem, perc, obj, nouns2[llem]]
                            else:
                                anom4[k] = obj

        clem_wonum = defaultdict(dict)
        for k, v in self.co_lemmas4.items():
            ku, num = cut_num(k, 1)
            clem_wonum[ku][num] = v
        self.clem_wonum = clem_wonum
        self.missing_proper2 = []
        b = 0
        old_all = merge_2dicts(self.old_wonum, self.old_variants)
        done = set()

        for e, dct in en([anom2, anom4]):
            llem = '9' if not e else '8'
            for k, ldct in dct.items():
                obj = clem_wonum.get(k)
                obj1 = old_all.get(k)
                if not obj and not obj1:
                    if k not in done:
                        self.missing_proper2.append([k, 'x', self.prop_lalems[k]])
                        done.add(k)
                elif not obj and obj1:
                    b += 1
                else:
                    b += 1
                    for x, y in obj.items():
                        if y['capital'] in [1, 2]:
                            # b += 1
                            if not e and y['pos'] == 'n':
                                self.llem2clem[k][llem] = x
                                break
                            elif e and y['pos'] in ['a', 'd', 'o']:
                                self.llem2clem[k][llem] = x
                                break

                    else:
                        if len(obj) == 1:
                            clem = vgf.dct_idx(obj)
                            if not e and obj[clem]['pos'] == 'n':
                                self.llem2clem[k][llem] = clem
                            elif e and obj[clem]['pos'] in ['a', 'd', 'o']:
                                self.llem2clem[k][llem] = clem
                            else:
                                if k not in done:
                                    self.missing_proper2.append([k, 'x', self.prop_lalems[k]])
                                    done.add(k)

                        else:
                            if k not in done:
                                self.missing_proper2.append([k, 'x', self.prop_lalems[k]])
                                done.add(k)

        p(f'still missing {len(self.missing_proper2)} proper nouns')
        return

    def use_lasla_def2coll_def(self):
        file = f'{fold}lasla_def2coll_def'
        lst = to.from_txt2lst_tab_delim(file, 1, 1)
        dct11 = defaultdict(dict)
        for x in lst:
            if x[0].startswith('__'):
                lem = x[0][2:].strip()
            elif x[0][0] == '*':
                llem = x[0][1:]
                clem = x[1]
                # p(llem, clem)
                if clem == '0':
                    clem = ''
                if clem == '??':
                    pass
                else:
                    self.llem2clem[lem][llem] = clem
                    # self.test(lem, clem, llem, 'use_lasla_def2coll_def')
                    dct11[lem][llem] = clem

            elif x[0][0] == '#':
                pass

    def use_imperfect_matches(self):
        file = f'{fold}imperfect_matches'
        file1 = f'{fold}cambig_by_hand'
        lst = to.from_txt2lst_tab_delim(file, 1, 1)
        lst1 = to.from_txt2lst_tab_delim(file1, 1, 1)
        lst += lst1
        self.imatches = {}
        to_del = []
        first = 0
        for l in lst:
            if l[0]:
                if l[0].startswith('__'):
                    lem = l[0][2:]
                if l[0][0] == '#' and '*' in l[0]:
                    s = l[0]
                    s = re.sub(r'[#\*]', '', s)
                    num = s
                    if num == '0':
                        num = ''
                    self.imatches[lem] = num
                elif l[0][0] == '#' and '!' in l[0]:
                    s = l[0]
                    s = re.sub(r'[#\*\!]', '', s)
                    num = s
                    to_del.append((lem, num))

        if first:
            for k, v in to_del:
                lem = k + v
                pos = self.co_lemmas4[lem]['pos']
                del self.lem2forms_pos[k][pos][v]

            '''
            if the sheet is not made then make it otherwise
            we will use it in colatinus2 to delete lemmas there
            '''
            lst = [x + y for x, y in to_del]

            file2 = f'{fold}del_lemmas'
            to.from_lst2txt(lst, file2)
        return

    def match_bambig(self, bambig):
        '''
        if a lemma is ambiguous in collatinus but not in lasla
        then we simply need to find the index number in collatinus
        that the lasla lemma maps to
        cambig by hand 71
        '''
        error = set()
        for x in bambig:
            word = x[0]
            cdcts = x[2]
            ldcts = x[3]
            for lasl_lem, lasl_forms in ldcts.items():
                if word in self.llem2clem and lasl_lem in self.llem2clem[word]:
                    pass
                else:
                    cdct2score = {}
                    wdct = {}
                    cdct_rv_dct = {}
                    for clem, cdct in cdcts.items():
                        cdct_rv = self.pos2word_collatinus(cdct[0])
                        cdct_rv_dct[clem] = cdct_rv
                        perc, wrong = self.compare_by_form(cdct_rv, lasl_forms)
                        cdct2score[clem] = perc
                        wdct[clem] = wrong

                    dct3 = sort_dct_val_rev(cdct2score)
                    if len(cdcts) > 2:
                        bb = 8

                    score1 = vgf.dct_idx(dct3, 0, 'v')
                    score2 = vgf.dct_idx(dct3, 1, 'v')

                    if score1 == score2:
                        assert 0
                        x.append(cdct_rv_dct)
                        bambig_by_hand.append(x)
                    else:
                        found = 0
                        if score1 > score2 + 17:
                            clem = vgf.dct_idx(dct3)
                            found = 1
                        elif score2 > score1 + 17:
                            clem = vgf.dct_idx(dct3, 1)
                            found = 1
                        if not found:
                            p(word, lasl_lem, 'ambig')
                            assert 0
                        else:

                            self.llem2clem[word][lasl_lem] = clem
                            # p(word, lasl_lem, clem)
                            dct5 = defaultdict(int)
                            for s, t in self.llem2clem[word].items():
                                if s not in ['9', '8']:
                                    dct5[t] += 1
                                    if dct5[t] > 1:
                                        error.add(word)
        if error:
            for word in error:
                p(f'two indexes in lasla {word} map to the same idx in collatinus')
            assert 0
        return

    def match_cambig_nl(self, cambig_nl):
        '''
        if a lemma is ambiguous in collatinus but not in lasla
        then we simply need to find the index number in collatinus
        that the lasla lemma maps to
        cambig by hand 71
        '''
        first = 0
        for x in cambig_nl:
            word = x[0]
            cdcts = x[2]
            ldct = x[3]
            lasl_lem = vgf.dct_idx(ldct)
            if word in self.llem2clem and lasl_lem in self.llem2clem[word]:
                pass
            else:
                lasl_forms = vgf.dct_idx(ldct, 0, 'v')
                cdct2score = {}
                wdct = {}
                cdct_rv_dct = {}
                for clem, cdct in cdcts.items():
                    cdct_rv = self.pos2word_collatinus(cdct[0])
                    cdct_rv_dct[clem] = cdct_rv
                    perc, wrong = self.compare_by_form(cdct_rv, lasl_forms)
                    cdct2score[clem] = perc
                    wdct[clem] = wrong

                dct3 = sort_dct_val_rev(cdct2score)
                score1 = vgf.dct_idx(dct3, 0, 'v')
                score2 = vgf.dct_idx(dct3, 1, 'v')

                if score1 == score2:
                    '''
                    if you're building the list for the first time then
                    use this otherwise use imatches
                    '''
                    if first:
                        x.append(cdct_rv_dct)
                        self.cambig_nl_by_hand.append(x)
                    else:
                        if word in self.imatches:
                            clem = self.imatches[word]
                            self.llem2clem[word][lasl_lem] = clem
                        else:
                            dct4 = {}
                            for s, t in dct3.items():
                                if not s:
                                    dct4['0'] = t
                                else:
                                    dct4[s] = t

                            dct4 = sort_dct_key(dct4)
                            clem = vgf.dct_idx(dct4)
                            if clem == '0':
                                clem = ''
                            self.llem2clem[word][lasl_lem] = clem

                else:
                    clem = vgf.dct_idx(dct3)
                    if dct3[clem] != 100:
                        if word in self.imatches:
                            clem = self.imatches[word]
                            self.llem2clem[word][lasl_lem] = clem
                        else:
                            self.llem2clem[word][lasl_lem] = clem

                    else:
                        self.llem2clem[word][lasl_lem] = clem
                        for z in cdct2score.keys():
                            if z != clem:
                                self.extra_clems[word].append(z)
        if first:
            self.add_2by_hand()
        return

    def add_2by_hand(self):
        lst = []
        lst2 = ['lemma', 'model', 'geninf', 'perf']
        b = 0
        for l in self.cambig_nl_by_hand:
            lem = l[0]
            b += 1
            if b and b % 10:
                lst.append(b)
            lst.append(f'__{lem}')
            for k in l[4].keys():
                obj = self.co_lemmas4[lem + k]
                lst.append(f'#{k}')
                for z in lst2:
                    lst.append(obj[z])
                defn = get_def(obj, 1, 1, 1)
                defn = ' '.join(defn)
                lst.append(defn)

        file = f'{fold}cambig_by_hand'
        to.from_lst2txt(lst, file)
        vgf.open_txt_file(file)

    def print_imperfect(self, imperfect_matches):
        lst = []
        for l in imperfect_matches:
            lem = l[0]
            lst.append(["", ""])
            lst.append(["__" + l[0]])
            defs = []
            for k, v in l[4].items():
                obj = self.co_lemmas4[lem + k]
                defn = get_def(obj, 0, 1, 1)
                defn = " ".join(defn)
                defs.append(f'{k} {defn}')
                lst.append([k, v])
            for d in defs:
                lst.append([d])

            for k, v in l[5].items():
                if not k:
                    lst.append(['#0'])
                else:
                    lst.append([f'#{k}'])
                for t in v:
                    lst2 = t[0] + t[1]
                    lst.append(lst2)

        file = f'{fold}imperfect_matches'
        to.from_lst2txt_tab_delim(lst, file)
        vgf.open_txt_file(file)

    def pos2word_collatinus(self, dct):
        dct1 = {}
        for num, lst in dct.items():
            dct1[lst[1]] = [norm_str_jv(y, 1) for y in lst[0]]
        return dct1

    def compare_by_form(self, cdct, lforms):
        b = 0
        wrong = []
        for l in lforms:
            # word, pos, num = l
            word, pos, num = l
            cforms = cdct.get(pos)

            if cforms:
                if word in cforms:
                    b += 1
                else:
                    wrong.append([l, cforms])

        return int((b / len(lforms)) * 100), wrong

    def got_everything(self):
        missing = {}
        missingp = {}
        for x,y in self.las_lem_freq.items():
            xu, num = cut_num(x,1)
            try:
                self.llem2clem[xu][num]
            except:
                if num in ['8','9']:
                    missingp[x]=y
                else:
                    missing[x]=y
        missing = sort_dct_val_rev(missing)
        missingp = sort_dct_val_rev(missingp)



        if missing:
            p(f'still missing {len(missing)} lemmas')
            to.from_lst2txt(list(missing.keys()), f'{fold}missing5')
            if not public:
                vgf.open_txt_file(f'{fold}missing5')
        return




    def test(self, word, clem, llem, func):
        odct = self.llem2clem_old.get(word)
        if odct:
            old_clem = odct.get(llem)
            if old_clem and old_clem != clem:
                self.clem_errors[func][word] = [llem, clem, old_clem]

    def get_las_lem_freq(self):
        self.las_lem_freq = defaultdict(int)
        for k, v in self.las_freq.items():
            self.las_lem_freq[k[0]] += v
        self.las_lem_freq = sort_dct_key(self.las_lem_freq)

    def add_redund_lems(self):
        '''
        these are proper nouns which have the exact same
        declension as their common name counterparts
        '''

        for k, v in self.redund_prop.items():
            for x, y in v.items():
                try:
                    clem = self.llem2clem[k][y]
                    self.llem2clem[k][x] = clem
                except:
                    pass

    def add_redund_map(self):
        self.redundant_map['quantum2'] = 'quantum3'
        for k, v in self.redundant_map.items():
            ku, kn = cut_num(k, 1)
            vu, vn = cut_num(v, 1)
            obj = self.llem2clem.get(ku)
            try:
                clem = obj[vn]
                self.llem2clem[ku][kn] = clem
            except:
                p(f'error in rendundant map {k} {v}')

        return





    def add_gender(self):
        dct = {
            'fm': 'B',
            'mn': 'X',
            'fn': 'Y',
            'fmn': 'C',
            'm': 'M',
            'n': 'N',
            'f': 'F',
            '': ''
        }

        error = set()
        error2 = defaultdict(dict)
        error3 = []
        for x, y in self.llem2clem.items():
            obj = self.all_lalems[x]

            for k, v in y.items():
                clem = x + v
                llem = x + k

                itm = self.co_lemmas4.get(clem)
                if not itm:
                    error2[x][k] = v
                else:
                    if itm['pos'] == 'n':
                        gen = dct[itm['pos']]
                        if gen:
                            self.noun2gender[llem] = gen
                        else:
                            error.add(clem)
        return

    def build_lem2forms_rev(self, kind=0):
        p('building lem2forms_rev')
        if kind:
            self.llem2clem = pi.open_pickle(f'{fold}llem2clem2')
            self.co_lemmas5 = pi.open_pickle(f'{fold}co_lemmas5')
        self.lem2forms_rev = {}
        self.lem2forms_rev_jv = {}
        p('opening pickles')
        lem2forms_ui = pi.open_pickle(f'{fold}lem2forms_ui')
        lem2forms_jv = pi.open_pickle(f'{fold}lem2forms_jv')
        c = 0
        # excel_functions.from_lst2book()
        for k, v in self.llem2clem.items():
            c += 1
            vgf.print_intervals(c, 200, None, len(self.llem2clem))
            for x, y in v.items():
                clem = k + y
                obj = lem2forms_ui[clem]
                obj2 = lem2forms_jv[clem]
                dct = defaultdict(set)
                dct2 = defaultdict(set)
                for b in obj.values():
                    pos = b[1]
                    dct[pos] = b[0]
                for b in obj2.values():
                    pos = b[1]
                    dct2[pos] = b[0]
                self.lem2forms_rev[clem] = dct
                self.lem2forms_rev_jv[clem] = dct2
        return


class bottom_most_la(match_colwlas):
    def __init__(self):
        match_colwlas.__init__(self)

    def begin_mcl(self, kind=0):
        if kind > -1:
            self.get_atts_mcl()
            self.use_fake_lemmas()
            self.use_la_fake_ambigs()
            self.use_typos()
            self.use_wrong_lasla_lemma()
            self.use_wrong_lpos()
            self.fix_las_freq()
            self.get_las_lem_freq()
            self.use_match_miss()
            self.use_imperfect_matches()
            self.use_lasla_def2coll_def()
            self.elim_pos_in_col()
            self.delete_bogus_pos()
            self.get_num_lems()
            self.output(5)  # used in the o_memorize module

        if kind > 0:
            self.get_lalems_pos()
            self.combine_proper()
            delattr(self, 'lalems_pos_rev2')
            self.lasla_pos_anomalies()
            self.elim_redundant_lasla()
            delattr(self, 'lalems_pos_rev3')
            self.remove_proper_l2f()
            self.four_categories()
            self.add_redund_lems()
            self.add_redund_map()
            self.got_everything()
            self.add_gender()
            self.build_lem2forms_rev()
            self.output(9)
            return

    def begin_mcl2(self):
        self.begin_mcl()
        self.del_attribs()
        self.rough_preliminary()

    def del_attribs(self):
        lst = ['lem2forms']
        if not self.kind == 3:
            for x in lst:
                delattr(self, x)


if eval(not_execute_on_import):
    if vgf.pycharm():
        args = [0, '1', '1', 'IX', '', 0, 0]
    else:
        args = vgf.get_arguments()

    if args[1] == 'rv':
        ins = convert2txt()
        ins.review()

    elif args[1] == 'pm':
        ins = prelim_match()
        ins.begin_pm()

    elif args[1] == 'pm2':
        ins = prelim_match()
        ins.kind = 0
        ins.rough_preliminary()

    elif args[1] == 'pm3':
        ins = bottom_most_la()
        ins.kind = 1
        ins.build_lem2forms_rev()
        ins.rough_preliminary()

    elif args[1] == 'fm':
        ins = handle_still_missing()
        ins.begin_fm(2)

    elif args[1] == 'a2c':
        ins = bottom_most_la()
        ins.build_colat5()

    elif args[1] == 'w2m':
        ins = bottom_most_la()
        ins.short_cut_w2m()
        ins.begin_w2m()

    else:
        ins = bottom_most_la()
        num = 0 if not args[1] else int(args[1])
        ins.begin_mcl(num)
