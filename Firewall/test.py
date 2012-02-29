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
from math import *
import os

matrix=[]
links=[]
counter=[]
li=0
ips=[]
cips=[]
fsize=os.path.getsize("/home/ubuntu/access.log")
print(fsize)

def function():
    global matrix 
    matrix=[]
    filer="/home/ubuntu/access.log"
    f=open(filer,"r")
    #filew="/home/ubuntu/access.log.bak"
    #g=open(filew,"w")
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
        li=[IP,action,meth,link,cont,time]
        matrix.append(li)
    f.close()
function()
def ipsco():
    global matrix
    global counter,links,li,tot
    counter=[]
    links=[]
    li=0
    tot=0
    for line in matrix:
        tot=tot+1
        site=line[3]
        ok=0
        c=0
        for i in links:
            if site==i:
                counter[c]=counter[c]+1
                ok=1
                break
            c=c+1
        if ok==0:
            links.append(site)
            counter.append(1)
            li=li+1
ipsco()
li2=0
def ipblocked():
    global matrix,li2,cips,ips
    cips=[]
    ips=[]
    li2=0
    for line in matrix:
        ip=line[0]
        ok=0
        c=0
        for i in ips:
            if ip==i:
                cips[c]=cips[c]+1
                ok=1
                break
            c=c+1
        if ok==0:
            ips.append(ip)
            cips.append(1)
            li2=li2+1
ipblocked()

def sortipsco():
    global counter,links
    for i in range(li):
        for j in range(i+1,li):
            if(counter[j]>counter[i]):
                aux=counter[j]
                counter[j]=counter[i]
                counter[i]=aux
                aux=links[j]
                links[j]=links[i]
                links[i]=aux
sortipsco()

def finit():
    global fsize
    b=os.path.getsize("/home/ubuntu/access.log")
    if b!=fsize:
        fsize=b
        function()
        ipsco()
        ipblocked()
        sortipsco()
    
SSok=0
def SScomm():
    global SSok,li,counter,links,CHok,IPok
    finit()
    CHok=0
    IPok=0
    def get_list(event):
        index = listbox.curselection()[0]
        seltext = listbox1.get(index)
        enter1.delete(0, 50)
        enter1.insert(0, seltext)
    lab=Label(root,width=71,height=11)
    lab.grid(row=1,column=0,sticky=W)
    frame = Frame(root)
    listbox1 = Listbox(frame,width=43)
    for i in range(0,li):
        listbox1.insert(END, counter[i])
    listbox = Listbox(frame,width=43)
    listbox.grid(row=0,column=2)
    yscroll = Scrollbar(frame,command=listbox.yview, orient=VERTICAL)
    yscroll.grid(row=0, column=1, sticky=N+S)
    for i in range(0,li):
        listbox.insert(END, links[i])
    listbox.config(yscrollcommand=yscroll.set)
    enter1 =Entry(frame, width=5, bg='white',justify=CENTER)
    enter1.insert(0, '')
    enter1.grid(row=0, column=3)
    listbox.bind('<ButtonRelease-1>', get_list)
    
    if SSok==0:
        #lab.destroy()
        frame.grid(row=1,column=0,sticky=W)
    else:
        #frame.destroy()
        lab.grid(row=1,column=0,sticky=W)
        #lab.grid(row=2,column=2)
               
    SSok=1-SSok
CHok=0        
def CHcomm():
    global CHok,counter,links,SSok,IPok
    finit()
    SSok=0
    IPok=0
    lab=Label(root,width=71,height=11)
    lab.grid(row=1,column=0,sticky=W)
    frame=Frame(root)
    listbox2 = Listbox(frame,width=36)
    listbox2.grid(row=0,column=2)
    yscroll = Scrollbar(frame,command=listbox2.yview, orient=VERTICAL)
    yscroll.grid(row=0, column=1, sticky=N+S)
    for i in range(0,7):
        listbox2.insert(END, links[i])
    listbox2.insert(END,"Others")
    listbox2.config(yscrollcommand=yscroll.set)
    listbox3 = Listbox(frame,width=7)
    listbox3.grid(row=0,column=3)
    s=0
    for i in range(0,7):
        listbox3.insert(END, str(ceil(counter[i]/tot*100))+'%')
        s=s+counter[i]
    listbox3.insert(END,str(floor((tot-s)/tot*100))+'%')
    canvas=Canvas(frame,width=200,height=156,border=3,relief="groove",bg="white")
    canvas.grid(row=0,column=4)
    x=5
    colors=["cyan","red","orange","yellow","green","blue","gray","purple"]
    for i in range(0,7):
        canvas.create_rectangle(0, x, ceil(counter[i]/tot*200), x+12, fill=colors[i])
        x=x+16
        
    canvas.create_rectangle(0,x,floor((tot-s)/tot*200),x+12,fill=colors[7])
        
    
    if CHok==0:
        #lab.destroy()
        frame.grid(row=1,column=0,sticky=W)
    else:
        #frame.destroy()
        lab.grid(row=1,column=0,sticky=W)
    CHok=1-CHok
IPok=0
def LIcomm():
    asd=1
    

def IPcomm():
    global ips,IPok,matrix,cips,SSok,CHok
    finit()
    CHok=0
    SSok=0
    lab=Label(root,width=71,height=11)
    lab.grid(row=1,column=0,sticky=W)
    frame=Frame(root)
    listbox4 = Listbox(frame,width=36)
    listbox4.grid(row=0,column=2)
    yscroll = Scrollbar(frame,command=listbox4.yview, orient=VERTICAL)
    yscroll.grid(row=0, column=1, sticky=N+S)
    listbox4.insert(END,"  ")
    for i in range(0,li2):
        listbox4.insert(END, ips[i])
    listbox4.config(yscrollcommand=yscroll.set)
    listbox5 = Listbox(frame,width=7)
    listbox5.grid(row=0,column=3)
    listbox6 = Listbox(frame,width=7)
    listbox6.grid(row=0,column=4)
    listbox7 = Listbox(frame,width=7)
    listbox7.grid(row=0,column=5)
    listbox5.insert(END,"Allowed")
    listbox6.insert(END,"Denied")
    listbox7.insert(END,"Total")
    for i in range(0,li2):
        c=0
        for j in matrix:
            if j[0]==ips[i]:
                if j[1][4]=='D':
                    c=c+1
        listbox5.insert(END,str(cips[i]-c))
        listbox6.insert(END,str(c))
        listbox7.insert(END,str(cips[i]))
    butLI=Button(frame,text="history",command=LIcomm)
    butLI.grid(row=0,column=6)
    if IPok==0:
        #lab.destroy()
        frame.grid(row=1,column=0,sticky=W)
    else:
        #frame.destroy()
        lab.grid(row=1,column=0,sticky=W)
    IPok=1-IPok

#Main
root=Tk()
root.geometry("640x480+400+100")
root.title("Squid-logs Statistics©                                                                            by Proxymus")
root.bind("<Escape>", lambda e: e.widget.quit())
root.resizable(FALSE,FALSE)
#Statistics-Site%
def init():
    lab=Label(root,width=71,height=11)
    lab.grid(row=1,column=0)
init()
frbut=Frame(root,width=100)
frbut.grid(row=0)
Label(frbut,text="      ").grid(row=0,column=0)
butSS=Button(frbut, text="Sites", command=SScomm,width="20")
butSS.grid(row=0,column=1)
butCH=Button(frbut, text="Chart", command=CHcomm,width="20")
butCH.grid(row=0,column=2)
butIP=Button(frbut,text="IP stats",command=IPcomm,width="20")
butIP.grid(row=0,column=3)
root.mainloop()