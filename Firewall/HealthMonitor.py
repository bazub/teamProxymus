import subprocess

root=Tk()
root.geometry("640x480+400+100")
root.title("Squid-logs Statistics©                                                                            by Proxymus")
root.bind("<Escape>", lambda e: e.widget.quit())
root.resizable(FALSE,FALSE)

while 1:
    a=subprocess.call("PING 10.140.32.74")
    if a:
        
    