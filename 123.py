import requests
import json
import time

# The correct API endpoint from your cURL
API_URL = "https://jntuhresults.dhethi.com/api/getAcademicResult"

# Exact headers from your browser request
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://jntuhconnect.dhethi.com",
    "priority": "u=1, i",
    "referer": "https://jntuhconnect.dhethi.com/",
    "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
}

# Load hall tickets
try:
    with open("halltickets.txt", "r") as f:
        hall_tickets = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print("Error: halltickets.txt not found. Please create it first.")
    exit()

all_results = []

print(f"Starting data collection for {len(hall_tickets)} students...")

for htno in hall_tickets:
    try:
        params = {'rollNumber': htno.upper()}
        response = requests.get(API_URL, params=params, headers=HEADERS)

        if response.status_code == 200:
            data = response.json()
            if data:
                # Store the roll number inside the object for later analysis
                data['scraped_roll_no'] = htno
                all_results.append(data)
                print(f"✅ Success: {htno}")
            else:
                print(f"❓ Empty data for: {htno}")
        elif response.status_code == 404:
            print(f"❌ 404 Not Found: {htno} (Check if this roll no exists)")
        else:
            print(f"⚠️ Failed {htno}: Status {response.status_code}")

        # 1 second delay to stay under the radar
        time.sleep(1)

    except Exception as e:
        print(f"🛑 Error with {htno}: {e}")

# Save to your ASUS VivoBook's local drive
with open("student_data_master.json", "w") as f:
    json.dump(all_results, f, indent=4)

print(f"\nFinished! Total records saved: {len(all_results)}")
