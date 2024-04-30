import copy
import statistics
import cv2
import math
import numpy as np
from centroids_and_contours_detection import centroid_contour, compute_centroids
from record_data import write_in_csv_centroids_positions


if __name__ == '__main__':
    videofile_output = "D:\\logique_lentille\\recordings\\fmr_outdoor_calib\\positions_spots"
    calib_eye_recording_path = "D:\\logique_lentille\\recordings\\fmr_outdoor_calib\\exported_video.avi"
    centroids_list, spots_distance = [], []

    cap = cv2.VideoCapture(calib_eye_recording_path)
    
    nb_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.set(cv2.CAP_PROP_POS_FRAMES, nb_frames)
    duration_in_sec= cap.get(cv2.CAP_PROP_POS_MSEC)/1000

    thresh = 200
    current_frame_nb = 0
    cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_nb)
    ret, frame = cap.read()
    contours_init, centroids_init = compute_centroids(frame, thresh)
    print(contours_init)
    timestamp = ((current_frame_nb+1)/nb_frames)*duration_in_sec
    if len(contours_init)> 1 :
        centroids_list.append([timestamp, centroids_init[0][0],centroids_init[0][1], centroids_init[1][0],centroids_init[1][1]])
        c1_c2 = math.sqrt((centroids_init[0][0] - centroids_init[1][0])**2 + (centroids_init[0][1]-centroids_init[1][1])**2)
        spots_distance.append(c1_c2)
        print(c1_c2)
        frame_two_centroids = copy.deepcopy(frame)   
        cv2.drawMarker(frame_two_centroids, (centroids_init[0][0],centroids_init[0][1]), (0, 0, 255), cv2.MARKER_CROSS, 5, 2)
        cv2.drawMarker(frame_two_centroids, (centroids_init[1][0],centroids_init[1][1]), (0, 255, 0), cv2.MARKER_CROSS, 5, 2)
    elif len(contours_init) == 1 :
        centroids_list.append([timestamp, centroids_init[0][0],centroids_init[0][1],None,None])
        spots_distance.append(None)
        frame_two_centroids = copy.deepcopy(frame)   
        cv2.drawMarker(frame_two_centroids, (centroids_init[0][0],centroids_init[0][1]), (0, 0, 255), cv2.MARKER_CROSS, 5, 2)
    else : 
        centroids_list.append([timestamp, None,None,None,None])
        spots_distance.append(None)
        frame_two_centroids = copy.deepcopy(frame)       
    
    print(f"Frame {current_frame_nb} - Number of contour found: {len(contours_init)}")
    current_frame_nb+=1

    #while current_frame_nb < 980 :
    while current_frame_nb < nb_frames :
        # Image pre-processing        
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_nb)
        ret, frame = cap.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        T, frame_thr = cv2.threshold(frame_gray, 200, 255, cv2.THRESH_BINARY)

        # Get all contours of the current frame
        contours, hierarchy = cv2.findContours(frame_thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        nb_contour = len(contours)
        print(f"Frame {current_frame_nb} - Number of contour found: {nb_contour}")

        # Get all centroids of the current frame
        centroids_current_frame = []
        for contour in contours:
            centroid = list(centroid_contour(contour))
            centroids_current_frame.append(centroid)
        
        # Get VSEL centroids of the previous frame
        centroids_previous_frame = centroids_list[-1][1:]
        nb_centroids_previous_frame = sum(centroids_coord is not None for centroids_coord in centroids_previous_frame)/2

        if nb_centroids_previous_frame > 1 and nb_contour > 1 : # ajouter distance entre deux spots conditions.
            print("a")
            c1x, c1y = centroids_previous_frame[0], centroids_previous_frame[1]
            c2x, c2y = centroids_previous_frame[2], centroids_previous_frame[3]
            centroid_list, dist1_list, dist2_list=[], [], []
            for centroid_to_select in centroids_current_frame :
                ctsx, ctsy = centroid_to_select[0], centroid_to_select[1]
                dist1 = math.sqrt((c1x - ctsx)**2 + (c1y-ctsy)**2)
                dist2 = math.sqrt((c2x - ctsx)**2 + (c2y-ctsy)**2)
                centroid_list.append([centroid_to_select[0], centroid_to_select[1]])
                dist1_list.append(dist1)
                dist2_list.append(dist2)
            current_c1 = centroid_list[dist1_list.index(min(dist1_list))]
            current_c2 = centroid_list[dist2_list.index(min(dist2_list))] 
            dist_c1_c2 = math.sqrt((current_c1[0] - current_c2[0])**2 + (current_c1[1] - current_c2[1])**2)
            print(current_c1, current_c2, dist_c1_c2)
            if current_c2 == current_c1 : # si les deux spots identifiés sont les mêmes
                print("a1")
                dist_old_c1_c1 = math.sqrt((c1x - current_c1[0])**2 + (c1y-current_c1[1])**2)
                dist_old_c2_c2 = math.sqrt((c2x - current_c2[0])**2 + (c2y-current_c2[1])**2)
                if dist_old_c1_c1 < dist_old_c2_c2 :
                    current_c2 = [None, None]
                else : 
                    current_c1 = [None, None]
                spots_distance.append(None)
            elif dist_c1_c2 < statistics.mean([dist for dist in spots_distance if dist is not None]) *0.7  or dist_c1_c2 > statistics.mean([dist for dist in spots_distance if dist is not None])*1.3: #si la distance entre les deux points est plus petite que la 90%  ou plus grand que 110% de la distance moyenne alors l'un des deux points est un reflet
                print("a2")
                looking_for_the_smallest_distance=[]
                looking_for_the_smallest_distance.append(math.sqrt((c1x - current_c1[0])**2 + (c1y-current_c1[1])**2))
                looking_for_the_smallest_distance.append(math.sqrt((c1x - current_c2[0])**2 + (c1y-current_c2[1])**2))
                looking_for_the_smallest_distance.append(math.sqrt((c2x - current_c1[0])**2 + (c2y-current_c1[1])**2))
                looking_for_the_smallest_distance.append(math.sqrt((c2x - current_c2[0])**2 + (c2y-current_c2[1])**2))
                id_smallest = looking_for_the_smallest_distance.index(min(looking_for_the_smallest_distance))
                if id_smallest == 0 or id_smallest == 2 :
                   current_c2 = [None, None]
                else :
                    current_c1 = [None, None] 
                spots_distance.append(None)
            else : 
                print("a3")
                spots_distance.append(dist_c1_c2)

        elif (nb_centroids_previous_frame == 1 and nb_contour > 1) or (nb_centroids_previous_frame < 1 and nb_contour > 1):
            print("b")
            c1x, c1y = next(x[1] for x in reversed(centroids_list) if x[1] is not None), next(x[2] for x in reversed(centroids_list) if x[2] is not None)
            c2x, c2y = next(x[3] for x in reversed(centroids_list) if x[3] is not None), next(x[4] for x in reversed(centroids_list) if x[4] is not None)
            dist_c1_c2_previous = math.sqrt((c1x - c2x)**2 + (c1y - c2y)**2)
            centroid_list, dist1_list, dist2_list=[], [], []
            for centroid_to_select in centroids_current_frame :
                ctsx, ctsy = centroid_to_select[0], centroid_to_select[1]
                dist1 = math.sqrt((c1x - ctsx)**2 + (c1y-ctsy)**2)
                dist2 = math.sqrt((c2x - ctsx)**2 + (c2y-ctsy)**2)
                centroid_list.append([centroid_to_select[0], centroid_to_select[1]])
                dist1_list.append(dist1)
                dist2_list.append(dist2)
            current_c1 = centroid_list[dist1_list.index(min(dist1_list))]
            current_c2 = centroid_list[dist2_list.index(min(dist2_list))]
            dist_c1_c2 = math.sqrt((current_c1[0] - current_c2[0])**2 + (current_c1[1] - current_c2[1])**2)
            print(current_c1, current_c2, dist_c1_c2)
            if current_c2 == current_c1 :
                print("b1")
                dist_old_c1_c1 = math.sqrt((c1x - current_c1[0])**2 + (c1y-current_c1[1])**2)
                dist_old_c2_c2 = math.sqrt((c2x - current_c2[0])**2 + (c2y-current_c2[1])**2)
                if dist_old_c1_c1 < dist_old_c2_c2 :
                    current_c2 = [None, None]
                else : 
                    current_c1 = [None, None]
                spots_distance.append(None)
            elif dist_c1_c2 < statistics.mean([dist for dist in spots_distance if dist is not None])*0.7 or dist_c1_c2 > statistics.mean([dist for dist in spots_distance if dist is not None])*1.3: #si la distance entre les deux points est plus petite que la 90%  ou plus grand que 110% de la distance moyenne alors l'un des deux points est un reflet
                print("b2")
                looking_for_the_smallest_distance=[]
                looking_for_the_smallest_distance.append(math.sqrt((c1x - current_c1[0])**2 + (c1y-current_c1[1])**2))
                looking_for_the_smallest_distance.append(math.sqrt((c1x - current_c2[0])**2 + (c1y-current_c2[1])**2))
                looking_for_the_smallest_distance.append(math.sqrt((c2x - current_c1[0])**2 + (c2y-current_c1[1])**2))
                looking_for_the_smallest_distance.append(math.sqrt((c2x - current_c2[0])**2 + (c2y-current_c2[1])**2))
                id_smallest = looking_for_the_smallest_distance.index(min(looking_for_the_smallest_distance))
                if id_smallest == 0 or id_smallest == 2 :
                   current_c2 = [None, None]
                else :
                    current_c1 = [None, None] 
                spots_distance.append(None)
            else : 
                print("b3")
                spots_distance.append(dist_c1_c2)
           

        elif (nb_centroids_previous_frame > 1 and nb_contour == 1) or (nb_centroids_previous_frame == 1 and nb_contour == 1) or (nb_centroids_previous_frame < 1 and nb_contour == 1) :
            print("d")
            c1x, c1y = next(x[1] for x in reversed(centroids_list) if x[1] is not None), next(x[2] for x in reversed(centroids_list) if x[2] is not None)
            c2x, c2y = next(x[3] for x in reversed(centroids_list) if x[3] is not None), next(x[4] for x in reversed(centroids_list) if x[4] is not None)
            
            cx, cy = centroids_current_frame[0][0], centroids_current_frame[0][1]

            dist_c_c1 = math.sqrt((cx-c1x)**2+(cy-c1y)**2)
            dist_c_c2 = math.sqrt((cx-c2x)**2+(cy-c2y)**2)

            if dist_c_c1 < dist_c_c2 :
                current_c1, current_c2 = [cx, cy], [None, None]
            else :
                current_c1, current_c2 = [None, None], [cx, cy]

            spots_distance.append(None)
            

        else : # nb contour == 0 
            print("e")
            current_c1, current_c2 = [None, None], [None, None]
            spots_distance.append(None)

        frame_two_centroids = copy.deepcopy(frame)
        
        if current_c1[0] != None :
            cv2.drawMarker(frame_two_centroids, (current_c1[0], current_c1[1]), (0, 0, 255), cv2.MARKER_CROSS, 5, 2)
        if current_c2[0] != None :
            cv2.drawMarker(frame_two_centroids, (current_c2[0], current_c2[1]), (0, 255, 0), cv2.MARKER_CROSS, 5, 2)
        

        timestamp=((current_frame_nb+1)/nb_frames)*duration_in_sec 
        centroids_list.append([timestamp, current_c1[0], current_c1[1], current_c2[0], current_c2[1]])

        #End of processing for the current frame
        current_frame_nb += 1
    

    print(len(centroids_list))
    write_in_csv_centroids_positions(centroids_list, videofile_output)

    cap.release()
    cv2.destroyAllWindows()

