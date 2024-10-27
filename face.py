import cv2
import numpy as np
from deepface import DeepFace
import mtcnn
import random

def augment_image(image):
    
    angle = random.uniform(-30, 30)
    height, width = image.shape[:2]
    M = cv2.getRotationMatrix2D((width // 2, height // 2), angle, 1.0)
    rotated_image = cv2.warpAffine(image, M, (width, height))

    
    if random.random() > 0.5:
        rotated_image = cv2.flip(rotated_image, 1)

    
    brightness_factor = random.uniform(0.5, 1.5)
    augmented_image = cv2.convertScaleAbs(rotated_image, alpha=brightness_factor, beta=0)

    return augmented_image

def capture_faces_from_camera():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    # Use MTCNN for better face detection
    mtcnn_detector = mtcnn.MTCNN()
    faces = mtcnn_detector.detect_faces(frame)

    # Extract the faces from the frame
    captured_faces = [frame[int(face['box'][1]):int(face['box'][1] + face['box'][3]),
                             int(face['box'][0]):int(face['box'][0] + face['box'][2])] for face in faces]

    return captured_faces


img_path = "IMG_20241004_184228.jpg"
image = cv2.imread(img_path)


camera_faces = capture_faces_from_camera()


if not camera_faces:
    print("No faces detected in the camera stream.")
    exit()


mtcnn_detector = mtcnn.MTCNN()
image_faces = mtcnn_detector.detect_faces(image)


if not image_faces:
    print("No faces detected in the image.")
    exit()


image_face_box = image_faces[0]['box']
x, y, w, h = image_face_box
image_face = image[y:y+h, x:x+w]

camera_face = camera_faces[0]


augmented_image_face = augment_image(image_face)
augmented_camera_face = augment_image(camera_face)


result = DeepFace.verify(img_path, augmented_camera_face, model_name='VGG-Face', enforce_detection=False)


if result["verified"]:
    print("Faces match!")
else:
    print("Faces do not match.")
