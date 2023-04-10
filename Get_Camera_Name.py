import os
import json

tmcdata_dir = '~/trafficvision/webroot/tmcdata'
#tmcdata_dir = 'c:/trafficvision/webroot/tmcdata'
infodump = ''
for dir in os.listdir(tmcdata_dir):
    if os.path.isdir(f'{tmcdata_dir}/{dir}'):
        try:
            with open(f'{tmcdata_dir}/{dir}/camera_info.json', 'r') as fp:
                data = json.load(fp)
                cameraname = data['camera_name']
                print(cameraname)
                infodump += f'{cameraname} = {dir}\n'            
        except Exception as e:
            print(e)
            
with open('infodump.txt', 'w') as f:
    f.write(infodump)
