import cv2
from deepface import DeepFace
import mtcnn


def capture_faces_from_camera():
    
    cap = cv2.VideoCapture(0)

    
    ret, frame = cap.read()

    
    cap.release()

    
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    
    captured_faces = [frame[y:y+h, x:x+w] for (x, y, w, h) in faces]

    return captured_faces

img_path = "IMG_20241004_184228.jpg"
image = cv2.imread(img_path)


camera_faces = capture_faces_from_camera()


if not camera_faces:
    print("No faces detected in the camera stream.")
    
    exit()


mtcnn_detector = mtcnn.MTCNN(min_face_size=20)
image_faces = mtcnn_detector.detect_faces(image)


if not image_faces:
    print("No faces detected in the image.")
    
    exit()


image_face_box = image_faces[0]['box']
x, y, w, h = image_face_box
image_face = image[y:y+h, x:x+w]

camera_face = camera_faces[0]


result = DeepFace.verify(img_path, camera_face, enforce_detection=False)


if result["verified"]:
    print("Faces  match!")
else:
    print("Faces do not match.") 
