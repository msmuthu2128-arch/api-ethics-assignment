# api-ethics-assignment
Task 1 — PII Classification & Handling
1. full_name
Type: Direct PII
Action: Drop
Why:
Full name directly identifies a person. No need for research purposes → safest is complete removal.

2. email
Type: Direct PII
Action: Drop (or Pseudonymize if tracking needed)
Why:
Email uniquely identifies individuals.
If NOT needed → drop
If user-level tracking needed → replace with hashed ID

3. date_of_birth
Type: Indirect PII (Quasi-identifier)
Action: Mask / Generalize
How:
Convert to age or age group (e.g., 25–30)
Why:
Exact DOB can re-identify users when combined with other fields.

4. zip_code
Type: Indirect PII
Action: Mask / Generalize
How:
Keep only first 3 digits (e.g., 600***)
Or convert to region/state
Why:
ZIP + DOB + gender can uniquely identify individuals (known re-identification risk).

5. job_title
Type: Indirect PII
Action: Generalize
How:
Convert to categories (e.g., "Healthcare", "IT", "Labor")
Why:
Rare job titles can identify individuals indirectly.

6. diagnosis_notes
Type: Sensitive Personal Data (Highly sensitive, may contain PII inside text)
Action: Clean + Pseudonymize
How:
Remove names, phone numbers using NLP/regex
Keep medical info only
Why:
Contains health data (HIPAA-level sensitive)
May include embedded PII in free text