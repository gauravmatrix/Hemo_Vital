from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (
    # 1. Public & Core Views
    IndexView,
    AboutView,
    ContactView,

    # 2. Authentication & Registration Views
    CustomLoginView,
    CustomLogoutView,
    RegistrationView,
    UserRegisterView,
    HospitalRegisterView,

    # 3. Central Dashboard Redirector
    DashboardRedirectView,
    PasswordResetRequestView, 
    PasswordResetConfirmView,

    # 4. Donor-Specific Views
    DonorDashboardView,
    DonorProfileView,
    SettingsView,
    DonationHistoryView,
    LeaderboardView,
    NearbyRequestsView,
    RespondToRequestView,

    # 5. Hospital-Specific Views
    HospitalDashboardView,
    BloodRequestCreateView,
    BloodCampCreateView,
    ManageRequestsView,
    BloodStockView,
    HospitalProfileView,
    UpdateDonationStatusView,

    # 6. AI & Analytics Views
    ChatbotView,
    AIAnalyticsDashboardView,
    AIDonorMatchingView,
    BloodDemandPredictionView,
    DonorRetentionAnalyticsView,
    AnalyticsDataView,

    # 7. API Views
    confirm_donation,
)

app_name = 'core'

urlpatterns = [
    # ==========================================
    # 1. Public & Core URLs
    # ==========================================
    path('', IndexView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),

    # ==========================================
    # 2. Authentication & Registration URLs
    # ==========================================
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('register/user/', UserRegisterView.as_view(), name='user_register'),
    path('register/hospital/', HospitalRegisterView.as_view(), name='hospital_register'),
    
    # ==========================================
    # 3. Central Dashboard Redirector
    # ==========================================
    path('dashboard/', DashboardRedirectView.as_view(), name='dashboard_redirect'),
    
    # ==========================================
    # 4. Donor-Specific URLs
    # ==========================================
    path('donor/dashboard/', DonorDashboardView.as_view(), name='donor_dashboard'),
    path('donor/profile/', DonorProfileView.as_view(), name='donor_profile'),
    path('donor/settings/', SettingsView.as_view(), name='donor_settings'),
    path('donor/history/', DonationHistoryView.as_view(), name='donation_history'),
    path('donor/leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('donor/requests/', NearbyRequestsView.as_view(), name='nearby_requests'),
    path('donor/respond/', RespondToRequestView.as_view(), name='respond_to_request'),

    # ==========================================
    # 5. Hospital-Specific URLs
    # ==========================================
    path('hospital/dashboard/', HospitalDashboardView.as_view(), name='hospital_dashboard'),
    path('hospital/request/create/', BloodRequestCreateView.as_view(), name='create_request'),
    path('hospital/camp/create/', BloodCampCreateView.as_view(), name='create_camp'),
    path('hospital/requests/manage/', ManageRequestsView.as_view(), name='manage_requests'),  # ✅ YEH LINE CHECK KARO
    path('hospital/stock/', BloodStockView.as_view(), name='blood_stock'),
    path('hospital/profile/', HospitalProfileView.as_view(), name='hospital_profile'),
    path('hospital/donation/<int:donation_id>/update/', UpdateDonationStatusView.as_view(), name='update_donation_status'),
    path('hospital/donation/<int:donation_id>/confirm/', views.confirm_donation, name='confirm_donation'),

    # ==========================================
    # 6. AI Analytics & Chatbot URLs
    # ==========================================
    
    # Ai and Analytics - FIXED VERSION
    path('hospital/ai/analytics/', AIAnalyticsDashboardView.as_view(), name='ai_analytics_dashboard'),
    path('hospital/ai/matching/<int:request_id>/', AIDonorMatchingView.as_view(), name='ai_donor_matching_detail'),
    path('hospital/ai/demand-prediction/', BloodDemandPredictionView.as_view(), name='blood_demand_prediction'),
    path('hospital/ai/donor-retention/', DonorRetentionAnalyticsView.as_view(), name='donor_retention_analytics'),
    path('matching/', views.AIDonorMatchingView.as_view(), name='ai_donor_matching'),

    # ✅ Analytics Data API - YEH USE KAR RAHA HAI JAVASCRIPT
    path('hospital/analytics/data/', AnalyticsDataView.as_view(), name='analytics_data'),

# ==========================================
# 8. API URLs for AJAX calls - REMOVE DUPLICATE
# ==========================================
# ❌ YE LINE COMMENT KAREIN YA DELETE KAREIN
# path('api/analytics/', AnalyticsDataView.as_view(), name='api_analytics'),

path('api/chatbot/', ChatbotView.as_view(), name='api_chatbot'),


    # ==========================================
    # 7. Chatbot URLs
    # ==========================================
    path('chatbot/', ChatbotView.as_view(), name='chatbot'),
    path('chatbot/message/', ChatbotView.as_view(), name='chatbot_message'),

    # ==========================================
    # 8. API URLs for AJAX calls
    # ==========================================
    # path('api/analytics/', AnalyticsDataView.as_view(), name='api_analytics'),
    path('api/chatbot/', ChatbotView.as_view(), name='api_chatbot'),

    # Password Reset URLs
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('hospital/donation/<int:donation_id>/confirm/', UpdateDonationStatusView.as_view(), name='confirm_donation'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)