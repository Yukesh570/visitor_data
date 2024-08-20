from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


@api_view(['POST'])
def register(request):
    data=request.data
    image=request.FILES.get('image')
    try:
        visitor=Visitor_data.objects.create(
            name=data['name'],
            phone_no=data['phone_no'],
            address=data['adderss'],
            email=data['email'],
            no_of_person=data['no_of_perosn'],
            purpose=data['purpose'],
            created_at=data['created_at'],
            image=image
        )
    except:
            message={'detail':'User with this email already exists'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)

        