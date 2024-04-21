import cv2
from deepface import DeepFace
import mtcnn

# Function to capture faces from the camera using OpenCV
def capture_faces_from_camera():
    # Open the camera (you can specify the camera index, e.g., 0 for the default camera)
    cap = cv2.VideoCapture(0)

    # Read a frame from the camera
    ret, frame = cap.read()

    # Close the camera
    cap.release()

    # Use face detection to get a list of faces
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Extract the faces from the frame
    captured_faces = [frame[y:y+h, x:x+w] for (x, y, w, h) in faces]

    return captured_faces

# Load the image
img_path = "C:\\Users\\nipun\\Downloads\\Untitled design.jpg"
image = cv2.imread(img_path)

# Capture faces from the camera
camera_faces = capture_faces_from_camera()

# Check if faces were detected in the camera stream
if not camera_faces:
    print("No faces detected in the camera stream.")
    # Handle this case appropriately, e.g., exit the program or provide a default camera face
    exit()

# Assuming you have one face in the image and one in the camera stream
# Use MTCNN for face detection with custom parameters
mtcnn_detector = mtcnn.MTCNN(min_face_size=20)
image_faces = mtcnn_detector.detect_faces(image)

# Check if faces were detected in the image
if not image_faces:
    print("No faces detected in the image.")
    # Handle this case appropriately, e.g., exit the program or provide a default image face
    exit()

# Extract the face region from the detected faces
image_face_box = image_faces[0]['box']
x, y, w, h = image_face_box
image_face = image[y:y+h, x:x+w]

camera_face = camera_faces[0]

# Compare faces using DeepFace
result = DeepFace.verify(img_path, camera_face, enforce_detection=False)

# Check the result
if result["verified"]:
    print("Faces  match!")
else:
    print("Faces do not match.")
