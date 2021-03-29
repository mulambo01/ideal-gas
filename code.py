from matplotlib import pyplot as plt
import numpy as np
import time
import math
import random
from mpl_toolkits import mplot3d

QtP=1000
Tmax=10
dt=0.01
QtT=int(Tmax/dt)
QD=3
pcm=np.zeros((QtT,QD))
vcm=np.zeros((QtT,QD))
P=np.zeros((QtT,QtP,QD))
V=np.zeros((QtT,QtP,QD))
qtR=0.

# P[0] = np.load("posi.npy")
# V[0] = np.load("veloc.npy")


def temper():
 i=0
 Ec=0
 while(i<QtP):
  Ec = Ec + V[0][i].dot(V[0][i])/2.
  i=i+1
 return Ec/(QtP+1)


i=0
while(i<QtP):
 vx=0.01*(random.randint(0,200)-100.)/100.
 vy=0.0001*(random.randint(0,200)-100.)/100.
 vz=(random.randint(0,200)-100.)/100.
 x=random.randint(0,100)/100.
 y=random.randint(0,100)/100.
 z=random.randint(0,100)/100.
 P[0][i][0]=x
 P[0][i][1]=y
 P[0][i][2]=z
 V[0][i][0]=vx
 V[0][i][1]=vy
 V[0][i][2]=vz
 i=i+1
np.save("posi.npy", P[0])
np.save("veloc.npy", V[0])

force=np.zeros((QtT))


def reflete(k):
 global qtR 
 j=0
 force[k]=0.
 while(j<QtP):
  i=0
  f=0
  while(i<QD):
   if(P[k][j][i]<0.):
    P[k][j][i]=-P[k][j][i]
    V[k][j][i]=-V[k][j][i]
    f=1
   elif(P[k][j][i]>1.):
    P[k][j][i]=2.-P[k][j][i]
    V[k][j][i]=-V[k][j][i]
    f=1
   i=i+1
  if(f==1):
   dV=(V[k][j]-V[k-1][j]).transpose()
   dV=dV.dot(dV)
   dV=math.sqrt(dV)/dt
   force[k]=force[k]+dV
  j=j+1
 if(force[k]!=0.):
  qtR=qtR+1
# print(force[k])

def cm(k):
 i=0
 while(i<QtP):
  pcm[k]=pcm[k]+P[k][i]
  vcm[k]=vcm[k]+V[k][i]
  i=i+1
 pcm[k]=pcm[k]/QtP
 vcm[k]=vcm[k]/QtP

cm(0)



iStart=20
i=1
press=0.
while(i<QtT):
 P[i]=P[i-1]+V[i-1]*dt
 V[i]=V[i-1]
 reflete(i)
 cm(i)
 i=i+1
# Mpress=force.transpose()
# Mpress=Mpress.dot(Mpress)
# Mpress=math.sqrt(Mpress)/(2*QD*QtT)
Mpress = np.sum(force)/(2*QD*QtT)

temperat=temper()
print("press:",Mpress)
print("temperat:",temperat)
print("k=", temperat/Mpress)


# tpause=0.1
# fig = plt.figure(figsize = (10, 7))
# ax = plt.axes(projection ="3d")
# plt.ion()
# ax.set_xlim3d([0.0, 1.0])
# ax.set_xlabel('X')
# ax.set_ylim3d([0.0, 1.0])
# ax.set_ylabel('Y')
# ax.set_zlim3d([0.0, 1.0])
# ax.set_zlabel('Z')
# ax.set_title('3D Test')

# i=0
# x=P[i].transpose()[0].tolist()
# y=P[i].transpose()[1].tolist()
# z=P[i].transpose()[2].tolist()

# sc=ax.scatter3D(x, y, z, color = "green")

# plt.draw()
# plt.pause(tpause)

# i=1
# while(i<QtT):
#  x=P[i].transpose()[0].tolist()
#  y=P[i].transpose()[1].tolist()
#  z=P[i].transpose()[2].tolist()
#  sc._offsets3d = ([x,y,z])
#  plt.pause(tpause)
#  plt.draw()
#  i=i+1


# i=0
# while(i<QtT):
# plt.xlim(0,1)
# plt.ylim(0,1)
# plt.zlim(0,1)
# plt.grid(True)
#  plt.ion()
#  plt.pause(0.1)
#  plt.clf()
#  plt.plot(pcm[i][0], pcm[i][1], "x")
#  plt.plot(P[i].transpose()[0].tolist(), P[i].transpose()[1].tolist(), "o")
#  plt.show()
#  i=i+1
