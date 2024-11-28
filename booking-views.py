from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Event, Space
from .serializers import EventSerializer, SpaceSerializer
from django.utils import timezone
from django.db.models import Q

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['GET'])
    def upcoming_events(self, request):
        events = Event.objects.filter(
            start_time__gte=timezone.now(),
            status='approved'
        ).order_by('start_time')
        
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def my_events(self, request):
        events = Event.objects.filter(
            organizer=request.user
        ).order_by('-start_time')
        
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'])
    def approve_booking(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'error': 'Only admins can approve bookings'}, status=403)
        
        event = self.get_object()
        event.status = 'approved'
        event.save()
        
        return Response({
            'message': 'Booking approved successfully',
            'event': EventSerializer(event).data
        })
    
    def create(self, request):
        # Additional validation before creating an event
        space = Space.objects.get(pk=request.data.get('space'))
        participant_count = request.data.get('participant_count', 0)
        
        if participant_count > space.capacity:
            return Response({
                'error': 'Participant count exceeds space capacity'
            }, status=400)
        
        return super().create(request)

class SpaceViewSet(viewsets.ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    
    @action(detail=False, methods=['GET'])
    def available_spaces(self, request):
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        
        # Find spaces not booked during specified time
        booked_spaces = Event.objects.filter(
            Q(start_time__lte=end_time) & Q(end_time__gte=start_time)
        ).values_list('space_id', flat=True)
        
        available_spaces = Space.objects.exclude(id__in=booked_spaces)
        
        serializer = SpaceSerializer(available_spaces, many=True)
        return Response(serializer.data)
