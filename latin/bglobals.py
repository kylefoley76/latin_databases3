import copy,os, sys
public = 1


'''
make sure public is set to 1, when I code for myself
the general functions folder is used for all of my separate
projects, but since that would confuse other people only
those functions relevant to this project are used.

unidecode2 must be used because unidecode changes
ȳ to u
'''

from unidecode2 import unidecode
from collections import defaultdict
vol = os.path.join(os.path.dirname(__file__)) + '/general_la/'

if not public:
    vol2 = '/users/kylefoley/'
    gen_dir = f'{vol2}documents/pcode'
    if not os.path.exists(gen_dir):
        assert 0, 'my mistake the public variable needs to be set to 1'

    sys.path.append(gen_dir)
    from general import *
    lfold = f'{vol2}documents/pcode/latin/latin/'
else:
    from general_la import *
    lfold = ''

fold = f'{vol}files/'
bfold = f'old/old_files/'
lafold = f'{vol}lasla/'
lafold2 = f'{vol}lasla2/'
phi_fold = f'{vol}phi/'
phi_fold2 = f'{vol}phi2/'

cobr = chr(774)  # both hat and lemma
conu = chr(7909)
tie = chr(865)
ac = chr(769) # accent mark
el = chr(8255)
circle = "\u25e6"

diph = ['ae', 'au', 'ei', 'eu', 'oe']
## only words with the cui, cuius or huic huius
## have the ui diphthong
authors = ['LS', 'GG', 'GJ', 'Ge', 'FG', 'Lw', 'YO', 'PO', 'WW']
authors2 = ['LS', 'GG', 'GJ', 'Ge', 'Lw', 'YO', 'PO']
authors3 = ['PO', 'GG', 'Ge', 'LS', 'LW', 'GJ', 'YO']
encs = {'que', 'ue', 'ne', 'st','cum','dum','nam'}
def_order = ['co', 'ls', 'lw', 'gj', 'gg', 'ge']
def_order_long = ['lw', 'co', 'ls', 'gj', 'gg', 'ge']
false_diph = set()

class JVReplacer(object):  # pylint: disable=R0903
    """Replace J/V with I/U."""

    def __init__(self):
        """Initialization for JVReplacer, reads replacement pattern tuple."""
        patterns = [(r'j', 'i'), (r'v', 'u'), (r'J', 'I'), (r'V', 'U')]
        self.patterns = \
            [(re.compile(regex), repl) for (regex, repl) in patterns]

    def replace(self, text):
        """Do j/v replacement"""
        for (pattern, repl) in self.patterns:
            text = re.subn(pattern, repl, text)[0]
        return text


jv = JVReplacer()




def enclitics(word, fake_enclitics):
    for e in encs:
        if word == e:
            return e, ""

        if word.endswith(e) and word not in fake_enclitics:
            if word.endswith('que') and e == 'ue':
                pass
            else:
                enc = word[-(len(e)):]
                if enc == 'ue':
                    enc = 've'
                nword = word[:-(len(e))]
                return nword, enc
    return word, ''





def both_long_short(s):
    dct = {
        'ā': 'â',
        'ē': 'ê',
        'ī': 'î',
        'ū': 'û',
        'ō': 'ô',
        'ȳ': 'ÿ',
        'Ā': 'Â',
        'Ē': 'Ê',
        'Ī': 'Î',
        'Ō': 'Ô',
        'Ū': 'Û',
        'Ȳ': 'Ÿ',
    }

    e = 0
    while e < len(s):
        x = s[e]
        if x == cobr:
            pl = s[e - 1]
            t = dct[pl]
            s = replace_at_i(e - 1, s, t)
            s = delete_at_i( e,s)
        else:
            e += 1
    return s


def get_def_many(dct):
    s = ""
    for k,v in dct.items():
        t = get_def(v,1,0,1)
        if not k:
            k = '0'
        s += " "+ f"#{k} - {t}"
    return  s


def get_def(ins, large=0, all=0, dct=0):
    if not large:
        lst = def_order
    else:
        lst = def_order_long
    lst1 = []
    for auth in lst:
        try:
            if dct:
                val = ins[f'def_{auth}']
            else:
                val = getattr(ins, f'def_{auth}')
        except:
            val = ''

        if val and not all:
            return val
        elif val:
            lst1.append(val)

    if all:
        return lst1
    else:
        return ""


def greek_models():
    lst1 = ['vita_g1', 'vita_g2', 'vita_g2a', 'lupus_g', 'templum_g', 'miles_g', 'miles_g2', 'civis_g', 'clio_g']
    lst1 += ['perseus', 'artios']
    lst = [
        'leda',
        'cometes',
        'cybele',
        'perseus',
        'delos',
        'ilion',
        'aer',
        'tethys',
        'opes',
        'ciuis',
        'thales',
        'poesis',
        'manes',
        'apis',
        'clio',

    ]
    return lst1


def divide_words(dct1, end=0):
    dct = defaultdict(dict)
    for k in dct1.keys():
        if not end:
            dct[k[0]].setdefault(len(k), []).append(k)
        else:
            try:
                dct[k[-2:]].setdefault(len(k), []).append(k)
            except:
                pass
    # for k,v in dct.items():
    #     v = sort_dct_key(v)

    return dct



def collat_lem(lem):
    dct = {
        'lemma':lem,
        'model':'',
        'geninf':'',
        'perf':'',
        'capital':0,
        'def_co':'',
        'pos':'',
        'def_lw':'',
        'def_ls':'',
        'def_gj':'',
        'def_gg':'',
        'def_ge':'',
        'parent':'',
        'macronized':0
    }
    return dct


class entry:
    def __init__(self, word):
        self.rest = []
        self.pos = []
        self.idioms = []
        self.defs = []
        self.accent = ""
        self.word = word
        self.raw = []
        self.gender = []
        self.conj = ""
        self.pos2 = ''
        self.pos_abb = ""
        self.prop2 = ''
        self.fridioms = []

    def __repr__(self):
        return self.word


def new_lem(lst):
    dct = {
        'lemma': lst[0],
        'quantity': lst[5],
        'model': lst[1],
        'geninf': lst[2],
        'perf': lst[3],
        'lexicon': lst[4],
        'syl': "",
        'capital': 0
    }
    return dct


def new_lem2(lem):
    dct = {
        'lemma': lem,
        'quantity': "",
        'model': "",
        'geninf': "",
        'perf': "",
        'lexicon': "",
        'syl': ""
    }
    return dct


def remove_hats(x):  # 299 257 275 333 363
    dct = {
        259: 'a',
        277: 'e',
        301: 'i',
        335: 'o',
        365: 'u',
        1118: 'y',
        297: 'i',
        235: 'e',
        65533: '',
        237: 'i'
    }
    for k, v in dct.items():
        x = x.replace(chr(k), v)
    return x


def cut_num(x, wdig=0):
    y = x
    if not x:
        if wdig:
            return x,""
        else:
            return ''

    if x[-1].isdigit():
        y = x[:-1]
    if wdig:
        if y != x:
            return y, x[-1]
        else:
            return x, ""
    return y


def cut_num2(x):
    while x[-1].isdigit():
        x = x[:-1]
    return x


def prefixes():
    lst = to.from_txt2lst(f'{fold}prefixes', 1)
    lst = [x.replace('\t', '') for x in lst]
    lst = [x.strip() for x in lst]
    lst2 = [x[:-1] for x in lst if x and x[-1] == '-']
    lst1 = [x[:-1] for x in lst if x and x[-1] == '+']
    lst2 = vgf.sort_lst_by_len(lst2, 1)
    # lst2.sort()
    pre2macron = {}
    for x in lst2:
        y = unidecode(x)
        pre2macron[y] = x
    return pre2macron, lst1


def remove_hats_diph(x, gu="", rd=0, io=0):
    # hd stands for research diphthongs
    uw = []
    x = x.replace(cobr, '')
    if gu:
        for e, let in en(gu):
            if let == conu:
                x = replace_at_i(e, x, "@")
                uw.append(e)

    cap = 0
    if x[0].isupper():
        o = x
        cap = 1
        x = x.lower()

    diph3 = ['ae', 'au', 'ei', 'eu', 'oe', 'ui']
    if io:
        diph3.append('io')

    mac = 'āēīōūȳ'
    brev = 'ăĕĭŏŭў'
    both = 'ō̆ā̆ē̆ī̆ū̆ȳ̆'
    fd = []
    no_uni = unidecode(x)
    b = 0
    widx = []
    for k, j in zip(x[0:-1], x[1:]):
        if k + j in ['qu', 'gu']:
            widx.append(b + 1)
        b += 1
    for z in widx:
        x = replace_at_i(z, x, 'w')
        no_uni = replace_at_i(z, no_uni, 'w')
    for i in range(len(x)):
        c = 2
        if i == len(x) - 1:
            c = 1
        lets = x[i:i + c]
        let = x[i]
        luni = no_uni[i:i + c]
        if luni in diph3:
            if any(z in list(lets) for z in mac + brev):
                lstm = []
                lstb = []
                lstbo = []
                for e, l in en(lets):
                    if l in mac:
                        lstm.append(e)
                    elif l in brev:
                        lstb.append(e)
                    elif l in both:
                        lstbo.append(e)

                if len(lstb) == 1 and (len(lstm) == 1 or
                                       (len(lstbo)) == 1):
                    idx = lstb[0]
                    let = unidecode(lets[idx])
                    x = replace_at_i(idx + i, x, let)
                    fd.append(i)
                elif len(lstb) == 2:
                    let = unidecode(lets[1])
                    x = replace_at_i(1 + i, x, let)
                    fd.append(i)

                # elif lstb or lstm or lstbo:
                #     fd.append(i)


        elif let in brev:
            let = unidecode(let)
            x = replace_at_i(i, x, let)
    for w in widx:
        x = replace_at_i(w, x, 'u')
    if cap:
        x = x.capitalize()
    x = x.replace('@', chr(7909))

    if rd:
        return x, fd, uw
    return x


def match_vowels(tword_mac, word, ns=1):
    if ns:
        word = norm_str_jv(word)
    vowels = re.sub(r'[^aeiouyāēīōūȳăĕĭŏŭў]', '', tword_mac)
    for e, l in en(word):
        if l in 'aeiouy':
            word = replace_at_i(e, word, vowels[0])
            if len(vowels) > 1:
                vowels = vowels[1:]
    return word


def match_vowels_all(star, follower, star_wmac):
    star_nc = elim_cons(star)
    follower_nc = elim_cons(follower)
    if star_nc.startswith(follower_nc):
        word1 = match_vowels(star_wmac, follower, 0)
    else:
        return ""
    return word1


def restore_jv(s, lst):
    j = lst[0]
    v = lst[1]
    w = lst[2]
    for l in j:
        s = replace_at_i(l, s, 'j')
    for l in v:
        s = replace_at_i(l, s, 'v')
    for l in w:
        s = replace_at_i(l, s, conu)
    return s


def elim_cons(word):
    return re.sub(r'[^aeiouyāēīōūȳăĕĭŏŭў]', '', word)


def elim_vows(word):
    return re.sub(r'[aeiouyāēīōūȳăĕĭŏŭў]', '', word)


def norm_str_wmac(x):
    x = jv.replace(x)
    return x.lower()


def norm_str_jv(x, caps=0):
    x = jv.replace(x)
    if caps:
        return unidecode(x)
    else:
        return unidecode(x).lower()


def last_vowel(x):
    if len(x) == 1:
        return 1

    b = len(x) - 1
    for l in reversed(x):
        if l in 'aeiouy':
            break
        b -= 1
    if x[b - 1:b + 1] in diph:
        return b - 1
    # if len(x) == 1:
    #     return 0

    return b


class decline:
    def __init__(self, lemmas={}, models={}, pos={}):
        if not lemmas:
            self.lemmas = pi.open_pickle(f'{fold}mac_lemmas_old', 1)
        else:
            self.lemmas = lemmas
        if not models:
            self.mmodels = pi.open_pickle(f'{fold}mmodels', 1)
            # self.models = pi.open_pickle(f'{fold}mod_vow2', 1)
        else:
            self.models = models
        if not pos:
            self.pos = pi.open_pickle(f'{fold}final_pos', 1)
        else:
            self.pos = pos

    def dec(self, lemma, ui=0, divide=0):
        '''
        the first member in the R list is the # of places subtracted
        from the ending of the root, the second member is a set of letters
        which appears before the ending
        in the keys in the dict 1 is always the geninf root
        and 2 is always the perf root

        hence to form a word, the root must be known, how much is subtracted
        from its ending and then the ending

        in the shortened decliner we simply state the ending, the root
        and how much is subtracted from the root

        '''

        model, mstem, tdct = self.long(lemma, ui)
        self.get_stem_dct(model, mstem, tdct)
        make_short = {
            'a':'ă',
            'e':'ĕ',
            'i':'ĭ',
            'o':'ŏ',
            'u':'ŭ',
        }

        fdct = {}
        sdct = defaultdict(list)
        sufd = model['sufd']
        for posn, v in model['des'].items():
            if posn not in model['abs']:
                if posn in [37]:
                    bb=8
                suf = self.suf.get(posn, [])
                if not sufd and suf:
                    sufd = suf
                pos1 = self.pos[posn]
                lst = []
                for l in v:
                    root = l[0]
                    endings = l[1]
                    if divide:
                        rlst = model['R'][root]
                        sub = rlst[0]
                        mid = rlst[1]
                        if not sub:
                            sub = 0
                        else:
                            sub = int(sub)
                        for ending in endings:
                            if sufd:
                                for s in sufd:
                                    sdct[pos1].append((root, sub, mid + ending + s))
                                    if not model['sufd']:
                                        sdct[pos1].append((root, sub, mid + ending))
                            else:
                                sdct[pos1].append((root, sub, mid + ending))

                    else:
                        rlst = self.stems[root]
                        for beg in rlst:
                            for ending in endings:
                                found = 0
                                if not ui and ending and beg:
                                    new_dip = f'{beg[-1]}{ending[0]}'
                                    if new_dip in diph:
                                        found = 1
                                        beg = f'{beg[:-1]}{make_short[beg[-1]]}'
                                if sufd:
                                    for s in sufd:
                                        word = f'{beg}{ending}{s}'
    #although rarely used tu in sn gets put in there twice
                                        if word not in lst:
                                            lst.append(word)

                                        if not model['sufd']:
                                            word = f'{beg}{ending}'
                                            if word not in lst:
                                                lst.append(word)

                                else:
                                    word = f'{beg}{ending}'
                                    if found:
                                        if word not in false_diph:
                                            false_diph.add(word)
                                            # p (f'false diphthong {word}')
                                    if word not in lst:
                                        lst.append(word)

                sufd = model['sufd']
                fdct[posn] = [lst, pos1]
                # splst.append([slst, pos1])

        if divide:
            return sdct
        return fdct

    def get_atts(self):
        self.sdct = {}
        self.lem_info = self.lemmas[self.lemma]


    def long(self, lemma, ui, divide=0):
        self.lemma = lemma
        self.ui = ui
        tdct = {}
        lem_info = self.lemmas[lemma]
        if self.ui:
            lem_info = self.ui_norm(lem_info)
        model = self.models[lem_info["model"]]
        if not divide:
            self.use_suf(model)

        mstem = lem_info['lemma']
        if mstem[-1].isdigit():
            mstem = mstem[:-1]
        ## the geninf stem is always the 1st root and the
        ## perfect is always second
        for e, x in en(['geninf', 'perf']):
            if lem_info[x]:
                tdct[str(e + 1)] = lem_info[x]
            else:
                tdct[str(e + 1)] = mstem
        tdct['0'] = mstem
        return model, mstem, tdct

    def ui_norm(self, lem_info):
        lem_info = copy.deepcopy(lem_info)
        for x in ['lemma', 'geninf', 'perf']:
            if lem_info[x]:
                lem_info[x] = norm_str_jv(lem_info[x])
        return lem_info

    def short(self, lemma, ui, test=0):
        model, mstem, tdct = self.long(lemma, ui,1)
        self.get_stem_dct(model, mstem, tdct,1)
        if test:
            final = defaultdict(set)
        else:
            final = defaultdict(list)

        for k, v in model['sim'].items():
            for tpl in v:
                root = tpl[0]
                ending = tpl[2]
                stems = self.stems[root]
                for stem in stems:
                    word = f'{stem}{ending}'
                    if test:
                        final[k].add(word)
                    else:
                        final[k].append(word)

        return final







    def get_stem_dct(self, model, mstem, sdct, divide=0):
        self.stems = {}
        for k, v in model['R'].items():
            de = int(v[0])
            add = v[1]
            lst = sdct.get(k, mstem).split(',')
            if divide:
                add = ""
            lst = [f"{x[:len(x) - de]}{add}" for x in lst]
            self.stems[k] = lst

    def use_suf(self, model):
        self.suf = defaultdict(set)
        if model['suf']:
            for l in model['suf']:
                w = l[0]
                for n in l[1]:
                    self.suf[n].add(w)
            for x,y in self.suf.items():
                self.suf[x] = list(y)

bb=8