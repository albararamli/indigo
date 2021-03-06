#!/usr/bin/env python
import glob
import os,sys,thread,socket
from threading import Thread, Lock
#_db_lock=threading.Lock()

import time, subprocess
from time import sleep

TCP_TH_ID=0
def proxy_thread0():
    global TCP_TH_ID
    while True:
        #print("yyy")
        ###############
        path_here='data/'+"{:04d}".format(TCP_TH_ID)+'_XX.txt'
        l2=sorted(glob.glob(path_here))
        #print(l2)
        if len(l2)==1:
            print("EXIT IT ==> "+path_here)
            os.system("mv "+ path_here +" " + path_here.replace("XX.txt", "XX2AA.txt"))

        path_here='data/'+'DONE.txt'
        l1=sorted(glob.glob(path_here))
        if(len(l1)>0 or len(l2)>0):
            os._exit(1) #sys.exit(1)
        time.sleep(1)
        ###############

def main():
    global TCP_TH_ID

    print(">>>")
    print "This is the name of the script: ", sys.argv[0]
    print "Number of arguments: ", len(sys.argv)
    print "The arguments are: " , str(sys.argv)
    print "The ip are: " , str(sys.argv[1])
    print "The port are: " , str(sys.argv[2])
    print "The th_id are: " , str(sys.argv[3])

    TCP_IP = str(sys.argv[1]) #'127.0.0.1'
    TCP_PORT = int(sys.argv[2]) #5005
    TCP_TH_ID = int(sys.argv[3]) #0
    BUFFER_SIZE = 1500  # Normally 1024, but we want fast response
    thread.start_new_thread(proxy_thread0,())

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP, TCP_PORT))

    print("starting now:")
    s.listen(1000)

    conn, addr = s.accept()
    print 'Connection address:', addr

    

    while 1:
        #conn.settimeout(1)
        #try:
        print("Wait sender to send a req")
        data = conn.recv(BUFFER_SIZE)
        #if not data: break
        if data:
            print "received data:", "THANKS" #data
            conn.send(data)  # echo
        else:
            print("LOST")

            #path_here='data/'+'DONE.txt'
            #l=sorted(glob.glob(path_here))
            #if(len(l)>0):
            #     os._exit(1) #sys.exit(1)
        #except:
            #print("NO NO NO")
    conn.close()
    s.close()
    #import os
    #os.system('read -p "Press [Enter] to continue...')

if __name__ == '__main__':
    main()
