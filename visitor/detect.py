import cv2
from django.http import StreamingHttpResponse
import os
from django.conf import settings
from django.http import HttpResponse

import datetime
latest_img=None
cropped_img=None
def detection():
    global latest_img,cropped_img
    f_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap =cv2.VideoCapture(0)
    image_counter = 0
    try:
        while cap.isOpened():
            ret, img =cap.read()
            if not ret:
                break
            latest_img = img  # Store the latest image in the global variable

            gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            face =f_cascade.detectMultiScale(gray,1.1,4)

            

            for(x,y,w,h) in face:
                padding = 90  # Increase the padding as needed
                width=150
                cv2.rectangle(img, (x - 153, y - 93), (x + w + 153, y + h + 93), (255, 0, 0), 2)    
                # cv2.putText(img,"person", (x + w - 60, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
                face_region = img[y:y + h, x:x + w]
                cropped_img=img[y - padding:y + h + padding, x - width:x + w + width]

            _, encoded_img = cv2.imencode('.jpg', img)

            frame = encoded_img.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            print('========running=======')
    finally:
        cap.release()

def video_feed(request):
    return StreamingHttpResponse(detection(),
        content_type='multipart/x-mixed-replace; boundary=frame')
    



def img_cap():
    images=os.path.join(settings.MEDIA_ROOT,'images')
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"face_detected_{timestamp}.jpg"
    file_path = os.path.join(images, filename)
    # Save the image
    cv2.imwrite(file_path, latest_img)

    print(f"Image saved as {filename}")