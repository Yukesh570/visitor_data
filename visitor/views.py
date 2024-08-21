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

from .detect import run_detection
# Create your views here.


@api_view(['POST'])
def register(request):
    # visitor=Visitor_data.objects.get(id=id)
    # pk=visitor.id
    # print('---------------',pk)
    data=request.data
    # image=request.FILES.get('image')
    run_detection()
    
    try:
        visitor=Visitor_data.objects.create(
            name=data['name'],
            phone_no=data['phone_no'],
            address=data['address'],
            email=data['email'],
            no_of_person=data['no_of_person'],
            purpose=data['purpose'],
            created_at=data['created_at'],
            # image=image
        )
        serializers=VisitorSerializer(visitor,many=False)
        return Response(serializers.data, status=status.HTTP_201_CREATED)

        # return render(request, 'index.html')

    except Exception as e:
            print(data)
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
    



def get_latest_image():
    image_pattern=os.path.join(settings.MEDIA_ROOT,'images','*.jpg')

    image_files=glob.glob(image_pattern)
    if not image_files:
        return None
    
    latest_image=max(image_files,key=os.path.getmtime)
    return latest_image
    

def serve_latest_image(request):
    latest_image_path = get_latest_image()
    print(f'Latest image path: {latest_image_path}')  # Print the result for debugging

    if latest_image_path is None:
        return HttpResponse("No images found.", status=404)

    # Determine the MIME type of the image
    mime_type, _ = mimetypes.guess_type(latest_image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type for unknown types

    with open(latest_image_path, 'rb') as img:
        response = HttpResponse(img.read(), content_type=mime_type)
        response['Content-Disposition'] = f'inline; filename={os.path.basename(latest_image_path)}'
        return response