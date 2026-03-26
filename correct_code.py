#Fixed Code (Ethical + TOS Compliant)

import requests
import time
import hashlib
from datetime import datetime

API_URL = "https://healthstats-api.example.com/records"
API_KEY = "free_tier_key_abc123"

# ---------- Helper Functions ----------

def hash_value(value):
    """Pseudonymize sensitive identifiers"""
    if value:
        return hashlib.sha256(value.encode()).hexdigest()
    return None

def calculate_age(dob):
    """Convert DOB to age"""
    if not dob:
        return None
    try:
        birth_year = int(dob.split("-")[0])
        current_year = datetime.now().year
        return current_year - birth_year
    except:
        return None

def generalize_job(job_title):
    """Convert job title into category"""
    if not job_title:
        return "Other"
    
    job_title = job_title.lower()
    
    if "engineer" in job_title or "developer" in job_title:
        return "IT"
    elif "doctor" in job_title or "nurse" in job_title:
        return "Healthcare"
    elif "teacher" in job_title:
        return "Education"
    else:
        return "Other"

def clean_text(text):
    """Basic cleaning of diagnosis notes"""
    if not text:
        return None
    
    # Simple example (real-world → use NLP/PII detection tools)
    return text.replace("\n", " ").strip()

def sanitize_record(record):
    """Remove/transform PII fields"""
    return {
        "user_id": hash_value(record.get("email")),  # pseudonymized
        "age": calculate_age(record.get("date_of_birth")),
        "zip_prefix": str(record.get("zip_code"))[:3] if record.get("zip_code") else None,
        "job_category": generalize_job(record.get("job_title")),
        "diagnosis_notes": clean_text(record.get("diagnosis_notes"))
    }

# ---------- Main Data Collection ----------

def fetch_data():
    records = []
    page = 1
    max_pages = 100  # safety cap (avoid abuse)

    while page <= max_pages:
        try:
            response = requests.get(
                API_URL,
                params={"page": page, "key": API_KEY},
                timeout=10
            )

            # Handle HTTP errors
            if response.status_code != 200:
                print(f"Stopping: API returned {response.status_code}")
                break

            data = response.json()

            # Stop if no more data
            if not data.get("results"):
                print("No more data available.")
                break

            records.extend(data["results"])

            print(f"Fetched page {page}")
            page += 1

            # Respect rate limit
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            break

    return records

# ---------- Run Pipeline ----------

raw_records = fetch_data()

# Sanitize before storage
cleaned_records = [sanitize_record(r) for r in raw_records]

# Store only cleaned data
save_to_database(cleaned_records)

print(f"Stored {len(cleaned_records)} cleaned records safely.")