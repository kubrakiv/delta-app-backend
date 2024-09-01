from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import Profile, Role, AdminProfile, LogistProfile, DriverProfile
from user.serializers import UserSerializer, UserSerializerWithToken, RoleSerializer

from django.contrib.auth.hashers import make_password
from rest_framework import status


class AdminRolePermission(BasePermission):
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        role_name = "admin"
        return  request.user.role.name == role_name


class LogistRolePermission(BasePermission):
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        role_name = "logist"
        return  request.user.role.name == role_name


class DriverRolePermission(BasePermission):
	
	def has_permission(self, request, view):
		if not request.user or not request.user.is_authenticated:
			return False

		role_name = "driver"
		return  request.user.role.name == role_name


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v 

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
	data = request.data

	role_name = data.get("role")
	print("role_name", role_name)
	role = Role.objects.filter(name=role_name).first()

	try:
		profile = Profile.objects.create(
            role=role,
			first_name=data['first_name'],
            last_name=data['last_name'],
			username=data['email'],
			email=data['email'],
            phone_number=data['phone_number'],
			password=make_password(data['password'])
		)
		serializer = UserSerializerWithToken(profile, many=False)
		return Response(serializer.data)
	except:
		message = {'detail': 'Profile with this email already exists'}
		return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    profile = request.user
    print("updateUserProfile", profile)
    data = request.data

    role_name = data.get("role")
    role = Role.objects.filter(name=role_name).first()
    
    profile.role = role
    profile.first_name = data['first_name']
    profile.last_name = data['last_name']
    profile.username = data['email']
    profile.email = data['email']
    profile.phone_number = data['phone_number']
    
    if data['password'] != '':
        profile.password = make_password(data['password'])

    profile.save()

    serializer = UserSerializerWithToken(profile, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([AdminRolePermission])
def updateUser(request, pk): # this function is for User Edit Page
    data = request.data
    print("updateUser", data)

    role_name = data.get("role")
    role = Role.objects.filter(name=role_name).first()

    # Manipulations with user profile data
    profile = Profile.objects.get(id=pk)

    profile.role = role
    profile.first_name = data['first_name']
    profile.last_name = data['last_name']
    profile.username = data['email']
    profile.email = data['email']
    profile.phone_number = data['phone_number']
    
    profile.is_staff = data['is_admin']

    profile.save()

    serializer = UserSerializer(profile, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    profile = request.user
    serializer = UserSerializer(profile, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AdminRolePermission])
def getUsers(request):
    profiles = Profile.objects.all()
    serializer = UserSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AdminRolePermission])
def getUserById(request, pk):
    profile = Profile.objects.get(id=pk)
    serializer = UserSerializer(profile, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([AdminRolePermission])
def deleteUser(request, pk):
    profileForDeletion = Profile.objects.get(id=pk)
    profileForDeletion.delete()
    return Response('Profile was deleted')
