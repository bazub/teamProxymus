'''
Created on Feb 15, 2012

@author: ubuntu
'''
'''
VARIABLES USED

time= timestamp
IP= originating IP


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
    #Select timestamp (no miliseconds)
    while 1:
        if(line[i]=='.'):
            time=int(line[0:i])
        if(line[i]==' '):
            break
        i=i+1
    while line[i]==' ':
        i=i+1
    #Select elapsed
    while 1:
        if(line[i]==' '):
            break
        i=i+1
    while line[i]==' ':
        i=i+1
    #Select IP
    aux=i
    while 1:
        if(line[i]==' '):
            IP=line[aux:i]
            break
        i=i+1
    #Select TCP_HIT/MISS/etc
    i=i+1
    aux=i    
    ret=""
    while 1:
        if(line[i]=='/'):
            ret=line[aux:i]
            while line[i]!=' ':
                i=i+1
            break
        i=i+1
    
    
        
        