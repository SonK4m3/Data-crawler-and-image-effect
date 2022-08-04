import cv2 as cv
import numpy as np
import mediapipe as mp

def extract_index_nparray(nparray):
    index = None
    for num in nparray[0]:
        index = num
        break
    return index

mp_face_mesh = mp.solutions.face_mesh

img = cv.imread('./Photos/15-36-40.jpg')
height, width = img.shape[:2]

with mp_face_mesh.FaceMesh(static_image_mode=True,
                           max_num_faces=2,
                           refine_landmarks=True,
                           min_detection_confidence=0.5) as face_mesh:
    results = face_mesh.process(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    
    blank = np.zeros(img.shape[:2], np.uint8)
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmark_points = []
            for xyz in face_landmarks.landmark:
                x = int(xyz.x * width)
                y = int(xyz.y * height)
                landmark_points.append((x, y))
                # print(x, y)
                cv.circle(img, (x, y), 1, (0, 0, 255), -1)
            
            points = np.array(landmark_points, np.int32)
            convexhull = cv.convexHull(points)
            cv.polylines(blank, [convexhull], True, 255, thickness=1)  
            
            #delaunay triangulation
            rect = cv.boundingRect(points)
            subdiv = cv.Subdiv2D(rect)
            subdiv.insert(landmark_points)
            triangle = subdiv.getTriangleList()
            triangle = np.array(triangle).astype(int)
            
            indexes_triangles = []
            for t in triangle:
                pt1 = (t[0], t[1])
                pt2 = (t[2], t[3])
                pt3 = (t[4], t[5])
                
                index_pt1 = np.where((points == pt1).all(axis=1))
                index_pt1 = extract_index_nparray(index_pt1)
                
                index_pt2 = np.where((points == pt2).all(axis=1))
                index_pt2 = extract_index_nparray(index_pt2)
                
                index_pt3 = np.where((points == pt3).all(axis=1))
                index_pt3 = extract_index_nparray(index_pt3)
                
                
                if index_pt1 is not None and index_pt2 is not None and index_pt3 is not None:
                    triangle = [index_pt1, index_pt2, index_pt3]
                    indexes_triangles.append(triangle)
                        
            for triangle_index in indexes_triangles:
                pt1 = landmark_points[triangle_index[0]]
                pt2 = landmark_points[triangle_index[1]]
                pt3 = landmark_points[triangle_index[2]]
                triangle1 = np.array([pt1,pt2,pt3], np.int32)
                
                rect1 = cv.boundingRect(triangle1)
                (x,y,w,h) = rect1
                cropped_triangle = img[y:y+h, x:x+w]
                cropped_mask = np.zeros((h,w), np.uint8)
                
                points = np.array([[pt1[0] - x, pt1[1] - y],
                                   [pt2[0] - x, pt2[1] - y],
                                   [pt3[0] - x, pt3[1] - y]], np.int32)
                
                cv.fillConvexPoly(cropped_mask, points, 255)
                cropped_triangle = cv.bitwise_and(cropped_triangle, cropped_triangle, mask=cropped_mask)
        
                #draw
                cv.line(blank, pt1, pt2, 255, 1)
                cv.line(blank, pt2, pt3, 255, 1)
                cv.line(blank, pt3, pt1, 255, 1)
        
        #save
        cv.imwrite('./delaunay_triangulation.jpg', blank)
        #show
        cv.imshow('blank', blank)

cv.imshow('image', img)
cv.waitKey(0)


