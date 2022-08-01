import cv2 as cv
from matplotlib import image
import numpy as np
import dlib
import mediapipe as mp

def resized_image(image, scale=1000):
    height, width = image.shape[:2]
    x = scale/width
    return cv.resize(image, (scale, int(height * x)))

def draw_circle(image, x, y):
    return cv.circle(image, (x, y), 1, (0,255,0), 1)

def get_lankmark(image):
    img_gray = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    mask = np.zeros((img_gray.shape[0], img_gray.shape[1]), dtype='uint8')
   
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    faces = detector(img_gray)
   
    for face in faces:
        landmarks = predictor(img_gray, face)
        landmarks_points = []
        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            landmarks_points.append((x, y))
            
            # cv.circle(image, (x,y), 3, (0,0,255), -1)
    points = np.array(landmarks_points, np.int32)
    convexhull = cv.convexHull(points)
    
    cv.polylines(image, [convexhull], True, (0,0,255), thickness=3)
    cv.fillConvexPoly(mask, convexhull, 255)
    
    face_image_1 = cv.bitwise_and(image, image, mask=mask)
    
    return [image, face_image_1]

img = cv.imread('./Photos/man.jpg')
img = resized_image(img)

annotated_image, face_image = get_lankmark(img)

cv.imshow('man', annotated_image)
cv.imshow('mask', face_image)
cv.waitKey(0)
cv.destroyAllWindows()