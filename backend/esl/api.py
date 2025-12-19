import time
import psutil
import os

from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView

from esl.models import *
from esl.serializers import *

from django.db.models import Avg, Count, Max, Min

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    @action(url_path="info", methods=["GET"], detail=False)
    def get_info(self, request, *args, **kwargs):
        data = {
            "is_authenticated": request.user.is_authenticated
        }
        if request.user.is_authenticated:
            data.update({
                "is_superuser": request.user.is_superuser,
                "username": request.user.username,
                "user_id": request.user.id,
            })
        return Response(data)

    @action(url_path="login", methods=["POST"], detail=False)
    def login(self, request, *args, **kwargs):
        username = request.data.get("user")
        password = request.data.get("pass")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"success": True})
        return Response({"success": False, "error": "Invalid credentials"}, status=400)

    @action(url_path="logout", methods=["GET"], detail=False)
    def logout(self, request, *args, **kwargs):
        logout(request)
        return Response({"success": True})

class HealthViewset(viewsets.ViewSet):
    def list(self, request):
        time.sleep(10)
        return Response({
            "status": "healthy",
            "service": "backend"
        })

class StressTestViewset(viewsets.ViewSet):
    @action(detail=False, methods=['POST'], url_path='stress')
    def memory_stress(self, request):
        mb_to_allocate = int(request.data.get('mb', 500))
        duration = int(request.data.get('duration', 30))
        
        elements_per_mb = 1024 * 1024 // 8 
        
        memory_blocks = []
        
        try:
            chunk_size_mb = 100
            bytes_per_chunk = chunk_size_mb * 1024 * 1024
            
            for i in range(0, mb_to_allocate, chunk_size_mb):
                remaining_mb = min(chunk_size_mb, mb_to_allocate - i)
                if remaining_mb <= 0:
                    break
                    
                array_size = (remaining_mb * elements_per_mb,)
                chunk = np.ones(array_size, dtype=np.float64)
                memory_blocks.append(chunk)
                
                process = psutil.Process(os.getpid())
                current_mb = process.memory_info().rss / 1024 / 1024
                print(f"Allocated {remaining_mb}MB, Total RSS: {current_mb:.2f}MB")
            
            print(f"Holding memory for {duration} seconds...")
            time.sleep(duration)
            
            process = psutil.Process(os.getpid())
            final_mb = process.memory_info().rss / 1024 / 1024
            
            return Response({
                'status': 'success',
                'target_mb': mb_to_allocate,
                'duration_seconds': duration,
                'final_memory_mb': final_mb,
                'message': f'Memory stress test completed'
            })
            
        except MemoryError:
            return Response({
                'status': 'oom',
                'message': 'Out of Memory - pod should be killed',
                'target_mb': mb_to_allocate
            }, status=500)