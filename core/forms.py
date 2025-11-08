from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django import forms
from django.utils import timezone

from .models import (
    CustomUser, UserProfile, HospitalProfile, ContactMessage,
    BloodRequest, BloodCamp, Donation, BloodStock, AIPredictionLog,PasswordResetToken,
)

# ============================================================================ #
# 1. AUTHENTICATION & REGISTRATION FORMS
# ============================================================================ #

class UserRegistrationForm(UserCreationForm):
    """Form for Hemo User (Donor) registration."""
    gender = forms.ChoiceField(choices=UserProfile.Gender.choices, widget=forms.Select(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    weight = forms.IntegerField(label="Weight (in Kgs)", min_value=40, max_value=150, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    blood_group = forms.ChoiceField(choices=UserProfile.BloodGroup.choices, widget=forms.Select(attrs={'class': 'form-control'}))
    contact_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91XXXXXXXXXX'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pincode = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    
    # Availability settings
    availability_radius = forms.IntegerField(
        label="Availability Radius (km)", 
        min_value=1, 
        max_value=100, 
        initial=10,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to password fields
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.Role.DONOR
        if commit:
            user.save()
            # Create user profile
            UserProfile.objects.create(
                user=user,
                gender=self.cleaned_data.get('gender'),
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                weight=self.cleaned_data.get('weight'),
                blood_group=self.cleaned_data.get('blood_group'),
                contact_number=self.cleaned_data.get('contact_number'),
                address=self.cleaned_data.get('address'),
                city=self.cleaned_data.get('city'),
                state=self.cleaned_data.get('state'),
                pincode=self.cleaned_data.get('pincode'),
                profile_photo=self.cleaned_data.get('profile_photo'),
                availability_radius=self.cleaned_data.get('availability_radius')
            )
        return user

class HospitalRegistrationForm(UserCreationForm):
    """Form for Hemo Hospital Admin registration."""
    admin_full_name = forms.CharField(label="Your Full Name", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    admin_gender = forms.ChoiceField(label="Your Gender", choices=UserProfile.Gender.choices, widget=forms.Select(attrs={'class': 'form-control'}))
    admin_dob = forms.DateField(label="Your Date of Birth", widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    admin_designation = forms.CharField(label="Your Designation", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    hospital_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    hospital_reg_id = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    hospital_logo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label="Hospital Address", widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pincode = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact_number = forms.CharField(label="Hospital Contact Number", max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    website = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to password fields
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.Role.HOSPITAL
        
        full_name_parts = self.cleaned_data.get('admin_full_name', '').split()
        user.first_name = full_name_parts[0] if full_name_parts else ''
        user.last_name = ' '.join(full_name_parts[1:]) if len(full_name_parts) > 1 else ''
        
        if commit:
            user.save()
            # Create hospital profile
            HospitalProfile.objects.create(
                user=user,
                admin_full_name=self.cleaned_data.get('admin_full_name'),
                admin_gender=self.cleaned_data.get('admin_gender'),
                admin_dob=self.cleaned_data.get('admin_dob'),
                admin_designation=self.cleaned_data.get('admin_designation'),
                hospital_name=self.cleaned_data.get('hospital_name'),
                hospital_reg_id=self.cleaned_data.get('hospital_reg_id'),
                address=self.cleaned_data.get('address'),
                city=self.cleaned_data.get('city'),
                state=self.cleaned_data.get('state'),
                pincode=self.cleaned_data.get('pincode'),
                contact_number=self.cleaned_data.get('contact_number'),
                website=self.cleaned_data.get('website'),
                hospital_logo=self.cleaned_data.get('hospital_logo')
            )
        return user

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Enter your email...'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Enter your password...'
        })

# ============================================================================ #
# 2. PROFILE & SETTINGS FORMS
# ============================================================================ #

class UserProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = UserProfile
        fields = ['gender', 'date_of_birth', 'weight', 'blood_group', 'contact_number', 
                 'address', 'city', 'state', 'pincode', 'profile_photo', 
                 'is_available', 'availability_radius']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'availability_radius': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class HospitalProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label="Admin First Name", max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Admin Last Name", max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = HospitalProfile
        exclude = ['user', 'is_verified']
        widgets = {
            'admin_full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'admin_gender': forms.Select(attrs={'class': 'form-control'}),
            'admin_dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'admin_designation': forms.TextInput(attrs={'class': 'form-control'}),
            'hospital_name': forms.TextInput(attrs={'class': 'form-control'}),
            'hospital_reg_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'hospital_logo': forms.FileInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email_notifications_enabled', 'sms_notifications_enabled']
        widgets = {
            'email_notifications_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sms_notifications_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'email_notifications_enabled': 'Enable Email Notifications',
            'sms_notifications_enabled': 'Enable SMS Notifications',
        }

# ============================================================================ #
# 3. DONOR-SPECIFIC FORMS
# ============================================================================ #

class DonationResponseForm(forms.Form):
    age = forms.IntegerField(
        label="Current Age", 
        required=True, 
        min_value=18, 
        max_value=65,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your current age'
        })
    )
    weight = forms.IntegerField(
        label="Current Weight (in Kgs)", 
        required=True, 
        min_value=50,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your current weight'
        })
    )
    has_disease = forms.BooleanField(
        label="I confirm I am NOT suffering from any chronic diseases.", 
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18 or age > 65:
            raise forms.ValidationError("Age must be between 18 and 65 years to donate blood.")
        return age
    
    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight < 50:
            raise forms.ValidationError("Weight must be at least 50 kg to donate blood.")
        return weight

class DonationStatusUpdateForm(forms.ModelForm):
    """Form for updating donation status"""
    class Meta:
        model = Donation
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'})
        }

# ============================================================================ #
# 4. HOSPITAL-SPECIFIC FORMS
# ============================================================================ #

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        exclude = ['hospital', 'is_active', 'created_at', 'fulfillment_percentage', 'donor', 'status']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'units_required': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'urgency': forms.Select(attrs={'class': 'form-control'}),
            'family_member_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Any additional notes...'}),
            'expires_on': DateTimeInput(attrs={'class': 'form-control'}),
        }
    
    def clean_units_required(self):
        units = self.cleaned_data.get('units_required')
        if units < 1:
            raise forms.ValidationError("Units required must be at least 1.")
        if units > 10:
            raise forms.ValidationError("Cannot request more than 10 units at once.")
        return units
    
    def clean_expires_on(self):
        expires_on = self.cleaned_data.get('expires_on')
        if expires_on and expires_on <= timezone.now():
            raise forms.ValidationError("Expiry date must be in the future.")
        return expires_on

class BloodCampForm(forms.ModelForm):
    class Meta:
        model = BloodCamp
        exclude = ['organized_by', 'is_active', 'actual_donors']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blood Donation Camp 2024'}),
            'venue': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'start_datetime': DateTimeInput(attrs={'class': 'form-control'}),
            'end_datetime': DateTimeInput(attrs={'class': 'form-control'}),
            'expected_donors': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_datetime = cleaned_data.get('start_datetime')
        end_datetime = cleaned_data.get('end_datetime')
        
        if start_datetime and end_datetime:
            if start_datetime >= end_datetime:
                raise forms.ValidationError("End datetime must be after start datetime.")
            if start_datetime <= timezone.now():
                raise forms.ValidationError("Start datetime must be in the future.")
        
        return cleaned_data

class BloodStockUpdateForm(forms.ModelForm):
    """Form for updating blood stock levels"""
    class Meta:
        model = BloodStock
        fields = ['units', 'units_available', 'minimum_threshold', 'critical_threshold']
        widgets = {
            'units': forms.NumberInput(attrs={'class': 'form-control'}),
            'units_available': forms.NumberInput(attrs={'class': 'form-control'}),
            'minimum_threshold': forms.NumberInput(attrs={'class': 'form-control'}),
            'critical_threshold': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        units = cleaned_data.get('units')
        units_available = cleaned_data.get('units_available')
        minimum_threshold = cleaned_data.get('minimum_threshold')
        critical_threshold = cleaned_data.get('critical_threshold')
        
        if units_available and units and units_available > units:
            raise forms.ValidationError("Available units cannot exceed total units.")
        
        if minimum_threshold and critical_threshold and minimum_threshold <= critical_threshold:
            raise forms.ValidationError("Minimum threshold must be greater than critical threshold.")
        
        return cleaned_data

# ============================================================================ #
# 5. ANALYTICS & AI FORMS
# ============================================================================ #

class AnalyticsFilterForm(forms.Form):
    """Form for filtering analytics data"""
    DATE_RANGE_CHOICES = [
        ('7', 'Last 7 Days'),
        ('30', 'Last 30 Days'),
        ('90', 'Last 90 Days'),
        ('365', 'Last Year'),
        ('custom', 'Custom Range'),
    ]
    
    date_range = forms.ChoiceField(
        choices=DATE_RANGE_CHOICES,
        initial='30',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    blood_group = forms.ChoiceField(
        choices=[('', 'All Blood Groups')] + list(UserProfile.BloodGroup.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        date_range = cleaned_data.get('date_range')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if date_range == 'custom':
            if not start_date or not end_date:
                raise forms.ValidationError("Both start date and end date are required for custom range.")
            if start_date > end_date:
                raise forms.ValidationError("Start date cannot be after end date.")
        
        return cleaned_data

class AIPredictionFilterForm(forms.Form):
    """Form for filtering AI prediction logs"""
    PREDICTION_TYPE_CHOICES = [
        ('', 'All Types'),
        ('DONOR_MATCH', 'Donor Matching'),
        ('ELIGIBILITY_PREDICTION', 'Eligibility Prediction'),
        ('DEMAND_PREDICTION', 'Demand Prediction'),
        ('RETENTION_RISK', 'Retention Risk Analysis'),
    ]
    
    prediction_type = forms.ChoiceField(
        choices=PREDICTION_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    min_confidence = forms.FloatField(
        required=False,
        min_value=0.0,
        max_value=1.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': '0.0'
        })
    )

class ChatbotFeedbackForm(forms.Form):
    """Form for collecting chatbot feedback"""
    RATING_CHOICES = [
        (1, '⭐ - Poor'),
        (2, '⭐⭐ - Fair'),
        (3, '⭐⭐⭐ - Good'),
        (4, '⭐⭐⭐⭐ - Very Good'),
        (5, '⭐⭐⭐⭐⭐ - Excellent'),
    ]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True
    )
    
    feedback = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Any additional feedback...'
        })
    )
    
    improve_suggestions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Suggestions for improvement...'
        })
    )

# ============================================================================ #
# 6. CORE PUBLIC FORMS
# ============================================================================ #

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject of your message'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Your message here...'
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Basic email validation
        if not email or '@' not in email:
            raise forms.ValidationError("Please enter a valid email address.")
        return email

# ============================================================================ #
# 7. BULK ACTION FORMS
# ============================================================================ #

class BulkNotificationForm(forms.Form):
    """Form for sending bulk notifications"""
    NOTIFICATION_TYPE_CHOICES = [
        ('BLOOD_REQUEST', 'Blood Request Alert'),
        ('CAMP_ALERT', 'Blood Camp Notification'),
        ('SYSTEM_ALERT', 'System Update'),
    ]
    
    notification_type = forms.ChoiceField(
        choices=NOTIFICATION_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    target_blood_groups = forms.MultipleChoiceField(
        choices=UserProfile.BloodGroup.choices,
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    
    target_cities = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City names separated by commas'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter your notification message...'
        })
    )
    
    def clean_target_cities(self):
        cities = self.cleaned_data.get('target_cities', '')
        if cities:
            city_list = [city.strip() for city in cities.split(',') if city.strip()]
            return city_list
        return []

class BulkDonorExportForm(forms.Form):
    """Form for exporting donor data"""
    EXPORT_FORMAT_CHOICES = [
        ('csv', 'CSV Format'),
        ('excel', 'Excel Format'),
        ('json', 'JSON Format'),
    ]
    
    export_format = forms.ChoiceField(
        choices=EXPORT_FORMAT_CHOICES,
        initial='csv',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    include_personal_info = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    include_donation_history = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    include_analytics = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

# ============================================================================ #
# 8. SEARCH & FILTER FORMS
# ============================================================================ #

class DonorSearchForm(forms.Form):
    """Form for searching donors"""
    blood_group = forms.ChoiceField(
        choices=[('', 'All Blood Groups')] + list(UserProfile.BloodGroup.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by city...'
        })
    )
    
    availability = forms.ChoiceField(
        choices=[
            ('', 'All'),
            ('available', 'Available Only'),
            ('unavailable', 'Unavailable Only'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    min_donations = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min donations'
        })
    )

class BloodRequestSearchForm(forms.Form):
    """Form for searching blood requests"""
    STATUS_CHOICES = [
        ('', 'All Status'),
        ('active', 'Active Only'),
        ('fulfilled', 'Fulfilled Only'),
        ('expired', 'Expired Only'),
    ]
    
    blood_group = forms.ChoiceField(
        choices=[('', 'All Blood Groups')] + list(UserProfile.BloodGroup.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    urgency = forms.ChoiceField(
        choices=[('', 'All Urgency')] + list(BloodRequest.UrgencyLevel.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    hospital = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Hospital name...'
        })
    )

# ============================================================================ #
# PASSWORD RESET FORMS (NEW)
# ============================================================================ #

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter your registered email address'
        })
    )

class PasswordResetConfirmForm(forms.Form):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter new password'
        })
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Confirm new password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        
        # Basic password strength check
        if password1 and len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        
        return cleaned_data