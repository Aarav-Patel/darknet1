import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import csv
import time

def visualize(x_vid_dim, y_vid_dim):
    df = pd.read_csv("./pathdata.csv")
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
if __name__ == "__main__":
    x_video_dimension = 852
    y_video_dimension = 480
    visualize(x_video_dimension, y_video_dimension)