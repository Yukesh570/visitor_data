from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
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

        