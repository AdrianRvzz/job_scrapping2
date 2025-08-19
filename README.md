# JobScraper + Gemini AI

This project performs **job scraping** (using [JobSpy](https://github.com/speedyapply/JobSpy)) and enriches the data with **structured fields** (academic background, technical and soft skills) using the **Gemini API**.  
The results are saved into an **Excel file** ready for analysis.

📂 Repository: [job_scrapping2](https://github.com/AdrianRvzz/job_scrapping2)

---

## Features

- Scrapes job postings from **Indeed**  
- Supports both English (USA) and Spanish (Mexico) searches  
- Maps raw job fields to more user-friendly column names  
- Extracts structured information from job descriptions using **AI**  
- Exports results to **Excel**  

---

## Requirements

- Python 3.10+  
- Install dependencies:  

```bash
pip install pandas jobspy python-dotenv google-genai json-repair openpyxl

```

## Setup

1) Clone this repository:

```bash
git clone https://github.com/AdrianRvzz/job_scrapping2.git
cd job_scrapping2
```

2) Create a **.env** file in the project root with your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

3) Install dependencies:

```bash
pip install pandas jobspy python-dotenv google-genai json-repair openpyxl
```

4) Run the script:

```bash
python main.py
```

---

## Additional Files

### `testing.py`

- A testing script to validate the **Gemini extraction** pipeline.  
- Uses a sample job description (Amazon Software Engineer) to extract structured fields such as academic profile, bilingual requirement, technical skills, and soft skills.  
- Runs independently for quick validation of the **JSON repair + parsing flow**.  

Run with:

```bash
python testing.py
```

### `cleaning.py`

- A utility script to **clean and reformat the scraped Excel output**.  
- Selects only the necessary columns, applies consistent naming, and generates a clean Excel file.
- Input: `jobs_usa_structured.xlsx`  
- Output: `jobs_usa.xlsx`

Run with:

```bash
python cleaning.py
```

---

## Output

- **jobs_mexico_structured.xlsx** → Jobs scraped for Mexico (Spanish)
- **jobs_usa_structured.xlsx** → Jobs scraped for the USA (English)
- **jobs_usa.xlsx** → Cleaned and formatted USA jobs dataset

---

## Example Columns

- StudentId  
- Place  
- Company  
- Position  
- Salary  
- Source  
- Link  
- Academic Profile  
- English/Bilingual  
- Technical Skills  
- Technical Skills 2  
- Soft Skills  
- Soft Skills 2  

---

## References

- JobSpy Library: https://github.com/speedyapply/JobSpy  
- Gemini API Docs: https://ai.google.dev/gemini-api/docs/text-generation?authuser=2

---
