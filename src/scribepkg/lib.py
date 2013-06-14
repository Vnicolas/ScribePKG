# -*- coding: utf-8 -*-
#
##########################################################################
# scribepkg
# Christophe DEZE
# Nicolas Vairaa
#
# License CeCILL:
#  * in french: http://www.cecill.info/licences/Licence_CeCILL_V2-fr.html
#  * in english http://www.cecill.info/licences/Licence_CeCILL_V2-en.html
##########################################################################
"""
librairie de fonctions utiles a scribepkg
"""

import glob, os, PAM, grp
from xml.etree.ElementTree import ElementTree
from lxml import etree
from StringIO import StringIO

def get_group():
    """recuperation des groupes ESU
    """
    grps=[]
    tree = ElementTree(file=open("/home/esu/Base/ListeGM.xml"))
    root = tree.getroot()
    for GM in root.getiterator('GM'):
        grp = GM.get('nom')
        grps.append(grp)
    return grps

def get_state(nom):
    """on verifie la presence de l'installeur dans software
    """
    f = open('/home/wpkg/packages/' + nom + '.xml')
    xml = f.read()
    f.close()
    dvars = dict()
    state =""
    xml = etree.parse(StringIO(xml))
    for vars in xml.getiterator('variable'):
        dvars[vars.get('name')] = vars.get('value')
    if xml.getiterator('eoledl'):
        for eoledl in xml.getiterator('eoledl'):
            eole_dl = {}
            destnames = {}
            destname = eoledl.get('destname').replace('\\','/')
            for var, value in dvars.iteritems():
                destname = destname.replace('%' + var + '%', value)
            destname = ("/home/wpkg/softwares/" + destname)
            if os.path.isfile(destname):
                state = "OUI"
            else:
                state = "NON"
    return state

    
def get_package_description(filename):
    """on verifie la presence de l'installeur dans software
    """
    desc = ""
    try:
        xml = etree.parse(filename)
        
        dvars = dict()
        for vars in xml.getiterator('variable'):
            dvars[vars.get('name')] = vars.get('value')
            
        for p in xml.getiterator('package'):
            desc = p.get('name')   
        for var, value in dvars.iteritems():
            desc = desc.replace('%' + var + '%', value)   
    except:
        pass      
    return desc    
        
def get_packages():
    """on recupere la liste des packages           
    """
    pack = glob.glob('/home/wpkg/packages/*.xml')
    packages = []
    for i in pack:
        package = dict()
        (filepath, filename) = os.path.split(i)
        (shortname, extension) = os.path.splitext(filename)

        package['desc']=(get_package_description(i))
        package['shortname']=shortname
        package['longname']=i
        packages.append(package)

    return packages
def get_xml(xml):
    """ renvoit le contenu d'un fichier xml
    """
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
        set_profile(grp, "no")
    return profiles

def set_profile(ids, groupe):
    """
    creation fichiers contenant les applis pour un group
    """
    if not os.path.exists('/home/wpkg/profiles/'):
        os.makedirs('/home/wpkg/profiles/')
    filename = u'/home/wpkg/profiles/' + groupe + '.xml'
    xmlfp = open(filename, "w")
    xmlfp.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    xmlfp.write('<profiles>\n')
    xmlfp.write('<profile id="' + groupe + '">\n')
    for id in ids.strip().split(" "):
        xmlfp.write('<package package-id="' + id + '"/>\n')
    xmlfp.write('</profile>\n')
    xmlfp.write('</profiles>\n')
    xmlfp.close()

def login(username,password):
    """fonction qui renvoit true si l'on s'est bien connecte
    en domainadmins
    """
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

