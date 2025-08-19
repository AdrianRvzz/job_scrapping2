import pandas as pd
from jobspy import scrape_jobs
import os
from os.path import join, dirname
from dotenv import load_dotenv
from google import genai
from json_repair import repair_json, loads as json_repair_loads

# --- Load environment variables ---
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# --- Column mapping ---
column_mapping = {
    "id": "StudentId",
    "location": "Place",
    "company": "Company",
    "title": "Position",
    "min_amount": "Salary",
    "site": "Source",
    "job_url": "Link"
}

# --- Roles ---
roles_es = [
    "Analista de datos",
    "Científico de datos",
    "Ingeniería (Ingeniero) de datos",
    "Computación en la nube / DevOps",
    "Front end",
    "Back end",
    "Full Stack"
]

roles_en = [
    "Data Analyst",
    "Data Scientist",
    "Data Engineer",
    "Cloud Computing / DevOps",
    "Front End",
    "Back End",
    "Full Stack"
]

# --- Structured fields ---
structured_fields = [
    "Academic Profile",
    "English/Bilingual",
    "Technical Skills",
    "Technical Skills 2",
    "Soft Skills",
    "Soft Skills 2"
]

# --- Map API keys to nice names ---
key_mapping = {
    "academic": "Academic Profile",
    "bilingual": "English/Bilingual",
    "tech_skills_1": "Technical Skills",
    "tech_skills_2": "Technical Skills 2",
    "soft_skills_1": "Soft Skills",
    "soft_skills_2": "Soft Skills 2"
}

# --- Function to extract structured info ---
def extract_structured(desc):
    prompt = f"""
    You are given a job description. Extract six pieces of information and return a JSON-like object.

    - Start with {{ and end with }}.
    - Use double quotes for all keys and values.
    - Separate each key and value with colon ":".
    - Separate each pair with comma.
    - If a value is missing, write null (without quotes).

    Keys:
    "academic", "bilingual", "tech_skills_1", "tech_skills_2", "soft_skills_1", "soft_skills_2"

    Example:
    {{
    "academic": "Bachelor's degree in computer science",
    "bilingual": "English",
    "tech_skills_1": "Python, SQL",
    "tech_skills_2": "Microservices, REST APIs",
    "soft_skills_1": "Teamwork, communication",
    "soft_skills_2": "Motivated learner, problem solver"
    }}

    Job Description:
    \"\"\"{desc}\"\"\"
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        bad_json = response.text
        good_json = repair_json(bad_json)
        decoded = json_repair_loads(good_json)
        return decoded
    except Exception as e:
        print("Error parsing JSON:", e)
        # Return all None for structured fields
        return {api_key: None for api_key in key_mapping.keys()}

# --- Scraping function ---
def scrape_and_structure(roles, location_name, country_code, output_file):
    all_jobs = []

    for role in roles:
        print(f"Scraping jobs for role: {role} in {location_name}")
        jobs = scrape_jobs(
            site_name=["indeed"],
            search_term=role,
            google_search_term=f"{role} jobs in {location_name} since yesterday",
            location=location_name,
            results_wanted=5,
            hours_old=72,
            country_indeed=country_code
        )
        if not jobs.empty:
            jobs["role"] = role
            jobs = jobs.rename(columns=column_mapping)

            # Extract structured info
            structured_data = {field: [] for field in structured_fields}
            for desc in jobs.get("description", []):
                job_json = extract_structured(desc)
                # Map API keys to nice field names
                for api_key, nice_name in key_mapping.items():
                    structured_data[nice_name].append(job_json.get(api_key))

            # Add structured fields to DataFrame
            for field in structured_fields:
                jobs[field] = structured_data[field]

            # --- Print each job row after adding IA fields ---
            for idx, row in jobs.iterrows():
                print("\nFull job data with structured fields:")
                print(row.to_dict())

            all_jobs.append(jobs)

    if all_jobs:
        df = pd.concat(all_jobs, ignore_index=True)
        df.to_excel(output_file, index=False)
        print(f"Saved {len(df)} structured jobs to {output_file}")

# --- Run for Mexico (Spanish) ---
scrape_and_structure(roles_es, "Mexico", "mexico", "jobs_mexico_structured.xlsx")

# --- Run for USA (English) ---
scrape_and_structure(roles_en, "USA", "USA", "jobs_usa_structured.xlsx")
