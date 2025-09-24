## Author: Stefan M. West - ISU - 9/22/2025 1:45 P.M. ##
## Ran in powershell, detects input from Com Port and
#   runs subprocess. 
import serial
import subprocess

COM_PORT = 'COM5'
BAUD_RATE = 115200
TRIGGER_COMMAND = 'realtime_access.py'

ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
print("[ACTION] Listening For TRIGGER...")

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        print(f"[SERIAL] {line} >")
        if line == "TRIGGER":
            line = ""
            print("[ACTION] Opening webcam...")
            subprocess.run(['python', TRIGGER_COMMAND)
        

