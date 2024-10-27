import cv2
from deepface import DeepFace
import mtcnn


def capture_faces_from_camera():
    
    cap = cv2.VideoCapture(0)

    captured_faces = []
    
    while True:
        
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        
        
        detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            captured_faces.append(frame[y:y+h, x:x+w])

        
        cv2.imshow('Camera', frame)

        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c') and captured_faces:
            break
        elif key == ord('q'):
            print("Exiting...")
            break

    
    cap.release()
    cv2.destroyAllWindows()

    return captured_faces


img_path = "C:\\Users\\nipun\\Downloads\\Untitled design.jpg"
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
    print("Faces match!")
else:
    print("Faces do not match.")
