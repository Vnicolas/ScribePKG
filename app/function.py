import os
from xml.etree.ElementTree import ElementTree
from lxml import etree
import PAM
import grp


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

def save_file(code, path):
    f = open(path, 'w')
    f.write(code)
    f.close

def login(username,password):
    def pam_conv(auth, query_list, userData):
    #pam password authentification utility
        resp = []
        for i in range(len(query_list)):
            query, type = query_list[i]
            #print query, type
            if type == PAM.PAM_PROMPT_ECHO_ON or type == PAM.PAM_PROMPT_ECHO_OFF:
                resp.append((password, 0))
            elif type == PAM.PAM_PROMPT_ERROR_MSG or type == PAM.PAM_PROMPT_TEXT_INFO:
                resp.append(('', 0))
            else:
                return None
        return resp


    auth = PAM.pam()
    auth.start('WPKGjs')
    auth.set_item(PAM.PAM_USER, username)
    auth.set_item(PAM.PAM_CONV, pam_conv)
    if not 'DomainAdmins'  in [g.gr_name for g in grp.getgrall() if username in g.gr_mem]:
        return False
    try:
        #print "auth.authenticate()"
        auth.authenticate()
        auth.acct_mgmt()
        print "auth.authenticate"
        return True
    except PAM.error, resp:
        print 'Go away! (%s)' % resp
        return False
    except:
        print 'Internal error'
        return False

