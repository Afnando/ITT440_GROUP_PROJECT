import socket
import json
import sys
import os

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
   check = clientSocket.recv(2048).decode()

   if check == 'YES':
      quantity = input('Number quantity:')
      clientSocket.send(str.encode(quantity))        
      product =clientSocket.recv(2048).decode()
      print("Product select:",product)
      result=clientSocket.recv(2048).decode()
      print("Order Total:",result,)
      print("*-------------------------------*\n")  
    
   elif check == 'FINISH':
      
      ans = input("Do you want to delete item?>")
      clientSocket.send(str.encode(asn))
      fb = clientSocket.recv(2048).decode()
      
      ans1 = input("Enter the Product item name:")
      clientSocket.send(str.encode(ans1))
      fb1 = clientSocket.recv(2048).decode()
      
      ans2 = input("Cancel all this product?")
      clientSocket.send(str.encode(asn2))
      fb2 = clientSocket.recv(2048).decode()
      
      #recieve receipt file
      print('Session Ended')
      exit(0)
  
   elif check == 'NO':
      print("No Matched Item Code")

clientSocket.close()
