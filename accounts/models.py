from django.db import models
from django.contrib.auth.models import User


# ==============================
# EVENT MODEL
# ==============================

class Event(models.Model):

    CATEGORY_CHOICES = [
        ('concert', 'Concert'),
        ('sports', 'Sports'),
        ('festival', 'Festival'),
        ('college', 'College Event'),
        ('other', 'Other'),
    ]

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    location = models.CharField(
        max_length=200
    )

    event_date = models.DateField()

    event_time = models.TimeField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# ==============================
# BOOKING MODEL
# ==============================

class Booking(models.Model):

    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )

    tickets = models.PositiveIntegerField(
        default=1
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='confirmed'
    )

    booking_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


# ==============================
# USER PROFILE MODEL
# ==============================

class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    roll_number = models.CharField(
        max_length=50,
        blank=True
    )

    register_number = models.CharField(
        max_length=50,
        blank=True
    )

    course = models.CharField(
        max_length=200,
        blank=True
    )

    semester = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# ==============================
# NOTIFICATION MODEL
# ==============================

class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.title}"