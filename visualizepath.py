import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import csv
import time

def visualize(file_path):
    df = pd.read_csv(file_path)
    df.columns = ["X", "Y", "T", "P"]
    l = len(df)
    paths = df["P"].squeeze()
    max_path = int(paths.max())
    plt.figure()
    for path in range(1, max_path+1):
        p = df[df["P"] == path]
        X= p.loc[0:(l-max_path-1), "X"]
        Y= p.loc[0:(l-max_path-1), "Y"]
        plt.plot(X, Y, label=str(path))
    # plt.xlim([0, x_vid_dim])
    # plt.ylim([0, y_vid_dim])
    plt.show()
    time.sleep(0.01)
    plt.close()

def drawline(point1, point2, image, colors):
    import cv2
    x1, y1, f, pathid = point1
    x2, y2, f1, pathid1 = point2
    # draws red line
    cv2.line(image, (x1,y1), (x2,y2), (255,0,0), 5)
    return image

if __name__ == "__main__":
    x_video_dimension = 852
    y_video_dimension = 480
    visualize("./pathdata.csv")