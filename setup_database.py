# """
# EXPERT DATABASE SETUP SCRIPT for HemoVital
# This will COMPLETELY reset and setup your database properly
# """

# import os
# import django
# import sys

# # Setup Django environment
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hemovital.settings')
# django.setup()

# from django.db import transaction
# from django.contrib.auth import get_user_model
# from core.models import *
# from django.utils import timezone
# from datetime import date, timedelta

# def expert_database_setup():
#     print("🚀 EXPERT DATABASE SETUP STARTING...")
#     print("=" * 60)
    
#     try:
#         with transaction.atomic():
#             # STEP 1: COMPLETE DATABASE CLEAN
#             print("🧹 STEP 1: Cleaning database...")
            
#             # Delete in correct order to avoid foreign key constraints
#             models_to_clean = [
#                 ContactMessage, AIPredictionLog, Notification,
#                 Donation, BloodStock, BloodRequest,
#                 UserProfile, HospitalProfile, GlobalSetting
#             ]
            
#             for model in models_to_clean:
#                 count = model.objects.count()
#                 model.objects.all().delete()
#                 print(f"   ✅ Cleaned {model.__name__}: {count} records")
            
#             # Delete users last
#             user_count = CustomUser.objects.count()
#             CustomUser.objects.all().delete()
#             print(f"   ✅ Cleaned CustomUser: {user_count} records")
            
#             # STEP 2: CREATE SUPER ADMIN
#             print("\n👑 STEP 2: Creating super admin...")
#             admin = CustomUser.objects.create_superuser(
#                 username='admin',
#                 email='admin@hemovital.com', 
#                 password='admin123'
#             )
#             print("   ✅ Super Admin: admin@hemovital.com / admin123")
            
#             # STEP 3: CREATE HOSPITAL WITH PROFILE
#             print("\n🏥 STEP 3: Creating hospital...")
#             hospital_user = CustomUser.objects.create_user(
#                 username='cityhospital',
#                 email='admin@cityhospital.com',
#                 password='hospital123',
#                 role=CustomUser.Role.HOSPITAL
#             )
#             hospital_user.first_name = 'Dr. Rajesh'
#             hospital_user.last_name = 'Kumar'
#             hospital_user.save()
            
#             hospital_profile = HospitalProfile.objects.create(
#                 user=hospital_user,
#                 admin_full_name='Dr. Rajesh Kumar',
#                 admin_gender=UserProfile.Gender.MALE,
#                 admin_dob=date(1980, 6, 15),
#                 admin_designation='Chief Medical Officer',
#                 hospital_name='City General Hospital',
#                 hospital_reg_id='CGH2024DEL',
#                 address='123 Medical Road, Connaught Place',
#                 city='New Delhi',
#                 state='Delhi',
#                 pincode='110001',
#                 contact_number='+91-11-23456789',
#                 is_verified=True
#             )
#             print("   ✅ Hospital: admin@cityhospital.com / hospital123")
            
#             # STEP 4: CREATE BLOOD REQUESTS
#             print("\n🩸 STEP 4: Creating blood requests...")
#             blood_requests_data = [
#                 {
#                     'patient_name': 'Amit Sharma',
#                     'patient_age': 35,
#                     'blood_group': 'A+',
#                     'units_required': 3,
#                     'urgency': BloodRequest.UrgencyLevel.CRITICAL,
#                 },
#                 {
#                     'patient_name': 'Sunita Patel',
#                     'patient_age': 28, 
#                     'blood_group': 'B+',
#                     'units_required': 2,
#                     'urgency': BloodRequest.UrgencyLevel.URGENT,
#                 },
#                 {
#                     'patient_name': 'Rohan Verma',
#                     'patient_age': 45,
#                     'blood_group': 'O+',
#                     'units_required': 4,
#                     'urgency': BloodRequest.UrgencyLevel.NORMAL,
#                 }
#             ]
            
#             for i, req_data in enumerate(blood_requests_data, 1):
#                 blood_request = BloodRequest.objects.create(
#                     hospital=hospital_user,
#                     **req_data,
#                     family_member_name=f'Family Member {i}',
#                     contact_number=f'+91-98765432{10+i}',
#                     address=f'Hospital Ward {i}, City Hospital',
#                     expires_on=timezone.now() + timedelta(days=7)
#                 )
#                 print(f"   ✅ Blood Request {i}: {req_data['patient_name']} - {req_data['blood_group']}")
            
#             # STEP 5: CREATE DONORS WITH PROFILES
#             print("\n👥 STEP 5: Creating donors...")
#             donors_data = [
#                 {
#                     'username': 'rahul_donor',
#                     'email': 'rahul.sharma@email.com',
#                     'first_name': 'Rahul',
#                     'last_name': 'Sharma',
#                     'blood_group': 'A+',
#                 },
#                 {
#                     'username': 'priya_donor',
#                     'email': 'priya.patel@email.com', 
#                     'first_name': 'Priya',
#                     'last_name': 'Patel',
#                     'blood_group': 'B+',
#                 },
#                 {
#                     'username': 'amit_donor',
#                     'email': 'amit.verma@email.com',
#                     'first_name': 'Amit',
#                     'last_name': 'Verma', 
#                     'blood_group': 'O+',
#                 }
#             ]
            
#             for donor_data in donors_data:
#                 user = CustomUser.objects.create_user(
#                     username=donor_data['username'],
#                     email=donor_data['email'],
#                     password='donor123',
#                     role=CustomUser.Role.DONOR,
#                     first_name=donor_data['first_name'],
#                     last_name=donor_data['last_name']
#                 )
                
#                 UserProfile.objects.create(
#                     user=user,
#                     blood_group=donor_data['blood_group'],
#                     city='New Delhi',
#                     contact_number='+91-9876500000',
#                     is_available=True
#                 )
#                 print(f"   ✅ Donor: {donor_data['first_name']} {donor_data['last_name']} - {donor_data['blood_group']}")
            
#             # STEP 6: FINAL VERIFICATION
#             print("\n📊 STEP 6: Final verification...")
#             final_counts = {
#                 'Total Users': CustomUser.objects.count(),
#                 'Hospitals': CustomUser.objects.filter(role=CustomUser.Role.HOSPITAL).count(),
#                 'Donors': CustomUser.objects.filter(role=CustomUser.Role.DONOR).count(),
#                 'Blood Requests': BloodRequest.objects.count(),
#             }
            
#             for label, count in final_counts.items():
#                 print(f"   ✅ {label}: {count}")
            
#             first_request = BloodRequest.objects.first()
#             if first_request:
#                 print(f"   ✅ First Blood Request ID: {first_request.id}")
#             else:
#                 print("   ❌ No blood requests created!")
#                 raise Exception("Blood requests creation failed!")
            
#             print("\n🎉 EXPERT SETUP COMPLETED SUCCESSFULLY!")
#             print("=" * 60)
#             print("🔐 LOGIN CREDENTIALS:")
#             print("   Super Admin: admin@hemovital.com / admin123")
#             print("   Hospital: admin@cityhospital.com / hospital123") 
#             print("   Donors: [any donor email] / donor123")
#             print("\n🌐 TEST URLS:")
#             print(f"   AI Analytics: http://localhost:8000/hospital/ai/analytics/")
#             print(f"   Donor Matching: http://localhost:8000/hospital/ai/matching/{first_request.id}/")
#             print("=" * 60)
            
#     except Exception as e:
#         print(f"\n❌ SETUP FAILED: {e}")
#         print("💡 TROUBLESHOOTING:")
#         print("   1. Make sure all migrations are applied: python manage.py migrate")
#         print("   2. Check if database file exists and is not locked")
#         print("   3. Try deleting db.sqlite3 and running migrations again")
#         sys.exit(1)

# if __name__ == '__main__':
#     expert_database_setup()