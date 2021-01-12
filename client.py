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

d = {'1':('Cleanser',30.45),'2':('Exfoliator',95.00),'3':('Serum',78.80),'4':('Sunscreen',47.50)}
data = json.dumps(d)
m= 0
sum = 0
n = []
n1 = []
qty =0
sum2 = 0
tott=0

def process_start(s_sock):
  global data,sum,tott
  s_sock.send(str.encode(data))
  name1 = s_sock.recv(2048).decode('utf-8')
  s_sock.send(str.encode(name1))
  num = s_sock.recv(2048).decode('utf-8')
  s_sock.send(str.encode(num))

  n=[]
  while True:
   # name = s_sock.recv(2048)
   # s_sock.send(str.encode(name))
   # num = s_sock.recv(2048)
   # s_sock.send(str.encode(num))
    
    opt = s_sock.recv(2048)

    if str(opt.decode('ascii')) in d.keys():
    
      s_sock.send(b"YES")
      name,cost = d[str(opt.decode('ascii'))]
      qty = s_sock.recv(2048).decode('utf-8')
      print(qty)
      s_sock.send(name.encode())
      print ('Product selected -> :',name,'\n','Cost->:',cost)
      sum = float(sum) + (float(qty)*float(cost))
      print('Total->:',sum)
      s_sock.send(bytes(str(sum),'ascii'))
    
      #insert data to list
      n.append([name,cost,qty,sum])

    elif str(opt.decode('ascii')) == '99':

      s_sock.send(b"FINISH")
      print(type(n))
      print (n)
      ans = s_sock.recv(2048).decode('utf-8')
      print ("ans")
      print (ans)
      #sum2=0
     # for list in range(len(n)):
    #    for value in range(len(n[list])):
   #       name = n[list][0]
  #        cost = n[list][1]
 #         qty = n[list][2]
#          sum = n[list][1]*int(n[list][2])
       # sum2 = sum2 +sum
      #  n1.append([name,cost,qty,sum])
     #   print("n1")
    #    print (n1)
   #     print ("Sum:")
  #      print (sum)
 #       print ("Sum2:")
#        print (sum2)

      if ans == "YES":
        s_sock.send(bytes(str(ans),'ascii'))
        ans1 = s_sock.recv(2048).decode('utf-8')
        fb1 = [item[0] for item in n]
        res = [ele for ele in fb1 if(ele in ans1)]
        if bool(res) == True:
          s_sock.send(b"The Product exist") #fb1 in client
          ans2 = s_sock.recv(2048).decode('utf-8') #ans2 in client
          s_sock.send(bytes(str(ans2),'ascii')) #fb2 in client
          print ("fb1")
          print (fb1)

          if ans2 == "YES":

            tot2 =0
            tot =0
            for list in range(len(n)):
              for value in range(len(n[list])):
                qty1=n[list][2]
                cost1=n[list][1]
                tot1 = int(qty1)*float(cost1)
                n[list][3] = tot1
                if n[list][0] == ans1:
                  qty2 = n[list][2]
                  cost2=n[list][1]
                  tot=int(qty2)*float(cost2)
                  print(tot)
                  y = list
                  y1 = n[y][3]
              tot1 = n[list][3]
              tot2 = tot2+tot1 #total bef delete
            print(y)
            print("Delete list==>")
            del n[y]
            tot1 = tot1+tot1
            global tott1
            tott=0
            for i in range(len(n)):
              for j in range (len(n[i])):
                print(n[i][3])
                tott1= n[i][3]
              tott= tott+tott1
              print(tott)
            print (n) #lepas delete
            anss2 = s_sock.recv(2048).decode('utf-8')
            print (anss2)
            s_sock.send(bytes(str(anss2),'ascii'))
            anss3 = s_sock.recv(2048).decode('utf-8')
            print (anss3)
            s_sock.send(bytes(str(n),'ascii'))
            anss4 = s_sock.recv(2048).decode('utf-8')
            s_sock.send(bytes(str(tott),'ascii'))
      
      else:
        print("Client Dont delete anything..")
        sum2=0

        for list in range(len(n)):
          for value in range(len(n[list])):
            name = n[list][0]
            cost = n[list][1]
            qty = n[list][2]
            sum = n[list][1]*int(n[list][2])
          sum2 = sum2 +sum
          n1.append([name,cost,qty,sum])
          print (n1)
          tott= sum2
          print (sum2)
        n = n1.copy()
        print (n)

        s_sock.send(bytes(str(ans),'ascii'))
        print (ans)
        ans44=s_sock.recv(2048).decode('utf-8')
        print (ans44)
        s_sock.send(bytes(str(sum2),'ascii'))
        ans55 =s_sock.recv(2048).decode('utf-8')
        print (ans55)
        s_sock.send(bytes(str(n),'ascii'))
      #insert list to table
      x = (tabulate(n, headers=['Product Name','Price','Quantity','Amount(RM)'],tablefmt="grid",colalign=("center","center","center","center")))
      y = name1
      z = num
      z1 = str(tott)
      #write table into file
      receipt_file(x,y,z,z1)

      #send_file
      send_file()

      print("Connection endend")
      break

    else:
      s_sock.sendall(b"No")
      print('No mathced item code')
      continue


  s_sock.close()

def receipt_file(x,y,z,z1):
  date_time = datetime.date.today()
  date_time_str = str(date_time)
  extension = ".txt"
  filename = date_time_str + extension

  with open(filename,'w') as f:
    f.write("Name: ")
    f.write(y)
    f.write("\nNumber phone: ")
    f.write(z)
    f.write('\nTotal Price(RM): ')
    f.write(z1)
    f.write("\nOrder Information\n\n")
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

  with open(filename,'rb') as f:
    sendF = f.read(1024)
    s_sock.sendall(sendF)
    f.close()

def delete_detail(n,y):
  print ("y")
  print (y)
  print ("Nilai n")
  print ("n[0]")
  print (n[0])
  print ("n[1]")
  print (n[1])
  print ("Delete n[y]")
  print (n[y])
  del n[y]
  print ("N after")
  print (n)
  for i in range(len(n)):
    tot1 =0
    print("tot in func")
    for j in range(len(n[i])):
      tot= n[i][3]
      print (n[i][j])
    tot1= tot1+tot
    print (tot1)

if __name__ == '__main__':

  s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  s.bind(("",8888))
  print ('listening...')
  s.listen(3)

  try:
    while True:
      try:
        s_sock,s_addr = s.accept()
        print ("\nConnection from:", s_addr)
        p = Process(target = process_start,args = (s_sock,))
        p.start()

      except socket.error:
        print ('got a socket error')

  except Exception as e:
    print ('an exception occured!')
    print (e)

