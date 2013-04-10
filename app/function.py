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



def get_softwares():
	import glob, re
	softs = glob.glob('softwares/*')
	for i in softs:
		soft = re.sub(r'^.*/', "", i)
		print soft "Probleme de boucle infinie"
		softs.append(soft)
	return soft


