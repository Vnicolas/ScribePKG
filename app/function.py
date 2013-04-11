def get_group():
	grps=[]
	from xml.etree.ElementTree import ElementTree
	tree = ElementTree(file=open("grp_eole/ListeGM.xml"))
	root = tree.getroot()
	for GM in root.getiterator('GM'):
		grp = GM.get('nom')
		print  grp
		grps.append(grp)
	return grps



def get_packages():
	packs=[]
	import glob, os
	pack = glob.glob('packages/*.xml')
	for i in pack:
		os.path.split(i)
		(filepath, filename) = os.path.split(i)
		(shortname, extension) = os.path.splitext(filename)
		print shortname 
		packs.append(shortname)
	return packs

def get_xml():
	from xml.dom import minidom
	xmldoc = minidom.parse('packages/Gimp.xml')
	ficxml = xmldoc.toxml()
	print ficxml
	return ficxml

