# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 00:24:24 2022

@author: Michael
"""

import socket as sk
import os
import time

def getFileList():
    file_list = ""
    for filename in os.listdir("./Files"):
        file_list = file_list + "\n" + filename
    return file_list

def findFile(f):
    for filename in os.listdir("./Files"):
        if f == filename:
            return True
    return False
 

sock = sk.socket(sk.AF_INET,sk.SOCK_DGRAM)
server_address = ('localhost', 10000)
sock.bind(server_address)
print('Server: ON')


while True:
    data,addr = sock.recvfrom(32768)
    client_msg = data.decode('utf8').lower()
    
    if client_msg == "list" :
        print("Client Sent List Command")
        message = getFileList()
        sock.sendto(message.encode(),addr)
    elif client_msg.startswith("get "):
        print("Client Sent Get Command")
        #print(client_msg)
        file_name = client_msg.split('get ')[-1]
        if findFile(file_name):
            
            file_size = os.path.getsize("./Files/" + file_name)        
            print("File Name: "+file_name)
            print("File Size: " + str(file_size))
            sock.sendto(file_name.encode(),addr)
            sock.sendto(str(file_size).encode(),addr)
        
            with open("./Files/"+ file_name,"rb") as file:
                s = 0
                while s <= file_size:
                    print("Transfer In Progress... " + str(s) + "/" + str(file_size))
                    data = file.read(32768)
                    if not (data):
                        break
                    sock.sendto(data,addr)
                    time.sleep(0.002)
                    s += len(data)
                
                print("File Transfered")
        else:
            message = 'File didn\'t find'
            sock.sendto(message.encode(),addr)
    elif client_msg.startswith("put "):
        print("Client Sent Put Command")
        print('started Receiving The File...')
        file_name = sock.recv(100).decode()
        print("File name: " +file_name)
        file_size = sock.recv(100).decode()
        print("File size: " +str( file_size))
        with open("./Files/" + file_name, "wb") as file:
            s = 0
            while s < int(file_size):
                print("Reception In Progress..." + str(s) + "/" + str(file_size))
                data = sock.recv(32768)
                if not (data):
                    break
                file.write(data)
                s += len(data)
                
            print("s = "+ str(s))
            print("size = "+ str(file_size))
            if str(s) == str(file_size):
                print("File Received")
                message = 'OK'
                sock.sendto(message.encode(),addr)
            else:
                message = 'NO'
                sock.sendto(message.encode(),addr)
                print("File Error")
           
            file.close()
    else:
       message = "Error"
       sock.sendto(message.encode(),addr)
    