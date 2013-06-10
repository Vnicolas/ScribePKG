#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#inspiré de download_installer de Klaas tjebbes
from StringIO import StringIO
import os, traceback, urllib, zipfile, shutil
from lxml import etree

WPKG_PATH = '/home/wpkg'
PACKAGES_PATH = os.path.join(WPKG_PATH, 'packages')
SOFTWARE_PATH = os.path.join(WPKG_PATH, 'softwares')

def get_dls(pkgxml):
    """parse un fichier <package>.xml et recupere les infos de telechargement
    dl = lien
    destname = rep/nom_fichier.exe : nom de fichier de destination avec repertoire, est contenu dans %SOFTWARE%
    unzip = 1 : lancer 'unzip' "fichier.zip" apres avoir telecharger "fichier.zip"
    """
 
    f = open(pkgxml)
    xml = f.read()
    f.close()
    xml = etree.parse(StringIO(xml))
    
    dvars = dict()
    for vars in xml.getiterator('variable'):
       dvars[vars.get('name')] = vars.get('value')
       eole_dls = []
    if xml.getiterator('eoledl'):
        for eoledl in xml.getiterator('eoledl'):
            eole_dl = {}
            eole_dl['url'] = eoledl.get('dl')
            if eole_dl['url'] != None:
                for var, value in dvars.iteritems():
                    eole_dl['url'] = eole_dl['url'].replace('%' + var + '%', value)
                eole_dl['dest'] = eoledl.get('destname')
                eole_dl['zip'] = eoledl.get('unzip')
                if eole_dl['dest'] == None :
                    eole_dl['dest'] = SOFTWARE_PATH
                else:
                    for var, value in dvars.iteritems():
                        eole_dl['dest'] = eole_dl['dest'].replace('%' + var + '%', value)
                    path = os.path.dirname("/home/wpkg/softwares/" + eole_dl['dest'])
                    if not os.path.exists(path):
                        os.makedirs(path)
                eole_dls.append(eole_dl)
    else:
        print "Ce fichier ne contient aucun lien de telechargement"
    return eole_dls

def downloading(dl):
    FichierURL=dl['url']
    dest=("/home/wpkg/softwares/" + dl['dest'])
    zip=dl['zip']

    try:
        filename,msg = urllib.urlretrieve(FichierURL)
        if zip == '1':
            sourceZip = zipfile.ZipFile(filename, 'r')
            for name in sourceZip.namelist():
                sourceZip.extract(name, dest)
            sourceZip.close()
        else:
            shutil.move(filename, dest)
    except :
        traceback.print_exc()

def _hook( nb_blocs, taille_bloc, taille_fichier):
    percent = min((nb_blocs*taille_bloc*100)/taille_fichier, 100)
    if percent >= 100:
        print "Le telechargement est termine !" , taille_fichier
        #self.statictextinfo.SetLabel("100 % .")
        #if self.FichierDest != None:
        #    self.parent.textctrlexe.SetValue(self.FichierDest)
        #self.parent.button1.SetLabel(u'Enregistrer')
        #raise Abort
    print percent

def get_installers(xmlfile):
    for dl in get_dls(xmlfile):
        downloading(dl)

