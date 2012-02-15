'''
Created on Feb 15, 2012

@author: ubuntu
'''
filer="/home/ubuntu/access.log"
f=open(filer,"r")
filew="/home/ubuntu/access.log.bak"
g=open(filew,"w")
while 1:
    line=f.readline()
    if not line: break
    i=0
    c=0
    for i in line:
        c=c+1
    i=0
    while 1:
        if(line[i]=='.'):
            time=int(line[0:i])
        if(line[i]==' '):
            break
        i=i+1
    while line[i]==' ':
        i=i+1
    while 1:
        if(line[i]==' '):
            break
        i=i+1
    while line[i]==' ':
        i=i+1

    
    
        
        