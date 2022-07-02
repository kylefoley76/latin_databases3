import shutil
import urllib.request
import requests
from bglobals import *


p('running post installation')
s='https://storage.googleapis.com/download/storage/v1/b/deduction4/o/data.zip?generation=1656711258549150&alt=media'
urllib.request.urlopen(s)
file = f'{vol}data.zip'
r = requests.get(s, stream=True, verify=False)
if r.status_code == 200:
    r.raw.decode_content = 1
    with open(file, 'wb') as f:
        f.write(r.content)
else:
    assert 0, 'failed to download data files'
vgf.unzip(file,vol)
dir1 = f'{vol}users/kylefoley/documents/pcode/latin/latin/general_la/temp/'


for x in ['files','lasla','lasla2','phi','phi2']:
    src = f'{dir1}{x}'
    dest = f'{vol}{x}'
    shutil.move(src,dest)
shutil.rmtree(f'{vol}/users')
os.remove(f'{vol}data.zip')

