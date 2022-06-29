import sys
from gglobal import *
vol='/users/kylefoley/'

gen_dir = f'{vol}documents/pcode/'
gen_dir2 = f'{vol}documents/pcode/latin/latin/general_la/'
gen_dir3 = f'{vol}documents/pcode/other/'
sys.path.append(gen_dir)
sys.path.append(gen_dir3)
sys.path.append(gen_dir2)


if public:
    import general_la.very_general_functions as vgf
    import general_la.trans_obj as to
    import general_la.pickling as pi
    from general_la.abbreviations import *
    # import general_la.excel_functions as ef

else:
    gen_dir2 = f'{vol}documents/pcode/general/'
    sys.path.append(gen_dir2)
    import general.very_general_functions as vgf
    import general.trans_obj as to
    import general.pickling as pi
    import general.time_func as tf
    import general.excel_functions as ef
    from general.abbreviations import *




