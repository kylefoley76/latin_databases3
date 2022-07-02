import os.path
import shutil

from bglobals import *




file = f'{vol}temp/'

if not os.path.exists(file):
    os.mkdir(file)
    os.mkdir(file + 'files/')
for x in ['files','lasla','lasla2','phi','phi2']:
    src = f'{vol}{x}/'
    dfold = f'{file}{x}/'
    if x != 'files':
        shutil.copytree(src,dfold)
    else:

        for y in os.listdir(src):
            if y != ds:
                file1 = f'{src}{y}'


                gi = vgf.get_gigs(file1)
                if gi < 60:
                    dest = f'{dfold}{y}'
                    shutil.copy(file1,dest)
                else:
                    p(f'too big{file1}')
p ('now zipping')
vgf.zipdir1(file,file[:-1])
shutil.rmtree(file)
p ('now uploading')
vgf.upload_blob(file[:-1]+'.zip', 'data.zip')
os.remove(file[:-1]+'.zip')


