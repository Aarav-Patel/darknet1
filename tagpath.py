
# average human width is 0.41 m
# assume that if two points are within 0.41 m it is the same person on same path
# if camera is 24 fps it would require someone to run 9.8 m/s to break this rule
# average walking speed is 1.4 m/s and usian bolt top speed is 10.44 m/s

# simulates data from model
# l  = side length of area
# fr = framerate default 30 f/s
# speed = walking speed default 1m/s

"""
def simulate(l=10, fr=30, speed=1):
    # generate x and y positions for all frames
    x = [1.0, 2.0, 3.0, 4.0, 4.7, 8.0, 10.0]
    # generates 
    # 10m / (1m/s / 30 fps)
    # 10m * (30fps/ 1m/s)
    # generates in default case 300 equally spaced values corresponding to number of frames taken of a person walking 1 m/s for 10m 
    y = np.linspace(0, l, int(l/(speed/fr)))
    
    arr = []
    for vy in y:
        for vx in x:
            # ensure frame index 
            if(vy == 0):
                t = 0
            else:
                t =  int(math.ceil(vy*fr)-1)
            tup = (vx, vy, t)
            arr.append(tup)
    x , y = np.meshgrid(x,y)
    t = y*fr
    
    # display data:
    # fig = plt.figure()
    # ax = fig.add_subplot(projection='3d')
    # ax.scatter(x, y, t)
    # plt.show()


    arr = np.array(arr)
    np.savetxt('output.csv', arr, delimiter=",")
    return arr
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import math
import csv
import time
import random
# returns number of paths given data

def converttoarr():
    f = open(file_path, 'r')

    reader = csv.reader(f, delimiter=",")
    data = [row for row in reader]

    if len(data) < 2:
        return
    
    # arr = [[] for x in range(max_frame_number+1)]
    arr = []

    idx = -1
    frame = []
    for p in data:
        if idx != int(p[2]):
            if len(frame) != 0:
                arr.append(frame)
            idx = int(p[2])
            frame = []

        frame.append( [ int(p[0]), int(p[1]) ] )


        #frame_index =  int(p[2])
        # arr[frame_index].append([p[0]*(x_m/x_px), p[1]*(x_m/x_px)])

        #arr[frame_index].append( [int(p[0]), int(p[1])] )

    return arr



def distance(point1, point2):
    xd = point2[0] - point1[0]
    yd = point2[1] - point1[1]
    return math.sqrt(xd**2 + yd**2)



hpathid = 0
def pathTag(arr):
    global hpathid
    for i in range(len(arr)-1):
        curr_frame = arr[i]
        next_frame = arr[i+1]
        if i == 0:
            for pt in range(len(curr_frame)):
                arr[i][pt].append(pt)
                hpathid += 1
        
        for j in range(len(curr_frame)):
           
            for k in range(len(next_frame)):
                
                curr_point = curr_frame[j]
                next_point = next_frame[k]
                # make distance as sub
                d = distance(curr_point, next_point)
                
                if d < dist_threshold:
                    # append next point with id of curr point if curr point has path id
                    # if not give currpoint and next point new path id
                    if len(arr[i+1][k]) == 2:
                        if len(arr[i][j]) > 2:
                            arr[i+1][k].append(arr[i][j][2])
                        else:    
                            hpathid += 1
                            if len(arr[i][j]) == 2:
                                arr[i][j].append(hpathid)
                            arr[i+1][k].append(hpathid)
            
    print(hpathid)  
    # print(arr)
    return arr

def parallel_tagpath(curr_frame, next_frame):
    arr = [curr_frame, next_frame]
    for j in range(len(curr_frame)):
        for k in range(len(next_frame)):
            curr_point = curr_frame[j]
            next_point = next_frame[k]
            # make distance as sub
            d = distance(curr_point, next_point)
            if d < dist_threshold:
                # append next point with id of curr point if curr point has path id
                # if not give currpoint and next point new path id
                if len(next_frame[k]) == 2:
                    if len(curr_frame[j]) > 2:
                        next_frame[k].append(curr_frame[j][2])
                    else:    
                        hpathid += 1
                        if len(arr[i][j]) == 2:
                            arr[i][j].append(hpathid)
                        arr[i+1][k].append(hpathid)

def makeVisualizationData(arr, file, hpathid):
    newdata = []
    for f, frame in enumerate(arr):
        
        for p in frame:
            # x = x_video_dimension - p[0]
            x = p[0]
            y = p[1]
            f = p[2]
            if len(p) > 3:
                newdata.append((x, y, f, p[3]))
            else:
                hpathid += 1
                newdata.append((x, y, f, hpathid))

    np.savetxt(file, newdata, delimiter=",")

if __name__ == "__main__":
    file_path = "/Users/adammalyshev/Documents/projects/ATT/model_output.csv"
    x_px = 32.5
    x_m = 0.333
    num_frames=100

    x_video_dimension = 852
    y_video_dimension = 480
    dist_threshold = 15
    # start = time.time()
    arr = converttoarr()
    # print("repackaged array: ", arr)
    tagged_arr = pathTag(arr)
    makeVisualizationData(tagged_arr, x_video_dimension, y_video_dimension)
    # print(time.process_time())
    # print("--- %s seconds ---" % (time.time() - start))