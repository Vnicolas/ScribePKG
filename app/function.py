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

def get_xml():
	global real
	ofi = open('packages/RealAlternative.xml', 'r')
	real = ofi.read()
	real = real.decode('utf-8', 'xmlcharrefreplace')
	return real

def get_softinstalled():
	softs=[]
	LM=[]
	global LM, n
	import glob
	LM = glob.glob('profiles/*.xml')
	for n in LM:
		tree = ElementTree(file=open(n))
		root = tree.getroot()
		sroot = root.getiterator('package')
		for GS in sroot:
			soft = GS.get('package-id')
			softs.append(soft)

	return softs, soft, LM, n


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
    print profiles
    return profiles

def set_profile(grp):
    """
    creation fichiers contenant les applis pour un group
    """
    if not os.path.exists('/home/wpkg/profiles/'):
        os.makedirs('/home/wpkg/profiles/')
    filename = u'/home/wpkg/profiles/' + grp + '.xml'
    xmlfp = open(filename, "w")
    xmlfp.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    xmlfp.write('<profiles>\n')
    xmlfp.write('<profile id="' + grp + '">\n')
    xmlfp.write('</profile>\n')
    xmlfp.write('</profiles>\n')
    xmlfp.close()
