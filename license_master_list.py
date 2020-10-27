import toml
from datetime import datetime
import glob

all = glob.glob('c:/users/12157/documents/github/tv-zim/deployments/**/*.toml', recursive=True)
parsed = [toml.load(item) for item in all]
f = open('c:/users/12157/desktop/py_script/expiration.txt', 'w')
f.write("List of Deployments, Licenses, and Expirations:\n")
for file in parsed:
	expiration_date = file['po']['expiration']
	id = file['id']
	lic = file['po']['licenses']
	d0 = datetime.strptime(expiration_date, '%Y/%m/%d')
	d1 = datetime.today()
	delta = d0-d1
	d3 = delta.days
	f.write('Deployment = ' + id + ', License Number =  ' + str(lic) + ', expires in ' + str(d3) + ' days.\n')
f.close()
