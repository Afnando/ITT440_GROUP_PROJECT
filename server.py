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
sum = 0
n = []
qty = 0

def process_start(s_sock):
  global data,sum
  s_sock.send(str.encode(data))

  while True:
    opt = s_sock.recv(2048)

    if str(opt.decode('ascii')) in d.keys():

        s_sock.send(b"YES")
        name , cost = d[str(opt.decode('ascii'))]
        qty = s_sock.recv(2048).decode('utf-8')
        print(qty)        
        s_sock.send(name.encode())
        print('Product selected-> :',name,'\n','Cost-> :',cost)
        sum=float(sum)+(float(qty)*float(cost))
        print('Total->:',sum)
        s_sock.send(bytes(str(sum),'ascii'))

        #insert data to list
        n.append([name,cost,qty,sum])

    elif str(opt.decode('ascii')) == '99':
      
        s_sock.send(b"FINISH")
        #insert list to table
        x = (tabulate(n, headers=['Product Name', 'Price','Quantity','Amount(RM)'],tablefmt="grid",colalign=("center","center","center","center")))

        #write table into file
        receipt_file(x)
       
        # send_file()
        print("Connection endend")
        break

    else:
        s_sock.sendall(b"NO")
        print('No matched item code')
        continue

  s_sock.close()

def receipt_file(x):

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

      except socket.error:
        print('got a socket error')

  except Exception as e:
    print('an exception occured!')
    print(e)
