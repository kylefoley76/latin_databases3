from collections import defaultdict, deque
from bglobals import *
from other.filter_txt import clean_str


"""
each instance of | and \ and  should be removed before editing
the text

\ indicates that the line should be parsed into a question

text to the left of | is question to the right is answer

if no | is present, then comma is delimiter

if | and , not present then error

if || is present then these are just notes and should just
be reread

if // in line then q and a are reversed

{ } are meant to delimit several lines or pick out a small part
of a single line

chapter are delineated by starting with __



"""


class fact_entries:
    def __init__(self):
        self.known = 0
        self.imp = 0
        self.num = 0
        self.qu = []
        self.ans = []


class vocabulary:
    def __init__(self):
        pass

    def begin(self):
        self.get_atts()
        self.main()
        self.attach_defs()
        self.output()

    def main(self):
        b = 0
        words = []
        for x, y in zip(self.s[:-1], self.s[1:]):
            if x == '/' and y == '/' and b > 400:
                for t in range(b, b - 30, -1):
                    w = self.s[t]

                    if w == ' ':
                        word = self.s[t + 1:b]
                        break

                word = word.lower()
                _, word, _ = elim_punctuation(word, 1)
                str1 = f"{self.s[b - 75:t + 1]}<{self.s[t + 1:b]}>{self.s[b:b + 150]}"
                str1 = str1.replace('//', '')
                words.append([word, str1])
            b += 1
        self.words = words
        return

    def attach_defs(self):
        self.word2def = []
        for lst in self.words:
            w = lst[0]
            sent = lst[1]
            wu = norm_str_jv(w)
            self.wu = wu
            obj = self.macronizer.get(wu)
            if obj:
                for x, y in obj.items():
                    if x == w:
                        lems = {x: y}
                        break
                else:
                    lems = obj
                defn = self.print_defs2(lems)
                self.word2def.append([w, sent, defn])

            else:
                p(f'{wu} not found')
        return

    def print_defs2(self, lems):
        defs = []
        for word, dct in lems.items():
            for lem, posl in dct.items():
                lemu = norm_str_jv(lem)
                itm = self.excel_wnum.get(lemu)
                if itm:
                    defn = get_def(itm, 1)
                    defs.append([lem, " ".join(posl), defn])
                else:
                    p(f'no excel object for {self.wu}')
        return defs

    def output(self):
        lst = []
        for l in self.word2def:
            w = l[0]
            lst1 = [w, l[2][0][0], l[1]]
            lst1 += [l[2][0][1], l[2][0][2]]
            lst.append(lst1)

            if len(l[2]) > 1:
                for x in l[2][1:]:
                    if x:
                        lst.append([w, x[0], '', x[1], x[2]])
        p('putting into excel')
        ef.from_lst2book(lst, f'{lfold}grammar/grammar_words')
        ef.open_wb('grammar_words.xlsx', f'{lfold}grammar/')
        return

    def get_atts(self):
        file = f'{lfold}grammar/grammar'
        lst = to.from_txt2lst(file, 1)
        self.excel_wnum = pi.open_pickle(f'{fold}from_excel_wnum', 1)
        self.macronizer = pi.open_pickle(f'{fold}macronizer', 1)

        self.s = ''
        for x in lst: self.s += f' {x}'
        self.s = self.s.replace('\t', ' ')
        self.s = self.s.replace('\n', ' ')

        return


class facts:
    def __init__(self):
        pass

    def new_system(self):
        file = f'{lfold}grammar/latin_grammar3'
        self.lst = to.from_txt2lst(file, 1)
        start = 0
        lst2 = ['lll', 'nnn', 'ddd', 'list_', 'ooo', '|', 'ppp', 'ttt',
                'defn_', 'dbdb', 'aaa']
        self.cat = lst2
        self.lst = [x.replace('\f', '\n') for x in self.lst]
        found = 1
        state = ''
        lstate = ''
        ## r b
        ## r e b
        ## NO r r  or b e
        b = 0
        c = 0
        started = 0
        tlst = []
        lst1 = []
        kind = ""
        for g, x in en(self.lst):
            x = x.replace('\t', ' ')
            x = x.strip()
            state2 = ''

            if 'As impersonals,' in x:
                bb = 8

            if g == 3351:
                bb = 8

            if '__start' in x or '__on' in x:
                start = 1
                if x == '__start':
                    lstate = 'b'
                found = 0

                if started:
                    lst1.append([kind, tlst])
                tlst = []

                started = 1
            elif '__off' in x:
                start = 0
                found = 1
                lstate = 'list_'
                kind = 'list_'


            elif '__stop' in x:
                break

            if not start and started:
                if not x == '__off':
                    tlst.append(['', x])

            elif start:
                if not x or x.startswith('__'):
                    state = 'b'
                    if not found and lstate in ['r', 'e']:
                        # p (last_x)
                        self.lst[g] = 'rrr ' + self.lst[g]
                        p('')
                        b += 1
                    if found:
                        lst1.append([kind, tlst])
                        tlst = []
                    found = 0

                else:
                    if '2. Numerals, Comparatives' in x:
                        bb = 8
                    if x[0].isdigit():
                        state = 'r'
                        for e, y in en(x):
                            if not y.isdigit():
                                break
                        num = x[:e]
                        if int(num) < 10:
                            if lstate == 'b':
                                p(x)
                                p('')
                            state = 'e'
                    else:
                        if lstate in ['r', 'e']:
                            p(x)
                            p('')
                        state = 'r'

                    if state == 'r' and "|" in x:
                        found = 1
                        c += 1
                        tlst.append(['r', x])
                        kind = 'q'

                    elif not found and state in ['r', 'e']:
                        found = 0
                        states = 0
                        for z in lst2:
                            if z in x:
                                found = 1
                                kind = z
                                tlst.append([state, x])
                                break
                                # states += 1
                                # if states > 1:
                                #     p (x)
                        else:
                            tlst.append(['e', x])
                    else:
                        tlst.append(['e', x])

                lstate = state
                last_x = x

        self.lst1 = [x for x in lst1 if x[0] != 'ddd']
        self.new_systems2()
        to.from_lst2txt(self.lst, f'{lfold}grammar/latin_grammar4')
        vgf.open_txt_file(f'{lfold}grammar/latin_grammar4')
        return

    def new_systems2(self):
        lst2 = []
        b = 0
        num = 1
        for x in self.lst1:
            deci = 0
            typ = ""
            if 'list_' in x[0]:
                typ = 'i'

            for f, z in en(x[1]):
                lst3 = [z[1], '']

                if 'uses of the accusative' in z[1]:
                    bb = 8

                if not typ:
                    typ = ''
                typ2 = ''
                if z[0] == 'e' and f == 0:
                    if '|' in z[1]:
                        lst3 = z[1].split('|')

                elif z[0] == 'e' and f > 0 and not typ == 'i':
                    typ2 = 'e'
                    z[1] = z[1].strip()
                    if not z[1][0].isdigit():
                        p(z[1])
                        p('')
                        b += 1
                    lst3 = [z[1], '']
                else:
                    if '|' in z[1]:
                        lst3 = z[1].split('|')

                if not z[0]:
                    typ = x[0]
                elif 'dbdb' in x[0][0]:
                    typ = 'b'
                elif not typ:
                    typ = x[0]

                if 'dbdb' in typ:
                    typ = 'b'
                elif typ == 'list_':
                    typ = 'i'
                else:
                    typ = typ[0]

                num2 = float(f'{num}.{deci}')
                deci += 1
                if not typ and not typ2 == 'e':
                    bb = 8

                lst2.append([num2, typ, typ2, lst3[0], lst3[1]])
            num += 1
        ef.from_lst2book(lst2, f'{lfold}grammar/rules_db')

        return

    def main(self, file):
        self.file = file
        self.first = 1
        file2 = f'{fold}{file}'
        self.lst = to.from_txt2lst(file2, 1)
        if self.first:
            self.get_from_excel()
        self.check_eq_brak()
        self.get_from_brack()
        self.get_from_bar()
        self.comma_check()
        self.split_questions()
        if self.first:
            self.add_old_info()
        self.level()
        self.print2excel()

    def get_from_excel(self):
        file3 = f'{fold}{self.file}_test.xlsx'
        p('loading excel')
        wb = ef.load_workbook_write(file3)
        sh = ef.get_sheet(wb, 'Sheet1')
        sh2 = ef.get_sheet(wb, 'Sheet2')
        lst = ef.from_sheet_tpl0(sh, 2)
        if self.first:
            ef.from_lst2sheet(sh2, lst)
            p('moving sheet1 to sheet2')
        self.wb = wb
        self.sh = sh
        self.sh2 = sh2
        equest = {}
        lnum = 0
        for x in lst[2:]:
            known = x[1]
            imp = x[2]
            num = x[3]
            qu = x[4]
            if qu == None:
                qu = ""
            ans = x[5]
            if ans == None:
                ans = ''

            if num != lnum:
                ins = fact_entries()
                ins.known = known
                ins.imp = imp
                if lnum != 0:
                    equest[lnum] = lins
                ins.qu.append(qu)
                ins.ans.append(ans)
                lins = ins
            else:

                ins.qu.append(qu)
                ins.ans.append(ans)
            lnum = num

        equest[num] = ins
        self.equest = {}
        for k, v in equest.items():
            str1 = "".join(v.qu)
            str1 = clean_str(str1)
            self.equest[str1] = v

        return

    def get_from_brack(self):
        str1 = ""
        on = 0
        self.questions = []

        for e, x in en(self.lst):
            for z in x:
                if z == '}':
                    on = 0
                    self.questions.append([start, str1])
                    str1 = ""
                elif on:
                    str1 += z
                elif z == "{":
                    on = 1
                    start = e
                    if start == 9468:
                        bb = 8
            if on:
                str1 += " "
        return

    def get_from_bar(self):
        for e, x in en(self.lst):
            if ("\\" in x or '|' in x) and "{" not in x and "}" not in x:
                if '\\' in x:
                    x = x.replace('\\', '')
                self.questions.append([e, x])

    def comma_check(self):
        error = 0
        for x in self.questions:
            quest = x[1]
            if "||" in quest:
                pass
            elif "|" not in quest:
                if quest.count(',') != 1:
                    p(f'wrong comma in {quest}')
                    error = 1

        if error:
            sys.exit()

    def check_eq_brak(self):
        b = 0
        error = 0
        for x in self.lst:
            for z in x:
                if z == '{':
                    b += 1
                elif z == "}":
                    b -= 1
                if b > 1 or b < 0:
                    p(f'no bracket in {z}')
                    b = 0
                    error = 1
        if error:
            sys.exit()

    def split_questions(self):
        self.questions = sort_by_col(self.questions, 0)
        lst = []
        self.notes = []
        for x in self.questions:
            quest = x[1]
            loc = x[0]
            if "||" in quest:
                self.notes.append(x)
            else:
                if '|' in quest:
                    let = "|"
                else:
                    let = ','
                lst1 = vgf.strip_n_split(quest, let)
                lst2 = [loc] + lst1
                lst.append(lst2)

        self.questions = lst

    def add_old_info(self):
        self.new_quest = []
        self.old_quest = []
        for v in self.questions:
            loc = v[0]
            qu = v[1]
            j = clean_str(qu)
            obj = self.equest.get(j)
            if obj:
                for x, y in zip(obj.qu, obj.ans):
                    lst1 = [obj.known, obj.imp, loc, x, y]
                    self.old_quest.append(lst1)
            else:
                self.new_quest.append(v)

    def level(self):
        lst1 = []
        if not self.first:
            self.new_quest = self.questions

        for e, x in en(self.new_quest):
            q = x[1]
            a = x[2]
            e = x[0]
            ql = vgf.limit_str_70(q, 60, 4, 0)
            al = vgf.limit_str_70(a, 60, 4, 0)
            lst1.append([e, ql, al])

        for x in lst1:
            b = len(x[1])
            c = len(x[2])
            d = b - c
            if d < 0:
                d *= -1
                f = [''] * d
                x[1] += f
            else:
                f = [''] * d
                x[2] += f
        lst3 = []
        for x in lst1:
            e = x[0]
            for y, z in zip(x[1], x[2]):
                lst3.append([None, None, e, y, z])
        if self.first:
            lst3 += self.old_quest
            lst3 = sort_by_col(lst3, 2)

        self.final = lst3

    def print2excel(self):
        file3 = f'{fold}{self.file}_test.xlsx'
        if not self.first:
            wb = ef.load_workbook_write(file3)
            sh = ef.get_sheet(wb, 'Sheet1')
            sh1 = ef.get_sheet(wb, 'Sheet2')

        self.final = [[None] + x for x in self.final]
        self.final.insert(0, [None, 'know', 'imp'])
        self.final.insert(0, [None, None])
        ef.from_lst2sheet(self.sh, self.final)
        p('now saving')
        self.wb.save(file3)
        ef.open_wb(f'{self.file}_test.xlsx', fold)


def temp17():
    lst = to.from_txt2lst(f'{dwn_dir}temp4', 1)
    beg = 0
    lst1 = []
    lst2 = []
    for x in lst:
        x = x.replace('”', '')
        x = x.replace('“', '')
        x = x.replace("'", '')

        idx1 = x.index('<')
        found2 = 0
        i = idx1
        while i > 0:
            b = x[i]
            if b.isdigit():
                beg = i + 1
                found2 = 1
                break
            i -= 1
        x1 = ''
        if not found2:
            p(f'no beginning for {x}')
            p('')
        else:
            x1 = x[beg:]
        if found2:
            pass

            if x1[0] == '.':
                x1 = x1[1:]
                x1 = x1.strip()

            lat = ""
            if "(" not in x1:
                p(f'no left bra in {x1}')
                p('')
                p('')
            else:
                lat = x1[:x1.index("(")]
            lat = lat.replace(';', '')
            eng = ""
            if ")" not in x1:
                p(f'no right bra in {x1}')
                p('')
            else:
                eng = x1[x1.index(")") + 1:]
                if ',' in eng[:2]:
                    eng = eng[2:]
            found = 0
            for e, y in en(eng):
                if y.isdigit() or y == '|':
                    eng = eng[:e - 1].strip()
                    found = 1
                    break

            lst2.append([lat, eng])

    ef.from_lst2book(lst2, f'{dwn_dir}temp5')
    to.from_lst2txt(lst1, f'{dwn_dir}temp20e')
    # to.from_lst2txt(lst2,f'{dwn_dir}temp20l')

    return


class grammar_index:
    def __init__(self):
        pass

    def begin(self):
        self.get_atts()
        self.step1()

    def get_atts(self):
        self.lsts = ef.from_book2lst(f'{lfold}grammar/rules_db')

    def step1(self):
        self.dct = defaultdict(set)
        e = 0
        for rw in self.lsts[0]:
            if e == 2096:
                bb = 8
            num = rw[3]
            qu = rw[8]
            ans = rw[9]
            if ans and 'adverbial; <tantum>' in ans:
                bb = 8

            for x in [qu, ans]:
                if x and '<' in x:
                    su = get_between_sline(x, '<', 1)
                    # su = unidecode(s)
                    su = su.lower()
                    su = re.sub(r'[^a-zāēīōūȳăĕĭŏŭў\s\.,]', '', su)
                    slst = vgf.strip_n_split(su, ',')
                    for z in slst:
                        if hl(z):
                            self.dct[z].add(int(num))
            e += 1
        lst2 = []
        for x, y in self.dct.items():
            y = list(y)
            y.sort()
            y = [str(z) for z in y]
            lst2.append([x, ' '.join(y)])
        ef.from_lst2book(lst2, f'{lfold}grammar/particles')
        ef.open_wb(f'{lfold}grammar/particles.xlsx')

        return


class quant_comp:
    def __init__(self):
        pass

    def begin(self, file):
        self.file = f"{lfold}books/{file} lat"
        self.get_atts()
        self.main()

    def get_atts(self):
        self.lst = to.from_txt2lst(self.file, 1)

    def main(self):
        self.words = deque([])
        self.words500 = deque([])
        on = 0
        i = 0
        for x in self.lst:
            y = x.split()
            for word in y:
                i += 1
                if not ha(word):
                    pass
                elif word == '__test_on' or word == 'bbb':
                    self.words = deque([])
                    on = 1
                    i = 0
                elif word == '__test_off' or word == 'eee':
                    on = 0

                elif on:
                    val = 1 if '/' not in word else 0

                    self.words.append(val)
                    self.words500.append(val)

                    if len(self.words500) >= 200:
                        self.words500.popleft()
                    # if i and i % 100 == 0:
                    #     p(int((sum(self.words500) / len(self.words500)) * 100))

        tot = int((sum(self.words) / len(self.words)) * 100)
        p(tot)
        return


if eval(not_execute_on_import):
    if vgf.pycharm():
        args = [0, 'gi', '', 'IX', '', 0, 0]
    else:
        args = vgf.get_arguments()

    if args[1] == 'fa':
        ins = facts()
        ins.main('latin grammar2')
    elif args[1] == 'vo':
        ins = vocabulary()
        ins.begin()
    elif args[1] == 'ns':
        ins = facts()
        ins.new_system()
    elif args[1] == 'gi':
        ins = grammar_index()
        ins.begin()
    elif args[1] == 'qc':
        ins = quant_comp()
        # ins.begin('nepos militiades lat')
        # ins.begin('augustino, confessiones lat')
        # ins.begin('tacitus')
        ins.begin(args[2])
    else:
        p('wrong argument')
