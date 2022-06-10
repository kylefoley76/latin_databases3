import sys
vol='/users/kylefoley/'
public2=1

gen_dir = f'{vol}documents/pcode/'
gen_dir2 = f'{vol}documents/pcode/general/'
gen_dir4 = f'{vol}documents/pcode/latin/latin/general/'
gen_dir3 = f'{vol}documents/pcode/other/'
sys.path.append(gen_dir)
sys.path.append(gen_dir2)
sys.path.append(gen_dir3)
sys.path.append(gen_dir4)


if public2:
    import latin.general.very_general_functions as vgf
    import latin.general.trans_obj as to
    import latin.general.pickling as pi
    from latin.general.abbreviations import *
else:
    import general.very_general_functions as vgf
    import general.trans_obj as to
    import general.pickling as pi
    import general.time_func as tf
    import general.excel_functions as ef
    from general.abbreviations import *




