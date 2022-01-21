#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 19:15:31 2021

@author: mayanknarang
"""
import glob
import os
import shutil
from pyraf import iraf
import re

def aperture_target(file):
    iraf.noao(_doprint=0) 
    iraf.twodspec(_doprint=0) 
    iraf.apextract(_doprint=0)
    iraf.apextract.unlearn()
    iraf.apall.unlearn()
    iraf.apall(input=file,nfind=1,lower=-15,upper=15,b_sample='-25:-15,15:25',background ='fit',weights ='variance',readnoi=5.75,gain=0.28,extras='no',interactive='yes',t_order=3) 



def aperture_FeNe(file,file3):
    iraf.noao(_doprint=0) 
    iraf.twodspec(_doprint=0) 
    iraf.apextract(_doprint=0)
    iraf.apextract.unlearn()
    iraf.apall.unlearn()
    iraf.apall(input=file,nfind=1,lower=-15,upper=15,b_sample='-25:-15,15:25',background ='none',weights ='none',readnoi=5.75,gain=0.28,extras='no',interactive='no',recenter='no',reference=file3,t_order=3) 


def identify(file):
    iraf.noao(_doprint=0) 
    iraf.twodspec(_doprint=0) 
    iraf.onedspec(_doprint=0)
    iraf.identify.unlearn()
    iraf.identify(images=file)
    
    
def refspec(file,file1):
    iraf.noao(_doprint=0)
    iraf.onedspec(_doprint=0)
    iraf.refspectra.unlearn()
    iraf.refspectra(input=file,reference=file1, sort='',group='')
    
    
    
def dispcor(file2):
    iraf.noao(_doprint=0)
    iraf.onedspec(_doprint=0)
    
    file4='wc'+file2
    iraf.dispcor.unlearn()
    iraf.dispcor(input=file2,output=file4)
    
def splot(file4):
    iraf.splot(file4)


def swrite(file4):
    iraf.wspectext(input=file4,output=file2a)




file = input("Enter the fits file you want to reduce (the file should be in the form 'fc_bc_object.fits'): ")

#file='fc_bc_V1207Tau.fits'
    
aperture_target(file)

file2a=file2 = re.sub('\.fits$', '', file)

file2=file2+'.ms.fits'
file2a='wc_'+file2a+'.txt'


Fene = input("Enter the lamp file you want to calibrate with: ")

aperture_FeNe(Fene,file)

file3 = re.sub('\.fits$', '', Fene)

file3=file3+'.ms.fits'

file4='wc'+file2
identify(file3)

refspec(file2,file3)
dispcor(file2)
splot(file4)
swrite(file4)
