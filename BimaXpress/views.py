import json
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from .models import Users
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse


class UsersAPI(APIView):
    @csrf_exempt
    def get(self, request):
        user = Users.objects.filter(hospital='abnew@gmail.com')
        serializer = UserSerializer(user, many=True)
        return JsonResponse(serializer.data,safe=False)
    
    @csrf_exempt
    def post(self, request, format=None):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            poll = Users(**data)
            poll.save()
            response = serializer.data
            return JsonResponse("Added Successfully",safe=False)

            
    @csrf_exempt
    def put(self, request, format=None):
        data=request.data
        user=Users.objects.filter(hospital=data['hospital'])
        serializer=UserSerializer(user,data=data)
        if serializer.is_valid():
            poll = Users(**data)
            poll.save()
            response = serializer.data
            return JsonResponse("Updated Successfully",safe=False)
    

    @csrf_exempt
    def delete(self, id=0):
        print(id)
        user=Users.objects.get(UserId=id)
        user.delete()
        return JsonResponse("Deleted Successfully",safe=False)


class DoctorAPI(APIView):
    @csrf_exempt
    def get(self, request):
        user = Users.objects.filter(role='doctor')
        serializer = UserSerializer(user, many=True)
        return JsonResponse(serializer.data,safe=False)
class ClaimAPI(APIView):
    @csrf_exempt
    def get(self, request):
        user = Users.objects.filter(role='claim_analyst')
        serializer = UserSerializer(user, many=True)
        return JsonResponse(serializer.data,safe=False)        