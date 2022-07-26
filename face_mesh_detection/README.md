## **Face Detection**
Define

    - Face detection is an AI based computer technology used to find and identify human faces in digital images
    - Face detection technology can be applied to various fields: security, biometrics, law enforcement, 
    entertainment and personal safety
    - Face detection has progressed from rudimentary computer vision techniques to advances in machine learning (ML) 
    to increasingly sophisticated artificial neural networks (ANN) and related technologies
        + computer vision: is the ability of a computer to see
        + machine learning: 
        + artificial neural networks:

How face detection works

    - Face detection applications use algorithms and ML to find human faces within larger images
    - Face detection algorithms typically start by searching for human eyes
    - The algorithm might then attempt to detect eyebrows, the mouth, nose, nostrils and the iris

MediaPipe Face Detection

    - MediaPipe Face Detection is an ultrafast face detection solution that comes with 6 landmarks and multiface support
    - Solution APIs:
        + Configuration Options: 
            MODEL_SELECTION: 
                Could be either 0 for short range and 1 for full range where objects are at some distance.
            MIN_DETECTION_CONFIDENCE: 
                Detection results confidence, could be adjusted according to requirements and input image
        + Output: DETECTIONS - contains s bounding box(xmin, ymin, width, height) 
        and 6 key points(right eye, left eye, nose tip, mouth center, right ear tragion, left ear tragion)

## **Face Mesh Detection**

    The Face Mesh model uses machine learning to infer the 3D surface geometry on human faces
Overview

    MediaPipe Face Mesh is a solution that estimates 468 3D face landmarks in real-time even on mobile devices
    
 Model
 
    - FACE_DETECTION_MODEL
    - FACE_LANDMARK_MODEL: 
        For 3D face landmarks we employed transfer learning and trained a network with several objectives: the network simultaneously 
        predicts 3D landmark coordinates on synthetic rendered data and 2D semantic contours on annotated real-world data. The resulting 
        network provided us with reasonable 3D landmark predictions not just on synthetic but also on real-world data.
    - ATTENTION_MESH_MODEL: 
        In addition to the Face Landmark Model we provide another model that applies attention to semantically meaningful face regions, 
        and therefore predicting landmarks more accurately around lips, eyes and irises, at the expense of more compute. It enables 
        applications like AR makeup and AR puppeteering
        
Face Transform Module

    - Key Concepts:
        METRIC_3D_SPACE
        CANONICAL_FACE_MODEL: 468 3D face landmark topology
    - Components:
        TRANSFORM_PIPELINE
        EFFECT_RENDERER
        
Solution APIs

    - Configuration Options
        STATIC_IMAGE_MODE: 
            If set to false, the solution treats the input images as a video stream. It will try to detect faces in 
            the first input images, and upon a successful detection further localizes the face landmarks. In subsequent images, 
            once all max_num_faces faces are detected and the corresponding face landmarks are localized, it simply tracks those 
            landmarks without invoking another detection until it loses track of any of the faces. This reduces latency and is 
            ideal for processing video frames. If set to true, face detection runs on every input image, ideal for processing 
            a batch of static, possibly unrelated, images. Default to false.
        MAX_NUM_FACES: 
            Maximum number of faces to detect. Default to 1.
        REFINE_LANDMARKS:
            Whether to further refine the landmark coordinates around the eyes and lips, and output additional landmarks around 
            the irises by applying the Attention Mesh Model. Default to false.
        MIN_DETECTION_CONFIDENCE:
            Minimum confidence value ([0.0, 1.0]) from the face detection model for the detection to be considered successful. 
            Default to 0.5.
        MIN_TRACKING_CONFIDENCE:
            Minimum confidence value ([0.0, 1.0]) from the landmark-tracking model for the face landmarks to be considered tracked 
            successfully, or otherwise face detection will be invoked automatically on the next input image. Setting it to a higher 
            value can increase robustness of the solution, at the expense of a higher latency. Ignored if static_image_mode is true, 
            where face detection simply runs on every image. Default to 0.5.
    - Outout:
        MULTI_FACE_LANDMARKS:
            Collection of detected/tracked faces, where each face is represented as a list of 468 face landmarks and each landmark 
            is composed of x, y and z. x and y are normalized to [0.0, 1.0] by the image width and height respectively. z represents 
            the landmark depth with the depth at center of the head being the origin, and the smaller the value the closer the landmark 
            is to the camera. The magnitude of z uses roughly the same scale as x.
        




