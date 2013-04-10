#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from lxml import etree
import xml2dict

import glob, os, re, sys

WPKG_PATH = '/home/wpkg'
PACKAGES_PATH = os.path.join(WPKG_PATH, 'packages')
SOFTWARE_PATH = os.path.join(WPKG_PATH, 'softwares')
SCRIPT_FILE = os.path.join(PACKAGES_PATH, 'download.sh')
SCRIPT_LOG_FILE = os.path.join(PACKAGES_PATH, 'download.log')

WGETCMD = "wget --no-check-certificate" # --progress=bar:force" # s'affiche mal dans le fichier de log généré par 'tee'

def convert(objet, vardict=None):
    """Parcour objet jusqu'à trouver une chaine et remplace les variables par leur valeur
    Les variables sont %variable%
    vardict = {'variable' : valeur}
    """
    if not vardict: return objet
    if type(objet) == list:
        l = []
        for item in objet:
            l.append(convert(item, vardict))
        return l
    if type(objet) == tuple:
        l = []
        for item in objet:
            l.append(convert(item, vardict))
        return tuple(l)
    if type(objet) == dict:
        dico={}
        for cle, val in objet.items():
            dico[convert(cle, vardict)] = convert(val, vardict)
        return dico
    if type(objet) == unicode:
        string =  objet.encode('iso8859-1')
        return convert(string, vardict)
    if type(objet) == str:
        objet = replace_vars(objet, vardict)
    return objet

def replace_vars(string, vardict):
    """remplace les variables %var% par leur valeur
    sans tenir compt de la casse
    """
    for var, val in vardict.items():
        var = '%%%s%%'%var
        rpl = re.compile(var, re.IGNORECASE)
        try: val = str(val)
        except: return string
        string = string.replace('\\', '/')
        if val.endswith('\\'):
            val = val[:-1]
        string = rpl.sub(val, string)
    return string

def get_xml_list():
    """liste les <package>.xml
    """
    return glob.glob(os.path.join(PACKAGES_PATH, '*.xml'))

def get_dls(pkgxml):
    """parse un fichier <package>.xml et recupere les infos de telechargement
    dl = lien
    destname = rep/nom_fichier.exe : nom de fichier de destination avec repertoire, est contenu dans %SOFTWARE%
    unzip = 1 : lancer 'unzip' "fichier.zip" apres avoir telecharger "fichier.zip"
    """
    if not pkgxml.has_key('eoledl'): return None
    dl_list = []
    eoledls = pkgxml['eoledl']
    if not type(eoledls) == list:
        eoledls = [eoledls]
    for i in eoledls:
        dl_dict = {}
        dl_dict['dl'] = i.get('dl')
        dl_dict['destname'] = i.get('destname')
        dl_dict['unzip'] = i.get('unzip')
        dl_list.append(dl_dict)
    return dl_list

def get_vars(pkgxml):
    """recupere les valeurs des elements <variable ...>
    """
    if not pkgxml.has_key('variable'): return None
    var_list = []
    variables = pkgxml['variable']
    if not type(variables) == list:
        variables = [variables]
    vardict = {}
    for i in variables:
        vardict[i.get('name')] = i.get('value')
    return vardict

def write_script(string):
    """ecrit dans le fichier script final, lance a la fin
    """
    f_handler = file(SCRIPT_FILE, 'a')
    f_handler.write('%s\n'%string)
    f_handler.close()

def gen_download(dl_list, pkgid):
    """genere les commandes 'wget' et les ecrit dans le script final
    """
    for dl_dict in dl_list:
        try:
            src = dl_dict['dl']
            dst = os.path.join(SOFTWARE_PATH, dl_dict['destname'])
            if dst.endswith('/') or dst.endswith('\\'):
                fname = os.path.join(dst, os.path.basename(src))
                write_script('if [ -f "%s" ] ;then'%(fname))
                #write_script("""echo '"%s" déjà téléchargé ("%s")'"""%(src, fname))
                write_script("echo -n")
                write_script('else')
                write_script("""echo 'Package : "%s"'"""%pkgid)
                write_script("""echo 'Telechargement de "%s"'"""%(src))
                write_script('%s --directory-prefix "%s" "%s"'%(WGETCMD, dst, src))
                write_script('if [ $? -ne 0 ] ;then')
                write_script("""echo 'ERREUR lors du téléchargement de "%s"'"""%(src))
                write_script("""echo '%s --directory-prefix "%s" "%s"'"""%(WGETCMD, dst, src))
                if dl_dict['unzip']:
                    write_script('else')
                    write_script('echo Decompression de %s'%fname)
                    write_script('unzip -o -d "%s" "%s"'%(dst, fname))
                write_script('fi')
                write_script('echo ""')
                write_script('fi')
            else:
                destdir = os.path.dirname(dst)
                write_script('if [ -f "%s" ] ;then'%(dst))
                #write_script("""echo '"%s" déjà téléchargé ("%s")'"""%(src, dst))
                write_script("echo -n")
                write_script('else')
                write_script("""echo 'Package : "%s"'"""%pkgid)
                write_script('[ ! -d "%s" ] && mkdir -p "%s"'%(destdir, destdir))
                write_script("""echo 'Telechargement de "%s"'"""%(src))
                write_script('%s --output-document "%s" "%s"'%(WGETCMD, dst, src))
                write_script('if [ $? -ne 0 ] ;then')
                write_script(""" echo 'ERREUR lors du téléchargement de "%s"'"""%(src))
                write_script("""echo '%s --output-document "%s" "%s"'"""%(WGETCMD, dst, src))
                write_script('rm -f "%s"'%(dst))
                if dl_dict['unzip']:
                    write_script('else')
                    write_script('echo Decompression de %s'%dst)
                    write_script('unzip -o -d "%s" "%s"'%(destdir, dst))
                write_script('fi')
                write_script('echo ""')
                write_script('fi')
        except Exception, e:
            print e, src
    write_script('')

def get_packages(xmldict):
    try:
        packages = xmldict['packages']['package']
        if not type(packages) == list:
            return [packages]
        return packages
    except Exception, e:
        sys.exit(e)

def main():
    file(SCRIPT_FILE, 'w').write('')
    write_script('#!/bin/bash')
    #for i in  ['Audacity.xml', 'Gimp.xml', 'QuicktimeAlternativeLite.xml']:
    for i in  get_xml_list():
        print '# Traitement de "'+i+'"'
        xmldict = xml2dict.ConvertXmlToDict(i)
        pkglist = get_packages(xmldict)
        for pkgxml in pkglist:
            pkgid = pkgxml['id']
            dl_list = convert(get_dls(pkgxml), get_vars(pkgxml))
            if dl_list:
                gen_download(dl_list, pkgid)
            else:
                print('Pas de téléchargement pour "%s"'%pkgid)
    write_script('setfacl -Rbk %s'%WPKG_PATH)
    write_script('setfacl -Rm u::rwx,g::r-x,o::r-x %s'%WPKG_PATH)
    #os.system('bash %s 2>&1 | tee %s'%(SCRIPT_FILE, SCRIPT_LOG_FILE))
    os.system('bash %s | tee %s'%(SCRIPT_FILE, SCRIPT_LOG_FILE))
    #os.unlink(SCRIPT_FILE)

if __name__ == '__main__':
    main()

