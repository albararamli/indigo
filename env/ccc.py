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
        path_here='data/'+"{:04d}".format(TCP_TH_ID)+'*_IN.txt'
        l2xx=sorted(glob.glob(path_here))

        #path_here='data/'+"{:04d}".format(TCP_TH_ID)+'*_D.txt'
        #l2x=sorted(glob.glob(path_here))

        path_here='data/'+"{:04d}".format(TCP_TH_ID)+'_X.txt'
        l2=sorted(glob.glob(path_here))

        if len(l2)==1 and len(l2xx)==0: #len(l2x)==0 and
            print("EXIT IT ==> "+path_here)
            os.system("mv "+ path_here +" " + path_here.replace("X.txt", "XX.txt"))
            os._exit(1) #sys.exit(1)

        path_here='data/'+'DONE.txt'
        l1=sorted(glob.glob(path_here))
        if(len(l1)>0):
            os._exit(1) #sys.exit(1)
        time.sleep(1)
        ###############



def main():
    global TCP_TH_ID
    print "This is the name of the script: ", sys.argv[0]
    print "Number of arguments: ", len(sys.argv)
    print "The arguments are: " , str(sys.argv)
    print "The ip are: " , str(sys.argv[1])
    print "The port are: " , str(sys.argv[2])
    print "The th_id are: " , str(sys.argv[3])


    TCP_IP = str(sys.argv[1]) #'127.0.0.1'
    TCP_PORT = int(sys.argv[2]) #5005
    TCP_TH_ID = int(sys.argv[3]) #0
    BUFFER_SIZE = 1500
    MESSAGE = 'x' * 1400
    thread.start_new_thread(proxy_thread0,())
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((TCP_IP, TCP_PORT))

    ########################################
    #import subprocess
    ########################################
    while True:
        fname=""
        if fname=="":
            l=sorted(glob.glob('data/'+"{:04d}".format(TCP_TH_ID)+'_*IN.txt'))
            #getVersion =  subprocess.Popen("ls data/", shell=True, stdout=subprocess.PIPE).stdout
            #version =  getVersion.read()
            #print("My version is", version.decode())
            #print('data/'+"{:04d}".format(TCP_TH_ID)+'_*IN.txt')
            #print(l)
            if len(l)>0:
                fname= l[0]
                print(fname)
                #os.system("rm "+ fname)
                os.system("mv "+ fname + ' ' +  fname.replace("IN.txt", "D.txt"))
                #
                #self.send()
                s.send(MESSAGE)
                #s.settimeout(3)
                print("Wait server to confirm the req")
                data = s.recv(BUFFER_SIZE)
                print("---")
                if data:
                    print "sent/received data:", " GOOD" #data
                else:
                    print("LOST")
    ########################################
    ########################################
    s.close()

    #import os
    #os.system('read -p "Press [Enter] to continue...')

if __name__ == '__main__':
    main()
