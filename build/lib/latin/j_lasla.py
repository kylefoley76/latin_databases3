import os
from bglobals import *




'''
1. convert lasla to text
1.4 stems A
1.5 memorization table
2. macronizer without lasla
3. parsed OLD
4. scan poetry
5. search engine
6. add english



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



def help():
    p ("""
    The purpose of this module is to normalize the lemmas, and the parts of speech (pos)
    of the LASLA database. We are not here interested in normalizing the words.
    We also take the first steps in developing a system such that the LASLA database
    can be easily converted into a readable text document.  First, we must distinguish words
    which are to be printed when converting to text and words which do not.
    The main object we output in this module is the 'auth2work' object.  This is dictionary of lists
    and in each list is contained another list each containing most of the time one word.
    This list has the following dimensions:
    
    0: here we write down certain categories and how the list should be handled
    
    "": the most common category, simply print the word
    !: do not print the word, in dimension 4 we will state why
    @: print the word, but do not use it for gathering statistics.
        these are words whose pos was not put in a standard form
    
    1: this dimension contains the lemma.  If a word is proper and a noun
        then the lemma ends with 9.  If the word is proper and a adjective
        then the lemma ends with 8.
        The index numbers of the lemmas in the original were found on the word
        not the lemma but this was changed here to putting the index numbers on the lemmas.
        lemmas are also put in all lowercase and j and v are placed with i and u respectively.
        
    2: this dimension contains the word.  All words are put in lowercase.  if they are
    proper then that info gets put on the lemmas as mentioned earlier.
        if the word is greek is became garbled in lasla and here is changed
        to simply [GREEK]
        
    3: the numbering of the latin text. nothing is changed here.
    
    4: the pos gets converted into something human readable. 
    we also use the pos found in the collatinus database which contains
    416 different pos.  lasla has about 10 other pos which are not contained in collatinus.
    the adjectives were also labeled with three codes which are not found in collatinus.
    these are
    C: masculine, feminine or neuter
    B: masculine, feminine
    X: masculine or neuter
    
    these are put in capital letters so as to be able to easily convert
    them to the official pos
    
    
    when an pos is missing an elemment we label that element with captal letters
    as follows
    
        gender = 'G'
        person = 'P'
        case = 'A'
        mood = 'M'
        voice = 'V'
        tense = 'T'
        number = 'N'
        degree = 'D'
    
    None of the converted collatinus pos have capital letters so
    if a pos has capital letters you know that something is wrong with it
    
    On a few occasions lasla used the number 0 although it is not written
    down in their guide book what 0 means.  
    
    
    
    """)











class parse_words:
    def __init__(self):
        pass

    def get_atts_pw(self):
        self.wst1 = set()
        self.wst2 = set()
        self.all_lines2 = set()
        self.odd_words = set()
        self.odd_words2 = set()
        self.odd_words3 = set()
        self.all_words_pw = set()
        self.bad_words = set()
        self.greek = set()
        self.tlemma = ''
        self.tword = ''
        self.lem_num = ''
        self.capitals = set()
        self.short = set()
        self.toword = ''
        self.pos3 = ''

        pass

    def del_attribs(self):
        self.all_atts = ['wst1', 'wst2', 'all_lines2',
                         'all_words_pw',
                         'bad_words', 'greek', 'tlemma', 'toword',
                         'pos3', 'capitals', 'short', 'lem_num']
        o = ['odd_words2', 'odd_words', 'odd_words3']
        for x in self.all_atts:
            delattr(self, x)

        more_atts = ['lem2forms']
        for x in more_atts:
            try:
                delattr(self, x)
            except:
                pass

    def parse_words_fu(self):

        for line in self.all_lines:
            self.tlemma = line[1]
            self.tword = line[0]
            self.pos3 = line[2]
            self.toword = self.tword

            if len(self.tword) > 1:
                if self.tword[0] == '$':
                    self.greek.add(self.tword)
                else:
                    self.parse_words_fu2()

                    if reg(r'[^a-zA-Z]', self.tword):
                        pass
                    else:
                        wordu = norm_str_jv(self.tword)
                        lemmau = norm_str_jv(self.tlemma)
                        if wordu in self.macronizer_new:
                            self.all_lines2.add((lemmau, wordu, self.pos3))
                            self.all_words_pw.add(wordu)
                        else:
                            self.bad_words.add(wordu)

        # col_words = set(self.macronizer_new.keys())
        # no_col = all_words - col_words
        # p (len(no_col))
        pi.save_pickle(self.all_lines2, f'{fold}lasla_lines2', 1)

        return

    def parse_words_pre(self):
        if len(self.tword) > 1:
            if self.tword[0] == '$':
                self.greek.add(self.tword)
            else:
                self.parse_words_fu2()

    def parse_words_fu2(self):
        self.lem_num = ""
        if "(" in self.tword:
            self.line2paren[(self.work, self.line)] = self.tword
            inside = vgf.inside(self.tword, '(', ')')
            if inside in self.sum2pos_dct:
                self.sum_word = inside
                self.sum_paren = 1

            self.tword = re.sub(r'\(.*\)', '', self.tword)
            self.has_paren = 1

        if not hl(self.tword):
            self.add2errors('odd_word2', self.tword)
        else:
            if self.tword[0].isdigit():
                self.lem_num = self.tword[0]
                self.tword = self.tword[1:]
                self.tword = self.tword.strip()




            elif self.is_proper():
                pass

            elif self.tword[0].isupper():
                self.tlemma = self.tlemma.capitalize()

            if len(self.tword) > 1 and self.tword[0] == ' ':
                self.odd_words3.add(self.toword)
            else:
                if reg(r'[^a-zA-Z]', self.tword):
                    self.odd_words.add(self.tword)

    def is_proper(self):
        if self.tword == 'Areos Pagos':
            bb = 8

        if len(self.tword) > 1 and self.tword[0] in ['N', 'A']:
            if self.tword[1].isupper():
                if len(self.tword) > 2:
                    if self.tword[2].isupper():
                        self.wst1.add(self.tword)
                    else:
                        beg = self.tword[0]
                        self.lem_num = '9' if beg == 'N' else '8'
                        self.tword = self.tword[1:]
            else:
                if len(self.tword) < 3:
                    self.short.add(self.tword)
                else:
                    if self.tword[:2].lower() == self.tlemma[:2].lower():
                        self.capitals.add((self.tword, self.tlemma))
                    else:
                        beg = self.tword[0]
                        self.lem_num = '9' if beg == 'N' else '8'
                        self.tword = self.tword[1:]


def is_proper2(word):
    if len(word) > 1 and word[0] in ['N', 'A']:
        if word[1].isupper():
            if len(word) > 2:
                word = word[1:]

    return word


class convert2txt(parse_words):
    def __init__(self):
        parse_words.__init__(self)

    def begin_ct(self):
        self.kind = ''
        self.get_atts_pw()
        self.get_atts()
        self.fix_sum()

        if not self.kind in ['small', 'debug']:
            self.ad_hoc()
            self.lasla_typos()
        self.main_loop()
        self.del_attribs()
        self.output(1)

        return

    def begin1(self):
        self.build_db()
        self.all_lasla_lemmas()
        self.parse_words_fu()

    def begin3(self):
        self.review()
        self.normal_words()
        self.review_errors2()
        self.review_errors()
        self.output(2)

    def get_atts(self):
        # self.kind = 'small'
        if not public:
            self.auth2work = pi.open_pickle(f'{fold}lasla_db', 1)
        else:
            self.rename_db3()
        if self.kind in ['small','debug']:
            self.auth2work = vgf.split_dct(self.auth2work, 0, 1)
            self.auth2work_db = copy.deepcopy(self.auth2work)
        self.final_pos = pi.open_pickle(f'{fold}final_pos', 1)
        self.final_pos_rv = {v: k for k, v in self.final_pos.items()}
        # self.lem2forms = pi.open_pickle(f'{sfold}lem2forms_wonum', 1)
        # self.macronizer_new = pi.open_pickle(f'{sfold}macronizer_new', 1)
        # self.all_lines = pi.open_pickle(f'{sfold}lasla_lines',1)
        # self.all_lines = pi.open_pickle(f'{sfold}lasla_lines2', 1)
        self.verb_dcts()
        self.errors = defaultdict(list)
        self.verb_dcts2()
        self.verbs_forms = defaultdict(set)
        self.adj_forms = defaultdict(set)
        self.lemma2decl = defaultdict(dict)
        self.pos_ct = defaultdict(int)
        self.bogus_pos = defaultdict(list)
        self.done = 0
        self.has_paren = 1
        self.sum_paren = 0
        self.true_pos = defaultdict(list)
        self.true_pos2 = defaultdict(list)
        self.no_case = defaultdict(list)
        self.no_gender = defaultdict(list)
        self.lem2info = defaultdict(list)
        self.all_lems = set()
        self.sum_errors = defaultdict(list)
        self.sum2pos_dct = pi.open_pickle(f'{fold}sum2pos', 1)
        self.sum_word = ""
        self.owords = defaultdict(set)
        self.lafreq = defaultdict(int)
        self.strange_words = set()
        self.sum_lemmas = set()
        self.adjacent2 = defaultdict(set)
        self.anomalies = defaultdict(set)
        self.line2paren = {}
        # self.anomalies2 = pi.open_pickle(f'{sfold}anomalies',1)

        return

    def output(self, kind=1):
        if kind == 3:
            pi.save_pickle(self.auth2work, f'{fold}lasla_db2', 1)
        elif kind:
            pi.save_pickle(self.auth2work, f'{fold}lasla_db2', 1)
            pi.save_pickle(self.bogus_pos, f'{fold}bogus_pos', 1)
            pi.save_pickle(self.true_pos2, f'{fold}bogus_pos2', 1)
            pi.save_pickle(self.errors, f'{fold}lasla_errors', 1)
            pi.save_pickle(self.anomalies, f'{fold}lasla_anomalies', 1)
            pi.save_pickle(self.lafreq, f'{fold}las_freq', 1)
            pi.save_pickle(self.lemma2decl, f'{fold}lemma2decl', 1)

        return

    def fix_sum(self):
        self.sum2pos_dct['iri'] = ['if.fu.pa']
        self.sum2pos_dct['siet'] = ['3.pr.sj.ac']
        self.sum2pos_dct['siem'] = ['4.pr.sj.ac']
        self.sum2pos_dct['sies'] = ['2.pr.sj.ac']
        self.sum2pos_dct['sient'] = ['6.pr.sj.ac']

    def rename_db1(self):
        lst = []
        for k,v in self.auth2work.items():
            for x,y in v.items():
                lst.append([k,len(y),x,x])
        file = f'{fold}rename_lasla'
        to.from_lst2txt_tab_delim(lst, file)
        vgf.open_txt_file(file)

    def rename_db2(self):
        lst = []
        lst2 = []
        for k,v in self.auth2work.items():
            dct={}
            for x,y in v.items():
                xu = x.split('_')
                xu = xu[1]
                lst.append([xu,f'{k},{x}'])
                dct[x] = y
            file = f'{lafold2}{k}'
            pi.save_pickle(dct,file)
        file2 = f'{fold}rename_lasla2'
        to.from_lst2txt_tab_delim( lst,file2)
        return

    def rename_db3(self):
        # file2 = f'{fold}rename_lasla2'
        # lst = to.from_txt2lst_tab_delim(file2)
        # dct = {}
        # for x in lst:
        #     k = x[0]
        #     auth, work = x[1].split(',')
        #     dct[auth]
        self.auth2work = {}
        file = f'{lafold}'
        for l in os.listdir(file):
            if not l[0]=='.':
                auth = l[:-4]
                file3 = file + l
                obj = pi.open_pickle(file3)
                self.auth2work[auth] = obj

        return



    def build_db(self):
        bpn = f'{lafold}bpn/'
        self.auth2work = defaultdict(dict)
        b = 0
        p (f"""
        now looping through the lasla files and putting
        them into a python user-friendly format
""")

        tot = len(os.listdir(bpn))
        for x in os.listdir(bpn):
            b += 1
            vgf.print_intervals(b, 5, None,tot)
            if x[0] != '.':
                auth = x[:x.index('_')]
                work = x[x.index('_') + 1:-4]
                lst = to.open_any(bpn + x)
                lst1 = lst.split('\n')
                words = []
                for z in lst1:
                    lst2 = z.split('  ')
                    lst3 = [w.strip() for w in lst2 if hl(w)]
                    if len(lst3) > 4:
                        lst4 = lst3[:3]
                        idx = z.index(f' {lst4[2]} ')
                        final = z[idx + len(lst4[2]) + 2:]
                        final = final.lstrip()
                        lst4.append(final)
                    else:
                        lst4 = lst3
                    lst4.insert(0, z)
                    words.append(lst4)
                self.auth2work[auth][work] = words
        pi.save_pickle(self.auth2work, f'{fold}lasla_db', 1)
        return

    def build_apn(self):
        apn = f'{lafold}apn/'
        self.auth2work_ap = defaultdict(dict)
        b = 0
        for x in os.listdir(apn):
            b += 1
            vgf.print_intervals(b, 5)
            if x[0] != '.':
                auth = x[:3]
                work = x[3:]
                lst = to.open_any(apn + x)
                lst1 = lst.split('\n')
                words = []
                for z in lst1:
                    lst2 = z.split('  ')
                    lst3 = [w.strip() for w in lst2 if hl(w)]
                    if len(lst3) > 4:
                        lst4 = lst3[:3]
                        idx = z.index(f' {lst4[2]} ')
                        final = z[idx + len(lst4[2]) + 2:]
                        final = final.lstrip()
                        lst4.append(final)
                    else:
                        lst4 = lst3
                    lst4.insert(0, z)
                    words.append(lst4)
                self.auth2work_ap[auth][work] = words

    def analyze(self):
        lstb = self.auth2work['Cato']['CatoAgricultura_CatAgr']
        lsta = self.auth2work_ap['Cat']['Agric.APN']
        lst1 = []
        sta = set()
        stb = set()
        for a, b in zip(lsta, lstb):
            if len(a) > 4 and len(b) > 4:
                if len(b[4]) == 13:
                    b[4] = b[4][:-1]
                sa = a[4].strip()
                sb = b[4].strip()
                sta.add(sa)
                stb.add(sb)
                if sa != sb:
                    p(sa, sb)
                # lst1.append([a[4],b[4]])
        stc = sta - stb

    def all_lasla_lemmas(self):
        self.all_lemmas = set()
        self.all_words = set()
        self.all_lines = set()

        errors = []
        b = 0
        for auth, works in self.auth2work.items():
            for name, work in works.items():
                b += 1
                vgf.print_intervals(b, 5)
                for info in work:
                    if not len(info) > 1:
                        errors.append(info)
                    else:
                        if len(info[1]) > 8:
                            word = info[1][8:]
                            self.lemma = norm_str_jv(word)
                            self.word = info[2]
                            self.all_words.add(self.word)
                            self.all_lemmas.add(self.lemma)
                            if len(info) > 4:
                                pos = info[4]
                                pos2 = self.elim_edit(pos)
                                self.all_lines.add((self.word, self.lemma, pos2))
                            else:
                                errors.append(info)

                        else:
                            errors.append(info)
        pi.save_pickle(self.all_lines, f'{fold}lasla_lines', 1)

        return

    def elim_edit(self, num2):
        if len(num2) > 9:

            if len(num2) > 12:
                s = num2[:9] + '   ' + num2[12]
                return s
            else:
                s = num2[:9]
                return s

        else:
            if num2[0] == 'B':
                bb = 8

            return num2

    def ad_hoc(self):
        self.auth2work['Plautus']['Captiui_PlCapt'][2069] = ['*', '01234567Thensaurochrysonicochrysides',
                                                             'Thensaurochrysonicochrysides', 285, 'ns']
        self.auth2work['Plautus']['Captiui_PlCapt'][5173] = ['*', '01234567Thensaurochrysonicochrysides',
                                                             'Thensaurochrysonicochrysides', 285, 'ns']

    def lasla_typos(self):
        lst = to.from_txt2lst_tab_delim(f'{fold}lasla_typos')
        lst1 = to.from_txt2lst_tab_delim(f'{fold}lasla_typos2', 0, 1)
        lst += lst1
        for x in lst:
            auth = x[0]
            work = x[1]
            line = x[2]
            idx = x[3]
            s = x[4]
            try:
                orig = self.auth2work[auth][work][line][idx]
                self.auth2work[auth][work][line][idx] = s
            except:
                self.auth2work[auth][work][line].append(s)

            # p (f'replaced {orig}  with {s}')
        return

    def main_loop(self):
        b = 0
        self.num_lines = 0
        self.insert = {}
        self.infos = []
        self.adjacent = set()
        self.ninfo = ''
        self.lword = ''
        self.enclits = set()
        self.adjacent3 = 1
        self.paren2loc = {}
        self.delay_sum = 0
        p (f"""
        now looping through the lasla database
        and normalizing it
""")

        for self.auth, works in self.auth2work.items():
            for self.work, self.infos in works.items():
                b += 1
                vgf.print_intervals(b,5,None,236)

                if self.kind == 'debug':
                    self.work = 'PhilippicaOratio_CicPhi08'
                    self.auth = 'Cicero'
                    self.infos = self.auth2work[self.auth][self.work]
                for self.line, info in en(self.infos):
                    if self.line == 4:
                        bb = 8
                    if self.work == '' and self.line == 2692:
                        bb = 8
                    self.num_lines += 1
                    self.info = info
                    self.cpos = ''
                    self.elsum = 0
                    self.backwards_sum = 0
                    self.sum_paren = 0
                    try:
                        self.ninfo = self.infos[self.line + 1]
                    except:
                        self.ninfo = ''
                    self.special = 0
                    self.main_loop2(info)


                if b in [50, 100]:
                    bb = 8
            # if b > 50:
            #     break

        return

    def temp17(self):
        lst5 = []
        for e, x in en(self.errors['bad_sum']):
            if e < 9 or e > 37:
                lst5.append([x[1], x[2], x[3], '2', x[0]])
        for e, x in en(self.errors['bad_sum']):
            if e < 9 or e > 37:
                lst5.append([x[1], x[2], x[3], 4, '0'])

        file = f'{fold}temp_typos'
        to.from_lst2txt_tab_delim(lst5, file)
        vgf.open_txt_file(file)

    def temp18(self):
        st = set()
        for self.auth, works in self.auth2work.items():

            for self.work, self.infos in works.items():
                # self.work = 'DeOfficiis_CicOffic1'
                # self.auth = 'Cicero'
                # self.infos = self.auth2work[self.auth][self.work]
                for self.line, info in en(self.infos):
                    if '&' in info[1] and info[0] != '!':
                        p(self.auth, self.work, self.line)
                        break

    def main_loop2(self, info):
        '''
        the lasla database has the following types of lines
        a standard line has a recoginizable pos and has no strange characters in the word

        '''

        if len(info) == 1:
            self.tword = ''
            self.tlemma = ''
            self.pos = ''
            self.add2pos('_1l')

        elif len(info) != 5 or info[2][0] == '$':
            if info[2][0] == '$':
                self.tword = 'GREEK'
                self.add2pos('_gr')
            else:
                self.add2pos('_4')
                self.add2errors('_4', self.tword)

        elif info[0] in ['*', '!']:
            pass

        else:
            word1 = ''
            if self.kind == 'set':
                self.word = info[1]
                self.lemma = info[0]
                num2 = info[2]
                self.num2 = num2
            else:
                self.cpos = 0
                self.has_paren = 0
                self.raw = info[0]
                self.tlemma = self.parse_lemma(info[1])
                self.word = info[2]
                self.idx = info[3]
                self.tword = self.word
                self.toword = self.tword
                self.parse_words_pre()
                self.tlemma = self.tlemma + self.lem_num



            if self.tword and self.tword[0] == '$':
                self.cpos = 'gr'
                self.add2pos('_gr')

            else:

                if reg(r'^#[A-Z]', self.info[4]):
                    self.info[4] = self.info[4][1:]
                    self.special = 1

                self.mpos = info[4][0]

                if reg(r'[A-Z]', self.mpos):
                    self.convert_pos3(info, self.mpos)

                elif self.tlemma == '#' or self.mpos in ['#', '0'] or \
                        self.tlemma in ['_sum2', '_eo2']:

                    if self.tword == 'dignam':
                        bb = 8

                    if self.tlemma.startswith('_sum') and self.tword.endswith('st') and \
                            len(self.tword) > 3 and '<' not in self.tword:
                        self.sum_elision()


                    elif not ' ' in self.tword:
                        """
                        these are words that were not understood or are in lacunae
                        if they are consecutive we might surround them with marks
                        if they are genuine words we will macronize them
                        """

                        self.add2pos('_nsp')



                    elif self.proper_space():
                        if self.tword in ['reos Pagos', 'oui Comi']:
                            self.add2errors('bad_name', self.tword)
                        self.add2pos('_psp')


                    elif self.tword.count('>') == 1 and self.separable():
                        pass
                    elif self.delay_sum:
                        self.auth2work[self.auth][self.work][self.line][0] = '!'
                        self.auth2work[self.auth][self.work][self.line][4] = 'ds'
                        self.delay_sum = 0
                    else:
                        if self.ninfo and len(self.ninfo) > 2:
                            onword = self.ninfo[2]
                        else:
                            onword = ''

                        if self.line > 0:
                            try:
                                olword = self.infos[self.line - 1][2]
                                lword = re.sub(r'[0-9]', '', olword).strip()
                                lword = is_proper2(lword)
                                lword = re.sub(r'[<>\(\)]', '', lword).strip()
                                self.lword = re.sub(r'\s{2,}', ' ', lword)
                            except:
                                self.lword = ''
                        else:
                            self.lword = ''

                        onword2 = self.lasla_match(onword)
                        word1 = self.lasla_match(self.tword)

                        if word1 == onword2:
                            '''
                            for the sum, eo words lasla assigned a pos on the following or previous word
                            where the pos of sum and its participle can be deduced
                            for the other words in the future after they are macronized combine them
                            since that makes it easier to find them as a lemma,
                             some words cannot be easily combined like tanto opere
                            for now
                            if words on consecutive lines are both the same then simply delete
                                one of the lines, combine and put on one line
                            
                            '''

                            if self.tlemma in ['_sum2', '_eo2']:
                                self.add2pos('_yf')
                            else:
                                self.is_compound(1)
                                self.add2pos('_rf')

                        elif word1 == self.lword:
                            if self.tlemma in ['_sum2', '_eo2']:
                                self.add2errors('sum4', self.tword)

                                self.add2pos('_yp')
                            else:
                                self.is_compound(-1)
                                self.add2pos('_rp')

                        elif self.tlemma in ['_sum2', '_eo2']:
                            '''
                            words should not be going in here
                            '''

                            self.add2errors('bad_sum', self.tword)
                            self.add2pos('_w')

                        else:
                            '''
                            these words have spaces but should not have them
                            
                            these words have no pos, if their macronization is
                            unambiguous then macronize them, otherwise use some notation
                            to indicate that there is a problem with them, assign
                            ambig pos if possible
                            in some case there is an error where the two words are truly separated
                            but < > was not put around properly
                            
                            if one of the words is a sum word then the words are
                            divided and put on seperate lines and a pos assigned
                            where possible
                            
                            '''
                            self.add2pos('_n')


                else:
                    self.add2pos('_b')
                    self.add2errors('bad_pos', self.tword)

                self.lword = word1 if word1 else self.tword

    def is_compound(self, idx):
        if self.tword.count(' ') > 1 and idx > 0:
            nw = self.auth2work[self.auth][self.work][self.line + 1][2]
            nw = self.lasla_match(nw)
            if nw == self.tword:
                self.auth2work[self.auth][self.work][self.line + 1][0] = '!'

    def sum_elision(self):
        self.add2pos('_sel')
        self.add2errors('_sel', self.tword)


    def proper_space(self):
        try:
            nword = self.infos[self.line + 1][2]
        except:
            nword = ''
        try:
            lword = self.infos[self.line - 1][2]
        except:
            lword = ''

        if nword and nword[0] in ['N', 'A'] and self.word == nword[1:]:
            return 1
        elif lword and lword[0] in ['N', 'A'] and self.word == lword[1:]:
            return 1

    def add2errors(self, id, word):
        self.errors[id].append([word, self.auth, self.work, self.line])

    def lasla_match(self, word):
        onword2 = re.sub(r'[0-9]', '', word).strip()
        onword2 = is_proper2(onword2)
        onword2 = re.sub(r'[<>]', '', onword2).strip()
        onword2 = re.sub(r'\s{2,}', ' ', onword2)
        return onword2

    def convert_pos3(self, info, mpos):
        if mpos == 'A':
            self.nouns(info)
        elif mpos == 'B':
            self.verbs(info)
        elif mpos == 'C':
            self.adj(info)
        elif mpos == 'M':
            self.adv(info)
        else:
            self.other(info)
            pass

    def parse_lemma(self, s):
        lemma = s[8:]
        lemma = norm_str_jv(lemma)
        return lemma

    def iri(self, cpos):
        if self.sum_word in ['iri', 'eiri'] and 'fu.pa' in cpos:
            return 1

    def build_lem2info(self):
        for k, v in self.auth2work.items():
            if v[0]:
                if v[2] not in ['gr', 's']:
                    self.lem2info[v[0]].append([v[1], v[2]])
                    self.lafreq[v] += 1

    def add2pos(self, cpos):
        '''
        seperable well-formed words now have a _ on the lemma

        '''

        self.cpos = cpos
        if '(' in self.tword and cpos != '_gr':
            self.add2errors('has_paren', self.tword)
            bb = 8

        if '&' in self.tlemma or reg(r'[0-9]', self.tlemma[:-1]):
            bb = 8

        lst = ['', self.tlemma.lower(), self.tword, self.idx, self.cpos]
        tpl = (self.tlemma.lower(),self.tword, self.cpos)
        self.auth2work[self.auth][self.work][self.line] = lst


        if "_" in cpos:
            '''
            _1l = blank line
            _4 = list does not have 5 elements (fix)
            _nsp = pos in #, 0 but not space in the word
            _y sum word were one line = next line
            _rf, _rp has space and word = next word (no longer anomalous)
            _w space in word and lemma is _sum2
            _n hash_words
            _sp seperable but ill formed
            _s seperable well formed 
            _npsp proper nouns with a space which equal the following word           
            '''
            if cpos.startswith('_r') or cpos in ['_ss', '_n', '_1l']:
                lst[0] = '!'
            elif cpos.startswith('_nsp'):
                lst[0] = '?'
            self.anomalies[cpos].add(self.tword)

        elif  reg(r'[\s&\*\)]',cpos):

            '''
            these are parts of speech which lasla left incomplete, ie,
            did not state the case or tense, etc
            '''
            lst[0] = '@'
            self.add2errors('miss pos', self.tword)


        elif cpos:

            if cpos == 'gd.pb':
                cpos = 'gv.pmb'
            elif cpos == 'gd.pd':
                cpos = 'gv.pmd'

            if cpos.startswith('gd.') and cpos not in self.final_pos_rv:
                bb=8


            if cpos in self.final_pos_rv or self.iri(cpos):
                if self.iri(cpos):
                    pass
                else:
                    self.pos_ct[self.final_pos_rv[cpos]] += 1
                self.true_pos[cpos].append([self.tlemma, self.tword])
                self.lafreq[tpl] += 1


            elif reg(r'[A-Z]',cpos):
                self.true_pos2[cpos].append([self.tlemma, self.tword])


            else:
                if cpos in ['m']:
                    pass
                else:
                    self.add2errors('bad_pos' ,cpos)
                    self.bogus_pos[cpos].append([self.auth, self.work, self.line, self.tlemma, self.tword])

            self.cpos = cpos

    def anomaly_test(self):
        lst = ['_yf', '_yp']
        for y in lst:
            for x in self.anomalies[y]:
                if not x.count('>') == 1 or not x.count('<') == 1:
                    p(x)

    def missing_pos(self):  # bogus 55 missing 92
        have = {}
        nums = list(self.final_pos.keys())
        for x, y in self.pos_ct.items():
            have[x] = self.final_pos[x]
            nums.remove(x)
        self.have_not = {}
        for x in nums:
            self.have_not[x] = self.final_pos[x]
        have = sort_dct_key(have)
        return

    def separable(self):
        if self.line == 757:
            bb = 8

        tword = re.sub(r'[<>\s]', '', self.tword)
        end = len(self.infos) if len(self.infos) < self.line + 30 else self.line + 30
        begin = 0 if self.line < 30 else self.line - 30

        for e, t in en(self.infos[begin:end]):
            if len(t) < 2 or t == self.info:
                pass
            else:
                str1 = re.sub(r'[<>\s0-9]', '', t[2])
                if str1 == tword:
                    lemma = self.parse_lemma(t[1])
                    if self.split_separable(self.tword, t[2], e, t, lemma):
                        return 1
                    elif self.delay_sum:
                        return 0
                    else:
                        self.add2pos('_sp')
                        return 1
        return 0

    def split_separable(self, tword, c, idx, info, lemma):
        # todo one of the lemmas should be preceded by _
        pos = info[4]
        start = idx - 30
        if start < 0:
            first = tword
            second = c
            kind = 0
        else:
            first = c
            second = tword
            kind = 1

        if first.count('<') > 1 or \
                first.count('>') > 1 or \
                second.count('<') > 1 or \
                second.count('>') > 1:
            return 0

        f = vgf.outside(first, '<', '>')
        s = vgf.outside(second, '<', '>')
        s = re.sub(r'[0-9]', '', s)
        f = re.sub(r'[0-9]', '', f)

        if not f and s:
            f = re.sub(r'[<>0-9]', '', first)
            if f:
                f = f.replace(s, '').strip()

        elif f and not s:
            s = re.sub(r'[<>0-9]', '', second)
            if s:
                s = s.replace(f, '').strip()

        if s in self.sum2pos_dct or \
                f in self.sum2pos_dct:
            self.delay_sum = 1
            return 0

        if not kind:
            self.tword = s
        else:
            self.tword = f

        if not self.tword:
            bb = 8

        if ' ' in self.tword:
            self.add2pos('_ss')

        else:

            self.tword = s
            if tword[0] == '<':
                self.tlemma = '_' + lemma
                altlemma = lemma + '_'
            else:
                self.tlemma = lemma + '_'
                altlemma = '_' + lemma

            idx2 = idx - 30
            self.auth2work[self.auth][self.work][self.line + idx2][1] = altlemma
            self.add2pos(pos)
        return 1

    def sum2pos(self, word, tpos):
        if word.count('<') > 1:
            p(f'{word} has two <')
            return
        elif word.count('(') > 1:
            p(f'{word} has two (')
            return
        else:
            be = self.get_be(word)
            self.sum_word = be
            pos = self.sum2pos_dct.get(be)
            if not pos:
                p(f'failure: {be}')
                return
            if len(pos) > 1:
                if be == 'esto':
                    return pos[0]
                elif 'im' in tpos:
                    return pos[1]
                elif 'sj' in tpos:
                    return pos[1]
                else:
                    return pos[0]
            else:
                return pos[0]

    def sum2pos2(self, word):
        oword = word
        word2 = self.get_be(word)
        if word2 in self.sum2pos_dct:
            self.sum_word = word2
            return 1
        mark = ['(', ')'] if "(" in word else ["<", ">"]
        if word[0] != mark[0]:
            word = word.replace(mark[1], '')
            word = word.replace(' ' + mark[0], mark[1] + ' ')
            word = mark[0] + word
        else:
            word = word.replace(mark[0], '')
            word = word.replace(mark[1] + ' ', " " + mark[0])
            word = word + mark[1]

        try:
            word2 = self.get_be(word)
        except:
            return 0
        if word2 in self.sum2pos_dct:
            self.sum_word = word2
            self.backwards_sum = 1

            # p(f'success {oword}')
            return 1

    def anticipate_sum_elision(self):
        '''
        this is for those verbs or words whose ending
        est is attached onto, the controversial decision
        was made to not bother with the post of 'est'

        '''

        if self.tword.endswith('st') or \
                self.tword.endswith("'s"):
            try:
                nlemma = self.infos[self.line + 1][1]
                nlemma = self.parse_lemma(nlemma)
                nword = self.infos[self.line + 1][2]
                nword = re.sub(r'[0-9]', '', nword)
                if nlemma == '_sum' and nword == self.tword:
                    if self.tword.endswith("st"):
                        self.tword = self.tword[:-2] + '|st'
                        self.sum_word = 'est'
                    else:
                        self.tword = self.tword[:-2] + '|s'
                        self.sum_word = 'es'

                    self.delay_sum = 1
                    self.elsum = 1
                    self.infos[self.line + 1][0] = '*'
                    self.infos[self.line + 1][1] = '_sum2'
                    return 1
            except:
                pass

    def anticipate_sum(self, pos):
        start = vgf.beg_list(self.infos, self.line - 30)
        stop = vgf.end_list(self.infos, self.line + 30)
        tword2 = self.lasla_match(self.tword)
        found = 0
        if self.backwards_sum:
            bb = 8

        for i in range(self.line - 1, start, -1):
            try:
                oword = self.infos[i][2]
                word = self.lasla_match(oword)
                if word == tword2:
                    if self.sum_word == 'iri':
                        self.infos[i][1] = 'eo2'
                    else:
                        self.infos[i][1] = 'sum2'
                    self.infos[i][4] = pos
                    self.infos[i][2] = self.sum_word
                    self.infos[i][0] = "*"
                    found = 1
                    break
            except:
                pass

        if not found:
            for i in range(self.line + 1, stop):
                try:
                    oword = self.infos[i][2]
                    word = self.lasla_match(oword)
                    if word == tword2:
                        if self.sum_word == 'iri':
                            self.infos[i][1] = 'eo2'
                        else:
                            self.infos[i][1] = 'sum2'
                        self.infos[i][4] = pos
                        self.infos[i][2] = self.sum_word
                        self.infos[i][0] = "*"
                        found = 1
                        break
                except:
                    pass

        if not found:
            if "(" in self.word:
                self.errors['paren'].append([self.word])
            else:
                pass
                '''
                if there is no sum counterpart then that is because two participles share a single auxiliary such as
                imploratus adoptione et accitus es
                '''
                # self.errors['sum_counter'].append([self.work, self.line, self.infos[start:stop]])
                # p(f'no sum counterpart for {self.tword}')
        else:
            if not self.backwards_sum:
                pass
                self.tword = re.sub(r'<.*>', '', self.tword).strip()
            else:
                s = vgf.inside(self.tword, '<', '>')
                if not s:
                    self.add2errors('inside', self.tword)
                else:
                    pass
                    self.tword = s

        return

    def sum2pos3(self, tpos):
        pos = self.sum2pos_dct.get(self.sum_word)
        if not pos:
            p(f'failure: {self.sum_word}')
            return
        if len(pos) > 1:
            if self.sum_word == 'esto':
                return pos[0]
            elif 'im' in tpos:
                return pos[1]
            elif 'sj' in tpos:
                return pos[1]
            else:
                return pos[0]
        else:
            return pos[0]

    def get_be(self, word):
        if word.count('<') > 1:
            s = get_between_sline(word)
            return self.get_be2(s, word)

        else:
            mark = ['(', ')'] if "(" in word else ["<", ">"]
            s = word[word.index(mark[0]) + 1:word.index(mark[1])]
            if ' ' in s:
                return self.get_be2(s, word)
            else:
                return s

    def get_be2(self, s, word):
        lst = s.split()
        t = set(x for x in lst if x in self.sum2pos_dct)
        if not len(t) == 1:
            self.add2errors('no_be', word)
        else:
            return list(t)[0]

    def find_missing(self):
        if self.kind == 'set':
            self.all_lems = set(x[0] for x in self.all_lines)
            self.lem2info = defaultdict(list)
            for x in self.new_lines:
                self.lem2info[x[1]].append([x[0], x[2]])

        missing_pdct = defaultdict(list)
        b = 0
        for x in self.have_not.values():
            p(f'{b} of {len(self.have_not)}')
            b += 1
            num = self.final_pos_rv[x]
            for lem in self.all_lems:
                itms = self.lem2forms.get(lem)
                if itms:
                    for itm in itms:
                        lst = itm.get(num)
                        if lst:
                            lst1 = lst[0]
                            lst1 = [norm_str_jv(t) for t in lst1]
                            for word in lst1:
                                obj = self.word2pos.get(word)
                                if obj:
                                    for pair in obj:
                                        missing_pdct[x].append([word] + pair)

        not_attested = set(self.have_not.values()) - set(missing_pdct.keys())
        nota = {}
        for x in not_attested:
            num = self.final_pos_rv[x]
            nota[num] = x
        nota = sort_dct_key(nota)

        return

    def nouns(self, info, ignore=0):
        num2 = info[4][1:]
        try:
            decl = num2[0]
        except:
            decl = '0'



        if not ignore:
            self.add_lem2decl(self.tlemma, ('n', decl))
        try:
            number = 's' if num2[2] == '1' else 'p'
        except:
            number = 'N'
        try:
            case = self.num2case[num2[1]]
        except:
            case = 'A'

        if case == 'i':
            self.add2pos('inv')
        else:
            self.add2pos(number + case)





    def verb_dcts(self):
        self.num2tense = {
            '0': '&',
            '1': 'pr',
            '2': 'ip',
            '3': 'fu',
            '4': 'pf',
            '5': 'pp',
            '6': 'fp',
            '7': 'xp',
            '8': 'xq',
            '9': 'xf',
        }
        self.num2mood = {
            '0': '*',
            '1': 'in',
            '2': 'im',
            '3': 'sj',
            '4': 'pr',
            '5': 'gv',
            '6': 'gd',
            '7': 'if',
            '8': 'su',
            '9': 'sup',
        }
        self.num2gen = {
            '0': ')',
            '1': 'C',
            '2': 'f',
            '3': 'B',
            '4': 'm',
            '5': 'X',
            '6': 'n',
            ' ': ' '
        }

        self.num2gen2 = {
            '0': ' ',
            '1': 'm',
            '2': 'f',
            '3': 'm',
            '4': 'm',
            '5': 'm',
            '6': 'n',
            ' ': 'm'
        }


        self.num2case = {
            '1': 'n',
            '2': 'v',
            '3': 'a',
            '4': 'g',
            '5': 'd',
            '6': 'b',
            '7': 'l',
            '8': 'i',
            ' ': ' '
        }

    def verb_dcts2(self):
        self.num2tense2 = {
            '0': '',
            '1': 'present',
            '2': 'imperfect',
            '3': 'future',
            '4': 'perfect',
            '5': 'past perfect',
            '6': 'future perfect',
            '7': 'periphrastic 1',
            '8': 'periphrastic 2',
            '9': 'periphrastic 3',
        }
        self.num2mood2 = {
            '0': '',
            '1': 'indicative',
            '2': 'imperative',
            '3': 'subjunctive',
            '4': 'participle',
            '5': 'gerundive',
            '6': 'gerund',
            '7': 'infinitive',
            '8': 'supine_n',
            '9': 'supine_m',
        }

        self.num2case2 = {
            '1': 'nominative',
            '2': 'vocative',
            '3': 'accusative',
            '4': 'genitive',
            '5': 'dative',
            '6': 'ablative',
            '7': 'locative',
            '8': 'indeclinable',
            ' ': ' '
        }

        self.num2gen2a = {
            '0': '',
            '1': 'common',
            '2': 'feminine',
            '3': 'masc_fem',
            '4': 'masculine',
            '5': 'masc_neuter',
            '6': 'neuter',
            ' ': 'unknown'
        }

    def add_lem2decl(self, k, v):

        if type(v) == int:
            bb = 8
        elif v[1] == ' ':
            v = (v[0], '0')

        if k not in self.lemma2decl:
            self.lemma2decl[k] = defaultdict(int)
        self.lemma2decl[k][v] += 1

    def sum_conditions(self):
        if self.sum_paren:
            return 1
        if reg(r'[<\(]', self.tword) and self.sum2pos2(self.tword):
            return 1
        if self.tlemma in ['_sum2', '_eo2']:
            return 1
        if self.anticipate_sum_elision():
            return 1

    def verbs(self, info):
        num2 = info[4]
        self.sum_word = ''
        gender = 'G'
        para = 0
        person = 'P'
        case = 'A'
        mood = 'M'
        voice = 'V'
        tense = 'T'
        number = 'N'
        for e, x in en(num2[1:]):
            self.verbs_forms[e].add(x)
            if e == 0:
                decl = x
            elif e == 1:
                if not hl(x):
                    pass
                else:
                    case = self.num2case[x]
            elif e == 2:
                number = 's' if x == '1' else 'p'

            elif e == 3:
                pass
            elif e == 4:
                mood = self.num2mood[x]

            elif e == 5:
                if x in ['7', '8', '9']:
                    para = 1
                tense = self.num2tense[x]
            elif e == 6:
                if x in ['1', '3', '4']:
                    voice = 'ac'
                elif x == '2':
                    voice = 'pa'
            elif e == 7:
                if not hl(x):
                    person = '0'
                else:
                    person = int(x)
                    if number == 'p':
                        person += 3

                    person = str(person)
            elif e == 11:
                gender = self.num2gen[x]

        self.add_lem2decl(self.tlemma, ('v', decl))

        if self.sum_conditions():
            total = ''
            if self.sum_word == 'esse':
                total = 'if.pr.ac'
            elif self.sum_word == 'fuisse':
                total = 'if.pf.ac'
            if self.sum_word == 'iri':
                total = 'if.fu.pa'
                self.anticipate_sum(total)
                self.add2pos('sup')

            elif mood == 'if' or self.sum_word in ['esse', 'fuisse']:

                if tense == 'xf':
                    total2 = f'fu.{voice}.{number}{gender}{case}'
                elif tense == 'xq':
                    total2 = f'pf.pa.{number}{gender}{case}'
                else:
                    total2 = f'{tense}.{voice}.{number}{gender}{case}'
                if not self.elsum and not self.sum_paren:
                    self.anticipate_sum(total)
                self.add2pos(total2)
            else:
                tpos = f'{person}.{tense}.{mood}.{voice}'
                tpos2 = f'{person}.{mood}.{voice}'
                if not self.sum_paren:
                    if not total:
                        total = self.sum2pos3(tpos)
                    totala = f'{total[0]}{total[4:]}'
                    if tpos2 != totala:
                        self.sum_errors[tpos].append([tpos, self.sum_word, total])

                if tense in ['xq', 'xp']:
                    total2 = f'pf.pa.{number}{gender}{case}'
                else:
                    total2 = f'pf.pa.{number}{gender}{case}'
                if not self.elsum and not self.sum_paren:
                    self.anticipate_sum(total)
                self.add2pos(total2)

        elif mood == 'su':
            self.add2pos('su')
        elif mood == 'sup':
            self.add2pos('sup')


        elif para:
            if tense == 'xf':
                tense = 'fu'
            total = f'{person}.{tense}.{mood}.{voice}'
            self.add2pos(total)

        elif mood == 'gd':
            self.add2pos('gd.' + case)

        elif mood == 'if':
            self.add2pos(f'{mood}.{tense}.{voice}')

        elif mood == 'gv':
            total = f'gv.{number}{gender}{case}'
            self.add2pos(total)

        elif mood not in ['pr', 'gv']:
            total = f'{person}.{tense}.{mood}.{voice}'
            self.add2pos(total)

        else:

            if mood == 'pr' and tense == 'fu':
                mood = 'fu'
            elif mood == 'pr' and voice == 'pa':
                mood = 'pf'
            if not case:
                num3 = num2[:8] + '   ' + num2[11]
                self.no_case[num3].append(info)

            total = f'{mood}.{voice}.{number}{gender}{case}'
            self.add2pos(total)

    def uverbs(self, num2, dct):
        for e, x in en(num2[1:]):
            dct[e].add(x)

    def adj(self, info, ignore=0):
        num2 = info[4]
        gender = 'G'
        degree = 'D'
        number = 'N'
        decl = 'E'
        case = 'A'
        for e, x in en(num2[1:]):
            self.adj_forms[e].add(x)
            if e == 0:
                decl = x
            elif e == 1:
                case = self.num2case[x]
            elif e == 2:
                number = 'p' if x == '2' else 's'
            elif e == 3:
                if x == '1':
                    degree = 'p'
                elif x == '2':
                    degree = 'c'
                elif x == '3':
                    degree = 's'
            elif e == 11:
                gender = self.num2gen[x]

                if x == '0':
                    self.add2errors('zero', self.tword)

        if gender == 'C':
            bb=8

        if case == 'i':
            self.add2pos('inv')

        elif degree in ['c', 's']:
            total = number + gender + case + degree


            self.add2pos(total)
        else:
            total = number + gender + case
            if self.tlemma == 'nemo':
                total = total.replace(' ','')

            self.add2pos(total)
        if not ignore:
            self.add_lem2decl(self.tlemma, ('a', decl))

    def adv(self, info):
        if not self.kind == 'set':
            num2 = info[4]
        else:
            num2 = info[2]

        try:
            num = num2[1]
        except:
            num = '0'

        self.add_lem2decl(self.tlemma, ('d', num))

        dct = {
            '1': 'd',
            '2': 'ac',
            '3': 'as'
        }
        self.add2pos(dct[num2[4]])

    def other(self, info):
        if not self.kind == 'set':
            num2 = info[4]
        else:
            num2 = info[2]

        try:
            num = num2[1]
        except:
            num = '0'

        self.add_lem2decl(self.tlemma, (num2[0], num))

        if num2[0] in ['E', 'G']:
            self.nouns(info, 1)

        elif num2[0] in ['F', 'I', 'J', 'L', 'K', 'H',
                         ]:
            self.adj(info, 1)

        elif num2[0] in ['O', 'R', 'N', 'E', 'U', 'P', 'Q', 'T', 'S']:
            self.owords[num2[0]].add(self.tword)
            self.add2pos('d')

        else:
            self.add2pos('m')

    def review(self):
        self.auth2work = pi.open_pickle(f'{fold}lasla_db2', 1)
        self.auth2work_db = pi.open_pickle(f'{fold}lasla_db', 1)
        self.errors = pi.open_pickle(f'{fold}lasla_errors', 1)
        self.anomalies = pi.open_pickle(f'{fold}lasla_anomalies', 1)
        self.bogus_pos = pi.open_pickle(f'{fold}bogus_pos', 1)
        self.final_pos = pi.open_pickle(f'{fold}final_pos', 1)
        self.final_pos_rv = {v: k for k, v in self.final_pos.items()}

    def temp23(self):
        s = 'BellumGallicum_CaesBG1'
        lst = []
        for e, x in en(self.auth2work['Caesar'][s]):
            if x[0] != '!':
                lst.append(x[2])
            if e > 100:
                break
        to.from_lst2txt(lst, f'{fold}temp_ceasar')
        vgf.open_txt_file(f'{fold}temp_ceasar')

    def review_errors2(self):
        b = 0
        for self.auth, works in self.auth2work.items():
            for self.work, self.infos in works.items():
                b += 1
                p(b)
                for self.line, info in en(self.infos):
                    word = info[2]
                    lem = info[1]
                    pos = info[4]
                    cat = info[0]
                    if cat != '!' and pos not in ['m']:
                        if not lem:
                            self.add2errors('no_lem', word)
                        elif lem in ['#', '0']:
                            pass
                        elif lem[0] == '_' or lem[-1] == '_':
                            pass
                        elif reg(r'[^a-z]', lem[:-1]):
                            self.add2errors('blem', info[2])
                        elif len(info) != 5:
                            self.add2errors('blen', info[2])
                        elif "$" in word:
                            self.add2errors('bad_greek', info[2])
                        elif pos not in self.final_pos_rv \
                                and not '_' in pos:
                            self.add2errors('bpos', pos)
        return

    def normal_words(self):
        b = 0
        for self.auth, works in self.auth2work.items():
            for self.work, self.infos in works.items():
                b += 1
                p(b)
                for self.line, info in en(self.infos):
                    info[2] = re.sub(r'<.*>', '', info[2]).strip()
                    if '|st' in info[2]:
                        info[2] = info[2][:-3]
                    elif '|s' in info[2]:
                        info[2] = info[2][:-2]

                    if info[1] in ['_sum2', '_eo2']:
                        info[1] = info[1][1:]

    def review_errors(self):
        '''


        '''

        lst1 = []
        kind = 0

        if self.kind not in ['small','debug']:
            if kind:
                self.auth2work_db = pi.open_pickle(f'{fold}lasla_db2', 1)
            else:
                self.auth2work_db = self.auth2work

        errors2 = defaultdict(list)
        errors3 = defaultdict(list)
        words = {}
        for x, l in self.errors.items():

            for e, y in en(l):
                # if e > 100:
                #     break

                infos = self.auth2work_db[y[1]][y[2]]
                infos2 = self.auth2work[y[1]][y[2]]
                lst = vgf.cut_list(infos, y[3], -10)
                lst4 = vgf.cut_list(infos2, y[3], -10)
                yu = copy.deepcopy(y)
                y.append(lst)
                yu.append(lst4)
                errors2[x].append(y)
                errors3[x].append(yu)
                words[y[0]] = lst4

        # lst2 = []
        # errors3 = defaultdict(list)
        #
        # for x, l in self.errors.items():
        #     for e, y in en(l):
        #         infos = self.auth2work[y[1]][y[2]]
        #         lst = vgf.cut_list(infos, y[3], -10)
        #         lst2.append([(y[0], lst)])
        return


class fix_ill_formed_words:
    def __init__(self):
        pass

    def begin_fiw(self):
        pass

    def research_bad_words(self):
        bad_words = []
        bad_words = []
        paren = []
        spaces = set()
        abb = {}
        aux = set()
        bad_period = []
        for x, y in self.lafreq.items():
            word = x[1]
            lemma = x[0]
            if reg(r'[\(\<]', word):
                try:
                    if self.sum2pos2(word):
                        aux.add(word)
                        pass
                    else:
                        paren.append(x)
                except:
                    paren.append(x)

            elif ' ' in word:
                spaces.add(x)

            elif ('9' in lemma or '8' in lemma) and word.count('.') == 1 and \
                    word[-1] == '.':
                pass
            elif word.count('.') == 1 and \
                    word[-1] == '.':
                abb[x] = y
            elif '.' in word:
                bad_period.append(word)
            elif reg(r'[^A-Za-z]', word):
                bad_words.append(x)

        lst = [aux, paren, spaces, abb, bad_period, bad_words]
        pi.save_pickle(lst, f'{fold}ill_formed_words', 1)
        pi.save_pickle(self.bogus_pos, f'{fold}bogus_pos', 1)

        return


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


if eval(not_execute_on_import):
    if vgf.pycharm():
        args = [0, 'c', '', 'IX', '', 0, 0]
    else:
        args = vgf.get_arguments()

    if args[1] == 'c':
        ins = convert2txt()
        ins.kind = ''
        ins.begin_ct()
    elif args[1] == 'r':
        ins = convert2txt()
        ins.begin3()
    else:
        p ('wrong argument')
