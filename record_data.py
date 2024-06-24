import csv
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

def save_frame(frame, frame_id, save_bool = True, folder_name ='frames'):
    parent_dir = os.getcwd()
    folder_path = os.path.join(parent_dir,folder_name)
    if not os.path.isdir(folder_path) and save_bool: 
        os.mkdir(folder_path)
    if save_bool :
        cv2.imwrite(f'{folder_path}\\frame_{frame_id}.png', frame)

def write_in_csv_centroids_positions(centroids_list, videofile_name) :
    with open(videofile_name + '.csv', 'w') as csvfile:

        headerList = ['Timestamps[s]', 'x_left', 'y_left', 'x_right', 'y_right'] if len(centroids_list[0]) == 5 else ['Timestamps[s]', 'x', 'y']
        
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=headerList)
        writer.writeheader()
        for i in range (len(centroids_list)):
            current_row = {'Timestamps[s]' : centroids_list[i][0],
                            'x_left' : centroids_list[i][1],
                            'y_left' : centroids_list[i][2],
                            'x_right' : centroids_list[i][3],
                            'y_right' : centroids_list[i][4]} if len(centroids_list[0]) == 5 else {'Timestamps[s]' : centroids_list[i][0],
                            'x' : centroids_list[i][1],
                            'y' : centroids_list[i][2]}
            writer.writerow(current_row)

def write_in_csv_centroids_positions_n_spots_distance(centroids_list, spots_distance, videofile_name) :
    with open(videofile_name + '.csv', 'w') as csvfile:
        headerList = ['Timestamps[s]', 'x_left', 'y_left', 'x_right', 'y_right', 'distance']
        
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=headerList)
        writer.writeheader()
        for i in range (len(centroids_list)):
            current_row = {'Timestamps[s]' : centroids_list[i][0],
                            'x_left' : centroids_list[i][1],
                            'y_left' : centroids_list[i][2],
                            'x_right' : centroids_list[i][3],
                            'y_right' : centroids_list[i][4],
                            'distance' : spots_distance[i]}
            writer.writerow(current_row)

if __name__ == '__main__':
    data = np.genfromtxt('.\\calib_exported_video.csv', delimiter=';', skip_header=1)
    timestamps = data[:, 0]
    xl = data[:, 1]
    yl = data[:, 2]
    xr = data[:, 3]
    yr = data[:, 4]

    fig, axs = plt.subplots(2,2)
    axs[0,0].plot(timestamps, xl)
    axs[0,0].set_title('X left')
    axs[0,1].plot(timestamps, yl)
    axs[0,1].set_title('Y left')
    axs[1,0].plot(timestamps, xr)
    axs[1,0].set_title('X right')
    axs[1,1].plot(timestamps, yr)
    axs[1,1].set_title('Y right')

    for ax in axs.flat:
        ax.set(xlabel='time in seconds')
    for ax in axs.flat:
        ax.label_outer()
    
    plt.show()
    