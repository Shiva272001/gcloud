import os
from google.cloud import bigquery
import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = "plenary-byway-498412-n2"
vertexai.init(project=PROJECT_ID, location="us-central1")
model = GenerativeModel("gemini-2.0-flash")
bq_client = bigquery.Client(project=PROJECT_ID)

def ask_citymind(question: str) -> str:
    prompt = f"""You are a data analyst. Convert this question into a
    BigQuery SQL query for table `citymind_data.traffic`
    (columns: date, zone, vehicle_count, avg_speed).
    Return ONLY the SQL query, nothing else.
    Question: {question}"""
    
    sql = model.generate_content(prompt).text.strip().strip("`")
    
    try:
        results = bq_client.query(sql).result()
        rows = [dict(row) for row in results]
        summary_prompt = f"Summarize these results in plain English: {rows}"
        summary = model.generate_content(summary_prompt).text
        return summary
    except Exception as e:
        return f"Error executing query or summarizing: {str(e)}"

if __name__ == "__main__": 
    print(ask_citymind("Which zone had the highest traffic yesterday?"))