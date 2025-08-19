import pandas as pd

# Carga el archivo Excel
df = pd.read_excel("jobs_usa_structured.xlsx")  # reemplaza con el nombre de tu archivo

# Selecciona y renombra las columnas según el nuevo formato
column_mapping = {
    "StudentId": "Student ID",
    "Place": "Place",
    "Company": "Company",
    "Position": "Position",
    "Academic Profile": "Academic Profile",
    "English/Bilingual": "English/Bilingue",
    "Technical Skills": "Technical skills",
    "Technical Skills 2": "Technical skills 2",
    "Soft Skills": "Soft skills",
    "Soft Skills 2": "Soft skills 2",
    "Salary": "Salary",
    "Source": "Source",
    "Link": "Link"
}

# Filtra solo las columnas que existen en tu Excel
existing_cols = {k: v for k, v in column_mapping.items() if k in df.columns}

# Aplica el renombramiento y reordena
df_clean = df[list(existing_cols.keys())].rename(columns=existing_cols)

# Guarda el nuevo Excel limpio
df_clean.to_excel("jobs_usa.xlsx", index=False)

print("Archivo limpio generado: jobs_usa.xlsx")
