import subprocess
from tkinter.messagebox import *
from tkinter import *
import datetime

root=Tk()
root.geometry("640x480+400+100")
root.title("HM HealthMonitor©                                                                    by Proxymus")
root.bind("<Escape>", lambda e: e.widget.quit())
root.resizable(FALSE,FALSE)
def PIcomm():
    '''
    a=subprocess.call("PING 10.140.16.2")
    print(a)
    if a:
        showwarning("ERROR!!","Your Apache server is down!")
    else:
        showwarning(" ","Your Apache serves is online!")
    '''
    ip="10.131.16.2"
    proc = subprocess.Popen("ping %s" % ip, shell=True,stdout=subprocess.PIPE)
    c=0
    while True:
            line = proc.stdout.readline()
            if line.strip() == "":
                pass
            else:
                #print (line.strip())
                if c==2:
                    what=line[0:-2]
                c=c+1
            if not line: break
    if c==12:
        showwarning(" ","Your Apache serves is online!")
        
    else:
        showwarning("ERROR!!","Your Apache server is down!\nCheck C:\Logs\webserver.log for details.\n\nBecause we know you are lazy\nwe will open the folder for you;)")
        now = datetime.datetime.now()
        try:
            doc = open('C:\Logs\webserver.log', 'a')
        except IOError:
            doc= open('C:\Logs\webserver.log','w')
        doc.write(now.strftime("%d-%m-%Y %H:%M")+'    ')
        doc.write(what.decode("utf-8"))
        doc.write('\n')
        doc.close
        subprocess.call("explorer C:\Logs")
Label(root,height=14).grid(row=0)
Label(root,width=21).grid(row=1,column=0)
butPI=Button(root, text="Check Apache", command=PIcomm,width="20")
butPI.grid(row=1,column=1)
fr=Frame(root)
fr.grid(row=2,columnspan=2)
photo=PhotoImage(file="image.gif")
ca=Canvas(fr,height=80,width=434)
ca.create_image(329,29,image=photo)
ca.grid(row=7,column=1,sticky=W)


root.mainloop()    