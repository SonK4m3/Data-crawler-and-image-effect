try:
    import cv2 as cv
    import mediapipe as mp
    import os
except Exception as e:
    print('Caught error while importing {}'.format(e))

IMAGE_DIR = './Task_3/Photos'

# resize image to standard image 
def resize_image(image, height_size=500):

    height, width = image.shape[:2]
    scale = height_size/height
    resized_image = cv.resize(image, 
                            (int(width * scale), height_size), 
                            interpolation=cv.INTER_AREA)
    return resized_image

#draw retangle in face 
def draw_rectangle(image, location:list):

    x, y, width, height = location[:4]
    cv.rectangle(image, (x, y), 
                (x + width, y + height), 
                (0, 255, 0), 
                thickness=1)
    return image

def get_face_detection():

    list_dir = os.listdir(IMAGE_DIR)
    #import the main face detection model
    mp_face_detection = mp.solutions.face_detection

    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        for indx, file in enumerate(list_dir):
            image = cv.imread(IMAGE_DIR + '/' + file)
            image = resize_image(image)
            height, width = image.shape[:2]

            #print image information
            print('{} {}'.format(indx + 1, IMAGE_DIR + '/' + file))
            print('(width, height) = ({}, {})'.format(width, height))

            #find faces
            results = face_detection.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
            if not results.detections:
                print('Image have no one')
                continue 
            annotated_image = image.copy()
            for num, detection in enumerate(results.detections):
                #get location of detection
                bbox = detection.location_data.relative_bounding_box
                bbox_points = [int(bbox.xmin * width),int(bbox.ymin * height),int(bbox.width * width),int(bbox.height * height)]
                #draw rectangle
                annotated_image = draw_rectangle(annotated_image, bbox_points)
                #print location
                xmin, ymin, width_detection, height_detection = bbox_points[:4]
                print('\t{}: '.format(num), end='')
                print('(x, y, width, height) = ({}, {}, {}, {})'.format(xmin, ymin, width_detection, height_detection))
            #show image
            cv.imshow('face_detection', annotated_image)
            cv.waitKey(0)


if __name__ == '__main__':
    get_face_detection()
