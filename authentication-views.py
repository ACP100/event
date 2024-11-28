from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['POST'])
    def user_login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data
            })
        
        return Response({'error': 'Invalid credentials'}, status=400)
    
    @action(detail=False, methods=['POST'])
    def user_logout(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'})
    
    @action(detail=False, methods=['POST'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data
            })
        return Response(serializer.errors, status=400)
