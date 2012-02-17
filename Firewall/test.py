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
ips=[]
counter=[]
li=0

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
function()
SSok=0
def ipsco():
    global matrix
    global counter,ips,li
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
ipsco()
def SScomm():
    global SSok,li,counter,ips
    def get_list(event):
        index = listbox.curselection()[0]
        seltext = listbox1.get(index)
        enter1.delete(0, 50)
        enter1.insert(0, seltext)
    frame = Frame(root)
    listbox1 = Listbox(frame,width=43)

    for i in range(0,li):
        listbox1.insert(END, counter[i])
    listbox = Listbox(frame,width=43)
    listbox.grid(row=0,column=2)
    yscroll = Scrollbar(frame,command=listbox.yview, orient=VERTICAL)
    yscroll.grid(row=0, column=1, sticky=N+S)
    for i in range(0,li):
        listbox.insert(END, ips[i])
    listbox.config(yscrollcommand=yscroll.set)
    enter1 =Entry(frame, width=5, bg='white',justify=CENTER)
    enter1.insert(0, '')
    enter1.grid(row=0, column=3)
    listbox.bind('<ButtonRelease-1>', get_list)
    lab=Label(root,width=51,height=11)
    if SSok==0:
        lab.destroy()
        frame.grid(row=1,column=0)
    else:
        frame.destroy()
        lab.grid(row=1,column=0)
        #lab.grid(row=2,column=2)
               
    SSok=1-SSok
        
def CHcomm():
    asd=1
    

#create a window
root=Tk()
root.geometry("640x480+400+100")
root.title("Squid-logs Statistics©                                                                               by Proxymus")
root.bind("<Escape>", lambda e: e.widget.quit())
root.resizable(TRUE,TRUE)
#Statistics-Site%
frbut=Frame(root,width=100)
frbut.grid(row=0,columnspan=2)
Label(frbut,text="      ").grid(row=0,column=0)
butSS=Button(frbut, text="Site%", command=SScomm,width="20")
butSS.grid(row=0,column=1)
butCH=Button(frbut, text="Chart", command=CHcomm,width="20")
butCH.grid(row=0,column=2)
root.mainloop()