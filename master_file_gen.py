#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 19:24:30 2021

@author: mayanknarang
"""
import glob
import os
import shutil
from pyraf import iraf

import list_obs

print('Thank you for using my python scripts for the data reduction')



def masterbias(bias_list, output='Zero', combine='median', reject='avsigclip', ccdtype='', rdnoise=5.75, gain=0.28):

    bias=', '.join(bias_list) #convert array to IRAF readable list
    print('Creating master Bias')

    # load packages
    iraf.imred(_doprint=0)
    iraf.ccdred(_doprint=0)
    # unlearn settings
    iraf.imred.unlearn()
    iraf.ccdred.unlearn()
    iraf.ccdred.ccdproc.unlearn()
    iraf.ccdred.combine.unlearn()
    iraf.ccdred.zerocombine.unlearn()
    iraf.ccdred.setinstrument.unlearn()
    # setup task
    iraf.ccdred.zerocombine.output = output
    iraf.ccdred.zerocombine.combine = combine
    iraf.ccdred.zerocombine.reject = reject
    iraf.ccdred.zerocombine.ccdtype = ccdtype
    iraf.ccdred.zerocombine.rdnoise = rdnoise
    iraf.ccdred.zerocombine.gain = gain
    # run task
    iraf.ccdred.zerocombine(input=bias)
    
    
def mflat(bias_list, output='Flat', combine='median', reject='avsigclip', ccdtype='', rdnoise=5.75, gain=0.28):
    print('Creating master Flat')
    bias=', '.join(bias_list) #convert array to IRAF readable list
   

    # load packages
    iraf.imred(_doprint=0)
    iraf.ccdred(_doprint=0)
    # unlearn settings
    iraf.imred.unlearn()
    iraf.ccdred.unlearn()
    iraf.ccdred.ccdproc.unlearn()
    iraf.ccdred.combine.unlearn()
    iraf.ccdred.zerocombine.unlearn()
    iraf.ccdred.setinstrument.unlearn()
    # setup task
    iraf.ccdred.zerocombine.output = output
    iraf.ccdred.zerocombine.combine = combine
    iraf.ccdred.zerocombine.reject = reject
    iraf.ccdred.zerocombine.ccdtype = ccdtype
    iraf.ccdred.zerocombine.rdnoise = rdnoise
    iraf.ccdred.zerocombine.gain = gain
    # run task
    iraf.ccdred.zerocombine(input=bias)


def mscience(bias_list, values, combine='median', reject='avsigclip', ccdtype='', rdnoise=5.75, gain=0.28):
    print('Creating master Science')
    count=0
    while (count<len(values)):
        
        
        bias=', '.join(bias_list[count]) #convert array to IRAF readable list
        print(values[count],'=',bias)
       
    
        # load packages
        iraf.imred(_doprint=0)
        iraf.ccdred(_doprint=0)
        # unlearn settings
        iraf.imred.unlearn()
        iraf.ccdred.unlearn()
        iraf.ccdred.ccdproc.unlearn()
        iraf.ccdred.combine.unlearn()
        iraf.ccdred.zerocombine.unlearn()
        iraf.ccdred.setinstrument.unlearn()
        # setup task
        iraf.ccdred.zerocombine.output = values[count]
        iraf.ccdred.zerocombine.combine = combine
        iraf.ccdred.zerocombine.reject = reject
        iraf.ccdred.zerocombine.ccdtype = ccdtype
        iraf.ccdred.zerocombine.rdnoise = rdnoise
        iraf.ccdred.zerocombine.gain = gain
        # run task
        iraf.ccdred.zerocombine(input=bias)
        
        count=count+1


def flat_bc(operand1='Flat.fits',operand2='Zero.fits',op='-',result='bc_Flat'):
        print('Doing Bias correction of flat')
        iraf.imutil()
        iraf.imutil.imarith.unlearn()    
        iraf.imarith(operand1=operand1,operand2=operand2,op=op,result=result)  
        
        
        
        
def scie_bc(target,operand2='Zero.fits',op='-'):
        print('Doing Bias correction for all Science targets')
        count=0
        aa=[]
        while(count<len(target)):
            iraf.imutil()
            iraf.imutil.imarith.unlearn()
            opp=target[count]+'.fits'
            print(opp)
            iraf.imarith(operand1=opp,operand2=operand2,op=op,result='bc_'+opp)  
            aa.append('bc_'+opp)
            count=count+1
        return aa
    
    
def scie_fc(target,operand2='bc_Flat.fits',op='/'):
        print('Doing Flat field corection for all Science targets')
        count=0
        aa=[]
        while(count<len(target)):
            iraf.imutil()
            iraf.imutil.imarith.unlearn()
            opp=target[count]
            print(opp)
            iraf.imarith(operand1=opp,operand2=operand2,op=op,result='fc_'+opp)  
            aa.append('fc_'+opp)
            count=count+1
        return aa    
    
print('Gennarating object list')
a=list_obs.make_list()
masterbias(a[0])
mflat(a[1])
mscience(a[4],a[3])
flat_bc()
sc_bc=scie_bc(a[3])
scie_fc(sc_bc)   


print('Now run the run_apall.py file')



