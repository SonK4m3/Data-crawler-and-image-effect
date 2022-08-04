## **Cropping face**

## Requirements
```
cv2
mediapipe
numpy
```
## Step 1 
    Using face detection to detect dimension has faces
## Step 2
    Using face mesh detection to get face mesh in the face
    We have vector position of landmark points is (x, y, z) but we append (x, y) to List
## Step 3
    Calculating convex hull of list position of landmark points 
    We draw convex hull and crop it into new image

## **SWAPPING FACE**
    We swaped face in source image to face in destination image
## Reference
    `https://pysource.com/2019/05/28/face-swapping-explained-in-8-steps-opencv-with-python/`
## Requirements
```
cv2
numpy
dlib
matplotlib
```
```
shape_predictor_68_face_landmarks.dat
```
## STEP
    1. Take two images
    2. Find landmark points of bot images
    3. Triangulation source image
    4. Triangulation destination image
    5. Extract and warp triangles
    6. Link the warp triangles together
    7. Replace the face on the destination image
    8. Seamless Cloning




