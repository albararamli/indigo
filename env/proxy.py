#****************************************************
#                                                   *
#               HTTP PROXY                          *
#               Version: 1.0                        *
#               Author: Luu Gia Thuy                *
#                                                   *
#****************************************************


import os,sys,thread,socket
from sender import Sender
#from dagger.run_sender import get_sender
#from run_receiver import get_receiver
from contextlib import closing
from threading import Thread, Lock
import time, subprocess
from time import sleep
import glob

#mutex=Lock()

#********* CONSTANT VARIABLES *********
BACKLOG = 50            # how many pending connections queue will hold
MAX_DATA_RECV = 1500  # max number of bytes we receive at once
DEBUG = True            # set to True to see the debug msgs
BLOCKED = []            # just an example. Remove with [""] for no blocking at all.
TH_ID_G=0
#**************************************
#********* MAIN PROGRAM ***************
#**************************************
def main():
    os.system("rm -fR data/*")
    # check the length of command running
    if (len(sys.argv)<2):
        print "No port given, using :8080 (http-alt)" 
        port = 8080
    else:
        port = int(sys.argv[1]) # port from argument

    # host and port info.
    host = ''               # blank for localhost
    
    print "Proxy Server Running on ",host,":",port

    try:
        # create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuse the port -albara
        # associate the socket to host and port
        s.bind((host, port))

        # listenning
        s.listen(BACKLOG)
    
    except socket.error, (value, message):
        if s:
            s.close()
        print "Could not open socket:", message
        sys.exit(1)

    # get the connection from client
    while 1:
        conn, client_addr = s.accept()

        # create a thread to handle request
        thread.start_new_thread(proxy_thread, (conn, client_addr))
        
    s.close()
#************** END MAIN PROGRAM ***************

def printout(type,request,address):
    if "Block" in type or "Blacklist" in type:
        colornum = 91
    elif "Request" in type:
        colornum = 92
    elif "Reset" in type:
        colornum = 93

    print "\033[",colornum,"m",address[0],"\t",type,"\t",request,"\033[0m"

def find_free_port():
    #mutex.acquire()
    port = 0
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = s.getsockname()[1]
    #mutex.release()
    return port

#*******************************************
#********* PROXY_THREAD FUNC ***************
# A thread to handle request from browser
#*******************************************
def proxy_thread2(TH_ID,arrx, conn,ooo):
    print("Yiefe="+str(TH_ID))
    while 1:
        l=glob.glob('/home/arramli/aaa/pantheon/data/'+str(TH_ID)+'_*D.txt')
        for fname in l:
            print(fname)
            os.system("rm "+fname)
            os.system("rm "+  fname.replace("D.txt", "IN.txt"))
            data = arrx[   int(fname.split('_')[1])   ]
            conn.send(data)
        if ooo[0]==1:
            ooo[0]=2
            os.system("touch "+  fname.replace("D.txt", "X.txt"))

def proxy_thread(conn, client_addr):
    #mutex.acquire()
    global TH_ID_G
    TH_ID=TH_ID_G
    TH_ID_G=TH_ID_G+1
    ######################################
    fff=open("../ip.txt","r")
    ip=fff.read()
    ip=ip.rstrip()
    port = find_free_port()
    ######################################
    command_s = "src/wrappers/indigo.py sender " + str(port) + " "+str(TH_ID)#mm-delay 10 
    #os.system(command_s)
    os.system('gnome-terminal -e '+"'"+'sh -c "'+command_s+ ';exec bash"'+"'")

    #subprocess.Popen(command_s, stdout=subprocess.PIPE, shell=True)
    ######################################
    command_r = "src/wrappers/indigo.py receiver " + ip + " " + str(port) #mm-delay 10 
    #os.system(command_r)
    os.system('gnome-terminal -e '+"'"+'sh -c "'+command_r+ ';exec bash"'+"'")
    #subprocess.Popen(command_r, stdout=subprocess.PIPE, shell=True)
    ######################################
    #mutex.release()
    D_ID=0

    # get the request from browser
    request = conn.recv(MAX_DATA_RECV)

    # parse the first line
    first_line = request.split('\n')[0]

    # get url
    url = first_line.split(' ')[1]

    for i in range(0,len(BLOCKED)):
        if BLOCKED[i] in url:
            printout("Blacklisted",first_line,client_addr)
            conn.close()
            sys.exit(1)


    printout("Request",first_line,client_addr)
    # print "URL:",url
    # print
    
    # find the webserver and port
    http_pos = url.find("://")          # find pos of ://
    if (http_pos==-1):
        temp = url
    else:
        temp = url[(http_pos+3):]       # get the rest of url
    
    port_pos = temp.find(":")           # find the port pos (if any)

    # find end of web server
    webserver_pos = temp.find("/")
    if webserver_pos == -1:
        webserver_pos = len(temp)

    webserver = ""
    port = -1
    if (port_pos==-1 or webserver_pos < port_pos):      # default port
        port = 80
        webserver = temp[:webserver_pos]
    else:       # specific port
        port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
        webserver = temp[:port_pos]
    ooo={}
    ooo[0]=0
    try:
        # create a socket to connect to the web server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        s.connect((webserver, port))
        s.send(request)         # send request to webserver
        arrx = {}
        thread.start_new_thread(proxy_thread2, (TH_ID, arrx, conn,ooo))

        while 1:
            # receive data from web server
            data = s.recv(MAX_DATA_RECV)
            
            if (len(data) > 0):
                fff=open("data/"+str(TH_ID)+"_"+str(D_ID)+"_IN.txt","w")
                fff.close()
                # send to browser
                ###conn.send(data)
                arrx[D_ID]=data
                D_ID=D_ID+1
            else:
                if ooo[0]=="2":
                    break
                else:
                    ooo[0]="1"
                   

        s.close()
        conn.close()

    except socket.error, (value, message):
        if s:
            s.close()
        if conn:
            conn.close()
        printout("Peer Reset",first_line,client_addr)
        sys.exit(1)
#********** END PROXY_THREAD ***********
    
if __name__ == '__main__':
    main()

