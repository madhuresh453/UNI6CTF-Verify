import os

print("🚀 Generating Certificates...")
os.system("python generator.py")

print("📧 Sending Emails...")
os.system("python mailer.py")

print("✅ DONE")