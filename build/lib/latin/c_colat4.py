
from bglobals import *
from e_pedocerto import check_vowels




class top_most:
    def __init__(self):
        pass

    def get_atts(self, kind=0):
## kind4 is used after co_lemmas5 has been built in j_lasla2

        import w_convert_mod
        p ('opening pickles')

        self.pos = pi.open_pickle(f'{fold}final_pos')
        self.mmodels = pi.open_pickle(f'{fold}mmodels')
        if not kind == 4:
            self.co_lemmas3 = pi.open_pickle(f'{fold}co_lemmas3')
            self.certain2 = defaultdict(list)
            self.almost_certain = defaultdict(list)
            self.lem_freq_crude = pi.open_pickle(f'{fold}lem_freq_crude')
            self.lem_freq_rank = pi.open_pickle(f'{fold}lem_freq_rank')
            self.lat_freq = pi.open_pickle(f'{fold}latin_freq')
            self.lat_freq = sort_dct_val_rev(self.lat_freq)
        else:
            self.co_lemmas3 = pi.open_pickle(f'{fold}co_lemmas5')

        p ('done opening')
        self.debug = {}
        self.lem2forms = {}
        self.lem2forms_pos = {}
        self.lem2forms_ui = {}
        self.macronizer_new = {}
        self.fake_enclitics = {}
        if kind == 'rs':
            self.ins_pedecerto()
            self.word2stress = {}
        else:
            self.word2stress = pi.open_pickle(f'{fold}word2stress')

    def shortcut(self):
        self.lem2forms_ui = pi.open_pickle(f'{fold}lem2forms_ui')
        self.pos = pi.open_pickle(f'{fold}final_pos')


    def output(self, kind=0):
        p('now saving')

        if kind == 6:
            pi.save_pickle(self.ui_models, f'{fold}ui_models')
        if kind == 7:
            pi.save_pickle(self.irregular, f'{fold}irregs_parsed')
            pi.save_pickle(self.co_lemmas3, f'{fold}co_lemmas4')
            pi.save_pickle(self.ui_models, f'{fold}ui_models')
        if kind in [0,4]:
            pi.save_pickle(self.lem2forms, f'{fold}lem2forms_jv')
            pi.save_pickle(self.lem2forms_ui, f'{fold}lem2forms_ui')
            pi.save_pickle(self.word2stress, f'{fold}word2stress')
            pi.save_pickle(self.lem2forms_pos, f'{fold}lem2forms_pos')
        if kind == 1:
            pi.save_pickle(self.fake_enclitics, f'{fold}fake_enclitics')
        if kind == 2:
            pi.save_pickle(self.macronizer_new, f'{fold}macronizer_new', 1)



class colat(top_most):
    def __init__(self):
        top_most.__init__(self)



    def quick_redund(self):
        dct2 = {}
        dct3 = defaultdict(int)
        authors2 = ['def_co', 'def_lw', 'def_ls', 'def_gj',
                    'def_gg', 'def_ge']
        dupl = set()
        for x, y in self.co_lemmas3.items():
            tpl = (y['lemma'], y['model'], y['geninf'], y['perf'])
            dct3[tpl] += 1
            three = 0
            if dct3[tpl] > 2:
                three = 1
            if tpl in dct2:
                dupl.add(x)

                obj = dct2[tpl]
                if obj['capital'] != y['capital']:
                    obj['capital'] = 2
                for auth in authors2:
                    s = obj[auth]
                    t = y[auth]
                    if s and t:
                        if three:
                            obj[auth] = f'{s} III. {t}'
                        else:
                            obj[auth] = f'I. {s} II. {t}'
                    elif not s and t:
                        obj[auth] = t
            else:
                dct2[tpl] = y

        p(f'eliminated {len(dupl)} redundancies')
        for d in dupl:
            del self.co_lemmas3[d]

        return


    def ad_hoc_pos(self):
        dct = {
            'nihil': 'inv',
        }
        for k, v in dct.items():
            self.co_lemmas3[k]['pos'] = v

    def expand_pos(self):
        dct = to.from_txt2dct_1d(f'{fold}more_pos')
        for k,v in dct.items():
            self.pos[int(k)] = v
        dct1 = {}
        for k,v in self.pos.items():
            if v.startswith('gd.') and len(v)> 4:
                dct1[k] = v.replace('gd.','gv.')
            else:
                dct1[k] = v
        self.pos = dct1
        pi.save_pickle(self.pos, f'{fold}final_pos')


    def build_ui_models(self, start=0):
        if start:
            self.mmodels = pi.open_pickle(f'{fold}mmodels')
        self.ui_models = copy.deepcopy(self.mmodels)
        # self.mod_vow = pi.open_pickle(f'{sfold}mod_vow')
        for k, v in self.ui_models.items():
            if v['R']:
                for x,y in v['R'].items():
                    y[1] = norm_str_jv(y[1])

            for x, y in v['des'].items():
                for e, l in en(y):
                    l2 = [norm_str_jv(z) for z in l[1]]
                    l = [l[0], l2]
                    y[e] = l
                v['des'][x] = y
            if v['suf']:
                for e,x in en(v['suf']):
                    v['suf'][e][0] = norm_str_jv(v['suf'][e][0])
            if v['sufd']:
                v['sufd'] = [norm_str_jv(t) for t in v['sufd']]
        return

    def start_decl(self):
        self.mdec_ui = decline(self.co_lemmas3, self.ui_models, self.pos)
        self.mdec = decline(self.co_lemmas3, self.mmodels, self.pos)

    def eliminate_adv_model(self):
        '''
        todo = we still need to add the definition to the new model
        sed and sēd = sē; ā and a; phū and phu are the only
        words which are invariant but have different vowel
        quantities

        sed -> ""
        a -> ""
        '''

        to_del = []
        invariants = {}
        for x, y in self.co_lemmas3.items():
            if y['model'] in ['inv', 'adv']:
                lem = y['lemma']
                if lem in invariants:
                    to_del.append(x)
                else:
                    invariants[lem] = y
                    y['model'] = 'inv'

        for x in to_del:
            del self.co_lemmas3[x]

        for x, y in self.co_lemmas3.items():
            if y['model'] == 'adv':
                p(f'{x} failed to delete adv model')

        return

    def restore_perfect(self):  # 89 unkn 55 known
        # p ('now fixing bad perfect stems')
        file = f'{fold}perfect_miss_old_miss'
        file2 = f'{fold}perfect_miss'
        lst3 = to.from_txt2lst_tab_delim(file)
        lst4 = to.from_txt2lst_tab_delim(file2)
        v2p = {}
        v2p2 = {}
        st = set()
        mac2nmac = defaultdict(set)

        for x in lst4:
            if x[1]:
                found = 1
                if ',' in x[1]:
                    found = 0
                    xu = norm_str_jv(x[0])
                    self.co_lemmas3[xu]['perf'] = x[1]
                    pass
                elif " " in x[1]:
                    lst5 = x[0].split(" ")
                    lst6 = x[1].split(" ")
                    u5 = unidecode(lst5[1])
                    u6 = unidecode(lst6[1])
                    v2p2[u5] = u6
                    k = x[0].replace(' ', '')
                    v = x[1].replace(' ', '')
                else:
                    k = x[0]
                    v = x[1]
                if found:
                    x0u = unidecode(k)
                    x1u = unidecode(v)
                    mac2nmac[x0u].add(k)
                    mac2nmac[x1u].add(v)
                    x0u = x0u.replace(' ', '')
                    v2p[x0u] = x1u
            elif " " in x[0]:
                lst5 = x[0].split(' ')
                u5 = unidecode(lst5[1])
                mac2nmac[u5].add(lst5[1])
                st.add(u5)

        st2 = set()
        for x in lst3:
            if " " in x[0]:
                lst5 = x[0].split(' ')
                xu = unidecode(lst5[1])
                mac2nmac[xu].add(lst5[1])
                st.add(xu)
            else:
                xu = unidecode(x[0])
                mac2nmac[xu].add(x[0])
                st2.add(xu)

        unknown = set()
        for x in st:
            y = mac2nmac[x]
            if x in v2p or x in v2p2:
                pass
            else:
                itm = 0
                for z in y:
                    if z in self.co_lemmas_wonum:
                        itm = self.co_lemmas_wonum[z]
                        if len(itm) > 1:
                            for t in itm:
                                if t['model'] in ['audio', 'capio']:
                                    itm = t
                                    break

                        else:
                            itm = itm[0]
                        break
                if itm and type(itm) == dict and itm['perf']:
                    v2p2[z] = itm['perf']
                else:
                    unknown.add(x)

        c = 0
        missing = set()
        missing2 = set()
        v2p3 = {}
        v2p3['scipio'] = 'scept'
        unknown.remove('scipio')  # check 'rio'

        for x in unknown:
            for k, v in self.co_lemmas_wonum.items():
                if k.endswith(x) and k != x:
                    done = 0
                    for z in v:
                        if z['model'] in ['capio', 'audio'] and z['perf']:
                            c += 1
                            done = 1
                            start = len(k) - len(x)

                            v2p3[x] = z['perf'][start:]
                            break

                    if done:
                        break
            else:
                lst9 = self.co_lemmas_wonum.get(x)
                if lst9:
                    missing.add(x)
                else:
                    missing2.add(x)

        v2p = merge_2dicts(v2p, v2p2)
        v2p = merge_2dicts(v2p, v2p3)
        self.restore_perfect2(lst3, lst4, v2p)

        return

    def restore_perfect2(self, lst3, lst4, v2p):
        ## missing 224
        missing = set()
        for x in lst4 + lst3:
            lem = x[0]
            try:
                perf = x[1]
            except:
                perf = ''
            if perf:
                perf = perf.replace(' ', '')

            if ' ' in lem:
                lem2 = lem.replace(' ', '')
                pre = lem.split(' ')[0]
                key = lem.split(' ')[1]
            else:
                pre = 0
                key = lem
                lem2 = lem
            if not perf:
                keyu = unidecode(key)
                nperf = v2p.get(keyu)
                if nperf:
                    if pre:
                        nperf = pre + nperf
            else:
                nperf = perf

            lemu = unidecode(lem2)
            obj = self.co_lemmas_wonum.get(lemu)
            if not obj:
                missing.add(lemu)
            elif nperf:
                found = 0
                for z in obj:
                    if z['model'] in ['capio', 'audio'] and not z['perf']:
                        found = 1
                        break
                if found:
                    z['perf'] = nperf

        """
        for verbs in the capio or audio model which end in pio
        about 12 out of 15 have a perfect stem which ends in pt
        for verbs in the capio or audio model which end in cio
        about 19 out of 21 have a perfect stem which ends in ct
        for verbs in the capio or audio model which end in rio
        about 8 out of 16 have a perfect stem which ends in rt
        the 38 verbs which end in something else all have a
        perfect stem which ends in it
        """

        missing2 = {}
        for x, y in self.co_lemmas3.items():
            if y['model'] in ['capio', 'audio'] and not y['perf']:
                wonum = cut_num(x)

                if wonum[-3:] in ['cio', 'pio']:
                    y['perf'] = x[:-2] + 't'
                else:
                    y['perf'] = x[:-1] + 't'
                y['inferred_form'] = 2

                missing2[x] = y

        return

    def get_pos_num(self, lst, lst2):
        '''
        this function is good for finding redundant lemmas

        '''

        nums = [189, 225, 261, 267, 303, 339, 127, 139, 85]
        lst4 = []
        b = 0
        for x, y in zip(lst, lst[1:]):
            if b % 2 == 0:
                if ';' not in y[0]:
                    lst4.append([x[0], y[0]])
            b += 1
        lst2 += lst4
        error = []
        for x in lst2:
            lst5, _ = self.mdec.dec(x[0])
            found = 0
            for num in nums:

                rw = lst5.get(num)
                if rw:
                    for y in rw[0]:
                        yu = unidecode(y)
                        if yu == unidecode(x[1]):
                            x[1] = y
                            found = 1
                            obj = self.from_excel_wnum[yu]
                            x.append(num)
                            x.append(obj.model)
                            break
                    if found:
                        break
            if not found:
                error.append(x)

        return

    def final_o(self):
        ## peredo missing this but peredo2 did not
        for x, y in self.co_lemmas3.items():
            if y['pos'] == 'v':
                if y['lemma'].endswith('o'):
                    y['lemma'] = y['lemma'][:-1] + 'ō'

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
            x = self.ui_models[k]
            x['pos'] = v['pos']
            self.ui_models[k] = x
            e += 1

        for k, v in self.co_lemmas3.items():
            v['pos'] = self.mmodels[v['model']]['pos']

        return

    def use_fix_collat_lemmas(self):
        lst = to.from_txt2lst_tab_delim(f'{fold}fix_collat_lemmas')
        for x in lst:
            if x[0].startswith('__'):
                lem = x[0][2:].strip()
                dct = self.co_lemmas3[lem]
            else:
                key = x[0].strip()
                val = x[1].strip()
                dct[key] = val

        return


    def fix_breve(self):
        p ('fixing breve')
        b =0
        for k, v in self.co_lemmas3.items():
            b += 1
            vgf.print_intervals(b,1000,None, len(self.co_lemmas3))
            og = v['geninf']
            op = v['perf']
            glst = v['geninf'].split(',')
            plst = v['perf'].split(',')
            v['lemma'] = remove_hats_diph(v['lemma'])

            if glst[0]:
                glst = [remove_hats_diph(x) for x in glst]
                ng = ','.join(glst)
                if ng != og:
                    v['geninf'] = ng
                    # p(f'fixed breve {og} {ng}')

            if plst[0]:
                plst = [remove_hats_diph(x) for x in plst]
                np = ','.join(plst)
                if np != op:
                    v['perf'] = np
                    # p(f'fixed breve {op} {np}')
        if cobr in self.co_lemmas3['iphicrates']['lemma']:
            assert 0

        return

    def implement_mod_errors(self):
        '''
        the following represents a minor improvement to
        the geninf and perf roots but still a lot of mistakes
        on the other hand, there were 21 different quantity
        for the lemma mostly of greek origin so i decided
        to ignore these since they might conflict with the
        fix breve method
        '''

        file = f'{fold}mod_errors'
        lst = to.from_txt2lst_tab_delim(file, 1, 1)
        lst = [x for x in lst if x[0][:2] != '__']
        itm = self.co_lemmas3['peredo']
        del self.co_lemmas3['peredo']
        itm['geninf'] = 'perēd'
        itm['perf'] = 'perēs'
        itm['lemma'] = 'peredo'
        self.co_lemmas3['peredo'] = itm
        lst2 = []
        lst3 = []
        for x in lst:
            lst1 = ["", '', '']
            lem = x[0]
            geninf = x[1]
            perf = x[2]
            lemu = norm_str_jv(lem)
            obj = self.co_lemmas3.get(lemu)
            if not obj:
                p(lem)
            else:
                lemn = cut_num(lem).lower()
                if lemn.endswith('o'):
                    lemn = lemn[:-1] + 'ō'

                if lemn != obj['lemma']:
                    lst3.append((lemn, obj['lemma']))

                if geninf != obj['geninf']:
                    lst1[0] = lem
                    lst1[1] = (geninf, obj['geninf'])
                if perf != obj['perf']:
                    lst1[0] = lem
                    lst1[2] = (perf, obj['perf'])

                obj['geninf'] = geninf
                obj['perf'] = perf
            if lst1[1] or lst1[2]:
                lst2.append(lst1)

        return



    def get_all_uwords(self):  # only 1110 homophones have different quantities
        '''
        we call a quantitative homonym a word which is spelled the same
        but the vowels have different quantities
        '''

        self.all_uwords = set()
        self.redundant = set()
        self.co_lemmas_wonum = defaultdict(list)
        for x, y in self.co_lemmas3.items():
            xu = unidecode(x)
            xu = cut_num2(xu)
            self.all_uwords.add(xu)
            self.co_lemmas_wonum[xu].append(y)
        self.homophones2 = {x: y for x, y in self.co_lemmas_wonum.items() if len(y) > 1}
        return

    def test_new_mods2(self):
        ### todo templum words ending in ium have a false locative
        ## ending in ii

        bad_pos = pi.open_pickle(f'{fold}temp_bad_pos')
        # las_freq = pi.open_pickle(f'{sfold}las_freq2')
        # dct4 = defaultdict(dict)
        # dct4f = {}
        # for k,v in las_freq.items():
        #     lem = k[0]
        #     mod = self.co_lemmas3.get(lem)
        #
        #     if mod:
        #         modu = mod['model']
        #         if mod['model'] == 'eo':
        #             if 'if.pr.pa' in k[2]:
        #                 if mod['model'] not in dct4:
        #                     dct4[modu] = defaultdict(list)
        #
        #                 dct4[modu][k[2]].append( k[1])

        # vgf.get_key(self.pos,'2.pr.im.ac') # 181
        # vgf.get_key(self.pos,'5.pr.im.ac') # 182
        # vgf.get_key(self.pos,'if.pr.pa') # 183

        lst1 = self.mdec_ui.dec('templum')


        rem = {}
        got = {}
        loc = {}
        fua = {}
        sum = {}
        modd = {}
        no_pos = {}
        for x,y in bad_pos.items():
            lem = x[0]
            word = x[1].lower().strip()
            pos = x[2]
            modu = x[3]
            if "<" in word:
                pass
            elif '_pl' in modu:
                modd[x] = y

            elif pos == 'if.fu.ac':
                fua[x] = y
            elif x[3] == 'deterior':
                pass

            else:
                if lem == 'facio':
                    bb=8
                dct = self.mdec_ui.dec(lem,1)
                num = vgf.get_key(self.pos, pos)
                lst5 = dct.get(num)

                if lst5:
                    if word in lst5[0]:
                        got[x]=y
                    else:
                        if 'gv.' in pos:
                            sum[x] = [y[0],lst5[0]]
                        else:

                            rem[x] = [y[0],lst5[0]]

                else:
                    if pos in ['sl', 'sfl']:
                        loc[x] = y
                    else:
                        no_pos[x]=[num,y]

        dct19 = defaultdict(list)
        dct18 = defaultdict(list)
        for k,v in loc.items():
            if k[2] == 'sl':
                mod = k[3]
                dct19[mod].append(k[1])
            elif k[2] == 'sfl':
                mod = k[3]
                dct18[mod].append(k[1])


        return


    def simplify_decline(self):
        mod2word = defaultdict(list)
        for k,v in self.co_lemmas3.items():
            # if ',' in v['geninf']:
            #     break
            mod2word[v['model']].append(k)

        for k,v in self.ui_models.items():
            if k == 'imitor':
                bb=8
            lst = mod2word[k]
            if lst:
                dct = self.mdec_ui.dec(lst[0],1,1)
                v['sim'] = dct
                self.ui_models[k] = v
        self.mod2word = mod2word
        dct1 = self.mdec_ui.short('ego', 1, 1)
        return


    def test_simplify(self):
        error = {}
        b = 1
        for k,v in self.co_lemmas3.items():
            b += 1
            vgf.print_intervals(b, 1000,None, len(self.co_lemmas3))
            # if ',' in v['geninf']:
            #     break
            dct2 = self.mdec_ui.dec(k,1,0)
            dct = {}
            for y, x in dct2.items():
                dct[x[1]] = set(x[0])

            dct1 = self.mdec_ui.short(k,1,1)
            if dct1 != dct:
                # error[k] = v
                dct3 = {}


                for x, y in dct1.items():
                    if dct[x] != y:
                        dct3[x] = [y, dct[x]]
                error[k] = dct3
                if len(error)>10:
                    break





        return



    def test_new_mods(self):
        dct3 = {}
        for mod, dct in self.ui_models.items():
            dct4 = {}
            for x,y in dct['R'].items():
                if y[1]:
                    dct4[x]=y
            if dct4:
                dct3[mod] = dct4

        # self.ins_pedecerto()
        # lalems = pi.open_pickle(f'{sfold}lalems2forms')
        #tuite in geneitive, 2 tu in nominative
        # lst1 = self.mdec.dec('lupus')
        lst6 = self.mdec.dec('fortis')
        self.add_accent2(lst6)
        lst7 = self.mdec_ui.dec('deus')
        lst  = self.mdec.dec('ego')
        lst3 = self.mdec.dec('nos')
        lst2 = self.mdec.dec('uos')
        lst4 = self.mdec.dec('se')
        return

    def build_macronizer(self):
        self.macronizer_new = defaultdict(dict)
        p ('now mapping words to their macrons')
        b = 0
        for k, forms in self.lem2forms.items():
            b += 1
            vgf.print_intervals(b, 1000, None, len(self.lem2forms))
            for num, form in forms.items():
                for word in form[0]:
                    wordu = norm_str_jv(word)
                    self.macronizer_new[wordu].setdefault(word, []).append([k, form[1]])

    def irreg(self,kind=0):
        '''
        this gets a few irregular declensions from the collatinus irregs sheet
        it will probably be abandoned later on
        '''

        irr = to.from_txt2lst(f'{fold}irregs')
        self.irregular = defaultdict(dict)
        dct = {}
        for l in irr:
            if not l[0] == '!':
                lst = vgf.strip_n_split(l, ":")
                lem = lst[1].lower()
                word = lst[0]
                loc = lst[2]
                loc = vgf.strip_n_split(loc, ',')
                lst2 = []
                for x in loc:
                    if '-' in x:
                        b, e = x.split('-')
                        for i in range(int(b), int(e) + 1):
                            lst2.append(i)
                    else:
                        lst2.append(int(x))
                loc = lst2
                word = word.replace(cobr, "").lower()
                word = remove_hats_diph(word, word)
                lemu = norm_str_jv(lem)
                itm = self.co_lemmas3.get(lemu)
                if not itm:
                    p(f'missing the irregular {lem}')

                else:
                    dct[lem] = itm
                    for x in loc:
                        self.irregular[lemu][x] = word
        return


    def use_del_lemmas(self):
        file2 = f'{fold}del_lemmas'
        lst = to.from_txt2lst(file2)
        for x in lst:
            del self.co_lemmas3[x]


    def more_adhoc(self):
        ## todo put these on a file because there will be a lot more then these
        if not self.debug:
            self.co_lemmas3['prosto']['perf'] = 'prōstāt'
            self.co_lemmas3['insto']['perf'] = 'īnstāt'
            self.co_lemmas3['ualamer']['geninf'] = 'valamr'
            self.co_lemmas3['uenafer2']['geninf'] = 'venāfr'
            self.co_lemmas3['adsum']['perf'] = ''
            self.co_lemmas3['intersum']['perf'] = ''
            self.co_lemmas3['magnus']['model'] = 'magnus'
            self.co_lemmas3['paruus']['model'] = 'magnus'
            self.co_lemmas3['bonus']['model'] = 'magnus'
            self.co_lemmas3['malus']['model'] = 'magnus'

    def ins_pedecerto(self):
        self.pdc = check_vowels()
        self.pdc.kind = 'a'
        self.pdc.single = 1
        self.pdc.get_atts2()



    def get_lem2forms(self):
        self.ins_pedecerto()
        p('now declining all words')
        self.lem2forms = {}
        self.word2stress = {}
        b = 0
        for word, obj in self.co_lemmas3.items():
            lst = self.mdec.dec(word)
            lst1 = self.mdec_ui.dec(word, 1)
            self.lem2forms[word] = self.add_accent2(lst)
            self.lem2forms_ui[word] = lst1
            pos = obj['pos']
            ku, num = cut_num(word, 1)
            if ku not in self.lem2forms_pos:
                self.lem2forms_pos[ku] = defaultdict(dict)
            if pos not in self.lem2forms_pos[ku]:
                self.lem2forms_pos[ku][pos] = defaultdict(list)
            self.lem2forms_pos[ku][pos][num].append(lst1)
            b += 1
            vgf.print_intervals(b, 100, None, len(self.co_lemmas3))
        return

    def add_accent2(self, dct):
        for k,v in dct.items():
            lst1 = []
            for z in v[0]:
                obj = self.word2stress.get(z)
                if obj:
                    lst1.append(obj)
                else:
                    obj = self.pdc.get_accent2(z)
                    self.word2stress[z] = obj
                    lst1.append(obj)
            dct[k][0] = lst1
        return dct


    def get_fake_enclitics(self):
        p('now getting fake enclitics')
        self.fake_enclitics = defaultdict(set)
        b = 0
        for y, x in self.lem2forms_ui.items():
            b += 1
            xu = cut_num(y)
            vgf.print_intervals(b, 1000, None, len(self.lem2forms_ui))
            for num, lst in x.items():
                pos2 = self.pos[num]
                for word in lst[0]:
                    for y in encs:
                        if word.endswith(y):
                            self.fake_enclitics[xu].add(pos2)
                            break

        return



class bottom_most_a4(colat):
    def __init__(self):
        '''
        this class is almost dead, none of its attributes are
        being used.

        begins with fin_lemmas2 outputs mac_lemmas_new

        '''

        colat.__init__(self)

    def begin_fc(self, kind=0, kind2=0):
        if kind == 4:
            self.get_atts(4)
            self.build_ui_models()
            self.start_decl()
            self.get_lem2forms()
            self.output(4)
        elif kind > -1 and kind < 2:
            self.get_atts(kind2)
            # self.expand_pos()
            self.use_fix_collat_lemmas()
            self.build_ui_models()
            self.start_decl()
            #self.test_new_mods2()
            self.simplify_decline()
            self.output(6)
            # self.test_simplify()
            self.test_new_mods()
            self.irreg()
            self.use_del_lemmas()
            self.more_adhoc()
            self.ad_hoc_pos()
            self.eliminate_adv_model()
            self.fix_breve()
            self.final_o()
            self.get_pos()
            self.implement_mod_errors()
            self.get_all_uwords()
            self.restore_perfect()
            self.quick_redund()
            self.output(7)
        if kind < 1:
            self.start_decl()
            # self.test_new_mods()
            self.get_lem2forms()
            self.output()
        if kind < 2:
            if kind == 3:
                self.shortcut()
            self.get_fake_enclitics()
            self.output(1)
        if kind < 3:
            if kind > 3:
                pass
            self.build_macronizer()
            self.output(2)


"""
build word2model
oxford to collatinus
get all variants
punctuate lasla
convert to text
poetry scanner
build databases
"""





if eval(not_execute_on_import):
    if vgf.pycharm():
        args = [0, 'rs', '', 'IX', '', 0, 0]
    else:
        args = vgf.get_arguments()

    if args[1] == 'rs': # redo stress
        ins = bottom_most_a4()
        ins.begin_fc(0,'rs')
    else:
        ins = bottom_most_a4()
        num = int(args[2]) if args[2] else 0
        ins.begin_fc(num)




