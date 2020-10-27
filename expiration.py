import toml
from datetime import datetime
import os
import sys
import fnmatch

def recursive_glob(treeroot, pattern):
	results=[]
	for base, dirs, files in os.walk(treeroot):
		goodfiles = fnmatch.filter(files, pattern)
		results.extend(os.path.join(base,f) for f in goodfiles)
	return results

zim_root = sys.argv[1]
all = recursive_glob(zim_root, 'deployments.toml')
output = []
for deployment in [toml.load(item) for item in all]:
	line = "exires on {}\t\tlicenses: {}\t\tid: {}".format(
		deployments['po']['expiration'], deployments['po']['licenses'], deployments['id'])
		output.append(line)
output.sort()
print('\n'.join(output))
