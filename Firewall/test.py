'''
Created on Feb 15, 2012

@author: ubuntu
import subprocess
subprocess.call
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
li=[IP,action,meth,link,cont,time]

subprocess.call("scp root@192.168.1.106:/var/log/squid/access.log /home/ubuntu/")
'''
from tkinter import *
from math import *
import os
from tkinter.messagebox import *
from tkinter.filedialog import *
import subprocess

matrix=[]
links=[]
counter=[]
li=0
ips=[]
cips=[]
IPip=0
#subprocess.call("scp root@192.168.1.106:/var/log/squid/access.log /home/ubuntu/")
fsize=os.path.getsize("/home/ubuntu/access.log")

def function():
    global matrix 
    matrix=[]
    #subprocess.call("scp root@192.168.1.106:/var/log/squid/access.log /home/ubuntu/")
    filer="/home/ubuntu/access.log"
    f=open(filer,"r")

    c=0
    
    while 1:
        li=[]
        line=f.readline()
        if not line: 
            break
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
        li=[IP,action,meth,link,cont,flink,time]
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
    #subprocess.call("scp root@192.168.1.106:/var/log/squid/access.log /home/ubuntu/")
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
    min=7
    if li<min:
        min=li
    for i in range(0,min):
        listbox2.insert(END, links[i])
    listbox2.insert(END,"Others")
    listbox2.config(yscrollcommand=yscroll.set)
    listbox3 = Listbox(frame,width=7)
    listbox3.grid(row=0,column=3)
    s=0
    for i in range(0,min):
        listbox3.insert(END, str(ceil(counter[i]/tot*100))+'%')
        s=s+counter[i]
    listbox3.insert(END,str(floor((tot-s)/tot*100))+'%')
    canvas=Canvas(frame,width=200,height=156,border=3,relief="groove",bg="white")
    canvas.grid(row=0,column=4)
    x=5
    colors=["cyan","red","orange","yellow","green","blue","gray","purple"]
    for i in range(0,min):
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
def nt(time):
    year=1970
    months=(31,28,31,30,31,30,31,31,30,31,30,31)
    monthso=(31,29,31,30,31,30,31,31,30,31,30,31)
    cm=0
    d=0
    h=0
    m=0
    s=0
    mon=("January","February","March","April","May","June","July","August","September","October","November","December")
    while time>0:
        if year%4!=0 and time>=31536000:
            year=year+1
            time=time-31536000
        elif time>=31622400:
            year=year+1
            time=time-31622400
        else:
            if year%4!=0:
                for mo in months:
                    if time>=mo*24*60*60:
                        cm=cm+1
                        time=time-mo*24*60*60
                    else:
                        while time>=24*60*60:
                            d=d+1
                            time=time-24*60*60
                        while time>=60*60:
                            h=h+1
                            time=time-60*60
                        while time>=60:
                            m=m+1
                            time=time-60
                        s=time
                        time=0
                        break
            else:
                for mo in monthso:
                    if time>=mo*24*60*60:
                        cm=cm+1
                        time=time-mo*24*60*60
                    else:
                        while time>=24*60*60:
                            d=d+1
                            time=time-24*60*60
                        while time>=60*60:
                            h=h+1
                            time=time-60*60
                        while time>=60:
                            m=m+1
                            time=time-60
                        s=time
                        time=0
                        break
    cm=mon[cm]
    if h<10:
        h='0'+str(h)
    if m<10:
        m='0'+str(m)
    if s<10:
        s='0'+str(s)
    return(str(h)+':'+str(m)+':'+str(s)+' '+str(d)+' '+cm+' '+str(year)+"\t")
def LIcomm():
    global IPi,matrix,IPip
    try:
        if IPi>0:
            f=0
            f=asksaveasfilename(defaultextension=".log",filetypes=[("Log file",".log"),("text",".txt")],initialdir="~/")
            if(f!=0 and len(f)):
                fout=open(f,"w")
                for line in matrix:
                    if str(line[0])==str(IPip):
                        time=nt(line[-1])
                        fout.write(time+IPip+'\t'+line[-2]+'\n')
                showwarning(" ","The full history has been\n saved successfuly")
                fout.close()
            
    except NameError:
        asd=1
IPok=0
def IPcomm():
    global ips,IPok,matrix,cips,SSok,CHok,IPi,IPip
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
    def get_list(event):
        global IPi,IPip
        IPi= int(listbox4.curselection()[0])
        IPip=listbox4.get(IPi)
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
    listbox4.bind('<ButtonRelease-1>', get_list)
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
Label(root,height=4).grid(row=5,column=0)
photo=PhotoImage(file="image.gif")
ca=Canvas(root,height=80,width=434)
ca.create_image(329,29,image=photo)
ca.grid(row=7,column=0,sticky=W)
root.mainloop()