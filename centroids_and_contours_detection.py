import copy
import cv2
import numpy as np

def bubble_sort_lists(li_origin):
    """
    Sort the list of lists by length of its list elements.

    Parameters
    ----------
    li_origin : List of lists

    Returns
    -------
    list_sorted : The list sorted by the size of each of its elements. The
    lists with biggest lengths are firsts. Delete the contours of two pixels or
    less.

    """
    li = list(copy.deepcopy(li_origin))
    # if li == []:
    #     return []
    for i in range(len(li) - 1, 0, -1):
        for j in range(i):
            #print(i,j,li[j], len(li[j]), len(li[j+1]))
            
            if len(li[j]) < len(li[j + 1]):
                temp = li[j + 1]
                #print(type(li[j+1]))
                li[j+1] = li[j]
                li[j] = temp
                # li[j + 1], li[j] = li[j], li[j + 1]
    try:
        while len(li[len(li)-1]) <= 2:
            li.pop()
        return li
    except:
        # print(li)
        # import pdb; pdb.set_trace()
        pass
    
def centroid_contour(c):
    """
    Compute the (non-weighted) centroid of a contour.

    Parameters
    ----------
    c : Open-cv contour.

    Returns
    -------
    cX : X-value of the centroid
    cY : Y-value of the centroid

    """
    M = cv2.moments(c)
    if M["m00"]:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        print("Unable to compute the centroid with moments for the\
                        angle of " + ". It is then computed\
                        with a mean of he X-values and Y-values.")
        
        if c.shape[0] > 1:  
            cX = int(np.mean(c[1, :, 0]))
            cY = int(np.mean(c[1, :, 1]))
        else :
            cX = c[0, 0, 0]
            cY = c[0, 0, 1]
    return cX, cY

def compute_centroids(im_cv, thresh=90):
        im_gray = cv2.cvtColor(im_cv, cv2.COLOR_BGR2GRAY)
        ret, im_thr = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(im_thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_sorted = bubble_sort_lists(contours)
        # print(type(contours_sorted))
        if contours_sorted is None:
            # print(contours_sorted is None)
            c1 = []
            cX1 = 0
            cY1 = 0
        else:
            c1 = contours_sorted[0]
            cX1, cY1 = centroid_contour(c1)
        # Recherche du deuxième plus grand contour suffisamment séparé pour être
        # le second spot
        c2 = []
        cX2 = 0
        cY2 = 0

        second_spot_exists = False
        if not(contours_sorted is None) and (len(contours_sorted) > 1):
            i = 2
            c_temp = contours_sorted[1]
            cX_temp, cY_temp = centroid_contour(c_temp)
            # Calcul de la distance entre les deux barycentres
            # il faut cette distance > 1/10 de la largeur de l'image pour être bien
            # sur deux spots séparés
            d_x = np.abs(cX1 - cX_temp)
            d_y = np.abs(cY1 - cY_temp)
            d_between_centroids = np.sqrt(d_x * d_x + d_y * d_y)
            second_spot_exists = (d_between_centroids > 0.05 * im_gray.shape[0])  # Comparaison à la largeur de l'image
            while not(second_spot_exists) and (i < len(contours_sorted)):
                c_temp = contours_sorted[i]
                cX_temp, cY_temp = centroid_contour(c_temp)
                d_x = np.abs(cX1 - cX_temp)
                d_y = np.abs(cY1 - cY_temp)
                d_between_centroids = np.sqrt(d_x * d_x + d_y * d_y)
                second_spot_exists = (d_between_centroids > 0.05 * im_gray.shape[0])
                i += 1

        if second_spot_exists:
            c2 = c_temp
            cX2 = cX_temp
            cY2 = cY_temp

        contours = [c1, c2]  # Recréation de la liste avec les 2 contours

        # Sauvegarde des barycentres
        if len(c2) == 0:  # Si il n'y a qu'un contour
            # if angles_list[k] < 0:
            #     centroids_left = [cX2, cY2]
            #     centroids_right = [cX1, cY1]
            # if angles_list[k] > 0:
            #     centroids_left = [cX1, cY1]
            #     centroids_right = [cX2, cY2]
            centroids_left = [cX1, cY1]
            centroids_right = [cX2, cY2]
        else:
            if cX1 < cX2:
                centroids_left = [cX1, cY1]
                centroids_right = [cX2, cY2]
            else:
                centroids_left = [cX2, cY2]
                centroids_right = [cX1, cY1]

        centroids = np.array([centroids_left, centroids_right])
        return (contours, centroids)
