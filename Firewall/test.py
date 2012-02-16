'''
Created on Feb 15, 2012

@author: ubuntu
'''
'''
VARIABLES USED

time= timestamp
IP= originating IP
action= TCP_X thingy
meth= Method (get/connect/etc)
link= Link (i.e. http://google.com)
flink= Full link (when meth==GET, i.e. http://google.com/blablabla/something)
cont=Content
li=temp line storage
matrix (global)=Stores log entries (only needed fields)
li=[IP,action,meth,link,cont]
'''
from tkinter import *

matrix=[]
def function():
    global matrix 
    filer="/home/ubuntu/access.log"
    f=open(filer,"r")
    filew="/home/ubuntu/access.log.bak"
    g=open(filew,"w")
    c=0
    
    while 1:
        li=[]
        line=f.readline()
        if not line: break
        i=0
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
        #Ignore elapsed
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
        while 1:
            if(line[i]=='/'):
                action=line[aux:i]
                aux=i+1
                while line[i]!=' ':
                    i=i+1
                break
            i=i+1
        #ignore Size
        i=i+1
        while 1:
            if(line[i]==' '):
                break
            i=i+1
        while line[i]==' ':
            i=i+1
        #Select Method  
        aux=i    
        while 1:
            if(line[i]==' '):
                meth=line[aux:i]
                break
            i=i+1      
        i=i+1
        #Select Link
        if(meth=="GET"):
            aux=i
            v=0
            while 1:
                if line[i]=='/':
                    v=v+1
                elif line[i]==' ':
                    flink=line[aux:i]
                    break
                if v==3:
                    link=line[aux:i]
                    v=v+1
                i=i+1
        elif meth=="CONNECT":
            aux=i
            while 1:
                if line[i]==' ':
                    link=line[aux:i]
                    break
                i=i+1
        #Add more methods?
        i=i+1
        #Ignore next_field
        while line[i]!=' ':
            i=i+1
        i=i+1
        while line[i]!=' ':
            i=i+1
        i=i+1
        #Select content
        cont=''
        if(action!="TCP_DENIED") & (meth!="CONNECT"):
            cont=line[i:-1]
        li=[IP,action,meth,link,cont]
        matrix.append(li)
def SScomm():
    global matrix
    ips=[]
    counter=[]
    li=0
    tot=0
    for line in matrix:
        tot=tot+1
        site=line[3]
        ok=0
        c=0
        for i in ips:
            if site==i:
                counter[c]=counter[c]+1
                ok=1
                break
            c=c+1
        if ok==0:
            ips.append(site)
            counter.append(1)
            li=li+1
    for i in range(0,li):
        print(ips[i]+' '+str(counter[i]))
        
        
function()
#create a window
root=Tk()
root.geometry("640x480+400+100")
root.title("Squid-logs Statistics©                                                                               by Proxymus")
root.bind("<Escape>", lambda e: e.widget.quit())
root.resizable(FALSE,FALSE)
#Statistics-Site%
butSS=Button(root, text="Site%", command=SScomm,width="40")
butSS.grid(row=1,column=1)

root.mainloop()
                   
        
        
        
        