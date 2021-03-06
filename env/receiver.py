# Copyright 2018 Francis Y. Yan, Jestin Ma
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

import time
import os
import os.path
import glob
import sys
import json
import socket
import select
import datagram_pb2
import project_root
from helpers.helpers import READ_FLAGS, ERR_FLAGS, READ_ERR_FLAGS, ALL_FLAGS



class Receiver(object):


    def __init__(self, ip, port,thid):
        self.thid = thid
        self.peer_addr = (ip, port)

        # UDP socket and poller
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.poller = select.poll()
        self.poller.register(self.sock, ALL_FLAGS)

    def cleanup(self):
        self.sock.close()

    def construct_ack_from_data(self, serialized_data):
        """Construct a serialized ACK that acks a serialized datagram."""

        data = datagram_pb2.Data()
        data.ParseFromString(serialized_data)

        ack = datagram_pb2.Ack()
        ack.seq_num = data.seq_num
        ack.send_ts = data.send_ts
        ack.sent_bytes = data.sent_bytes
        ack.delivered_time = data.delivered_time
        ack.delivered = data.delivered
        ack.ack_bytes = len(serialized_data)

        return ack.SerializeToString()

    def handshake(self):
        """Handshake with peer sender. Must be called before run()."""

        self.sock.setblocking(0)  # non-blocking UDP socket

        TIMEOUT = 1000  # ms

        retry_times = 0
        self.poller.modify(self.sock, READ_ERR_FLAGS)

        while True:
            self.sock.sendto('Hello from receiver', self.peer_addr)
            events = self.poller.poll(TIMEOUT)

            if not events:  # timed out
                retry_times += 1
                if retry_times > 10:
                    sys.stderr.write(
                        '[receiver] Handshake failed after 10 retries\n')
                    return
                else:
                    sys.stderr.write(
                        '[receiver] Handshake timed out and retrying...\n')
                    continue

            for fd, flag in events:
                assert self.sock.fileno() == fd

                if flag & ERR_FLAGS:
                    sys.exit('Channel closed or error occurred')

                if flag & READ_FLAGS:
                    msg, addr = self.sock.recvfrom(1600)

                    if addr == self.peer_addr:
                        if msg != 'Hello from sender':
                            # 'Hello from sender' was presumably lost
                            # received subsequent data from peer sender
                            ack = self.construct_ack_from_data(msg)
                            if ack is not None:
                                print("\n\n\n********************\nHERE WE GO\n***********************\n\n\n")
                                '''filepath = '/home/arramli/aaa-last/list.txt'
                                if os.path.isfile(filepath):
                                    fp = open(filepath, "r")
                                    line = fp.readline().strip()
                                    fp.close()
                                    line_time=int(line)/1000.0
                                    ############# DELAY ##############
                                    ############# DELAY ##############
                                    ############# DELAY ##############
                                    time.sleep(line_time) # 0.050 =50ms
                                    ############# DELAY ##############
                                    ############# DELAY ##############
                                    ############# DELAY ############## 
                                '''
                                self.sock.sendto(ack, self.peer_addr)
                        return

    def run(self):


        self.sock.setblocking(1)  # blocking UDP socket
        nnxnn=0
        while True:
            print("wwwwwwwwwwwwwww[ "+str(self.thid)+" ]wwwwwwwwwwwwwwwwww")

            path_here='data/'+"{:04d}".format(self.thid)+'_XX.txt'
            l2=sorted(glob.glob(path_here))
            print(l2)
            if len(l2)==1:
                print("EXIT IT ==> "+path_here)
                os.system("mv "+ path_here +" " + path_here.replace("XX.txt", "XX2AA.txt"))
                break
            else:
                print("Wait!")
		##################################
		path_here='data/'+'DONE.txt'
		lll=sorted(glob.glob(path_here))
		if(len(lll)>0):
		     os._exit(1) #sys.exit(1)
		##################################
            self.sock.settimeout(3)
            try:
                serialized_data, addr = self.sock.recvfrom(1600)
                print(len(serialized_data))
                if addr == self.peer_addr:
                    ack = self.construct_ack_from_data(serialized_data)
                    if ack is not None:
                        ############# DELAY ##############
                        ############# DELAY ##############
                        ############# DELAY ##############
                        #time.sleep(0.003) # 0.050 =50ms
                        ############# DELAY ##############
                        ############# DELAY ##############
                        ############# DELAY ##############
                        self.sock.sendto(ack, self.peer_addr)
                        print("n="+str(nnxnn))
                        nnxnn=nnxnn+1
                        #exit()
            except:
                print("hahahah")
            print("NEEEEEEXT\n")
