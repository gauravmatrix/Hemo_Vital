# import os
# import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
# django.setup()

# from core.models import CustomUser, HospitalProfile, UserProfile

# def fix_all_permissions():
#     print("Fixing user permissions...")
    
#     # 1. Verify all hospitals
#     hospitals_updated = HospitalProfile.objects.update(is_verified=True)
#     print(f"Verified {hospitals_updated} hospitals")
    
#     # 2. Ensure all users have profiles
#     for user in CustomUser.objects.all():
#         if user.role == CustomUser.Role.DONOR:
#             UserProfile.objects.get_or_create(user=user)
#         elif user.role == CustomUser.Role.HOSPITAL:
#             HospitalProfile.objects.get_or_create(user=user)
    
#     print("All user profiles ensured!")
    
#     # 3. Print user details for debugging
#     print("\n=== USER DETAILS ===")
#     for user in CustomUser.objects.all():
#         profile = "No profile"
#         if user.role == 'DONOR' and hasattr(user, 'userprofile'):
#             profile = "Donor Profile ✓"
#         elif user.role == 'HOSPITAL' and hasattr(user, 'hospitalprofile'):
#             profile = f"Hospital Profile ✓ (Verified: {user.hospitalprofile.is_verified})"
        
#         print(f"User: {user.email} | Role: {user.role} | {profile}")

# if __name__ == '__main__':
#     fix_all_permissions()