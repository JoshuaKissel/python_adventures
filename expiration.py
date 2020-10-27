import toml
from datetime import datetime
import glob

all = glob.glob('c:/users/12157/documents/github/tv-zim/deployments/**/*.toml', recursive=True)
parsed = [toml.load(item) for item in all]
f = open('c:/users/12157/documents/github/tv-zim/deployments/expiration.txt', 'w')
f.write("The following licenses are expiring in the next month:\n")
for file in parsed:
	expiration_date = file['po']['expiration']
	id = file['id']
	lic = file['po']['licenses']
	d0 = datetime.strptime(expiration_date, '%Y/%m/%d')
	d1 = datetime.today()
	delta = d0-d1
	d3 = delta.days
	if d3 <= 31:
		f.write(id + ' has ' + str(lic) + ' licenses that expire in ' + str(d3) + ' days.\n')
f.close()


	

#	print(parsed)
#	deployment_name=item.replace('\\','/').split('/')[-2]
#	print(deployment_name)

#for subdir, dirs, files in os.walk(r'C:\Users\12157\Documents\Github\tv-zim'):
#	for filename in files:
#		if filename.endswith('.toml'):
#			print(filename)
#			x = toml.load(filename)
#			expiration_date = x['po']['expiration']
#			id = x['id']
#			lic = x['po']['licenses']
#			d0 = datetime.strptime(expiration_date, '%Y/%m/%d')
#			d1 = datetime.today()
#			delta = d0-d1
#			d3 = delta.days
#			if d3 <= 99999999:
#				print(id + str(d3) + str(lic))