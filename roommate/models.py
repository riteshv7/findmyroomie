from django.db import models
from django.contrib.auth.models import AbstractUser

class RoomieUser(AbstractUser):
    # Additional user fields for FindMyRoomie
    phone = models.CharField(unique=True, max_length=15, null=True, blank=True)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=20, 
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        null=True,
        blank=True
    )
    occupation = models.CharField(max_length=100, blank=True)
    languages = models.JSONField(default=list, blank=True) # List of strings e.g. ["English", "Kannada"]
    
    # Roles: "seeker" and/or "lister"
    roles = models.JSONField(default=list, blank=True) # ["seeker", "lister"]
    
    # Seeker preference fields (stored as a JSON dictionary matching lifestyle filters)
    seeker_profile = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return self.username or self.phone or f"User {self.id}"

class Listing(models.Model):
    owner = models.ForeignKey(RoomieUser, on_delete=models.CASCADE, related_name='listings')
    
    ROOM_TYPES = [
        ('private_room', 'Private Room'),
        ('shared_room', 'Shared Room'),
        ('1rk', '1RK'),
        ('1bhk', '1BHK'),
        ('pg_bed', 'PG Bed')
    ]
    type = models.CharField(max_length=30, choices=ROOM_TYPES)
    
    BANGALORE_AREAS = [
        ('Koramangala', 'Koramangala'),
        ('HSR Layout', 'HSR Layout'),
        ('Indiranagar', 'Indiranagar'),
        ('BTM Layout', 'BTM Layout'),
        ('Bellandur', 'Bellandur'),
        ('Marathahalli', 'Marathahalli'),
        ('Whitefield', 'Whitefield'),
        ('Electronic City', 'Electronic City'),
        ('Other', 'Other')
    ]
    area = models.CharField(max_length=50, choices=BANGALORE_AREAS)
    
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    nearest_metro = models.CharField(max_length=100, blank=True)
    
    rent = models.IntegerField()
    deposit = models.IntegerField()
    setup_cost = models.IntegerField(default=0)
    monthly_expense_estimate = models.IntegerField()
    available_from = models.DateField()
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('looking_for_1', 'Looking for 1 Person'),
        ('occupied', 'Occupied')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    photos = models.JSONField(default=list, blank=True) # List of image URLs or file paths
    
    # Household profile representing the reality of the household (lifestyle fields)
    household_profile = models.JSONField(default=dict, blank=True)
    
    house_rules = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} in {self.area} (₹{self.rent}/mo)"

class Interest(models.Model):
    from_user = models.ForeignKey(RoomieUser, on_delete=models.CASCADE, related_name='sent_interests')
    
    TARGET_TYPES = [
        ('listing', 'Listing'),
        ('user', 'User')
    ]
    target_type = models.CharField(max_length=20, choices=TARGET_TYPES, default='listing')
    target_id = models.IntegerField() # ID of target Listing or User
    
    STATUS_CHOICES = [
        ('interested', 'Interested'),
        ('shortlisted', 'Shortlisted'),
        ('connected', 'Connected'),
        ('declined', 'Declined')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='interested')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user.username} -> {self.target_type} {self.target_id} ({self.status})"

class Message(models.Model):
    conversation_id = models.CharField(max_length=100, db_index=True) # e.g. "minId_maxId"
    sender = models.ForeignKey(RoomieUser, on_delete=models.CASCADE, related_name='sent_messages')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Msg from {self.sender.username} in {self.conversation_id} at {self.created_at}"
