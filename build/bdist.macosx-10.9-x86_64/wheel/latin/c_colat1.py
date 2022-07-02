
from bglobals import *


class get_co_lemmas1:
    def __init__(self):
        pass

    def begin(self):
        self.get_atts()
        self.parse_lemmes()
        self.lems_wo_hats()
        self.lemma_wo_hats2()
        self.lem_no_uni()
        self.no_jv()
        self.lem_no_caps()
        self.weed_out()
        self.use_asimil()
        # self.test()
        self.output()
        return

    def get_atts(self):
        self.co_lemmas1 = pi.open_pickle(f'{fold}co_lemmas1', 1)
        lst = to.from_txt2lst(f'{fold}assimilations')
        self.asimil = [x for x in lst if x[0] != '!']
        self.lat_freq = pi.open_pickle(f'{fold}latin_freq', 1)

    def output(self):
        pi.save_pickle(self.co_lemmas1a, f'{fold}co_lemmas1a', 1)


    def test(self):
        co2 = pi.open_pickle(f'{fold}co_lemmas1a', 1)
        if self.co_lemmas1a != co2:
            bb=8
        st = set()
        for k,v in self.co_lemmas1a.items():
            obj = co2[k]
            for x,y in v.items():
                if y != obj[x]:
                    st.add(x)
                    p (y, obj[x])
        return

    def parse_lemmes(self):
        lst = to.from_txt2lst(f'{fold}lemmes')
        lst1 = to.from_txt2lst(f'{fold}lem_ext')
        lst += lst1
        lst = [x for x in lst if x and x[0] != '!']
        lemmas = {}
        ana = []
        repeats = {}
        p (f'parsing the collatinus lemmes sheet')

        for e, x in en(lst):
            vgf.print_intervals(e,1000,None,len(lst))
            x = x.split('|')
            lem = new_lem(x)
            if x[0] in lemmas:
                repeats[x[0]] = lem
            else:
                lemmas[x[0]] = lem

            if lem['lemma'][0].isupper():
                lem['capital'] = 1
            lem['lemma'] = lem['lemma'].lower()
            lem['lemma'] = lem['lemma'].replace(cobr, '')

            if '=' in lem['lemma']:
                lst2 = lem['lemma'].split('=')
                lem["lemma"] = lst2[0]
                lem['syl'] = lst2[1]
            else:
                lem['syl'] = lem['lemma']
                ana.append(lem['lemma'])

        self.co_lemmas0 = lemmas
        return

    def lems_wo_hats(self):
        '''
        the following repeat lemmas can be deleted
        bracteola
        incohibilis
        Malthīnus
        paradoxon
        perlibet
        prendo

        delete first
        propylaeon
        pyrē̆thron
        sparton
        :return:
        '''

        dct = {}
        dct1 = {}
        self.repeats2 = {}
        self.repeats22 = defaultdict(list)
        self.lemmas_wo_hats = {}
        diph3 = ['ae', 'au', 'ei', 'eu', 'oe', 'ui']

        for k, y in self.co_lemmas0.items():
            x = y['lemma']
            if chr(7909) in y['syl']:
                bb = 8
            w = unidecode(x)
            z = remove_hats_diph(x, y['syl'])
            if z != x:
                if any(y in w for y in diph3):
                    dct[x] = z
                else:
                    dct1[x] = z
            self.repeats22[z].append(y)
            if z not in self.lemmas_wo_hats:
                y['lemma'] = z
                self.lemmas_wo_hats[z] = y
            else:
                assert z not in self.repeats2
                self.repeats2[z] = y
        self.repeats22 = {x: y for x, y in self.repeats22.items() if len(y) > 1}
        return

    def lemma_wo_hats2(self):
        self.lemmas_no_hats2 = {}
        self.repeats3 = defaultdict(list)
        for x, y in self.lemmas_wo_hats.items():
            y['spell'] = x
            z = remove_hats(x)
            y['lemma'] = z
            self.repeats3[z].append(y)
            if z not in self.lemmas_no_hats2:
                self.lemmas_no_hats2[z] = y
        self.repeats3 = {x: y for x, y in self.repeats3.items() if len(y) > 1}
        return

    def lem_no_uni(self):
        self.lem_nuni = {}
        self.repeats4 = defaultdict(list)
        for x, y in self.lemmas_wo_hats.items():
            z = unidecode(x)
            y['lemma'] = z
            self.repeats4[z].append(y)
            if z not in self.lem_nuni:
                self.lem_nuni[z] = y
        self.repeats4 = {x: y for x, y in self.repeats4.items() if len(y) > 1}

    def no_jv(self):
        self.lem_jv = {}
        self.i2j = {}
        self.repeats5 = defaultdict(list)
        for x, y in self.lem_nuni.items():
            self.key = x
            self.key = jv.replace(self.key.lower())
            self.key = re.sub(r'[0-9]', '', self.key)
            if x == 'sero':
                bb = 8

            if reg(r'[vj]', x):
                self.i2j_index(y['lemma'].lower())
            self.jv_index(y)
            y['jv'] = y['lemma']
            z = jv.replace(x)
            y['lemma'] = z
            self.repeats5[z].append(y)
            if z not in self.lem_jv:
                self.lem_jv[z] = y
        self.repeats5 = {x: y for x, y in self.repeats5.items() if len(y) > 1}
        pi.save_pickle(self.i2j, f'{fold}i2j', 1)

        return

    def jv_index(self, lem):
        b = 0
        g = lem['geninf'].lower()
        if g:
            lst = lem['geninf'].split(',')
            for x in lst:
                if reg(r'[vj' + conu + r']', x):
                    b += 1
                    x = x.lower()
                    x = unidecode(x)
                    self.i2j_index(x)

        g = lem['perf'].lower()
        if g:
            lst = lem['perf'].split(',')
            for x in lst:
                if reg(r'[vj' + conu + ']', x):
                    x = x.lower()
                    x = unidecode(x)
                    self.i2j_index(x)

    def i2j_index(self, k):
        '''
        only two words belong to a homononymous lemma and
        are sometimes spelled with u or v or i and j
        ('uediiouis', 'uediiou')
        ('ueiouis', 'ueiou')
        neither are common, so they are ignored
        '''

        j = []
        u = []
        w = []
        for e, x in en(k):
            if x == 'j':
                j.append(e)
            elif x == 'v':
                u.append(e)
            elif x == conu:
                w.append(e)
        k = jv.replace(k)
        k = re.sub(r'[0-9]', '', k)
        obj = self.i2j.get((self.key, k))
        if obj and obj != [j, u, w]:
            bb = 8
        else:
            self.i2j[(self.key, k)] = [j, u, w]

    def lem_no_caps(self):
        self.lem_lower = {}
        self.repeats6 = defaultdict(list)
        for x, y in self.lem_jv.items():
            z = x.lower()
            y['lemma'] = z
            self.repeats6[z].append(y)
            if z not in self.lem_lower:
                self.lem_lower[z] = y
        self.repeats6 = {x: y for x, y in self.repeats6.items() if len(y) > 1}
        return

    def weed_out(self):
        cdct = set(self.co_lemmas1.keys())
        dct = {}
        for k, v in self.lem_lower.items():
            if k in cdct:
                dct[k] = v
        self.co_lemmas1a = dct
        return


    def use_asimil(self):
        dct = {}
        dct1 = {}
        for x in self.asimil:
            y = x
            y = unidecode(y)
            lst = x.split(':')
            dct[lst[0]] = lst[1]
            lst = y.split(':')
            dct1[lst[0]] = lst[1]

        self.more_words = {}
        for x, y in self.lem_lower.items():
            for k, v in dct1.items():
                if x.startswith(k):
                    new_word = v + x[len(k):]
                    self.more_words[new_word] = [k]
                    break
        pi.save_pickle(self.more_words, f'{fold}auto_variants')

        return


if eval(not_execute_on_import):
    if vgf.pycharm():
        args = [0, 'aw', '', 'IX', '', 0, 0]
    else:
        args = vgf.get_arguments()

    ins = get_co_lemmas1()
    ins.begin()
