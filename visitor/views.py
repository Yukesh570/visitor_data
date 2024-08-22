from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
import cv2
import os
from .detect import *
import datetime
from django.conf import settings
import glob
from django.http import HttpResponse
import mimetypes
import requests
from django.utils import timezone
import json
# from io import BytesIO
import base64
from .detect import run_detection
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your views here.


def get_latest_image():
    image_pattern=os.path.join(settings.MEDIA_ROOT,'images','*.jpg')

    image_files=glob.glob(image_pattern)
    if not image_files:
        return None
    
    latest_image=max(image_files,key=os.path.getmtime)
    # print('url',latest_image)
    return latest_image
    

def serve_latest_image(request):
    latest_image_path = get_latest_image()
    
    if latest_image_path:
        try:
            with open(latest_image_path, "rb") as image_file:
                image_data = image_file.read()

                # print('imagedata',image_data)
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                print('------',image_base64)
                # Returning the base64 image data as an HTML response for demonstration
                html = f'<img src="data:image/jpeg;base64,{image_base64}" />'
                return HttpResponse(image_base64)
        
        except IOError:
            return HttpResponse("Error: Unable to read the image file.", status=500)
    
    return HttpResponse("Error: No image file found.", status=404)
# def serve_latest_image(request):
#     latest_image_path = get_latest_image()
#     print(f'Latest image path: {latest_image_path}')  # Print the result for debugging
#     if latest_image_path:
#         with open(latest_image_path, "rb") as image_file:



#             print('imagefile',image_file)
#         if image_file:
#             image_base64 = base64.b64encode(image_file).decode('utf-8')
#             print("base64=", image_base64)
#         else:
#             print("Error: Image file is empty or not readable.")
#     else:
#         print("Error: No image file found in the request.")
#     if latest_image_path is None:
#         return HttpResponse("No images found.", status=404)

#     # Determine the MIME type of the image
#     mime_type, _ = mimetypes.guess_type(latest_image_path)
#     if mime_type is None:
#         mime_type = 'application/octet-stream'  # Default MIME type for unknown types

#     with open(latest_image_path, 'rb') as img:
#         response = HttpResponse(img.read(), content_type=mime_type)
#         response['Content-Disposition'] = f'inline; filename={os.path.basename(latest_image_path)}'
#         return response

@api_view(['POST'])
def register(request):
    # visitor=Visitor_data.objects.get(id=id)
    # pk=visitor.id
    # print('---------------',pk)
    data=request.data
    # image=request.FILES.get('image')
    # run_detection()
    image=get_latest_image()

    try:
        # created_at = timezone.make_aware(timezone.datetime.strptime(data['created_at'], "%Y-%m-%d"))

        visitor=Visitor_data.objects.create(
            name=data['name'],
            phone_no=data['phone_no'],
            address=data['address'],
            email=data['email'],
            no_of_person=data['no_of_person'],
            purpose=data['purpose'],
            # created_at=created_at,
            image=image
            # image=image
        )
        serializers=VisitorSerializer(visitor,many=False)
        json_data = json.dumps(serializers.data)
        # print('Image object:', image)
        # print('Image name:', image.name)
        # print('Image size:', image.size)
        print('yukesh',image)
        if image:
            try:
                with open(image,"rb") as image_file:
                    print('=====================')
                    image_data=image_file.read()
                    # print('imagedata',image_data)
                    image_base64=base64.b64encode(image_data).decode('utf-8')
                    print(image_base64)

            except IOError:
                return HttpResponse("Error: Unable to read the image file.", status=500)
        # print('data=',json_data)
        api_url="https://dev.saraloms.com/api/user/save_visitors"
        headers={'Content-Type':'application/json'}
        response=requests.post(api_url,json=serializers.data,headers=headers)
        print('External API response status:', response.status_code)
        print('External API response content:', response.content)
        if response.status_code==200:
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"detail":"Failed to save data to external API."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # return Response(serializers.data, status=status.HTTP_201_CREATED)

        # return render(request, 'index.html')

    except Exception as e:
            print('------',data)
            message={'detail':'User with this email already exists'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def capture(request):
    try:
        img_cap()  # Call the function to capture an image

        # Return a success response
        return Response({'detail': 'Image captured successfully.'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f'Error: {e}')  # Print the error for debugging
        return Response({'detail': 'An error occurred. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
    



