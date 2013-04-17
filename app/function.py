def get_group():
	grps=[]
	from xml.etree.ElementTree import ElementTree
	tree = ElementTree(file=open("grp_eole/ListeGM.xml"))
	root = tree.getroot()
	for GM in root.getiterator('GM'):
		grp = GM.get('nom')
		grps.append(grp)
	return grps

def get_packages():
	packs=[]
	pack=[]
	i=[]
	global shortname, i
	import glob, os
	pack = glob.glob('packages/*.xml')
	for i in pack:
		os.path.split(i)
		(filepath, filename) = os.path.split(i)
		(shortname, extension) = os.path.splitext(filename)
		packs.append(shortname)
		pack.index(i)

	return packs, shortname, i, pack

def get_xml():
	global real
	ofi = open('packages/RealAlternative.xml', 'r')
	real = ofi.read()
	real = real.decode('utf-8', 'xmlcharrefreplace')
	return real


