from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import (
    CustomUser, UserProfile, HospitalProfile,
    Donation, Badge, UserBadge, Certificate,
    BloodRequest, BloodCamp, BloodStock,
    Notification, AIPredictionLog, ContactMessage, GlobalSetting,
    DonorAnalytics, HospitalAnalytics, ChatbotConversation, PasswordResetToken,
)

# ============================================================================ #
# 1. ACTIONS
# ============================================================================ #

@admin.action(description='Mark selected hospitals as verified')
def make_verified(modeladmin, request, queryset):
    """Admin action to mark one or more hospitals as verified."""
    updated = queryset.update(is_verified=True)
    modeladmin.message_user(request, f'{updated} hospital(s) marked as verified.')

@admin.action(description='Mark selected messages as resolved')
def mark_resolved(modeladmin, request, queryset):
    """Admin action to mark contact messages as resolved."""
    updated = queryset.update(is_resolved=True)
    modeladmin.message_user(request, f'{updated} message(s) marked as resolved.')

@admin.action(description='Export selected analytics data')
def export_analytics(modeladmin, request, queryset):
    """Admin action to export analytics data."""
    # This would typically generate and return a file
    modeladmin.message_user(request, f'Preparing export for {queryset.count()} records...')

@admin.action(description='Run AI predictions on selected items')
def run_ai_predictions(modeladmin, request, queryset):
    """Admin action to run AI predictions."""
    from . import services
    for item in queryset:
        # Example: Run demand prediction for hospitals
        if hasattr(item, 'hospitalprofile'):
            services.predict_blood_demand_advanced(item)
    modeladmin.message_user(request, f'AI predictions run for {queryset.count()} items.')

# ============================================================================ #
# 2. AUTHENTICATION & PROFILE ADMINS
# ============================================================================ #

class CustomUserAdmin(UserAdmin):
    """Custom admin for the CustomUser model."""
    model = CustomUser
    list_display = ('email', 'username', 'role', 'hemo_id', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'username', 'hemo_id', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('hemo_id', 'last_login', 'date_joined')
    
    fieldsets = UserAdmin.fieldsets + (
        ('HemoVital Information', {
            'fields': ('role', 'hemo_id')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('HemoVital Information', {
            'fields': ('role',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('userprofile', 'hospitalprofile')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'city', 'state', 'is_available', 'profile_completion_score', 'last_donation_date')
    list_filter = ('gender', 'blood_group', 'state', 'is_available')
    search_fields = ('user__email', 'user__username', 'contact_number', 'city')
    readonly_fields = ('profile_completion_score', 'total_donations', 'engagement_score')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'gender', 'date_of_birth', 'weight', 'blood_group')
        }),
        ('Contact Information', {
            'fields': ('contact_number', 'address', 'city', 'state', 'pincode')
        }),
        ('Profile Settings', {
            'fields': ('profile_photo', 'is_available', 'availability_radius')
        }),
        ('Donation Information', {
            'fields': ('last_donation_date', 'total_donations')
        }),
        ('Analytics', {
            'fields': ('profile_completion_score', 'engagement_score', 'last_activity')
        }),
        ('Notification Settings', {
            'fields': ('email_notifications_enabled', 'sms_notifications_enabled')
        }),
    )

@admin.register(HospitalProfile)
class HospitalProfileAdmin(admin.ModelAdmin):
    list_display = ('hospital_name', 'user', 'city', 'state', 'is_verified', 'verification_status')
    list_filter = ('is_verified', 'state', 'city')
    search_fields = ('hospital_name', 'hospital_reg_id', 'user__email', 'city')
    readonly_fields = ('user', 'total_blood_requests', 'fulfillment_rate')
    actions = [make_verified]
    
    fieldsets = (
        ('Administrator Information', {
            'fields': ('user', 'admin_full_name', 'admin_gender', 'admin_dob', 'admin_designation')
        }),
        ('Hospital Information', {
            'fields': ('hospital_name', 'hospital_reg_id', 'hospital_logo', 'website')
        }),
        ('Contact Information', {
            'fields': ('address', 'city', 'state', 'pincode', 'contact_number')
        }),
        ('Verification & Analytics', {
            'fields': ('is_verified', 'total_blood_requests', 'fulfillment_rate', 'avg_response_time')
        }),
    )
    
    def verification_status(self, obj):
        if obj.is_verified:
            return format_html('<span style="color: green;">✓ Verified</span>')
        else:
            return format_html('<span style="color: orange;">⏳ Pending</span>')
    verification_status.short_description = 'Status'

# ============================================================================ #
# 3. DONOR-RELATED ADMINS
# ============================================================================ #

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'hospital_name', 'donation_date', 'units', 'status', 'blood_request_link')
    list_filter = ('status', 'donation_date', 'has_disease')
    search_fields = ('donor__username', 'donor__email', 'hospital_name')
    readonly_fields = ('created_at',)
    list_editable = ('status',)
    
    fieldsets = (
        ('Donation Information', {
            'fields': ('donor', 'hospital_name', 'location', 'donation_date', 'units', 'status')
        }),
        ('Donor Health Information', {
            'fields': ('age', 'weight', 'has_disease')
        }),
        ('Request Link', {
            'fields': ('blood_request',)
        }),
        ('System Information', {
            'fields': ('created_at',)
        }),
    )
    
    def blood_request_link(self, obj):
        if obj.blood_request:
            return format_html('<a href="/admin/core/bloodrequest/{}/change/">{}</a>', 
                             obj.blood_request.id, obj.blood_request.patient_name)
        return "-"
    blood_request_link.short_description = 'Blood Request'

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'required_donations', 'icon_class')
    search_fields = ('name', 'description')
    list_editable = ('required_donations',)

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'date_awarded')
    list_filter = ('badge', 'date_awarded')
    search_fields = ('user__username', 'badge__name')
    readonly_fields = ('date_awarded',)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_id', 'donation', 'generated_on')
    search_fields = ('certificate_id', 'donation__donor__username')
    readonly_fields = ('certificate_id', 'generated_on')

# ============================================================================ #
# 4. HOSPITAL-RELATED ADMINS
# ============================================================================ #

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'hospital', 'blood_group', 'urgency', 'units_required', 'is_active', 'fulfillment_percentage', 'created_at')
    list_filter = ('urgency', 'is_active', 'blood_group', 'created_at')
    search_fields = ('patient_name', 'hospital__hospitalprofile__hospital_name', 'family_member_name')
    readonly_fields = ('created_at', 'fulfillment_percentage')
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('patient_name', 'patient_age', 'blood_group', 'urgency')
        }),
        ('Request Details', {
            'fields': ('units_required', 'family_member_name', 'contact_number', 'address', 'notes')
        }),
        ('Hospital Information', {
            'fields': ('hospital',)
        }),
        ('Status & Fulfillment', {
            'fields': ('is_active', 'expires_on', 'fulfillment_percentage', 'status')
        }),
        ('System Information', {
            'fields': ('created_at',)
        }),
    )
    
    def fulfillment_percentage_display(self, obj):
        return f"{obj.fulfillment_percentage}%"
    fulfillment_percentage_display.short_description = 'Fulfillment'

@admin.register(BloodCamp)
class BloodCampAdmin(admin.ModelAdmin):
    list_display = ('title', 'organized_by', 'venue', 'start_datetime', 'is_active', 'donor_participation')
    list_filter = ('is_active', 'start_datetime')
    search_fields = ('title', 'venue', 'organized_by__hospitalprofile__hospital_name')
    
    def donor_participation(self, obj):
        if obj.expected_donors > 0:
            percentage = (obj.actual_donors / obj.expected_donors) * 100
            return f"{obj.actual_donors}/{obj.expected_donors} ({percentage:.1f}%)"
        return f"{obj.actual_donors} donors"
    donor_participation.short_description = 'Participation'

@admin.register(BloodStock)
class BloodStockAdmin(admin.ModelAdmin):
    list_display = ('hospital', 'blood_group', 'units_available', 'stock_status', 'last_updated')
    list_filter = ('blood_group', 'last_updated')
    search_fields = ('hospital__hospitalprofile__hospital_name',)
    readonly_fields = ('last_updated',)
    
    def stock_status(self, obj):
        status = obj.get_stock_status()
        if status == 'Critical':
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', status)
        elif status == 'Low':
            return format_html('<span style="color: orange; font-weight: bold;">{}</span>', status)
        else:
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', status)
    stock_status.short_description = 'Status'

# ============================================================================ #
# 5. ANALYTICS & AI ADMINS
# ============================================================================ #

@admin.register(DonorAnalytics)
class DonorAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('donor', 'engagement_score', 'response_rate', 'retention_risk_score', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('donor__username', 'donor__email')
    readonly_fields = ('last_updated',)
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor',)
        }),
        ('Engagement Metrics', {
            'fields': ('engagement_score', 'response_rate', 'avg_response_time')
        }),
        ('Activity Tracking', {
            'fields': ('last_activity', 'total_notifications', 'notifications_read', 'profile_views')
        }),
        ('Risk Analysis', {
            'fields': ('retention_risk_score', 'churn_probability')
        }),
        ('System Information', {
            'fields': ('last_updated',)
        }),
    )

@admin.register(HospitalAnalytics)
class HospitalAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('hospital', 'fulfillment_rate', 'total_requests', 'total_donors_engaged', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('hospital__hospitalprofile__hospital_name',)
    readonly_fields = ('last_updated', 'blood_group_stats')
    
    fieldsets = (
        ('Hospital Information', {
            'fields': ('hospital',)
        }),
        ('Performance Metrics', {
            'fields': ('total_requests', 'fulfilled_requests', 'fulfillment_rate', 'avg_response_time')
        }),
        ('Donor Engagement', {
            'fields': ('total_donors_engaged', 'donor_satisfaction_score')
        }),
        ('Blood Group Statistics', {
            'fields': ('blood_group_stats',)
        }),
        ('System Information', {
            'fields': ('last_updated',)
        }),
    )

@admin.register(AIPredictionLog)
class AIPredictionLogAdmin(admin.ModelAdmin):
    list_display = ('prediction_type', 'target_user', 'confidence_score', 'timestamp')
    list_filter = ('prediction_type', 'timestamp')
    search_fields = ('target_user__username', 'target_user__email')
    readonly_fields = ('prediction_type', 'target_user', 'input_data', 'output_data', 'timestamp', 'confidence_score')
    actions = [run_ai_predictions]
    
    fieldsets = (
        ('Prediction Information', {
            'fields': ('prediction_type', 'target_user', 'confidence_score')
        }),
        ('Data', {
            'fields': ('input_data', 'output_data')
        }),
        ('System Information', {
            'fields': ('timestamp',)
        }),
    )
    
    def has_add_permission(self, request):
        return False

@admin.register(ChatbotConversation)
class ChatbotConversationAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_id', 'intent_detected', 'confidence_score', 'created_at')
    list_filter = ('intent_detected', 'created_at')
    search_fields = ('user__username', 'user_message', 'bot_response')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Conversation Information', {
            'fields': ('user', 'session_id')
        }),
        ('Messages', {
            'fields': ('user_message', 'bot_response')
        }),
        ('AI Analysis', {
            'fields': ('intent_detected', 'confidence_score')
        }),
        ('System Information', {
            'fields': ('created_at',)
        }),
    )

# ============================================================================ #
# 6. NOTIFICATION & SYSTEM ADMINS
# ============================================================================ #

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'is_read', 'created_at', 'short_message')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read',)
    
    def short_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at', 'is_resolved', 'short_message')
    list_filter = ('is_resolved', 'submitted_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'submitted_at')
    actions = [mark_resolved]
    list_editable = ('is_resolved',)
    
    def short_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message'

# ============================================================================ #
# 7. GLOBAL SETTINGS ADMIN
# ============================================================================ #

@admin.register(GlobalSetting)
class GlobalSettingAdmin(admin.ModelAdmin):
    list_display = ('setting_name', 'donation_gap_days', 'default_search_radius_km', 'ai_prediction_enabled', 'chatbot_enabled')
    list_editable = ('donation_gap_days', 'default_search_radius_km', 'ai_prediction_enabled', 'chatbot_enabled')
    
    def setting_name(self, obj):
        return "Global Settings"
    setting_name.short_description = "Settings"
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

# ============================================================================ #
# 8. CUSTOM ADMIN SITE CONFIGURATION
# ============================================================================ #

class HemoVitalAdminSite(admin.AdminSite):
    site_header = "HemoVital Administration"
    site_title = "HemoVital Admin"
    index_title = "Welcome to HemoVital Administration"
    
    def get_app_list(self, request):
        """
        Customize the app list in admin panel
        """
        app_list = super().get_app_list(request)
        
        # Reorder apps for better organization
        ordered_apps = []
        core_app = None
        
        for app in app_list:
            if app['app_label'] == 'core':
                core_app = app
                # Reorder models within core app
                model_ordering = [
                    'CustomUser', 'UserProfile', 'HospitalProfile',
                    'BloodRequest', 'Donation', 'BloodCamp', 'BloodStock',
                    'DonorAnalytics', 'HospitalAnalytics', 'AIPredictionLog',
                    'Notification', 'ChatbotConversation', 'ContactMessage',
                    'Badge', 'UserBadge', 'Certificate', 'GlobalSetting'
                ]
                
                ordered_models = []
                for model_name in model_ordering:
                    for model in app['models']:
                        if model['object_name'] == model_name:
                            ordered_models.append(model)
                            break
                
                # Add any remaining models not in ordering list
                for model in app['models']:
                    if model not in ordered_models:
                        ordered_models.append(model)
                
                core_app['models'] = ordered_models
                ordered_apps.insert(0, core_app)  # Put core app first
            else:
                ordered_apps.append(app)
        
        return ordered_apps

# ============================================================================ #
# REGISTRATION
# ============================================================================ #

# Register the CustomUser model with its custom admin class
admin.site.register(CustomUser, CustomUserAdmin)

# Optional: If you want to use the custom admin site
# hemovital_admin = HemoVitalAdminSite(name='hemovital_admin')

# ============================================================================ #
# PASSWORD RESET TOKEN ADMIN
# ============================================================================ #

@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token_short', 'created_at', 'expires_at', 'is_used', 'is_valid_display')
    list_filter = ('is_used', 'created_at', 'expires_at')
    search_fields = ('user__email', 'user__username', 'token')
    readonly_fields = ('token', 'created_at', 'expires_at')
    list_editable = ('is_used',)
    
    fieldsets = (
        ('Token Information', {
            'fields': ('user', 'token', 'is_used')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'expires_at')
        }),
    )
    
    def token_short(self, obj):
        return f"{obj.token[:10]}..." if obj.token else "-"
    token_short.short_description = 'Token'
    
    def is_valid_display(self, obj):
        if obj.is_valid():
            return format_html('<span style="color: green;">✓ Valid</span>')
        else:
            return format_html('<span style="color: red;">✗ Invalid</span>')
    is_valid_display.short_description = 'Status'
    
    def has_add_permission(self, request):
        return False  # Tokens should be created via views only