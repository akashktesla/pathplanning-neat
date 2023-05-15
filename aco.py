import numpy as np
import matplotlib.pyplot as plt  
import time

def gen_target(img):
    x = np.random.randint(50, 450)
    y = np.random.randint(50, 450)
    img[y-50:y+50, x-50:x+50] = (0, 0, 255)
    # cv.rectangle(img, (x-50, y-50), (x+50, y+50), (0, 0, 255), -1)

def ex_tracking(img,target):
    target_vec = target.flatten()
    cor_list = []
    index_list = []
    for i in range(50,450):
        for j in range(50,450):
            spx,spy = i-50,j-50
            epx,epy = i+50,j+50
            roi = img[spy:epy,spx:epx]
            roi_vec = roi.flatten()
            cor = np.corrcoef(roi_vec,target_vec)[0,1]
            print(cor)
            if cor>0:
                cor_list.append(cor);
            else:
                cor_list.append(0)
            index_list.append((i,j))
    confidence = max(cor_list)
    _index = index_list.index(confidence).any()
    return _index,confidence
def aco_tracking(img,target,loop_count):
    target_vec = target.flatten()
    cor_list = []
    index_list = []
    for i in range(5):
        for j in range(5):
            spx,spy = i*100,j*100
            epx,epy = i*(100)+100, j*100+100
            roi = img[spy:epy,spx:epx]
            roi_vec = roi.flatten()
            cor = np.corrcoef(roi_vec,target_vec)[0,1]
            if cor>0:
                cor_list.append(cor);
            else:
                cor_list.append(0)
            index_list.append((i,j))
            # find best performing frames
            # spawn random ants on those frames 
            # localize the fucking shit
    _index = index_list[cor_list.index(max(cor_list))]
    confidence=max(cor_list)
    print(_index)
    i = _index[0]
    j = _index[1]
    spx,spy = i*100,j*100
    epx,epy = i*(100)+100, j*100+100
    print(spx,spy)
    print(epx,epy)
    loop_counter=0
    #loop
    while loop_counter<loop_count:
        cor_list,index_list = aco_loop(img,target,spx,spy,epx,epy)
        print(cor_list,index_list)
        confidence = max(cor_list)
        print(f"confidence: {confidence}")
        _index = index_list[cor_list.index(max(cor_list))]
        i = _index[0]
        j = _index[1]
        spx,spy = i-50,j-50
        epx,epy = i+50, j+50
        loop_counter+=1
    return _index,confidence

def aco_loop(img,target,spx,spy,epx,epy):
    target_vec = target.flatten()
    cx=int((spx+epx)/2)
    cy=int((spy+epy)/2)
    ant_list = [(cx,cy)]
    ant_count = 0
    while ant_count<10:
        x = np.random.randint(spx,epx)
        y = np.random.randint(spy,epy)
        if x>50 and x<450 and y>50 and y<450:
            ant_list.append((x,y))
            ant_count+=1

    cor_list = []
    index_list = []
    for i in ant_list:
        # print(i)
        sx = i[0]-50
        sy = i[1]-50
        ex = i[0]+50
        ey = i[1]+50
        roi = img[sy:ey,sx:ex]
        roi_vec = roi.flatten()
        cor = np.corrcoef(roi_vec,target_vec)[0,1]
        if cor>0:
            cor_list.append(cor);
            index_list.append((i[0],i[1]))
        else:
            cor_list.append(0)
            index_list.append((i[0],i[1]))
    return cor_list,index_list

if __name__=="__main__":
    img = 255 * np.zeros((500, 500, 3), dtype=np.uint8)
    target = np.zeros((100, 100, 3), dtype=np.uint8)
    target[:, :] = (0, 0, 255)
    # x = list(range(1000))
    # y = []
    # for i in range(1000):
    #     img = 255 * np.zeros((500, 500, 3), dtype=np.uint8)
    #     gen_target(img)
    #     st = time.time()
    #     _index,conf = aco_tracking(img,target,loop_count=0)
    #     _time = time.time()-st
    #     y.append(conf)
    # print(x,y)
    # print("==============================================")
    # print(f"min: {min(y)}")
    # print(f"max: {max(y)}")
    # print(f"avg: {sum(y)/len(y)}")
    # plt.plot(x,y,label="loop_count = 0")
    # x = list(range(1000))
    # y = []
    # for i in range(1000):
    #     img = 255 * np.zeros((500, 500, 3), dtype=np.uint8)
    #     gen_target(img)
    #     st = time.time()
    #     _index,conf = aco_tracking(img,target,loop_count=5)
    #     _time = time.time()-st
    #     y.append(conf)
    # print(x,y)
    # print("==============================================5")
    # print(f"min: {min(y)}")
    # print(f"max: {max(y)}")
    # print(f"avg: {sum(y)/len(y)}")
    # # plt.plot(x,y,label="loop_count = 5")

    x = list(range(1000))
    y = []
    for i in range(1000):
        img = 255 * np.zeros((500, 500, 3), dtype=np.uint8)
        gen_target(img)
        st = time.time()
        _index,conf = aco_tracking(img,target,loop_count=10)
        _time = time.time()-st
        y.append(conf)
    print(x,y)
    print("==============================================10")
    print(f"min: {min(y)}")
    print(f"max: {max(y)}")
    print(f"avg: {sum(y)/len(y)}")
    plt.plot(x,y,label="loop_count = 10")


#     x = list(range(20))
#     y = []
#     for j in range(20):
#         z = []
#         for i in range(100):
#             img = 255 * np.zeros((500, 500, 3), dtype=np.uint8)
#             gen_target(img)
#             st = time.time()
#             _index,conf = aco_tracking(img,target,loop_count=j)
#             _time = time.time()-st
#             z.append(conf)
#         avg = sum(z)/len(z)
#         print(f"avg: {avg}")
#         y.append(avg)

#     print(x,y)
#     plt.plot(x,y)

    plt.xlabel("No of tests")
    plt.ylabel("Complexity")
    plt.legend()
    plt.show()
