import os
from xml.etree.ElementTree import ElementTree
from lxml import etree

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

def get_xml(xml):
	global real
	ofi = open(xml, 'r')
	real = ofi.read()
	xml = real.decode('utf-8', 'xmlcharrefreplace')
	return xml

def get_profile(grp):
    """
    lit la liste des appli affectes au groupe de  machines
    si elle n'existe pas on cree une vide
    """
    profiles=[]
    if grp==None:
    	return []
    filename = u'/home/wpkg/profiles/' + grp + '.xml'
    if os.path.exists(filename):
        xml = etree.parse(filename)
        for group in xml.getiterator('package'):
            profiles.append(group.get('package-id'))
    else:
        set_profile(grp)
    return profiles

def set_profile(ids):
    """
    creation fichiers contenant les applis pour un group
    """
    if not os.path.exists('/home/wpkg/profiles/'):
        os.makedirs('/home/wpkg/profiles/')
    filename = u'/home/wpkg/profiles/' + ids + '.xml'
    xmlfp = open(filename, "w")
    xmlfp.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    xmlfp.write('<profiles>\n')
    for j in ids:
        xmlfp.write('<profile id="' + j + '">\n')
    xmlfp.write('</profile>\n')
    xmlfp.write('</profiles>\n')
    xmlfp.close()