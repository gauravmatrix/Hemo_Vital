from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from datetime import timedelta
from django.utils import timezone

# ============================================================================ #
# 1. AUTHENTICATION & PROFILE MODELS
# ============================================================================ #

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email: raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', CustomUser.Role.ADMIN)
        if not extra_fields.get('is_staff'): raise ValueError(_('Superuser must have is_staff=True.'))
        if not extra_fields.get('is_superuser'): raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"; DONOR = "DONOR", "Donor"; HOSPITAL = "HOSPITAL", "Hospital"
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.DONOR)
    hemo_id = models.CharField(max_length=20, unique=True, blank=True, null=True, editable=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.hemo_id:
            prefix = "HV-HOS-" if self.role == self.Role.HOSPITAL else "HV-USR-"
            self.hemo_id = prefix + str(uuid.uuid4().hex)[:6].upper()
        super().save(*args, **kwargs)
    def __str__(self): return f"{self.email} ({self.get_role_display()})"

class UserProfile(models.Model):
    class BloodGroup(models.TextChoices):
        A_POSITIVE = 'A+', 'A+'; A_NEGATIVE = 'A-', 'A-'; B_POSITIVE = 'B+', 'B+'; B_NEGATIVE = 'B-', 'B-';
        O_POSITIVE = 'O+', 'O+'; O_NEGATIVE = 'O-', 'O-'; AB_POSITIVE = 'AB+', 'AB+'; AB_NEGATIVE = 'AB-', 'AB-'
    class Gender(models.TextChoices):
        MALE = 'Male', 'Male'; FEMALE = 'Female', 'Female'; OTHER = 'Other', 'Other'
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='userprofile')
    gender = models.CharField(max_length=10, choices=Gender.choices, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True, help_text="Weight in Kgs")
    blood_group = models.CharField(max_length=3, choices=BloodGroup.choices, null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', default='profile_photos/default.png')
    last_donation_date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    email_notifications_enabled = models.BooleanField(default=True)
    sms_notifications_enabled = models.BooleanField(default=False)
    availability_radius = models.PositiveIntegerField(default=10, help_text="Availability radius in km")
    profile_completion_score = models.PositiveIntegerField(default=0)
    
    # Analytics fields
    total_donations = models.PositiveIntegerField(default=0)
    engagement_score = models.FloatField(default=0.0)
    last_activity = models.DateTimeField(null=True, blank=True)
    
    def __str__(self): return f"Profile: {self.user.email}"
    
    def calculate_profile_completion(self):
        """Calculate profile completion percentage"""
        fields = ['gender', 'date_of_birth', 'weight', 'blood_group', 'contact_number', 'address', 'city', 'state', 'pincode']
        completed = sum(1 for field in fields if getattr(self, field))
        return int((completed / len(fields)) * 100)
    
    def save(self, *args, **kwargs):
        self.profile_completion_score = self.calculate_profile_completion()
        super().save(*args, **kwargs)

class HospitalProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='hospitalprofile')
    admin_full_name = models.CharField(max_length=255)
    admin_gender = models.CharField(max_length=10, choices=UserProfile.Gender.choices)
    admin_dob = models.DateField()
    admin_designation = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=255)
    hospital_reg_id = models.CharField(max_length=100, unique=True)
    hospital_logo = models.ImageField(upload_to='hospital_logos/', default='hospital_logos/default.png')
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    contact_number = models.CharField(max_length=15)
    website = models.URLField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    # Analytics fields
    total_blood_requests = models.PositiveIntegerField(default=0)
    fulfillment_rate = models.FloatField(default=0.0)
    avg_response_time = models.FloatField(default=0.0, help_text="Average response time in hours")
    
    def __str__(self): return f"Hospital: {self.hospital_name}"

# ============================================================================ #
# 2. DONOR-RELATED MODELS
# ============================================================================ #

class Donation(models.Model):
    class DonationStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        CONFIRMED = 'Confirmed', 'Confirmed'
        REJECTED = 'Rejected', 'Rejected'
        COMPLETED = 'Completed', 'Completed'

    donor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='donations')
    hospital_name = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    donation_date = models.DateField()
    units = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=DonationStatus.choices, default=DonationStatus.PENDING)
    
    # Enhanced fields for AI predictions
    age = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    has_disease = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Link to blood request
    blood_request = models.ForeignKey('BloodRequest', on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')

    def __str__(self):
        return f"{self.donor.username} - {self.status}"

class Badge(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon_class = models.CharField(max_length=50)
    required_donations = models.PositiveIntegerField(default=1)
    def __str__(self): return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    date_awarded = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ('user', 'badge')
    def __str__(self): return f"{self.user.username} - {self.badge.name}"

class Certificate(models.Model):
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE, related_name='certificate')
    certificate_id = models.CharField(max_length=50, unique=True)
    generated_on = models.DateTimeField(auto_now_add=True)
    file_path = models.FileField(upload_to='certificates/')
    def __str__(self): return f"Certificate for {self.donation}"

# ============================================================================ #
# 3. HOSPITAL-RELATED MODELS
# ============================================================================ #

class BloodRequest(models.Model):
    class UrgencyLevel(models.TextChoices):
        CRITICAL = 'Critical', 'Critical'
        URGENT = 'Urgent', 'Urgent'
        NORMAL = 'Normal', 'Normal'

    hospital = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blood_requests')
    patient_name = models.CharField(max_length=150)
    patient_age = models.PositiveIntegerField()
    blood_group = models.CharField(max_length=3, choices=UserProfile.BloodGroup.choices)
    units_required = models.PositiveIntegerField(default=1)
    urgency = models.CharField(max_length=20, choices=UrgencyLevel.choices, default=UrgencyLevel.NORMAL)
    family_member_name = models.CharField(max_length=150)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    expires_on = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Enhanced fields for analytics
    fulfillment_percentage = models.FloatField(default=0.0)
    donor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='donor_responses')
    status = models.CharField(max_length=20, choices=[('Pending','Pending'),('Accepted','Accepted'),('Fulfilled','Fulfilled')], default='Pending')

    def __str__(self):
        return f"{self.blood_group} request by {self.hospital.hospitalprofile.hospital_name}"

    def update_fulfillment(self):
        """Update fulfillment percentage based on confirmed donations"""
        confirmed_donations = self.donations.filter(status=Donation.DonationStatus.CONFIRMED)
        total_confirmed_units = confirmed_donations.aggregate(total=models.Sum('units'))['total'] or 0
        
        if self.units_required > 0:
            self.fulfillment_percentage = min(100, (total_confirmed_units / self.units_required) * 100)
            
            # Auto-deactivate if fully fulfilled
            if self.fulfillment_percentage >= 100:
                self.is_active = False
                self.status = 'Fulfilled'
        
        self.save()

class BloodCamp(models.Model):
    organized_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='camps')
    title = models.CharField(max_length=200)
    venue = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    expected_donors = models.PositiveIntegerField(default=0)
    actual_donors = models.PositiveIntegerField(default=0)
    
    def __str__(self): return self.title

class BloodStock(models.Model):
    hospital = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blood_stock')
    blood_group = models.CharField(max_length=3, choices=UserProfile.BloodGroup.choices)
    units = models.PositiveIntegerField(default=0)
    units_available = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Safety thresholds
    minimum_threshold = models.PositiveIntegerField(default=5)
    critical_threshold = models.PositiveIntegerField(default=2)

    class Meta:
        unique_together = ('hospital', 'blood_group')

    def __str__(self):
        return f"{self.hospital.hospitalprofile.hospital_name} - {self.blood_group}: {self.units} units"
    
    def get_stock_status(self):
        """Get stock status for alerts"""
        if self.units_available <= self.critical_threshold:
            return 'Critical'
        elif self.units_available <= self.minimum_threshold:
            return 'Low'
        else:
            return 'Adequate'

# ============================================================================ #
# 4. ANALYTICS & AI MODELS
# ============================================================================ #

class DonorAnalytics(models.Model):
    """Analytics data for donors"""
    donor = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='analytics')
    engagement_score = models.FloatField(default=0.0)
    response_rate = models.FloatField(default=0.0, help_text="Response rate to blood requests")
    avg_response_time = models.FloatField(default=0.0, help_text="Average response time in hours")
    last_activity = models.DateTimeField(null=True, blank=True)
    total_notifications = models.PositiveIntegerField(default=0)
    notifications_read = models.PositiveIntegerField(default=0)
    profile_views = models.PositiveIntegerField(default=0)
    
    # Risk scores
    retention_risk_score = models.FloatField(default=0.0)
    churn_probability = models.FloatField(default=0.0)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics for {self.donor.username}"

class HospitalAnalytics(models.Model):
    """Analytics data for hospitals"""
    hospital = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='hospital_analytics')
    total_requests = models.PositiveIntegerField(default=0)
    fulfilled_requests = models.PositiveIntegerField(default=0)
    fulfillment_rate = models.FloatField(default=0.0)
    avg_response_time = models.FloatField(default=0.0)
    total_donors_engaged = models.PositiveIntegerField(default=0)
    donor_satisfaction_score = models.FloatField(default=0.0)
    
    # Blood group specific stats
    blood_group_stats = models.JSONField(default=dict)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics for {self.hospital.hospitalprofile.hospital_name}"

class Notification(models.Model):
    class NotificationType(models.TextChoices):
        BLOOD_REQUEST = 'BLOOD_REQUEST', 'New Blood Request'
        REQUEST_UPDATE = 'REQUEST_UPDATE', 'Request Status Update'
        BADGE_UNLOCKED = 'BADGE_UNLOCKED', 'Badge Unlocked'
        CAMP_ALERT = 'CAMP_ALERT', 'New Blood Camp'
        SYSTEM_ALERT = 'SYSTEM_ALERT', 'System Alert'
        STOCK_ALERT = 'STOCK_ALERT', 'Blood Stock Alert'
    
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NotificationType.choices)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_content_type = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta: 
        ordering = ['-created_at']
    
    def __str__(self): 
        return f"Notification for {self.recipient.username}"

class AIPredictionLog(models.Model):
    class PredictionType(models.TextChoices):
        DONOR_MATCH = 'DONOR_MATCH', 'Donor Matching'
        ELIGIBILITY_PREDICTION = 'ELIGIBILITY_PREDICTION', 'Eligibility Prediction'
        DEMAND_PREDICTION = 'DEMAND_PREDICTION', 'Demand Prediction'
        RETENTION_RISK = 'RETENTION_RISK', 'Retention Risk Analysis'
    
    prediction_type = models.CharField(max_length=50, choices=PredictionType.choices)
    target_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    input_data = models.JSONField(null=True, blank=True)
    output_data = models.JSONField(null=True, blank=True)
    confidence_score = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): 
        return f"{self.get_prediction_type_display()} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class ChatbotConversation(models.Model):
    """Store chatbot conversations for training and analytics"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100)
    user_message = models.TextField()
    bot_response = models.TextField()
    intent_detected = models.CharField(max_length=100, null=True, blank=True)
    confidence_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Chat: {self.session_id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

# ============================================================================ #
# 5. OTHER CORE MODELS
# ============================================================================ #

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    
    def __str__(self): 
        return f"Message from {self.name}"

# ============================================================================ #
# 6. HEMOVITAL (Global Settings)
# ============================================================================ #

class GlobalSetting(models.Model):
    donation_gap_days = models.PositiveIntegerField(default=90)
    default_search_radius_km = models.PositiveIntegerField(default=10)
    site_contact_email = models.EmailField(default="support@hemovital.com")
    ai_prediction_enabled = models.BooleanField(default=True)
    chatbot_enabled = models.BooleanField(default=True)
    analytics_enabled = models.BooleanField(default=True)
    
    def __str__(self): 
        return "HemoVital Global Settings"
    
    def save(self, *args, **kwargs): 
        self.pk = 1
        super(GlobalSetting, self).save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        return cls.objects.get_or_create(pk=1)[0]

# ============================================================================ #
# SIGNALS
# ============================================================================ #

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile when user is created"""
    if created:
        if instance.role == CustomUser.Role.DONOR:
            UserProfile.objects.create(user=instance)
        elif instance.role == CustomUser.Role.HOSPITAL:
            HospitalProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def create_analytics(sender, instance, created, **kwargs):
    """Create analytics record when user is created"""
    if created:
        if instance.role == CustomUser.Role.DONOR:
            DonorAnalytics.objects.create(donor=instance)
        elif instance.role == CustomUser.Role.HOSPITAL:
            HospitalAnalytics.objects.create(hospital=instance)

@receiver(post_save, sender=Donation)
def update_donation_analytics(sender, instance, created, **kwargs):
    """Update analytics when donation is created/updated"""
    if instance.status == Donation.DonationStatus.CONFIRMED:
        # Update donor analytics
        donor_analytics, _ = DonorAnalytics.objects.get_or_create(donor=instance.donor)
        donor_analytics.total_notifications += 1
        donor_analytics.save()
        
        # Update hospital analytics if linked to blood request
        if instance.blood_request:
            hospital_analytics, _ = HospitalAnalytics.objects.get_or_create(hospital=instance.blood_request.hospital)
            hospital_analytics.fulfilled_requests += 1
            hospital_analytics.save()

# ============================================================================ #
# 7. PASSWORD RESET & AUTH MODELS
# ============================================================================ #

class PasswordResetToken(models.Model):
    """Custom password reset token model"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Password reset for {self.user.email}"

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

    class Meta:
        ordering = ['-created_at']

# ADD THIS SIGNAL at the end of models.py

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile when user is created"""
    if created:
        if instance.role == CustomUser.Role.DONOR:
            UserProfile.objects.create(user=instance)
        elif instance.role == CustomUser.Role.HOSPITAL:
            HospitalProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)  
def save_user_profile(sender, instance, **kwargs):
    """Save profile when user is saved"""
    try:
        if instance.role == CustomUser.Role.DONOR:
            instance.userprofile.save()
        elif instance.role == CustomUser.Role.HOSPITAL:
            instance.hospitalprofile.save()
    except (UserProfile.DoesNotExist, HospitalProfile.DoesNotExist):
        # Profile doesn't exist yet, it will be created by the other signal
        pass