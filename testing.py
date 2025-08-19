import os
from os.path import join, dirname
from dotenv import load_dotenv
from google import genai
import json
import json_repair

from json_repair import repair_json

# -------------------------------
# Cargar variables de entorno
# -------------------------------
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY no está definido en el archivo .env")

# -------------------------------
# Inicializar cliente Gemini
# -------------------------------
client = genai.Client(api_key=GEMINI_API_KEY)

# -------------------------------
# Campos estructurados a extraer
# -------------------------------
structured_fields = [
    "Academic Profile",
    "English/Bilingual",
    "Technical Skills",
    "Technical Skills 2",
    "Soft Skills",
    "Soft Skills 2"
]

# -------------------------------
# Función para extraer datos estructurados
# -------------------------------
def extract_structured(desc: str) -> dict:
    prompt = f"""
    You are given a job description. I want you to extract six pieces of information and return them in a JSON-like format.

    Instructions:
    - Start the output with {{ and end with }}.
    - Use double quotes for all keys and values.
    - Separate each key and value with a colon ":".
    - Separate each pair with a comma.
    - If a value is missing, write null (without quotes).

    Keys:
    "academic", "bilingual", "tech_skills_1", "tech_skills_2", "soft_skills_1", "soft_skills_2"

    Example output:
    {{
    "academic": "Bachelor's degree in computer science",
    "bilingual": "English",
    "tech_skills_1": "Python, SQL",
    "tech_skills_2": "Microservices, REST APIs",
    "soft_skills_1": "Teamwork, communication",
    "soft_skills_2": "Motivated learner, problem solver"
    }}

    Now extract the information from this job description:

    Job Description:
    \"\"\"{desc}\"\"\"
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,

        )
        print(response.text)
        bad_json_string = response.text
        good_json_string = repair_json(bad_json_string)

        decoded_object = json_repair.loads(good_json_string)
        print(decoded_object)
        return decoded_object
    except Exception as e:
        print("Error parsing JSON:", e)
        return {k: None for k in structured_fields}

# -------------------------------
# Descripción de trabajo de prueba
# -------------------------------
job_description = """

BASIC QUALIFICATIONS:
- 3+ years of React, C++ and SQL
- 3+ years of non-internship professional software development experience
- 2+ years of non-internship design or architecture (design patterns, reliability and scaling) of new and existing systems experience
- Experience programming with at least one software programming language

PREFERRED QUALIFICATIONS:
- 3+ years of full software development life cycle, including coding standards, code reviews, source control management, build processes, testing, and operations experience
- Bachelor's degree in computer science or equivalent

Additional Information:

Amazon is an equal opportunity employer and does not discriminate on the basis of protected veteran status, disability, or other legally protected status.
"""

# -------------------------------
# Ejecutar prueba
# -------------------------------
if __name__ == "__main__":
    structured_data = extract_structured(job_description)
    print(structured_data)
