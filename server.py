import socket
import sys
import os
import time
import errno
from multiprocessing import Process
import math
import json
import datetime
from tabulate import tabulate

d = {'1':('Cleanser',30.45),'2':('Exfoliator ',95.00),'3':('Serum',78.80),'4':('Sunscreen',47.50)}
data = json.dumps(d)
amount=0
total=0
qty=0
n=[]
noProcess = 0

def process_start(s_sock):
  global data,sum
  s_sock.send(str.encode(data))

  while True:
    opt = s_sock.recv(2048)
     if str(opt.decode('ascii')) in d.keys():

        s_sock.send(b"YES")
        name , cost = d[str(opt.decode('ascii'))]
        qty = s_sock.recv(2048).decode('utf-8)
        s_sock.send(name.encode())
        print('Product selected-> :',name,'\n','Cost-> :',cost)
        amount = (int(qty)*float(cost))
        sum = "{:.2f}".format(amount)
        print('Total->RM:',amount)
        total = float(total)+float(amount)
        total = "{:.2f}".format(total)
        print('Big Total->:RM',total)
        #join sum and total
        out=str(amount)+"-"+str(total)
        s_sock.send(out.encode())
        #insert data to list
        n.append([name,cost,qty,amount,total])
      elif str(opt.decode('ascii')) == '99':

        s_sock.send(b"FINISH")
        #insert list to table
        x = (tabulate(n, headers=['Product Name', 'Price','Quantity','Amount(RM)','>

        #write table into file
        receipt_file(n)
        
        send_file()

        print("Connection end", s_addr)
        break

    else:
        s_sock.send(b"NO")
        print('No matched item code')
  s_sock.close()

def receipt_file(n):

  date_time = datetime.date.today()
  date_time_str = str(date_time)
  extension = ".txt"
  filename = date_time_str + extension

  with open(filename, 'w') as f:
      f.write("Order Information\n\n")
      f.close()
  with open(filename, 'a') as f:
      f.write(x)

  f.close()

def send_file():

  date_time = datetime.date.today()
  date_time_str = str(date_time)
  extension = ".txt"
  filename = date_time_str + extension
  s_sock.send(filename.encode())

  with open(filename, 'rb') as f:
      sentF = f.read(1024)
      s_sock.sendall(sentF)
      f.close()

if __name__ == '__main__':

  s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  s.bind(("",8888))
  print('listening...')
  s.listen(3)

  try:
    while True:
      try:
        s_sock,s_addr = s.accept()
        print ("\nConnection from : ", s_addr)
        p = Process(target = process_start,args = (s_sock,))
        p.start()
        noProcess += 1
        print("Client:" , str(noProcess))

      except socket.error:
        print('got a socket error')

  except Exception as e:
    print('an exception occured!')
    print(e)
