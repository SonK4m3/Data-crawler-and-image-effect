try:
    import cv2 as cv
    import mediapipe as mp
    import os
except Exception as e:
    print('Caught error while importing {}'.format(e))

IMAGE_DIR = './face_mesh_detection/Photos'
SAVE_DIR = './face_mesh_detection/FaceMeshDetectionSavedImage'

#face_mesh_model
STATIC_IMAGE_MODE = True
MAX_NUM_FACES = 5
REFINE_LANDMARKS = True
MIN_DETECTION_CONFIDENCE = 0.1

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

def get_face_mesh_detection():

    make_dir(SAVE_DIR)

    list_dir = os.listdir(IMAGE_DIR)
    #import the main face detection model
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_face_mesh = mp.solutions.face_mesh
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    with mp_face_mesh.FaceMesh(
        static_image_mode = STATIC_IMAGE_MODE,
        max_num_faces = MAX_NUM_FACES,
        refine_landmarks = REFINE_LANDMARKS,
        min_detection_confidence = MIN_DETECTION_CONFIDENCE) as face_mesh:
        for indx, file in enumerate(list_dir):
            image = cv.imread(IMAGE_DIR + '/' + file)
            image = resize_image(image=image, height_size=700)

            #print image information
            height, width = image.shape[:2]
            print('{} {}'.format(indx + 1, IMAGE_DIR + '/' + file))
            print('(width, height) = ({}, {})'.format(width, height))

            #get face mesh results
            results = face_mesh.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))

            if not results.multi_face_landmarks:
                print('This is no anyone')
                continue
            
            annotated_image = image.copy()
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None, #can be drawing_spec
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                )
            #save image
            cv.imwrite(SAVE_DIR + '/' + file, annotated_image)
            # #show image
            # cv.imshow('face_detection', annotated_image)
            # cv.waitKey(0)


if __name__ == '__main__':
    get_face_mesh_detection()
