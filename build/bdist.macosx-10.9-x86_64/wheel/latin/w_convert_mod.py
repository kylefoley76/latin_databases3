from copy import deepcopy
import unicodedata
from bglobals import *



def normalize_unicode(lines):
    """ Transform lines into diacritics bytes free unicode
    """
    return unicodedata.normalize('NFKD', lines).encode('ASCII', 'ignore').decode()


#############################################################
# Convert morphos.la
# Each line of Morphos.la represents a declension name
#############################################################
search = re.compile(r'[^-]')
morphos = {}
test = 0

with open(f"{fold}morphos.txt") as f:
    for line in f.readlines():
        line = line.strip()
        if line.startswith("!") or len(line) < 2 or ":" not in line:
            pass
        else:
            # Person
            # If we have a person, we know it's a verb
            line = line \
                .replace("1ère", "v1-------") \
                .replace("2ème", "v2-------") \
                .replace("3ème", "v3-------")

            # Number
            line = line \
                .replace("singulier", "--s------") \
                .replace("pluriel", "--p------")

            # Tense
            line = line \
                .replace("présent", "---p-----") \
                .replace("imparfait", "---i-----") \
                .replace("parfait", "---r-----") \
                .replace("PQP", "---l-----") \
                .replace("futur antérieur", "---t-----") \
                .replace("futur", "---f-----")

            # Mood
            line = line \
                .replace("indicatif", "----i----") \
                .replace("subjonctif", "----s----") \
                .replace("infinitif", "v---n----") \
                .replace("impératif", "----m----") \
                .replace("gérondif", "----g----") \
                .replace("adjectif verbal", "----g----") \
                .replace("participe", "g---p----") \
                .replace("supin en -um", "----u----") \
                .replace("supin en -u", "----u----")

            # Voice
            line = line \
                .replace("actif", "-----a---") \
                .replace("passif", "-----p---")

            # Gender
            line = line \
                .replace("masculin", "------m--") \
                .replace("féminin", "------f--") \
                .replace("neutre", "------n--")

            # Case
            line = line \
                .replace("nominatif", "-------n-") \
                .replace("génitif", "-------g-") \
                .replace("accusatif", "-------a-") \
                .replace("datif", "-------d-") \
                .replace("ablatif", "-------b-") \
                .replace("vocatif", "-------v-") \
                .replace("locatif", "-------l-")

            # Degree
            line = line \
                .replace("comparatif", "a-------c") \
                .replace("superlatif", "a-------s") \
                .replace("positif", "a-------p")

            line = line.replace("461:", "416:--------")

            # Then we merge the tags
            new_tag = "---------"
            index, tags = line.split(":")
            tags = tags.split()

            for tag in tags:
                for x in search.finditer(tag):
                    i = x.start()
                    new_tag = new_tag[:i] + tag[i] + new_tag[i + 1:]

            morphos[index] = new_tag



#############################################################
# Convert modeles.la
# Line starting with $ are variable that can be reused
# Set of line starting with model are models
# R:int:int,int (Root number, Character to remove to get canonical form, number of character to add to get the root)
#  -> eg. : for uita, R:1:1,0 would get root 1, 1 character to remove, 0 to add -> uit
#  -> eg. : for epulae, R:1:2,0 would get root 1, 2 character to remove, 0 to add : epul
#############################################################


def parse_range(des_number):
    """ Range
    :return: Int reprenting element of the range
    """
    ids = []
    for des_group in des_number.split(","):  # When we have ";", we should parse it normally
        if "-" in des_group:
            start, end = tuple([int(x) for x in des_group.split("-")])
            ids += list(range(start, end + 1))
        else:
            ids += [int(des_group)]
    return ids

def get_model(pos):
    model = {
        "R": {},
        "abs": [],  # Unused desinence if inherits
        "des": {},  # Dict of desinences
        "suf": [],  # Dict of Suffixes
        "sufd": [],  # Possible endings
        "pos": pos  # Possible endings
    }
    return model


def convert_models(lines, tst=0):

    old2new = {}

    models = {}

    __R = re.compile("^R:(?P<root>\d+):(?P<remove>-|\w+)[,:]?(?P<add>\w+)?", flags=re.UNICODE)
    if not tst:
        __des = re.compile("^des[\+]?:(?P<range>[\d\-,]+):(?P<root>\d+):(?P<des>[\w"+cobr+"[\-,;]+)?$")
    else:
        __des = re.compile("^des[\+]?:(?P<range>[\d\-,]+):(?P<root>\d+):(?P<des>[\w\-,;]+)?$", flags=re.UNICODE)
    last_model = None
    variable_replacement = {}
    current_pos = 'n'
    lpos = 'n'
    real_last_model = ''
    for lineno, line in enumerate(lines):
        line = line.strip()
        if "des:189-200:2:$lupus" in line:
            bb=8

        if line.startswith('!;'):
            old2new[line[2:]] = last_model
        if line.startswith('pos:'):
            current_pos = line[4]
            models[last_model]['pos'] = current_pos

        # If we get a variable
        if line.startswith("$"):
            # We split the line on =
            var, rep = tuple(line.split("="))
            # We create a replacement variable
            variable_replacement[var] = rep
        elif len(line) > 0 and not line.startswith("!"):
            if line.startswith("modele:"):

                last_model = line[7:]
                models[last_model] = get_model(current_pos)
            elif line.startswith("pere:"):
                # Inherits from parent
                models[last_model].update(
                    deepcopy(models[line[5:]])
                )


            elif line.startswith("R:"):
                # Still do not know how to deal with "K"
                root, remove, chars = __R.match(line).groups()

                if remove == "-":
                    # ToDo: Check how radical with "-" should work
                    continue
                if chars == "0":
                    chars = ""
                models[last_model]["R"][root] = [remove, chars]
            elif line.startswith("des"):
                # We have new endings
                # des:range:root_number:list_of_des
                # First we apply desinence variables replacement
                if "$" in line:
                    for var, rep in variable_replacement.items():
                        # First we replace +$
                        if tst:
                            line = re.sub(
                                r"(\w+)(\+?\{})".format(var),
                                lambda x: (
                                    ";".join([x.group(1) + r for r in rep.split(";")])
                                ),
                                line, flags=re.UNICODE
                            )
                        else:
                            line = re.sub(
                                r"(\w+)(\+?\{})".format(var),
                                lambda x: (
                                    ";".join([x.group(1) + r for r in rep.split(";")])
                                ),
                                line
                            )

                        line = line.replace(var, rep)
                        if "$" not in line:
                            break
                try:
                    des_number, root, des = __des.match(line).groups()
                except AttributeError as E:
                    # print(line, lineno)
                    raise E
                if not des:
                    # ToDo : "Deal with empty value in desinence ?"
                    continue
                nums = parse_range(des_number)

                desinence = des.split(";")
                last_des = []
                for desinence_index, desinence_num in enumerate(nums):
                    if desinence_index >= len(desinence):
                        # We might have ranges where number of item < ranges. This seems to mean last item is repeated.
                        current_des = last_des
                    else:
                        current_des = desinence[desinence_index].replace("-", "").split(",")

                    if current_des:
                        desinence_int = int(desinence_num)
                        # If we have des+, we add to the known desinence
                        if line.startswith("des+") and desinence_int in models[last_model]["des"]:
                            models[last_model]["des"][desinence_int].append((root, current_des))
                        else:
                            models[last_model]["des"][desinence_int] = [(root, current_des)]
                        last_des = current_des
                    else:
                        print("Line %s : No desinence for id %s (%s)" % (lineno, desinence_num, last_model))

            elif line.startswith("abs:"):
                models[last_model]["abs"] = parse_range(line[4:])  # Add the one we should not find as desi
            elif line.startswith("suf:"):
                rng, suf = tuple(line[4:].split(":"))
                models[last_model]["suf"].append([suf, list(parse_range(rng))])  # Suffixes are alternative ending
            elif line.startswith("sufd:"):
                models[last_model]["sufd"] += line[5:].split(",")  # Sufd are suffix always present
            else:
                if line.startswith("pos"):
                    continue
                # print(line.split(":")[0], lineno)

    pi.save_pickle(old2new,f'{fold}old2new_mods',1)
    return models


def test_diff(new, old, new_lemmas=[]):
    dec_old = CollatinusDecliner(old)
    dec_new = CollatinusDecliner(new)
    num2pos = dec_old._data['pos']
    pos2num = {v:k for k,v in num2pos.items()}

    for k, v in old.items():
        if k == "sequor":
            bb = 8

        new_obj = new[k]
        for x, y in new_obj['des'].items():
            old_des = v['des'][x]
            if old_des != y:
                pass
                # p(k, x, old_des, y)
        if k in dec_old.co_lemmas0:
            dold = dec_old.decline(k)
            dnew = dec_new.decline(k)
            if dnew != dold:
                dctn = {v:k for k,v in dnew}
                dcto = {v:k for k,v in dold}

                # p(k)
                for x, n in dctn.items():
                    o = dcto.get(x)
                    if o and n != o:
                        # p (x,pos2num[x], n,o)
                        bb = 8



    return


def get_norm_mod(file, tst=0):
    with open(file) as f:
        if tst:
            lines = normalize_unicode(f.read()).split("\n")
        else:
            lines = f.read().split("\n")
        lines += to.from_txt2lst(f'{fold}modeles5')
        norm_models = convert_models(lines,tst)
    return norm_models


def test_mod(norm_models):
    assert norm_models["fortis"]["des"][13] == [("4", [''])], \
        "Root 4, Empty string (originally '-') expected, found %s %s" % norm_models["fortis"]["des"][13][0]
    assert norm_models["fortis"]["des"][51] == [("1", ["iorem"])], \
        "Root 4, iorem expected, found %s %s" % norm_models["fortis"]["des"][50][0]
    assert norm_models["dico"]["des"][181] == [("0", ["e"]), ("0", [""])], \
        "[(0, e), (0, ''), found %s %s " % tuple([str(x) for x in norm_models["dico"]["des"][181]])
    assert norm_models["edo"]["des"][122] == [("0", ["is"]), ("3", ["es"])], \
        "[(0, is), (3, es), found %s %s " % tuple([str(x) for x in norm_models["edo"]["des"][122]])

def test_old_mod():

    file = f"{fold}modeles4.txt"
    file_old = f"{fold}modeles.txt"
    norm_models_old = get_norm_mod(file_old, 1)
    norm_models = get_norm_mod(file, 1)
    test_diff(norm_models, norm_models_old)





############################################
#
#   Get the lemma converter
#
# lemma=lemma|model|genitive/infectum|perfectu|morpho indications
#
############################################

def parseLemma(lines):
    """
    :param lines:
    :param normalize:
    :return:
    # ToDo: Fix issue with
    Caeres2=Cāeres|miles|Cāerĭt,Cāerĭtēt||ĭtis, (-ētis), f.|2
    Caerēs=Cāerēs|diues|Cāerĭt||ĭtis|2
    """

    lemmas = {}
    lemma_without_variations = re.compile(
        r"^(?P<lemma>\w+\d?){1}(?:\=(?P<quantity>[\w,]+))?\|"
        r"(?P<model>\w+)?\|"
        r"[-]*(?P<geninf>[\w,]+)?[-]*\|"
        r"[-]*(?P<perf>[\w,]+)?[-]*\|"
        r"(?P<lexicon>.*)?",
        flags=re.UNICODE
    )
    for lineno, line in enumerate(lines):
        if not line.startswith("!") and "|" in line:
            if line.count("|") != 4:
                # We need to clean up the mess
                # Some line lacks a |
                # I assume this means we need;ĭbŭs to add as many before the dictionary
                should_have = 4
                missing = should_have - line.count("|")
                last_one = line.rfind("|")
                line = line[:last_one] + "|" * missing + line[last_one:]

            result = lemma_without_variations.match(line)
            if result:
                result = result.groupdict(default=None)
                # we always normalize the key
                lemmas[normalize_unicode(result["lemma"])] = result
            else:
                print("Unable to parse lemma", line)
    return lemmas
#
# def get_lemmas():
#     with open(f"{fold}lemmes.txt") as f:
#         lines = normalize_unicode(f.read()).split("\n")
#         lemmas = parseLemma(lines)
#
#     assert lemmas["volumen"]["geninf"] == "volumin"
#     assert lemmas["volumen"]["lemma"] == "volumen"
#     assert lemmas["volumen"]["model"] == "corpus"
#
#     with open(f"{fold}lem_ext.txt") as f:
#         lines = normalize_unicode(f.read()).split("\n")
#         lemmas.update(parseLemma(lines))


def begin_mod():
    file = f"{fold}modeles4.txt"
    norm_models = get_norm_mod(file)
    pi.save_pickle(norm_models, f'{fold}mmodels', 1)

begin_mod()