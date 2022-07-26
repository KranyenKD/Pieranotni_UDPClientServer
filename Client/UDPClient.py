# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 00:32:42 2022

@author: Michael
"""
import socket as sk
import os
import time

def sendmsg(msg):
    try:
        sock.sendto(msg.encode(),server_address)
    except Exception as info:
            print(info)

def findFile(f):
    for filename in os.listdir("./Files"):
        if f == filename:
            return True
    return False  
        
sock = sk.socket(sk.AF_INET,sk.SOCK_DGRAM)
server_address = ('localhost',10000)  

flag = True
while flag:
     command = input("Insert Command->")
     if command.lower() == "list":
         sendmsg(command)
         data,addr =sock.recvfrom(32768)
         print("Server:")
         print(data.decode('utf8'))
     elif command.lower() == "close":
         print("Chiusura Collegamento...")
         sock.close()
         flag = False
     elif command.lower().startswith("get "):
         sendmsg(command)
         file_name = sock.recv(100).decode()
         if file_name == 'File didn\'t find':
             print('Server: File didn\'t find')
         else:
             print("File Name: " + file_name)
             file_size = sock.recv(100).decode()
             print("File Size: " +str( file_size))
       
             with open("./Files/" + file_name, "wb") as file:
                 s = 0
                 while s < int(file_size):
                     print("Reception In Progress..." + str(s) + "/" + str(file_size))
                     data = sock.recv(32768)
                     if not (data):
                         break
                     file.write(data)
                     s += len(data)
                    

           
                 print("File Received")
                 file.close()
     elif command.lower().startswith("put "):
         file_name = command.split('put ')[-1]
         if findFile(file_name):
             sendmsg(command)
             file_size = os.path.getsize("./Files/" + file_name)
             print("file size" + str(file_size))
             print("Nome file:"+file_name)
             sendmsg(file_name)
             sendmsg(str(file_size))
        
     
             with open("./Files/"+ file_name,"rb") as file:
                 s = 0
                 while s <= file_size:
                     print("Transfer In Progress... " + str(s) + "/" + str(file_size))
                     data = file.read(32768)
                     if not (data):
                         break
                     sock.sendto(data,server_address)
                     time.sleep(0.002)
                     s += len(data)
                 res = sock.recv(100).decode()
                 #print(res)
                 if res == 'OK':
                     print("File Transfered")  
                 else:
                    print('Error..Try Again') 
            
         else:
            print('File didn\'t find')
     else:
         print("Comando errato")