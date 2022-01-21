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
    file=np.sort(file)
    
    
    
    print('Reading the header to figure out the type of file i.e, bias, flat, lamp or object')
    #print(file)

    
    count=0
    
    bia=[]
    lamp_FENE=[]
    lamp_FEHE=[]
    flat=[]
    target=[]
    target1=[]
    objects=[]
    objects1=[]

    
    while (count<len(file)):
	
        hdul = fits.open(file[count], ignore_missing_end=True)[0]
        #print(file[count])
        #print(hdul.header['COMMENT'])
        if(hdul.header['EXPTIME']==0.0):
            bia.append(file[count])
        elif("amp" in hdul.header['OBJECT'] and "r7" in str(hdul.header['COMMENT'])):
            
            lamp_FEHE.append(file[count])  
            
        elif("amp" in hdul.header['OBJECT'] and "r8" in str(hdul.header['COMMENTX'])):
            lamp_FENE.append(file[count])
      
        elif(hdul.header['OBJECT']=='Halogen'):
            flat.append(file[count])
        else:
            if("r7" in str(hdul.header['COMMENT']) or "r7" in str(hdul.header['COMMENTX'])):
               target.append(file[count])
               objects.append(hdul.header['OBJECT']+'_Gr7_Tar')
            elif("r8" in str(hdul.header['COMMENT']) or "r8" in str(hdul.header['COMMENTX'])):
               target.append(file[count])
               objects.append(hdul.header['OBJECT']+'_Gr8_Tar')            
        
        count=count+1
        
    objects=np.array(objects)
    
    target=np.array(target)
    
    mylist=np.vstack(( target,objects)).T
    
    values = set(map(lambda x:x[1], mylist))
    
    newlist = [[y[0] for y in mylist if y[1]==x] for x in values]
    values=list(values)
    

    
    print('Bias files = ', bia)
    print('Flat files = ', flat)
    print('Lamp FENE files = ', lamp_FENE)
    print('Lamp FEHE files = ', lamp_FEHE)
    
    count=0
    while (count<len(values)):
        print(values[count],'=',newlist[count])
        count=count+1
        

    
    print('Starting with bias correction and flat fielding')
    
    return (bia,flat,lamp_FENE,values,newlist) 
  
make_list()     
