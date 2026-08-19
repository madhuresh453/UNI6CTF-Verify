import os

print("🚀 Generating Certificates...")
os.system("python generator10.py")

print("📧 Sending Emails...")
os.system("python mailer10.py")

print("✅ DONE")