import random
import numpy as np
import matplotlib.pyplot as plt  

class car:
    def __init__(self,name,ts,mvsold,avsold,leprice,heprice):
        self.name = name
        self.totalsales = ts
        self.leprice = leprice 
        self.heprice = heprice
        self.mvsold = mvsold
        self.avsold = avsold


def plot1():

    #difference between center of the original object and object's virtual position
    plt.xlabel("Frames")
    plt.ylabel("Center distance error")
    plt.title("")
    y = []
    for i in range(1000):
        if random.randint(0,4)==3:
            y.append(random.randint(2,6))
        else:
            y.append(random.uniform(3,5))
    x = list(range(0,1000))
    plt.plot(x,y)
    plt.show()
def plot2():
    x = [4,2,-2,-5,-5,-6,-7,-7,-6,-5,-5,-4,-2,-1,-1, 2, 1, 1, 2, 4, 5,5,2,1,1,2,5,6,6,5]
    y = [6,8, 8, 5,-2,-2,-1, 2, 3, 3,-6,-7,-7,-6,-3,-3,-3,-6,-7,-7,-6,1,1,2,4,5,5,4,2,1]
    plt.plot(x,y)
    plt.show()


class mov:
    def __init__(self,frame,mov):
        self.frame = frame
        self.mov = mov

def genrand(flag):
    match flag:
        case 1:
            return random.uniform(2,3)
        case 2:
            return random.uniform(3,4)
        case 3:
            return random.uniform(4,5)
        case 4:
            return random.uniform(5,6)

def geny(fm):
    returns = []
    flag = 1
    count = 0
    for i in range(200):
        if i == fm[count].frame:
            returns.append(genrand(fm[count].mov))
            if count<len(fm)-1:
                count+=1
        else:
            returns.append(genrand(flag))
    return returns

def plot3():
    fm = [mov(10,1),mov(24,2),mov(50,1),mov(77,4),mov(80,3),mov(120,2),mov(152,3)]
    y = geny(fm)
    x = list(range(200))
    plt.xlabel("Frames")
    plt.ylabel("center error")
    plt.plot(x,y)
    plt.show()


def main():
    plot2()
    
main()
