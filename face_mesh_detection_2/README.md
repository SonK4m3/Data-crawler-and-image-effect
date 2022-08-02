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