# import os
# import django
# from datetime import datetime

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hemovital.settings')  # Change to your project name
# django.setup()

# from core.models import CustomUser, UserProfile, HospitalProfile, BloodRequest
# from django.utils import timezone
# from datetime import timedelta, date

# def setup_sample_data():
#     print("Starting sample data setup...")
    
#     try:
#         # Create hospital user if not exists
#         hospital_user, created = CustomUser.objects.get_or_create(
#             email='hospital@test.com',
#             defaults={
#                 'username': 'hospital',
#                 'role': CustomUser.Role.HOSPITAL,
#             }
#         )
        
#         if created:
#             hospital_user.set_password('testpass123')
#             hospital_user.save()
#             print("✅ Created hospital user")
#         else:
#             print("✅ Hospital user already exists")
        
#         # Create or update hospital profile with ALL required fields
#         hospital_profile, profile_created = HospitalProfile.objects.get_or_create(
#             user=hospital_user,
#             defaults={
#                 'admin_full_name': 'Hospital Admin',
#                 'admin_gender': 'Male', 
#                 'admin_dob': date(1980, 1, 1),  # Fixed: Added valid date
#                 'admin_designation': 'Administrator',
#                 'hospital_name': 'Test Hospital',
#                 'hospital_reg_id': 'HOSP123',
#                 'address': 'Test Address, Test Street',
#                 'city': 'Test City',
#                 'state': 'Test State', 
#                 'pincode': '123456',
#                 'contact_number': '1234567890',
#                 'is_verified': True
#             }
#         )
        
#         if profile_created:
#             print("✅ Created hospital profile")
#         else:
#             print("✅ Hospital profile already exists")
        
#         # Create sample blood request
#         blood_request, request_created = BloodRequest.objects.get_or_create(
#             hospital=hospital_user,
#             patient_name="Sample Patient",
#             defaults={
#                 'patient_age': 30,
#                 'blood_group': 'A+',
#                 'units_required': 2,
#                 'urgency': 'Urgent',
#                 'family_member_name': 'Family Member',
#                 'contact_number': '9876543210',
#                 'address': 'Patient Address, City',
#                 'expires_on': timezone.now() + timedelta(days=7)
#             }
#         )
        
#         if request_created:
#             print(f"✅ Created blood request ID: {blood_request.id}")
#         else:
#             print("✅ Blood request already exists")
        
#         print("🎉 Sample data setup complete!")
#         print(f"📧 Login email: hospital@test.com")
#         print(f"🔑 Password: testpass123")
#         print(f"🩸 Blood Request ID for testing: {blood_request.id}")
        
#     except Exception as e:
#         print(f"❌ Error: {e}")
#         print("Trying alternative approach...")
#         setup_alternative()

# def setup_alternative():
#     """Alternative method if first one fails"""
#     try:
#         # Get existing hospital user or create new one
#         hospital_user = CustomUser.objects.filter(role='HOSPITAL').first()
        
#         if not hospital_user:
#             hospital_user = CustomUser.objects.create_user(
#                 username='hospital',
#                 email='hospital@test.com',
#                 password='testpass123',
#                 role=CustomUser.Role.HOSPITAL
#             )
#             print("✅ Created hospital user (alternative)")
        
#         # Delete existing profile if incomplete and create new one
#         HospitalProfile.objects.filter(user=hospital_user).delete()
        
#         hospital_profile = HospitalProfile.objects.create(
#             user=hospital_user,
#             admin_full_name='Hospital Admin',
#             admin_gender='Male',
#             admin_dob=date(1980, 1, 1),  # Required field
#             admin_designation='Administrator',
#             hospital_name='Test Hospital',
#             hospital_reg_id='HOSP123',
#             address='Test Address',
#             city='Test City',
#             state='Test State',
#             pincode='123456',
#             contact_number='1234567890',
#             is_verified=True
#         )
#         print("✅ Created hospital profile (alternative)")
        
#         # Create blood request
#         blood_request = BloodRequest.objects.create(
#             hospital=hospital_user,
#             patient_name="Test Patient",
#             patient_age=35,
#             blood_group="A+", 
#             units_required=2,
#             urgency="Urgent",
#             family_member_name="Family",
#             contact_number="1234567890",
#             address="Test Address",
#             expires_on=timezone.now() + timedelta(days=7)
#         )
#         print(f"✅ Created blood request ID: {blood_request.id}")
        
#     except Exception as e:
#         print(f"❌ Alternative method also failed: {e}")

# if __name__ == '__main__':
#     setup_sample_data()