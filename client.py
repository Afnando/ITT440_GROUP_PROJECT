import socket
import json

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
   clientSocket.send(str.encode(option))
   product =clientSocket.recv(2048).decode()
   print("Product select:",product)
   result=clientSocket.recv(2048).decode()
   print("Order Total:",result,)
   print("*-------------------------------*\n")

clientSocket.close()
