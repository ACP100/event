from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('organizer', 'Organizer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    language_preference = models.CharField(max_length=10, default='en')
    theme_preference = models.CharField(max_length=20, default='default')

class Space(models.Model):
    SPACE_CATEGORIES = (
        ('lab', 'Laboratory'),
        ('hall', 'Hall'),
        ('conference', 'Conference Room'),
        ('other', 'Other')
    )
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SPACE_CATEGORIES)
    capacity = models.IntegerField()
    description = models.TextField(blank=True)
    amenities = models.JSONField(default=dict)
    layout_image = models.ImageField(upload_to='space_layouts/', null=True, blank=True)

class Event(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    participant_count = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    def save(self, *args, **kwargs):
        # Conflict detection logic
        conflicting_events = Event.objects.filter(
            space=self.space,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk)
        
        if conflicting_events.exists():
            raise ValueError("Space is already booked during this time.")
        
        super().save(*args, **kwargs)

class Feedback(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    rating = models.FloatField()
    comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reminder_time = models.DateTimeField()
