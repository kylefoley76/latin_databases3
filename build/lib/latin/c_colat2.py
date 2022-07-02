from bglobals import *


class top_most:
    def __init__(self):
        pass

    def get_atts(self):
        if not self.second:
            self.kind = 'g'  # this must be set to g in order to work
            # self.kind2 = 'e'
            self.kind2 = 'f'
            bb=8
            self.short = 0
            self.jv = JVReplacer()
            self.alemmas = defaultdict(dict)
            self.co_lemmas1a = pi.open_pickle(f'{fold}co_lemmas1a', 1)
            self.old2new_mods = pi.open_pickle(f'{fold}old2new_mods', 1)
            for k, v in self.co_lemmas1a.items():
                v['macron'] = ""
            self.lat_freq = pi.open_pickle(f'{fold}latin_freq', 1)
            lst = []
            self.ignore_stem = [x[0] for x in lst if len(x) > 1 and x[1] == 0]
            self.false_prefix = [x[0][1:] for x in lst if x[0][0] == '-']
            self.prefix, self.prefix2 = prefixes()
            self.accur = pi.open_pickle(f'{fold}accuracy', 1)
            self.pre3 = vgf.sort_lst_by_len(list(self.prefix.keys()), 1)
            self.pre_dcons = vgf.sort_lst_by_len(list(self.prefix2), 1)
            self.i2j = pi.open_pickle(f'{fold}i2j', 1)
            self.debug = ['peto']
            self.debug = ['aegates']
            self.debug = []
            self.lem2part = defaultdict(dict)
            self.lem2part2 = defaultdict(dict)
        if self.kind == 'g':
            self.form = 'geninf'
        else:
            self.form = 'perf'
        for k, v in self.co_lemmas1a.items():
            v[f'{self.form}m'] = []
        self.diph = ['ae', 'au', 'ei', 'eu', 'oe', 'ui']

        return

    def output(self, kind=1):
        if kind == 6:
            pi.save_pickle(self.stan2alt, f'{fold}stan2alt_spell', 1)
        if kind == 2:
            pi.save_pickle(self.co_lemmas1a, f'{fold}co_lemmas2', 1)
        if kind == 9:
            pi.save_pickle(self.col_dct, f'{fold}col_dct', 1)
        return


class step_three(top_most):
    def __init__(self):
        top_most.__init__(self)

    def quick_fix(self):
        if self.kind2 == 'e':
            return
        for k, v in self.co_lemmas1a.items():
            if k == 'crebresco':
                bb = 8

            if v['geninfm']:
                lst = [x for x in v['geninfm'] if not reg(r'[\)\(\-#]', x)]
                v['geninfm'] = lst
                self.co_lemmas1a[k] = v
            if v['perfm']:
                lst = [x for x in v['perfm'] if not reg(r'[\)\(\-#]', x)]
                v['perfm'] = lst
                self.co_lemmas1a[k] = v

    def fdiph_fu(self, med=0):
        if med:
            self.co_lemmas1a = pi.open_pickle(f'{fold}flemmas', 1)
            self.quick_fix()
            self.i2j = pi.open_pickle(f'{fold}i2j', 1)
        if not self.debug and not self.kind2 in ['e', 'f']:
            self.co_lemmas1a['nereides']['geninfm'] = ['nēried']
            self.co_lemmas1a['adrastis']['geninfm'] = ['ādrastid']
            self.co_lemmas1a['aeetias']['geninfm'] = ['aeētiad']
            self.co_lemmas1a['sanguinans']['geninfm'] = ['sanguinānt']

        self.counts = 0
        self.tjv = set()
        self.has_fd = {}
        self.errors_fd = {}
        if self.kind2 == 'e':
            lemmas = self.alemmas
        else:
            lemmas = self.co_lemmas1a

        auth_list = ['LS', 'GG', 'GJ', 'Ge', 'Lw', 'YO', 'PO']
        b =0
        for k, obj in lemmas.items():
            b += 1
            vgf.print_intervals(b,1000, None, len(lemmas))
            if self.kind2 == 'e':
                authors = auth_list
            else:
                authors = [0]

            for auth in authors:
                if auth:
                    v = obj.get(auth)
                else:
                    v = obj

                if v:
                    if k == 'ambiguitas':
                        bb = 8
                    self.lem_name = re.sub(r'[0-9]', '', v['lemma'])
                    if not 'geninfm' in v and self.kind2 == 'e':
                        pass
                    else:
                        v['geninfm'] = list(set(v['geninfm']))
                        v['perfm'] = list(set(v['perfm']))

                        if self.kind2 == 'e':
                            syl = v['macronjv']
                        else:
                            if not v['syl']:
                                syl = v['spell']
                            else:
                                syl = v['syl']
                        if not self.kind2 == 'e':
                            syl = norm_str_wmac(syl)
                            self.cat = 'macron'
                            self.step2(syl, v, k)
                            self.cat = 'geninfm'
                            syl = 0
                            if v[self.cat]:
                                bool1 = self.join_str(v)
                                if bool1:
                                    self.step2(syl, v, k)
                            self.cat = 'perfm'
                            if v[self.cat]:
                                bool1 = self.join_str(v)
                                if bool1:
                                    self.step2(syl, v, k)

        return

    def check_jv(self):
        '''
        the following are still missing
        ('accersio', 'accersiu')
        ('mauiael', 'mauiael')
        ('percompleo', 'percompleu')
        ('ioculatoria', 'ioculatoria')
        ('euilmerodach', 'euilmerodach')
        ('heuilath', 'heuilath')
        ('heuila', 'heuila')
        ('indignatiuum', 'indignatiuum')
        ('bethauen', 'bethauen')
        ('negatiua', 'negatiua')
        ('sepharuaim', 'sepharuaim')
        ('heuaeus', 'heuaeus')
        ('iuncina', 'iuncina')
        ('uolupe', 'uolup')
        ('c', 'inu')
        '''
        if self.kind2 == 'e':
            return
        miss = set(self.i2j.keys()) - self.tjv
        miss2 = self.tjv - set(self.i2j.keys())
        return

    def join_str(self, v):
        if v == 'z': return 0
        str1 = v[f'o{self.cat[:-1]}']
        str1_wom = unidecode(str1).lower()
        str1_wom = jv.replace(str1_wom)
        woml = str1_wom.split(',')
        dct = {}
        wo2mac = {}
        if type(v[self.cat]) == str:
            v[self.cat] = v[self.cat].split(',')

        for x in v[self.cat]:
            xwom = unidecode(x)
            wo2mac[xwom] = x
            found = 0
            for e, u in en(woml):
                if u == xwom:
                    dct[xwom] = e
                    found = 1
                    break
            if not found:
                self.errors_fd[v['lemma']] = v
        dct = sort_dct_val(dct)
        lst = []
        for x, y in dct.items():
            lst.append(wo2mac[x])
        str2 = ",".join(lst)
        str2_wom = unidecode(str2)
        if str2_wom != str1_wom:
            self.errors_fd[v['lemma']] = v
        v[self.cat] = str2

        return 1

    def step2(self, syl, v, k):
        if not syl:
            syl = v[f'o{self.cat[:-1]}'].lower()
            # if not syl:
            #     syl = v[f'{self.cat[:-1]}'].lower()

        syl2, fd, uw = remove_hats_diph(syl, syl, 1)
        if uw:
            self.add_uw(uw, v, syl)
        if fd:
            v[self.cat] = self.restore(fd, v, syl2)

        if fd or uw:
            self.has_fd[k] = v
        self.add_jv(v[self.cat], v)

    def add_uw(self, uw, v, syl):
        mac = v[self.cat]
        for i in uw:
            mac = replace_at_i(i, mac, chr(7909))
        v[self.cat] = mac

    def restore(self, fd, v, syl2):
        mac = v[self.cat]
        wo_mac = unidecode(syl2)
        brev = 'ăĕĭŏŭў'
        mac2 = ""
        found = 0
        for i in fd:
            lets = wo_mac[i:i + 2]
            letsm = syl2[i:i + 2]
            if lets in self.diph:
                if any(x in letsm for x in brev):
                    found = 1
                    mac2 = mac[:i] + syl2[i:i + 2]
                    if len(mac) > i + 2:
                        mac2 += mac[i + 2:]
                    else:
                        bb = 8
        if found:
            return mac2
        else:
            return mac

    def add_jv(self, mac3, v):
        if ',' in mac3:
            lst = mac3.split(',')
            lst1 = []
            for x in lst:
                y = self.add_jv2(x)
                lst1.append(y)
            y = ','.join(lst1)
        else:
            y = self.add_jv2(mac3)
        v[f'{self.cat}jv'] = y
        return

    def add_jv2(self, x):
        if x == 'adseruo':
            bb = 8
        macp = unidecode(x)
        lst = self.i2j.get((self.lem_name, macp), [[], []])
        if lst[0] or lst[1]:
            self.tjv.add((self.lem_name, macp))
            self.counts += 1

        for j in lst[0]:
            x = replace_at_i(j, x, 'j')
        for v in lst[1]:
            x = replace_at_i(v, x, 'v')
        return x


class step_two(step_three):
    def __init__(self):
        step_three.__init__(self)

    def begin_cl2(self):
        self.get_values()
        self.strincomm()  ## need an interval here
        self.get_lem_by_auth()
        self.still_missing()
        if self.kind2 == 'e':
            self.each_author()

    def get_values(self):  # 13062
        self.lem2part3 = defaultdict(dict)
        self.lem2part4 = defaultdict(dict)
        if self.kind == 'p':
            form = 'perf'
        else:
            form = 'geninf'

        c = 0
        self.no_geninf = defaultdict(dict)
        mult = defaultdict(dict)
        self.geninf2lem = defaultdict(set)

        for k, v in self.lem2part.items():  # todo put an interval here
            # p (k)
            lemma = self.co_lemmas1a[k]
            geninf = lemma[form]
            if geninf:
                c += 1
                geninf = norm_str_jv(geninf)
                geninf2 = tuple(vgf.strip_n_split(geninf, ","))
                for x, z in v.items():
                    if k == 'coerceo':
                        bb = 8

                    found = 1
                    got = 0
                    y = norm_str_jv(z)
                    geninf3 = 0
                    if all(t not in y for t in geninf2):
                        geninf3 = tuple(self.word2prefix.get(u, ("", u)) for u in geninf2)
                        found = 2
                        if all(t[1] not in y for t in geninf2):
                            self.no_geninf[k][x] = [geninf, y]
                            self.lem2part3[k][x] = [geninf, y, 0]
                            got = 1
                            found = 0

                    if not geninf3:
                        geninf3 = tuple(("", q) for q in geninf2)

                    if found:
                        if found == 2 and len(geninf2) > 1:
                            bb = 8
                        for gf in geninf3:
                            pre = gf[0]
                            gf = gf[1]
                            self.geninf2lem[(pre + gf), x].add(k)
                            if gf in y:
                                if len(geninf2) > 1:
                                    bb = 8
                                b = y.count(gf)
                                z = self.jv.replace(z)
                                lst = [gf, z]
                                for i in range(b):
                                    idx = y.index(gf)
                                    s = z[idx:idx + len(gf)]
                                    y = y[idx + len(gf):]
                                    z = z[idx + len(gf):]
                                    if pre:
                                        if gf[-1] == gf[0] and gf[:-1] in self.prefix2:
                                            pre_mac = pre
                                        else:
                                            pre_mac = self.prefix.get(pre)
                                        s = f'{pre}{s}'
                                    s = s.lower()
                                    lst.append(s)
                                got = 1
                                self.lem2part3[k].setdefault(x, []).append(lst)
                                if len(lst) > 3:
                                    mult[k][x] = lst
                    if not got:
                        self.lem2part3[k][x] = [geninf, y, 0]

        if c != len(self.lem2part3):
            p('missing in lem2part3')

        return

    def each_author(self):
        lst1 = ['LS', 'GG', 'GJ', 'Ge', 'Lw', 'YO', 'PO']
        b = 0
        for k, v in self.col_dct.items():
            already = 0
            for z in v:
                auth = z[0]
                if auth in lst1 and len(z) > 2:
                    if not self.second:
                        lem = new_lem2(k)
                        lem['lemma'] = z[2]
                        obj2 = self.co_lemmas1a[k]
                        lem['lexicon'] = obj2['lexicon']
                        lem['quantity'] = ""
                        lem['model'] = obj2['model']
                        lem['model'] = self.old2new_mods.get(lem['model'], lem['model'])
                        lem[self.form] = ""

                    else:
                        obj = self.alemmas.get(k)
                        if obj:
                            lem = obj[auth]
                    em = self.emiss.get(k)
                    if em:
                        if auth in em:
                            lem[f'{self.form}'] = em[auth]
                            if not already:
                                b += 1
                            already = 1
                    else:

                        obj = self.lem2part3.get(k)
                        if obj:
                            itm = obj.get(auth)
                            if itm:
                                if type(itm[0]) == list and itm[0][2]:
                                    lst4 = [y[2] for y in itm]
                                    d = ','.join(lst4)
                                    # if d != lem['lemma']:
                                    lem[f'{self.form}'] = d

                    if not self.second:
                        self.alemmas[k][auth] = lem

        return

    def adhoc_comma(self):
        lst = to.from_txt2lst_tab_delim(f'{fold}stem_comma')
        lst1 = to.from_txt2lst_tab_delim(f'{fold}stem_comma_got')
        dct4 = {}
        for x in lst:
            dct4[x[0], x[2]] = f'{x[4]},{x[5]}'
        for x in lst1:
            dct4[x[0], x[2]] = x[4]
        for x, y in dct4.items():
            obj = self.alemmas[x[0]]
            for k, v in obj.items():
                stem = x[1]
                s = y
                v[stem] = s

    def check_alemma(self):
        if self.second:
            '''
            tharsis: thars,tharsid
            iaiunitas: 'iaiunitat,ieiunitat'
            saeclaris: 'saeclar,saecular'
            '''

            dct = defaultdict(dict)
            for k, v in self.alemmas.items():
                lem = self.co_lemmas1a.get(k)
                if lem:
                    for l in ['geninf', 'perf']:
                        s = lem.get('o' + l)
                        if s:
                            gnum = s.count(',')
                            num = 0
                            ts = ''
                            for x, y in v.items():
                                t = y.get(l)
                                if t:
                                    if not ts:
                                        ts = t
                                    num1 = t.count(',')
                                    if num1 > num:
                                        num = num1
                                        ts = t
                            if num != gnum:
                                dct[k][l] = [lem[l], ts]
            if len(dct) > 1:
                p(f'{len(dct)} still have wrong commas')
                self.fix_stem_alt(dct)
        return

    def fix_stem_alt(self, dct):
        by_hand2 = []
        b = 0
        got = []
        lst7 = []
        for k, v in dct.items():
            for stem, y in v.items():
                orig = y[0]
                target = y[1]
                mlem = self.get_mac(k)
                if not target:
                    lst7.append([k, mlem, stem, orig])

                else:
                    targetu = unidecode(target)
                    ost = set(orig.split(','))
                    tst = targetu.split(',')
                    tst = [remove_hats_diph(f, f) for f in tst]
                    tst_or = target.split(',')
                    rem = ost - set(tst)
                    have = ost & set(tst)
                    tar_lst = target.split(',')
                    have_ma = []
                    for s in tar_lst:
                        su = unidecode(s)
                        if su in have:
                            have_ma.append(s)

                    lst = []
                    by_hand = []
                    for w in rem:
                        found = 0
                        vow1 = elim_cons(w)
                        for z in tst:
                            vow2 = elim_cons(z)
                            if vow1 == vow2:
                                b += 1
                                for s, com in zip(tst, tst_or):
                                    if s == z:
                                        break

                                nword = match_vowels(com, w)
                                lst.append(nword)
                                found = 1
                                break
                        if not found:
                            by_hand.append(w)
                    if by_hand:
                        by_hand = [k, mlem, stem, orig, target] + by_hand
                        by_hand2.append(by_hand)
                    else:
                        o = ','.join(have_ma + lst)
                        lst4 = [k, mlem, stem, orig, o]
                        got.append(lst4)
        return

    def get_mac(self, k):
        for auth in authors3:
            try:
                return self.alemmas[k][auth]['lemma']
            except:
                pass

    def strincomm(self, debug=0):
        if debug:
            self.lem2part3 = pi.open_pickle(f'{fold}lem2part3', 1)
            self.disg2 = pi.open_pickle(f'{fold}disg2', 1)
        dct = defaultdict(dict)
        hi2mi = {}
        cends = ['e', 'is', 'ium', 'um', 'ae', 'us', 'eos', 'idis', 'a',
                 'euntis', 'm.', 'f.', 'n.', 'ydis', 'ycis', 'i', 'es', 'yos', 'indecl.', 'ii', 'ius']
        self.mixed = defaultdict(dict)
        most = defaultdict(int)
        miss = defaultdict(dict)
        p (f'now mapping participles to lemmas')
        self.diff_stem = defaultdict(dict)
        b = 0
        for k, v in self.lem2part3.items():  # todo another interval here
            b += 1
            if self.kind == 'g':
                vgf.print_intervals(b,200,None,len(self.lem2part3))
            for x, y in v.items():
                if y[-1] == 0 and y[1]:
                    lemma = self.co_lemmas1a.get(k)
                    lemma = lemma['lemma']
                    lemma_mac = self.disg2[lemma][x]
                    if k == 'coerceo':
                        bb = 8

                    u = y[1].strip()
                    o = u
                    gns = y[0]
                    lst5 = []
                    gns_lst = gns.split(',')
                    mginf = []
                    got_ginf = []
                    lst = u.split()
                    fword = lst[0]
                    fword = fword.replace(',', '')
                    if any(cend == fword for cend in cends) or \
                            u in ['ire', 'are', 'ere']:
                        if all(not lemma.startswith(g) for g in gns_lst):
                            bad, good = self.almost_inside(gns_lst, lemma, lemma_mac)
                            if good:
                                y[-1] = good
                                if bad:
                                    self.mixed[k][x] = [y, bad]

                    elif '&mdash' in u:
                        pass
                    else:
                        most[o] += 1

                        best_fit = defaultdict(dict)
                        best_left = defaultdict(dict)
                        for g in gns_lst:
                            lst1 = list(g)
                            for e, s in en(lst):
                                t = norm_str_jv(s)
                                t = re.sub(r'[^a-z]', '', t)
                                lst2 = list(t)
                                n = 1
                                lidx = 0
                                mx = 0
                                while n < len(lst2):
                                    right = lst2[:n]
                                    left = lst1[-n:]
                                    if right == left:
                                        mx = n
                                        lidx = len(lst1) - n
                                    n += 1
                                if mx:
                                    best_fit[g][s] = mx
                                    best_left[g][s] = lidx

                        if best_fit:
                            for g, dc in best_fit.items():  ## use self.disg2, get str3 from there according to author then cut str
                                dc = sort_dct_val_rev(dc)
                                str2 = vgf.dct_idx(dc)
                                lidx = best_left[g][str2]
                                str2 = norm_str_wmac(str2)
                                str2 = remove_hats(str2)
                                mx = vgf.dct_idx(dc, 0, 'v')
                                str2 = str2[:mx]
                                str3 = g[:lidx]
                                lemma2 = lemma[:lidx]
                                lemma_mac, cidx = self.adj_cobr(lemma_mac)
                                nstr = lemma_mac[:lidx] + str2
                                nstr = self.rest_cobr(nstr, cidx)
                                if lemma2 != str3:
                                    self.diff_stem[k][x] = [g, o, nstr]
                                else:
                                    lst5.append(nstr)
                                    got_ginf.append(g)
                        else:
                            mginf.append(g)
                        if lst5:
                            if mginf:
                                hi2mi[tuple(got_ginf)] = mginf
                            lst6 = []
                            for t in lst5:
                                t = t.lower()
                                lst6.append([g, o, t])
                            self.lem2part3[k][x] = lst6
                            dct[k][x] = lst6
                        else:
                            self.lem2part3[k][x] = y
                            miss[k][x] = y

        return

    def adj_cobr(self, x):
        if cobr in x:
            idx = x.index(cobr)
            x = x.replace(cobr, "")
            return x, idx
        return x, 0

    def rest_cobr(self, x, cidx):
        if cidx:
            return add_at_i(cidx, x, cobr)
        return x

    def stem_head(self, k, v):
        olem = self.co_lemmas1a[k]
        s = olem[f'o{self.form}'].lower()
        s = s.replace(cobr, '')
        alt = self.stan2alt.get(k)
        syl = olem['syl']
        syl = remove_hats_diph(syl, syl)
        kvowels = re.sub(r'[^aeiouyāēīōūȳăĕĭŏŭў]', '', syl)
        lst = s.split(',')
        lst = [remove_hats_diph(x, x) for x in lst]
        for auth, alst in v.items():
            tword = self.lem_by_auth[k][auth]
            lst1 = []
            for word in lst:
                vowels = re.sub(r'[^aeiouyāēīōūȳăĕĭŏŭў]', '', word)
                if kvowels.startswith(vowels):
                    nstem = match_vowels(tword, word)
                    lst1.append(nstem)
                else:
                    self.missing[(k, syl)].add(word)
            alst[0][2] = ",".join(lst1)

        return

    def get_lem_by_auth(self):
        dct = defaultdict(dict)
        for k, v in self.col_dct.items():
            for z in v:
                if z[0] in authors:
                    if len(z) > 2:
                        dct[k][z[0]] = z[2]
        self.lem_by_auth = dct

    def still_missing(self):
        '''
        for this class we have already tested that all vowels
        are the same in the geninf and the lemma
                #aborigines, abcido
        '''
        '''
        currently there are no lsts in lem2part3 in the dictionary
        which are longer than 1
        '''

        for k, v in self.lem2part3.items():
            found = 0
            for x, y in v.items():
                if type(y[0]) == str:
                    v[x] = [y]
                    found = 1
            if found:
                self.lem2part3[k] = v

        err_corr = to.from_txt2lst_tab_delim(f'{fold}{self.form}_errors_corr')
        err_corr2 = to.from_txt2lst_tab_delim(f'{fold}{self.form}_errors_corr2')
        err_corr = {x[0]: x[2] for x in err_corr}
        err_corr2 = {x[0]: x[2] for x in err_corr2}
        err_corr = merge_2dicts(err_corr, err_corr2)
        self.missing = defaultdict(set)
        self.mac_roots = {}
        self.emiss = defaultdict(dict)
        setattr(self, f'{self.form}_errors', {})
        dct_err = getattr(self, f'{self.form}_errors')
        wrong_roots = []
        for k, v in self.lem2part3.items():
            if k in err_corr:
                self.add2v(k, v, err_corr)
            else:
                if all(z[2] == 0 for x, y in v.items() for z in y):
                    if k == 'coerceo':
                        bb = 8
                    self.stem_head(k, v)

        p(f'still missing {len(self.missing)}')
        to.from_lst2txt_tab_delim(wrong_roots, f'{fold}{self.form}_errors')
        return

    def add2v(self, k, v, err_corr):
        s = err_corr[k]
        for x, y in v.items():
            y[0][2] = s

    def temp24(self):
        lst = []
        dct2 = {}
        for x, y in self.missing.items():
            s = list(y)[0]
            lst.append([x[0], x[1], s])
            dct2[x[0]] = self.lem_by_auth[x[0]]
        to.from_lst2txt_tab_delim(lst, f'{fold}{self.form}_errors2')

    def almost_inside(self, gns, lemma, lemma_mac):
        lemma_mac_nc, cidx = self.adj_cobr(lemma_mac)
        if cidx:
            bb = 8
        lst = []
        found = 0
        fine = []
        for g in gns:
            b = 0
            for x, y in zip(g, lemma):
                if x != y:
                    rem = g[b:]
                    if reg(r'[aeiouy]', rem):
                        lst.append([g, rem])
                    else:
                        str1 = lemma_mac_nc[:b] + g[b:]
                        str1 = self.rest_cobr(str1, cidx)
                        fine.append(str1)
                        found = 1
                    break
                b += 1
        if cidx and not found:
            bb = 8

        if lst and fine:
            bb = 8

        return lst, ','.join(fine)


class step_one(step_two):

    def __init__(self):
        '''
        kind indicates whether we are parsing geninf (genitive/infinitive) or perf, g for
        geninf, p for perf (perfect)

        '''

        step_two.__init__(self)

    def fix_qerrors(self):
        dct = {
            'a_': 'ā',
            'e_': 'ē',
            'i_': 'ī',
            'o_': 'ō',
            'u_': 'ū',
            'y_': 'ӯ',
        }
        self.get_atts()
        self.step1()
        self.mlst = to.from_txt2lst_tab_delim(f'{fold}quantity_errors')
        still_miss = []
        for l in self.mlst:
            obj = self.col_dct.get(l[2])
            if not obj:
                still_miss.append(l)
            else:
                done = 0
                for auth in authors3:
                    if done:
                        break
                    for e, r in en(obj):
                        if r[0] == auth:
                            if len(r) > 2:
                                nword = r[2]
                                nword = nword.lower()

                                if e == 6:
                                    nword = nword.split('=')[0]
                                elif e == 7:
                                    str1 = nword
                                    for s, t in dct.items():
                                        str1 = str1.replace(s, t)
                                    if ',' in str1:
                                        lst4 = str1.split(',')
                                        str1 = lst4[0]
                                    if ':' in str1:
                                        lst4 = str1.split(':')
                                        str1 = lst4[0].strip()
                                    assert ' ' not in str1
                                    nword = str1

                                nword = remove_hats_diph(nword, nword)
                                done = 1
                                l[2] = nword
                                break

        self.still_miss = still_miss
        to.from_lst2txt_tab_delim(self.mlst, f'{fold}quantity_errors_corr')
        to.from_lst2txt_tab_delim(still_miss, f'{fold}quantity_errors2')

    def normalize_perf(self):
        # todo there are a lot of false diphthongs in the geninf
        # and perf stems because collatinus treats āe to mean that
        # the diphthong ae is long

        for k, v in self.co_lemmas1a.items():
            if v['geninf']:
                g = v['geninf']
                if g == '-':
                    g = ""
                v['ogeninf'] = g.lower()
                v['geninf'] = norm_str_jv(g)
            if v['perf']:
                g = v['perf']
                if g == '-':
                    g = ""
                v['operf'] = g.lower()
                v['perf'] = norm_str_jv(g)
        return

    def elim_prefix(self, word, targets, fake=0):
        lst = []
        for pre in self.pre3:
            if len(word) > len(pre) and word.startswith(pre):

                n = word[len(pre):]
                if n in targets:
                    return n, self.prefix[pre], pre, 0
        for pre in self.pre_dcons:
            if len(word) > len(pre) + 1 and word.startswith(pre) \
                    and word[len(pre)] == word[len(pre) + 1]:
                n = word[len(pre) + 1:]
                pre_dc = word[:len(pre) + 1]
                if n in targets:
                    return n, pre_dc, pre_dc, 0
                elif fake:
                    lst.append([n, pre_dc, pre_dc, 1])

        if fake:
            if lst:
                return lst[0]

            for pre in self.pre3:
                if len(word) > len(pre) and word.startswith(pre):
                    n = word[len(pre):]
                    return n, self.prefix[pre], pre, 0

        return 0, 0, 0, 0

    def step1(self):
        '''
        here we convert the lem_coll5 sheet into the col_dct method

        FG does not have vowel quantity
        YO has an = inbetween sometimes, just use first for now
        PO has _ instead of a macron
        WW can also be ignored
        Lw has syllables
        skip 4, 8 ww
        combined breve chr 774

        impes does not go into flemmas
        '''
        lems = []
        done = 0
        lst = to.from_txt2lst(f'{fold}lem_coll5')
        lst1 = to.from_txt2lst(f'{fold}lem_coll_extra')
        lst += lst1
        lst = [x.split('|') for x in lst]
        dct = defaultdict(list)
        lst1 = ['LS', 'GG', 'GJ', 'Ge', 'FG', 'Lw', 'YO', 'PO', 'WW']
        b = 0
        for e in range(0, len(lst), 10):
            for z in lst[e]:
                if 'impes=' in z:
                    # p('hey')
                    bb = 8
                if hl(z):
                    break

            if done:
                break
            for i in range(0, 9):
                str2 = lst1[i]
                str1 = lst[i + e + 1][0]
                if i == 6 and str2.startswith('Y'):
                    lst[i + e + 1][0] = 'YO'
                elif str1 != str2:
                    p(f'error {e}')
                    done = 1
                    break
                dct[z].append(lst[i + e + 1])
            b += 1
            if self.short:
                if b > 10_000:
                    break
        self.col_dct = dct

        if 'c' in self.col_dct:
            del self.col_dct['c']

        if self.debug:
            self.col_dct = {k: v for k, v in self.col_dct.items() if k in self.debug}
        return

    def fix_lw(self):
        jv = JVReplacer()
        bad = ['(', ',', ' or ', ' ']
        for k, v in self.col_dct.items():
            str2 = unidecode(k.lower())

            if str2[-1].isdigit():
                str2 = str2[:-1]

            if len(v[5]) > 2:
                str8 = v[5][2]
                str8 = str8.lower()
                str8 = jv.replace(str8)
                if str8[0] == '(':
                    str8 = str8[1:]
                if str8[-1] == ')':
                    str8 = str8[:-1]

                str1 = str8
                found = 0
                if ' - ' in str1:
                    idx = str1.index('-')
                    if "(" in str1:
                        idx2 = str1.index('(')
                        if idx2 > idx:
                            str1 = str1[:idx2].strip()
                        else:
                            assert 0

                    str3 = str1.replace(' - ', '')
                    str4 = unidecode(str3)
                    if str2 == str4:
                        str1 = str3
                        found = 1
                if not found:
                    dct7 = {}
                    for bd in bad:
                        if bd in str1:
                            dct7[bd] = str1.index(bd)
                    if dct7:
                        dct7 = sort_dct_val(dct7)
                        bd = vgf.dct_idx(dct7, 0, 'v')
                        str1 = str1[:bd]
                str1 = str1.replace('-', '')
                str1u = unidecode(str1)
                if str1u != str2:
                    p(f'{str1}    {str8}  {k}')
                str1 = remove_hats(str1)
                assert ' ' not in str1
                v[5][2] = str1
                try:
                    if v[5][3] and "," in v[5][3] and self.research_ostem(k):
                        self.lem2part[k]['Lw'] = v[5][3]
                except:
                    pass

        return

    def alternate_spell(self):
        ndct = {}
        self.stan2alt = {}
        for k, v in self.col_dct.items():
            if '=' in k:
                lst = k.split('=')
                self.stan2alt[lst[0]] = lst[1]
                ndct[lst[0]] = v
            else:
                ndct[k] = v
        self.col_dct = ndct

    def jv_rep(self):

        jv = JVReplacer()
        dct = {}
        b = 0
        for k, v in self.col_dct.items():
            k1 = jv.replace(k)
            if k1 in self.co_lemmas1a:
                dct[k1] = v

        self.col_dct = dct
        self.co_lemmas1a = {k: v for k, v in self.co_lemmas1a.items() if k in self.col_dct}
        return

    def fix_po(self):
        self.po_altsp = defaultdict(list)
        dct = {
            'a_': 'ā',
            'e_': 'ē',
            'i_': 'ī',
            'o_': 'ō',
            'u_': 'ū',
            'y_': 'ӯ',
        }
        idx = 2
        for k, v in self.col_dct.items():
            if len(v[7]) > 2:
                str1 = v[7][idx]
                str1 = str1.lower()
                str1 = self.jv.replace(str1)
                for s, t in dct.items():
                    str1 = str1.replace(s, t)

                if ',' in str1:
                    # if idx
                    str2 = str1[str1.index(',') + 1:]
                    if self.research_ostem(k):
                        self.lem2part[k]['PO'] = str2

                    lst4 = str1.split(',')
                    str1 = lst4[0]

                if ':' in str1:
                    lst4 = str1.split(':')
                    str1 = lst4[0].strip()

                assert ' ' not in str1

                v[7][2] = str1

        for k, v in self.col_dct.items():
            if len(v[7]) > 2:
                kd = self.del_num(k)
                z = v[7][2]
                oz = z
                if k == 'asylum':
                    bb = 8

                zu = unidecode(z)

                if zu != kd:
                    # p(f'{zu} {k} {oz}')
                    v[7][2] = ''
                else:
                    z = remove_hats(z)
                    v[7][2] = z

        return

    def del_num(self, x):
        if x[-1].isdigit():
            return x[:-1]
        return x

    def research_ostem(self, k):
        if self.co_lemmas1a[k].get('ogeninf') or self.co_lemmas1a[k].get('operf'):
            return 1

    # def redundant_stems(self):
    #     erased = 0
    #     '''
    #     i think this messed up the old decliner but not the new
    #     one so might be redundant
    #     '''
    #
    #     for k, v in self.lemmas.items():
    #         if v.get('operf') and v['operf'] == v['syl']:
    #             v['operf'] = ""
    #             v['perf'] = ""
    #             erased += 1
    #         if v.get('ogeninf') and v['ogeninf'] == v['syl']:
    #             v['ogeninf'] = ""
    #             v['geninf'] = ""
    #             erased += 1
    #     return

    def fix_ge(self):
        for k, v in self.col_dct.items():
            if len(v[3]) > 2:
                str1 = v[3][2]
                if str1:
                    kd = self.del_num(k)
                    str1 = self.jv.replace(str1)
                    str1 = str1.lower()
                    str1 = str1.replace('-', '')
                    str1 = str1.replace('*', '')
                    str1 = remove_hats(str1)
                    str1u = unidecode(str1)

                    if str1u != kd:
                        if not public:
                            p(f'ill-formed: {kd} {str1}')
                    assert ' ' not in str1
                    v[3][2] = str1
                try:
                    if v[3][3] and self.research_ostem(k):
                        self.lem2part[k]['Ge'] = v[3][3]
                except:
                    pass

        return

    def build_prefix_dct(self):
        self.word2prefix = {}
        self.all_geninf = set()
        self.fake_prefixes = set()
        excep = ['aetias', 'aeetis']
        if self.kind == 'p':
            form = 'perf'
        else:
            form = 'geninf'
        for k, v in self.lem2part.items():
            lemma = self.co_lemmas1a.get(k)
            if lemma[form] and lemma['model'] not in greek_models() \
                    and k not in excep:
                s = lemma[form]
                t = self.jv.replace(s)
                g = set(t.split(','))
                g = set(h.lower() for h in g)
                self.all_geninf |= g

        for w in self.all_geninf:
            y, z, pre, fake = self.elim_prefix(w, self.all_geninf, 1)
            if y:
                if fake and y not in self.ignore_stem:
                    self.fake_prefixes.add(y)
                self.word2prefix[w] = (pre, y)
        assert 'admeto' not in self.word2prefix
        return

    def jv_others(self):
        p(f'putting the macrons into a standard form')
        b = 0
        for k, v in self.col_dct.items():
            b += 1
            vgf.print_intervals(b,1000,None,len(self.col_dct))
            for i in range(0, 3):
                if len(v[i]) > 2:
                    str1 = self.jv.replace(v[i][2])
                    str1 = str1.lower()
                    str1 = remove_hats(str1)
                    if ' ' in str1:
                        # p (f'SPACE {str1}')
                        str1 = str1[:str1.index(' ')]

                    v[i][2] = str1
                try:
                    if self.research_ostem(k):
                        self.lem2part[k][v[i][0]] = v[i][3]
                except:
                    pass
        return

    def fix_yo(self):
        for k, v in self.col_dct.items():
            if len(v[6]) > 2:
                ku = self.del_num(k)
                str1 = v[6][2]
                ostr = str1
                str1 = self.jv.replace(str1)
                str1 = str1.split('=')[0]
                str1 = str1.lower()
                str1 = self.del_num(str1)
                str1u = unidecode(str1)
                if str1u != ku:
                    p(f'error in yo {k} {ostr} {str1}')
                no_hats = str1
                str1 = remove_hats(str1)
                assert ' ' not in str1
                v[6][2] = str1
                try:
                    if not v[6][4] and v[6][6]:
                        self.lem2part[k]['YO'] = self.jv.replace(v[6][6].lower())
                    elif v[6][4]:
                        self.lem2part[k]['YO'] = self.jv.replace(v[6][4].lower())
                    if v[6][5]:
                        self.lem2part2[k]['YO'] = self.jv.replace(v[6][5].lower())
                except:
                    pass

        return

    def lem2vquant(self, dct4, dct5, cap):
        ge = dct5.get('PO')
        if ge:
            return ge
            # if ge[0].isupper():
            #     return ge.capitalize()
            # else:
            #     return ge

        if 'YO' in dct4 and 'GJ' in dct4 and len(dct4) == 2:
            return dct5['YO']

        if len(dct5) == 1:
            # if cap:
            #     return vgf.dct_idx(dct5, 0, 'v').capitalize()
            # else:
            return vgf.dct_idx(dct5, 0, 'v')
        else:
            dct7 = defaultdict(int)
            for k, v in dct4.items():
                if k not in ['YO', 'GJ']:
                    dct7[v] += 1
            dct7 = sort_dct_val_rev(dct7)
            if len(dct7) == 1:
                # if cap:
                #     return vgf.dct_idx(dct5, 0, 'v').capitalize()
                # else:
                return vgf.dct_idx(dct5, 0, 'v')
            else:
                num1 = vgf.dct_idx(dct7, 0, 'v')
                num2 = vgf.dct_idx(dct7, 1, 'v')
                word1 = vgf.dct_idx(dct7, 0, 'k')
                if num1 > num2:
                    word = vgf.dct_idx(dct7)
                    for k, v in dct5.items():
                        if word in v:
                            return v
                    # if cap:
                    #     return word.capitalize()
                    # else:
                    assert 0

                else:
                    dct8 = {}
                    lst = []
                    for x, y in dct7.items():
                        if y == num1:
                            lst.append(x)
                    for x, y in dct4.items():
                        if y in lst:
                            dct8[x] = self.accur[x]

                    dct8 = sort_dct_val(dct8)
                    name = vgf.dct_idx(dct8)
                    # if cap:
                    #     return dct5[name].capitalize()
                    # else:
                    return dct5[name]


    def agreement(self, lem2quant=0):  # 5610
        p (f'deciding which dictionary author is the most reliable')

        lst = [0, 1, 2, 3, 5, 6, 7]
        disg = {}
        disg2 = {}
        b = 0
        for k, v in self.col_dct.items():
            b += 1
            vgf.print_intervals(b, 1000, None, len(self.col_dct))
            if k == 'xerxes':
                bb = 8
            wrds = set()
            dct4 = {}
            dct5 = {}
            lemma = self.co_lemmas1a[k]
            beg = 0
            for i in lst:
                if len(v[i]) > 2:
                    if v[i][1][0].isupper():
                        beg = 1
                        break

            for i in lst:
                if i == 2:
                    bb = 8
                if len(v[i]) > 2:
                    name = v[i][0]
                    word = v[i][2]
                    word2 = self.jv.replace(word).lower()
                    end = len(word)
                    if reg(r'[aeiou]$', k):
                        end = -1
                    word1 = word[beg:end]
                    wrds.add(word1)
                    dct4[name] = word1
                    dct5[name] = word2

            if len(wrds) > 1:
                rword = self.lem2vquant(dct4, dct5, beg)
                lemma['macron'] = rword
            else:
                lemma['macron'] = word

            disg[k] = dct4
            disg2[k] = dct5

        self.disg2 = disg2



        dct = {}
        for k, v in self.co_lemmas1a.items():
            if not v['macron']:
                dct[k] = v
                p(k)
        if dct:
            p('error in macron')
            assert 0

        return



    def match_gen2stem(self):
        '''
        beginning with this method, i adopted a method
        where i tried to find the vowel lengths by separating words
        from their prefix and assuming that the prefix always had
        the same vowel length and that the main stem also always
        had the same vowel length.  This idea was discarded
        since it assumed too much.  The only way to really find out
        if a stem always had the same vowel length was to check it against
        the pedecerto database
        '''

        disg = self.disg2
        self.gen2stem = defaultdict(dict)
        miss = []
        self.gen2entry = defaultdict(dict)

        # dct = {}
        # for k, v in self.lem2part3.items():
        #     for x, y in v.items():
        #         if not y[0][2]:
        #             dct[k] = v
        #             break

        for k, v in self.lem2part3.items():
            obj = disg[k]
            for x, y in v.items():
                if len(y) > 2 and not y[2]:
                    self.gen2stem[k][x] = [0, lst]
                else:
                    lst = [remove_hats(z[2]) for z in y if z[2]]
                    stem = obj[x]
                    for z in y:
                        if z[2]:
                            g = remove_hats(z[2])
                            self.gen2entry[k][(x, g)] = z[1]
                        else:
                            self.gen2entry[k][(x, 0)] = 0
                    self.gen2stem[k][x] = [stem, lst]
        file = f'{fold}gen2stem'
        lst = [self.gen2stem, self.gen2entry, self.word2prefix, self.fake_prefixes, self.all_geninf]
        pi.save_pickle(lst, file, 1)
        return

    def auth_contr(self, debug=0):
        if debug:
            file = f'{fold}gen2stem'
            lst = pi.open_pickle(file, 1)
            self.gen2stem = lst[0]
            self.gen2entry = lst[1]
            self.word2prefix = lst[2]
            self.fake_prefixes = lst[3]
            self.all_geninf = lst[4]

        self.self_contr = defaultdict(dict)
        analyze = defaultdict(dict)
        stats = defaultdict(int)
        tot = defaultdict(int)
        dct = defaultdict(dict)
        for x, y in self.gen2stem.items():
            for k, v in y.items():
                if k != 'YO':
                    dct[x][k] = v
        self.gen2stem = dct
        ratio = {}
        p (f'now getting the genitive or perfect stem'
           f' from the dictionary entry')
        c =0
        for x, y in self.gen2stem.items():
            if self.kind != 'p':
                c += 1
                vgf.print_intervals(c,200,None, len(self.gen2stem))
            wrong = 0
            for k, v in y.items():
                if not v[1]:
                    bb = 8

                stem = v[0]
                stem2 = unidecode(stem)
                if k in ['Ge', 'PO']:
                    bb = 8
                for gn in v[1]:
                    tot[k] += 1
                    gn2 = unidecode(gn)
                    b = 0
                    found = 0
                    for t, z in zip(stem2, gn2):
                        ms = stem[b]
                        mg = gn[b]
                        if t == z:
                            if ms != mg:
                                self.self_contr[x][k] = v
                                s = self.gen2entry[x][(k, gn)]
                                analyze[x][k] = [gn, stem, s, 0]
                                stats[k] += 1
                                wrong += 1
                                found = 1
                                break
                        else:
                            break

                        b += 1
                    if not found:
                        s = self.gen2entry[x][(k, gn)]
                        analyze[x][k] = [gn, stem, s, 1]
            # if len(y) > 1:
            rat = int((wrong / len(y)) * 100)
            ratio[x] = rat
        ratio = sort_dct_val_rev(ratio)
        rat_ana = {}
        for k, v in ratio.items():
            rat_ana[k] = analyze[k]
        self.rat_ana = rat_ana
        # for k, v in tot.items():
        #     mis = stats[k]
        #     perc = int((mis / v) * 100)
        #     p(k, perc)

        return

    def ana_wo_prefix(self):
        self.wo_prefix = defaultdict(list)
        self.wo_prefix_fake = defaultdict(list)
        anom = {}
        anom2 = {}
        anom3 = {}
        pdct = {
            'col': 'con',
            'sur': 'sub',
            'suc': 'sus'
        }

        for k, v in self.rat_ana.items():
            if not v:
                anom3[k] = v
            else:
                if k == 'recido2':
                    bb = 8

                obj = vgf.dct_idx(v, 0, 'v')
                word = obj[0]
                word_nm = unidecode(word)
                head = obj[1]
                head_nm = unidecode(head)
                tpl = self.word2prefix.get(word_nm)
                pre = ""
                if tpl and k not in self.false_prefix:
                    pre = tpl[0]
                    main = tpl[1]
                    start = len(pre)
                    bod_head = head_nm[start:]
                    bod_pre = head_nm[:start]
                    if bod_pre != pre:
                        if pre not in pdct:
                            start = 0
                        anom[k] = v
                else:
                    start = 0
                    bod_head = head_nm[start:]
                    main = word_nm

                dct = {}
                dct1 = {}
                for auth, lst in v.items():
                    if k == 'recido2' and auth == 'Lw':
                        bb = 8

                    try:
                        word3 = lst[0][start:]
                        head3 = lst[1][start:]
                        lst1 = [word3, head3, lst[2], k, lst[3], pre]
                        dct[auth] = lst1
                    except IndexError:
                        word3 = lst[0]
                        head3 = lst[1]
                        dct1[auth] = [word3, head3, lst[2], k, lst[3], pre]
                if dct1:
                    anom2[main] = dct1
                if main in self.fake_prefixes:
                    self.wo_prefix_fake[main].append(dct)
                self.wo_prefix[main].append(dct)
        return

    def ana_wo_prefix2(self):
        self.ranking = {
            'GJ': 2,
            'PO': 6,
            'Lw': 4,
            'LS': 3,
            'GG': 4,
            'Ge': 5
        }
        freq = defaultdict(dict)
        singles = defaultdict(dict)
        fake_freq = defaultdict(dict)
        for x, y in self.wo_prefix.items():
            single = 0
            if len(y) == 1:
                single = 1
            for dct in y:
                for auth, lst in dct.items():
                    word = lst[0]
                    lemma = lst[3]
                    # prefix = lst[4]
                    freq[x].setdefault(word, []).append([auth] + lst)

        self.freq = freq
        return

    def count_freq(self):
        self.stats = {}
        self.tots = {}
        # for k, v in self.freq.items():
        for k, v in self.freq.items():
            dct1 = {
                'PO': 0,
                'Ge': 0,
                'GJ': 0,
                'all': 0
            }
            dct2 = defaultdict(dict)
            for x, y in v.items():
                for z in y:
                    auth = z[0]
                    if auth not in dct1:
                        dct1["all"] += 1
                        num = dct2['all'].get(x, 0)
                        dct2['all'][x] = num + 1
                    else:
                        dct1[auth] += 1
                        num = dct2[auth].get(x, 0)
                        dct2[auth][x] = num + 1

            for x, y in dct2.items():
                tot = dct1[x]
                if tot:
                    for s, t in y.items():
                        perc = int((t / tot) * 100)
                        y[s] = perc
                    y = sort_dct_val_rev(y)
                    for s, t in y.items():
                        y[s] = [t, tot]
                    dct2[x] = y

            self.stats[k] = [dct2, v]

        # self.stats = vgf.sort_dct_val_rev(self.stats)
        # ana = {}
        # for k, v in self.stats.items():
        #     ana[k] = [v, self.tots[k[0]]]
        return

    def choose_winners(self):
        self.wmac = {}
        self.undecided = {}
        self.error_spell = defaultdict(list)
        self.undecided2 = {}
        self.uwords = {}
        for k, v in self.stats.items():
            if k == 'cid':
                bb = 8
            scores = v[0]
            threshold = 7
            done = 0
            if len(scores) == 1 and 'GJ' in scores:
                word, perc, tot = self.output_dct(scores, 'GJ')
                if perc > 70:
                    self.wmac[k] = word
                else:
                    self.undecided2[k] = v
                    self.uwords[k] = word

            else:
                lst1 = ['PO', 'Ge']
                b = 0
                while 1:
                    for auth in lst1:
                        word, perc, tot = self.output_dct(scores, auth)
                        if tot > threshold:
                            if perc > 66:
                                done = 1

                            elif tot > 7 and auth == 'PO':
                                self.undecided[k] = v
                                self.uwords[k] = word
                                done = 1
                            if done: break
                    b += 1
                    if b > 1:
                        break
                    threshold = 3
                if not done:
                    und = 0
                    word, perc, tot = self.output_dct(scores, 'all')
                    wordp, percp, totp = self.output_dct(scores, 'PO')
                    wordg, percg, totg = self.output_dct(scores, 'Ge')
                    if word != wordp:
                        if totp < 3 and tot > 7 and perc > 80:
                            pass
                        elif totp > 1 and perc == 100:
                            word = wordp
                        elif percp == 100:
                            word = wordp
                        elif percg == 100:
                            word = wordg
                        elif perc > 66:
                            self.wmac[k] = word
                        else:
                            und = 1

                    else:
                        if percp == 100:
                            word = wordp
                        elif percg == 100:
                            word = wordg
                        elif perc > 66:
                            pass
                        else:
                            und = 1

                    if und:
                        if wordp:
                            word = wordp
                        elif wordg:
                            word = wordg

                        self.undecided2[k] = v
                        self.uwords[k] = word

            self.wmac[k] = word
            self.adjust_lemma(v[1], word)

        return

    def adjust_lemma(self, v, word):
        pres = set()
        lem2word = defaultdict(set)
        lem2pre = defaultdict(set)
        lem2bod = defaultdict(set)
        for s, lst in v.items():
            for z in lst:
                pre = z[6]
                pres.add(pre)
                lemma = z[4]

                if unidecode(word) != unidecode(z[1]):
                    self.error_spell[lemma].append([word, z])
                else:
                    bod = word
                    if lemma == 'patron':
                        bb = 8

                    lem2bod[lemma].add(bod)
                    if pre and pre[-1] == bod[0] and pre[:-1] in self.prefix2:
                        pass
                    elif pre:
                        pre = self.prefix.get(pre, '')
                        if not pre:
                            p(lemma, bod)

                    str1 = f'{pre}{bod}'
                    str1_wo_mac = unidecode(str1)
                    # self.macrons[str1_wo_mac][lemma] = str1
                    lem2word[lemma].add(str1)
            for k, t in lem2word.items():
                lem = self.co_lemmas1a[k]
                assert len(lem2bod[k]) == 1
                lem[self.form + 'm'] += list(t)
            # p (k, t)
        return

    def output_dct(self, scores, auth):
        po = scores.get(auth, {})
        if not po:
            return 0, 0, 0
        word, lst = vgf.dct_idx(po, 0, 'i')
        perc = lst[0]
        tot = lst[1]
        return word, perc, tot

    def alt_geninf(self):
        dct = {}
        dct1 = {}
        wrong_vowels = [
            '''
            the following words are roots of lemmas for which not
            enough info has been given regarding their vowel quantity
            '''
        ]
        for k, v in self.co_lemmas1a.items():
            st1 = set(v[f'{self.form}m'])
            dctm = {unidecode(x): x for x in st1}
            st2 = set(dctm.keys())
            ost = v[self.form]
            if k == 'abscondo':
                bb = 8

            ost1 = ost.split(',')
            ost1 = set(unidecode(x).lower() for x in ost1)
            miss = ost1 - st2
            if st1 and miss:
                if v[self.form] and ',' not in ost or not st2:
                    dct[k] = v
                else:
                    arb = list(st2)[0]
                    arb_wma = dctm[arb]
                    # arb_wma = self.macrons[arb][k]
                    hvow = re.sub(r'[^aeioyu]', "", arb)
                    hvowma = re.sub(r'[^aeioyuāēīōūȳ]', "", arb_wma)
                    for w in ost1:
                        if w not in dctm:
                            oword = w
                            for e, t in en(w):
                                if t in 'aeioyu':
                                    if t == hvow[0]:
                                        w = replace_at_i(e, w, hvowma[0])
                                        if len(hvowma) == 1:
                                            break
                                        hvowma = hvowma[1:]
                                        hvow = hvow[1:]
                                    else:
                                        wrong_vowels.append([oword, k])
                                        break
                            # self.macrons[oword][k] = w
                            v[f'{self.form}m'].append(w)

        to.from_lst2txt(wrong_vowels, f'{fold}stems_unknown_quant')

        return

    def final_test(self):
        for i in range(2):
            if i:
                dct = {}
            for x, y in self.co_lemmas1a.items():
                if y[self.form]:
                    lst = y[f'{self.form}m']
                    lst = [unidecode(x) for x in lst]
                    st = set(lst)
                    ost = set(y[self.form].split(','))
                    ost = set(w.lower() for w in ost)
                    if not st == ost:
                        miss = ost - st
                        for w in miss:
                            self.match_macrons(y, w)
                        if i:
                            dct[x] = y

        return

    def match_macrons(self, lemma, w):
        lem_wo_mac = lemma['lemma']
        lem_wmac = lemma['spell'].lower()
        lem_wmac = jv.replace(lem_wmac)
        hvow = re.sub(r'[^aeioyu]', "", lem_wo_mac)
        hvowma = re.sub(r'[^aeioyuāēīōūȳ]', "", lem_wmac)
        if hvow:
            for e, t in en(w):
                if t in 'aeioyu':
                    if t == hvow[0]:
                        w = replace_at_i(e, w, hvowma[0])
                        if len(hvowma) == 1:
                            break
                        hvowma = hvowma[1:]
                        hvow = hvow[1:]
                    else:
                        break
            lemma[f'{self.form}m'].append(w)


class bottom_most(step_one):
    def __init__(self):
        step_one.__init__(self)

    def begin(self, second=0):
        '''
        we run the begin function twice, the first time the form
        is set to geninf in which case we parse the geninf form
        the second time it is set to perf

        there is a function which divides the lemmas into each
        author's information

        '''

        self.second = second
        self.get_atts()
        if not self.second:
            self.normalize_perf()
            self.step1()
            self.alternate_spell()
            self.output(6)
            self.jv_rep()
            self.fix_ge()
            self.fix_lw()
            self.fix_yo()
            self.fix_po()
            self.jv_others()
            self.output(9)
            self.agreement()
        self.build_prefix_dct()
        self.begin_cl2()
        self.match_gen2stem()
        self.auth_contr()
        self.ana_wo_prefix()
        self.ana_wo_prefix2()
        self.count_freq()
        self.choose_winners()
        self.alt_geninf()
        self.final_test()
        if second:
            self.quick_fix()
            self.fdiph_fu()
            self.check_jv()
            self.output(2)





if eval(not_execute_on_import):
    if vgf.pycharm():
        args = [0, 'pcf', '', 'IX', '', 0, 0]
    else:
        args = vgf.get_arguments()

    ins = bottom_most()
    ins.begin()
    ins.kind = 'p'
    p('step two')
    ins.begin(1)


