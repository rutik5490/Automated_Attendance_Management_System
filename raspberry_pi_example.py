#!/usr/bin/env python3
"""
Example script for Raspberry Pi to send attendance data to the Django server
This script simulates scanning a QR code or RFID tag and sending the data to the server
"""

import requests
import json
import time
from datetime import datetime

# Server configuration
SERVER_URL = 'http://localhost:8000/attendance/api/raspberry-pi/'
API_KEY = 'your-api-key-here'  # In a real implementation, you would use proper authentication

def send_attendance_data(student_id, subject_id, status='present'):
    """
    Send attendance data to the Django server
    """
    # Prepare data
    data = {
        'student_id': student_id,
        'subject_id': subject_id,
        'status': status
    }
    
    # Prepare headers
    headers = {
        'Content-Type': 'application/json',
        # 'Authorization': f'Bearer {API_KEY}'  # In a real implementation
    }
    
    try:
        # Send POST request
        response = requests.post(SERVER_URL, data=json.dumps(data), headers=headers)
        
        # Check response
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"Attendance recorded successfully for student {student_id}")
                return True
            else:
                print(f"Error recording attendance: {result.get('error')}")
                return False
        else:
            print(f"HTTP Error {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return False

def simulate_rfid_scan():
    """
    Simulate scanning RFID tags or QR codes
    In a real implementation, this would interface with actual hardware
    """
    # Simulated student and subject IDs
    # In a real implementation, these would come from the RFID/QR scanner
    scans = [
        {'student_id': 1, 'subject_id': 1, 'status': 'present'},
        {'student_id': 2, 'subject_id': 1, 'status': 'present'},
        {'student_id': 3, 'subject_id': 1, 'status': 'absent'},
    ]
    
    for scan in scans:
        print(f"Scanning student {scan['student_id']} for subject {scan['subject_id']}")
        success = send_attendance_data(
            scan['student_id'], 
            scan['subject_id'], 
            scan['status']
        )
        
        if success:
            print("Attendance recorded successfully")
        else:
            print("Failed to record attendance")
        
        # Wait a bit between scans
        time.sleep(1)

if __name__ == '__main__':
    print("Raspberry Pi Attendance System Simulation")
    print("=" * 40)
    print(f"Server URL: {SERVER_URL}")
    print()
    
    # Simulate scanning
    simulate_rfid_scan()
    
    print()
    print("Simulation complete")