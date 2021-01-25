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

d = {'1':('Cleanser',30.45),'2':('Exfoliator',95.00),'3':('Serum',78.80),'4':('Su>
data = json.dumps(d)

m= 0
sum = 0
n = []
n1 = []
qty =0
sum2 = 0
tott=0
sum = 0
n = []

def process_start(s_sock):
  global data,sum,tott
  s_sock.send(str.encode(data))
  name1 = s_sock.recv(2048).decode('utf-8')
  s_sock.send(str.encode(name1))
  num = s_sock.recv(2048).decode('utf-8')
  s_sock.send(str.encode(num))

  n=[]
  while True:

    opt = s_sock.recv(2048)

    if str(opt.decode('ascii')) in d.keys():
      s_sock.send(b"YES")
      name,cost = d[str(opt.decode('ascii'))]
      qty = s_sock.recv(2048).decode('utf-8')
      s_sock.send(name.encode())
      print ('\nProduct selected -> :',name,'\n','Cost->:',"{:.2f}".format(cost))
      print(' Quantity->',qty)
      sum = float(qty)*float(cost)
      sum = "{:.2f}".format(sum)
      print(' Total->:RM',sum)
      s_sock.send(bytes(str(sum),'ascii'))

      #insert data to list
      n.append([name,cost,qty,sum])

    elif str(opt.decode('ascii')) == 'del':

       s_sock.send(b"DELETE")
       print(type(n))
       print (n)
       ans = s_sock.recv(2048).decode('utf-8')
       print (ans)

       if ans == "YES" or ans == "yes" or ans == "y":
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

             if ans2 == "YES" or ans =="yes" or ans == "y":

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
           z1 = str(tott)

    elif str(opt.decode('ascii')) == '99':

        s_sock.send(b"FINISH")
        t=[]
        tot1 =0
        tot2 = 0
        for list in range(len(n)):
              for value in range(len(n[list])):
                   qty1=n[list][2]
                   cost1=n[list][1]
                   tot1 = int(qty1)*float(cost1)
                   n[list][3] = tot1

              tot1 = n[list][3]
              tot2 = tot2+tot1

        tot2 = "{:.2f}".format(tot2)
        z1=str(tot2)
        #insert list to table
        x = (tabulate(n, headers=['Product Name','Price(RM)','Quantity','Amount(R>

        # write table into file
        receipt_file(x,name1,num,z1)

        send_file(name1)
        print("Connection ended",s_addr)
        break
    elif str(opt.decode('ascii')) == '00':
         s_sock.send(b"EXIT")
         print("Connection ended",s_addr)
         break

    else:
      s_sock.send(b"NO")
      print('No mathced item code')
     # continue

  s_sock.close()

def receipt_file(x,name1,num,z1):

  fn = name1 + '-'
  date_time = datetime.date.today()
  date_time_str = str(date_time)
  extension = ".txt"
  filename = fn + date_time_str + extension


  with open(filename,'w') as f:
    f.write("Personal Information\n")
   f.write("\nName: ")
    f.write(name1)
    f.write("\nNumber phone: ")
    f.write(num)
    f.write('\nTotal Price(RM): ')
    f.write(z1)
    f.write("\n\nOrder Information\n\n")
    f.close()

  with open(filename, 'a') as f:
      f.write(x)
      f.close()

def send_file(name1):

  f1 = name1 + '-'
  date_time = datetime.date.today()
  date_time_str = str(date_time)
  extension = ".txt"
  filename = f1 + date_time_str + extension

  s_sock.send(filename.encode())

  with open(filename,'rb') as f:
    sendF = f.read(1024)
    s_sock.sendall(sendF)
    f.close()


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

