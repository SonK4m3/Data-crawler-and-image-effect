try:
    import cv2 as cv
    import mediapipe as mp
    import os
    import json
except Exception as e:
    print('Caught error while importing {}'.format(e))

IMAGE_DIR = './face_mesh_detection/Photos'
SAVE_DIR = './face_mesh_detection/FaceDetectionSavedImage'
MODEL_SELECTION = 1
MIN_DETECTION_CONFIDENCE = 0.5

def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

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

    make_dir(SAVE_DIR)

    list_dir = os.listdir(IMAGE_DIR)
    #import the main face detection model
    mp_face_detection = mp.solutions.face_detection

    with mp_face_detection.FaceDetection(model_selection=MODEL_SELECTION, min_detection_confidence=MIN_DETECTION_CONFIDENCE) as face_detection:
        data = []

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
            location = []
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

                #json 
                json_data = {
                    'x': xmin,
                    'y': ymin,
                    'width': width_detection,
                    'height': height_detection
                }

                location.append(json_data)
            data.append({
                'filename': IMAGE_DIR + '/' + file,
                'face_detection': location
            })
            #save image
            cv.imwrite(SAVE_DIR + '/' + file, annotated_image)
            #show image
            # cv.imshow('face_detection', annotated_image)
            # cv.waitKey(0)
        
        write_json('./face_mesh_detection/face_detection_results.json', data=data)

def write_json(filename, data):
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=4, ensure_ascii= False)


if __name__ == '__main__':
    get_face_detection()
