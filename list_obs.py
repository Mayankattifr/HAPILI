import os
import numpy as np
from astropy.io import fits

try:
	os.remove('bc_Flat.fits')
except OSError:
	pass   

try:
	os.remove('Zero.fits')
except OSError:
	pass

try:
	os.remove('Flat.fits')
except OSError:
	pass   

import os, glob
for filename in glob.glob("*bc_*"):
    os.remove(filename) 
    
for filename in glob.glob("*_Tar*"):
    os.remove(filename) 

import glob

def make_list():

#convert aea files to .fits

    os.system('find . ! -iname \'*.fits\' -iname \'[aea]*\' -exec mv {} {}.fits \;')
    
    #print(glob.glob("*.fits"))
    
    file=glob.glob("*.fits")
    
    
    
    print('Reading the header to figure out the type of file i.e, bias, flat, lamp or object')
    
    count=0
    
    bia=[]
    lamp=[]
    flat=[]
    target=[]
    objects=[]
    
    while (count<len(file)):
        hdul = fits.open(file[count])[0]
        if(hdul.header['EXPTIME']==0.0):
            bia.append(file[count])
        elif(hdul.header['OBJECT']=='FeNe'):
            lamp.append(file[count])
        elif(hdul.header['OBJECT']=='Halogen'):
            flat.append(file[count])
        else:
            target.append(file[count])
            objects.append(hdul.header['OBJECT']+'_Tar')
        
        count=count+1
        
    objects=np.array(objects)
    
    target=np.array(target)
    
    mylist=np.vstack(( target,objects)).T
    
    values = set(map(lambda x:x[1], mylist))
    
    newlist = [[y[0] for y in mylist if y[1]==x] for x in values]
    values=list(values)
    
    print('Bias files = ', bia)
    print('Flat files = ', flat)
    print('Lamp files = ', lamp)
    
    count=0
    while (count<len(values)):
        print(values[count],'=',newlist[count])
        count=count+1
    
    print('Starting with bias correction and flat fielding')
    
    return (bia,flat,lamp,values,newlist) 
  
make_list()     
