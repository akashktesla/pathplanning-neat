import numpy as np
import matplotlib.pyplot as plt


def main():
    signal1 = [1,2,3,4,5,6,1,2,3,4,2,2,3,4]
    signal2 = [1,2,3,4,5,3,4,5,2,2,1,3,5,2]
    target =  [5,2,1,2,3,4,2,1,2,3,4,2,1,2]
    x = range(len(target))
    signals = [signal1,signal2]
    final_signal = antcolony(signals,target)
    plt.plot(x,signal1)
    plt.plot(x,signal2)
    plt.plot(x,target)
    plt.plot(x,target,"r*")
    plt.plot(x,final_signal,"r*")
    plt.show()

def antcolony(signals,target):
    correlation_list = []
    for i in signals:
        correlation_list.append(correlation(i,target))
    pheromones_list = []
    for j in correlation_list:
        pheromones_list.append(pheromones(j))
    _max = max(pheromones_list)
    index = pheromones_list.index(_max)
    return signals[index]
    

def mod(a):
    if a>0:
        return a
    else:
        return -a

#a,b -> signals
def correlation(a,b):
    returns = []
    for i in range(len(a)):
        val = a[i]-b[i]
        val = mod(val)
        print(val)

    return returns 



def pheromones(a):

    return sum(a)

if __name__ == "__main__":
    main()
