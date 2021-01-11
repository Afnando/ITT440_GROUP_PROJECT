import socket
import json
import sys
import os
import struct

clientSocket = socket.socket()
host = "192.168.120.11"
port = 8888

try:
  clientSocket.connect((host,port))

except socket.error as e:
  print(str(e))

response = clientSocket.recv(1024).decode()
d = json.loads(response)
while True:
   print("Skincare Supplier")
   print("-----------------")
   for keys in d.keys():
         name , cost = d[keys]
         print('Item Code ->',keys,'Product -> :',name,'\n','The cost is :',cost)
   
   option = input('\nYour option:')
   clientSocket.send(str.encode(option.strip()))
   check = clientSocket.recv(1024).decode()
   if check == 'YES':
      quantity = input('Number quantity:')
      clientSocket.send(str.encode(quantity))
      product =clientSocket.recv(2048).decode()
      print("\n*-------------------------------*")
      print("Product select:",product)
      result=clientSocket.recv(2048).decode()   
      amount,total = result.split('-')
      print("Product sum:RM",amount)
      print("Order Total:",result,)
      print("*-------------------------------*\n")
 elif check == 'FINISH':

      #recieve receipt file
      received = clientSocket.recv(1024).decode()
      filename = received
      with open(filename,"wb") as f:

         data=clientSocket.recv(1024)
         f.write(data)
         f.close()

      print('Session Ended')
      exit(0)

   elif check == 'NO':
      print("No Matched Item Code!!!\n")

clientSocket.close()
