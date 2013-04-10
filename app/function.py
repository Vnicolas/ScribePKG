from xml.etree.ElementTree import ElementTree
tree = ElementTree(file=open("grp_eole/_ListeUtilisateurs.xml"))
root = tree.getroot()
for GU in root.getiterator('GU'):
	nom = GU.get('nom')
	print nom

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

