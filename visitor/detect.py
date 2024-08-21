import cv2
from django.http import StreamingHttpResponse

import threading

import datetime
latest_img=None
def detection():
    global latest_img
    f_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap =cv2.VideoCapture(0)
    image_counter = 0

    while True:
        _, img =cap.read()
        latest_img = img  # Store the latest image in the global variable

        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        face =f_cascade.detectMultiScale(gray,1.1,4)
        key = cv2.waitKey(1)

        # Save the image if the 's' key is pressed

        if len(face)>0:
            if key == ord('s'):
                # Generate a unique filename with timestamp
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"face_detected_{timestamp}.jpg"
                cv2.imwrite(filename, img)

                # Save the image
                
                print(f"Image saved as {filename}")
                image_counter += 1

        for(x,y,w,h) in face:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),1)
            cv2.putText(img,"person", (x + w - 60, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
            face_region = img[y:y + h, x:x + w]

        _, encoded_img = cv2.imencode('.jpg', img)

        frame = encoded_img.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def video_feed(request):
    return StreamingHttpResponse(detection(),
                                content_type='multipart/x-mixed-replace; boundary=frame')
    


def run_detection():
    detection_thread = threading.Thread(target=detection)
    detection_thread.start()


def img_cap():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"face_detected_{timestamp}.jpg"
    cv2.imwrite(filename, latest_img)

    # Save the image
    
    print(f"Image saved as {filename}")