import cv2 as cv
import numpy as np
import mediapipe as mp

PATH = './Photos/man.jpg'
SAVE_DIR = './Save image'

def resized_image(image, scale = 500):
    height, width = image.shape[:2]
    x = scale / width
    return cv.resize(image, (scale, int(height * x)))


def get_face_detection(path=PATH):
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils
    
    location_face_detection = []
    
    with mp_face_detection.FaceDetection(model_selection = 1, min_detection_confidence = 0.1) as face_detection:
        image = cv.imread(PATH)
        height, width = image.shape[:2]
        
        results = face_detection.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
        
        if not results.detections:
            return []
        
        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            x = int(bbox.xmin * width)
            y = int(bbox.ymin * height)
            w = int(bbox.width * width)
            h = int(bbox.height * height)
            location_face_detection.append([x,y,w,h])

        return location_face_detection
  
def get_face_mesh(path=PATH, xmin=0, ymin=0, width=0, height=0):
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    
    with mp_face_mesh.FaceMesh(
        static_image_mode = True, 
        max_num_faces = 3, 
        refine_landmarks = True, 
        min_detection_confidence = 0.5) as face_mesh:
        image = cv.imread(PATH)
        image = image[ymin:ymin+height, xmin:xmin+width]
        
        mask = np.zeros((image.shape[0], image.shape[1]), dtype='uint8')

        results = face_mesh.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
        
        if not results.multi_face_landmarks:
            return 
        
        annotated_image = image.copy()
        for face_landmarks in results.multi_face_landmarks:
            landmark_points = []
            
            for lm in face_landmarks.landmark:
                landmark_points.append((lm.x * width, lm.y * height))  
            # print(face_landmarks)
            # mp_drawing.draw_landmarks(
            #     annotated_image,
            #     face_landmarks,
            #     mp_face_mesh.FACEMESH_TESSELATION,
            #     None,
            #     mp_drawing_styles.get_default_face_mesh_tesselation_style()
            # )

            points = np.array(landmark_points, np.int32)
            convexhull = cv.convexHull(points)
            
            # cv.polylines(annotated_image, [convexhull], True, (0,0,255), thickness=3)
            cv.fillConvexPoly(mask, convexhull, 255)

            cropped_face = cv.bitwise_and(annotated_image, annotated_image, mask=mask)
        cv.imshow('a', resized_image(cropped_face))
        cv.waitKey(0)

if __name__ == '__main__':
    face_detections = get_face_detection()
    print(face_detections)
    for face_detection in face_detections:
        x, y, w, h = face_detection[:4]
        print("{} {} {} {}".format(x, y, w, h))
        get_face_mesh(xmin=x, ymin=y, width=w, height=h)
    