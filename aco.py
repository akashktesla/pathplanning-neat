# import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt  

def gen_target(img):
    x = np.random.randint(50, 450)
    y = np.random.randint(50, 450)
    img[y-50:y+50, x-50:x+50] = (0, 0, 255)
    # cv.rectangle(img, (x-50, y-50), (x+50, y+50), (0, 0, 255), -1)

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
    while ant_count<5:
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
    x = list(range(1000))
    y = []
    for i in range(1000):
        img = 255 * np.zeros((500, 500, 3), dtype=np.uint8)
        gen_target(img)
        _index,conf = aco_tracking(img,target,loop_count=0)
        y.append(conf)
    print(x,y)
    plt.plot(x,y)
    x = list(range(1000))
    y = []
    for i in range(1000):
        img = 255 * np.zeros((500, 500, 3), dtype=np.uint8)
        gen_target(img)
        _index,conf = aco_tracking(img,target,loop_count=3)
        y.append(conf)
    print(x,y)
    plt.plot(x,y)
    plt.show()
    cv.imshow('Image', img)
    key = cv.waitKey(0)
    cv.destroyAllWindows()

