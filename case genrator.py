import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import requests
import re
import ui_module

# function for clean text from unknown item
def clean_text(text):
    return re.sub(r'[^\u0600-\u06FF\uFB8A\u067E\u0686\u06GF\u0020-\u007E]', '', text)

# functions for send prompt to API
def generate_case_scenario_gemini(patient_data, api_key):
    prompt = f"""
    یک آزمون بالینی طراحی کنید:
    بیمار {patient_data['age']} ساله، {patient_data['gender']}، با علائم زیر:
    - {patient_data['symptoms']}
    سابقه بیماری‌ها: {patient_data['medical_history']}
    بر اساس اطلاعات فوق:
    1. شرح حال مختصر بیمار را ارائه دهید.
    2. سه تشخیص افتراقی اصلی را ذکر کنید.
    3. پیشنهادات برای تست‌های تشخیصی مناسب ارائه دهید.
    4. بهترین اقدام درمانی اولیه را توصیه کنید.
    """
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        response_data = response.json()
        if 'candidates' in response_data and response_data['candidates']:
            candidate = response_data['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                raw_text = "".join([part['text'] for part in candidate['content']['parts']])
                return clean_text(raw_text.strip())
    return f"Error: {response.status_code}, {response.text}"

def generate_case_scenario_openai(patient_data, api_key):
    prompt = f"""
    یک آزمون بالینی طراحی کنید:
    بیمار {patient_data['age']} ساله، {patient_data['gender']}، با علائم زیر:
    - {patient_data['symptoms']}
    سابقه بیماری‌ها: {patient_data['medical_history']}
    بر اساس اطلاعات فوق:
    1. شرح حال مختصر بیمار را ارائه دهید.
    2. سه تشخیص افتراقی اصلی را ذکر کنید.
    3. پیشنهادات برای تست‌های تشخیصی مناسب ارائه دهید.
    4. بهترین اقدام درمانی اولیه را توصیه کنید.
    """
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    data = {"model": "gpt-3.5-turbo-instruct", "prompt": prompt, "max_tokens": 1500}
    api_url = "https://api.openai.com/v1/completions"

    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        response_data = response.json()
        return clean_text(response_data.get("choices", [{}])[0].get("text", "").strip())
    return f"Error: {response.status_code}, {response.text}"

def generate_case_scenario_groq(patient_data, api_key):
    prompt = f"""
    یک آزمون بالینی طراحی کنید:
    بیمار {patient_data['age']} ساله، {patient_data['gender']}، با علائم زیر:
    - {patient_data['symptoms']}
    سابقه بیماری‌ها: {patient_data['medical_history']}
    بر اساس اطلاعات فوق:
    1. شرح حال مختصر بیمار را ارائه دهید.
    2. سه تشخیص افتراقی اصلی را ذکر کنید.
    3. پیشنهادات برای تست‌های تشخیصی مناسب ارائه دهید.
    4. بهترین اقدام درمانی اولیه را توصیه کنید.
    """
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    data = {'model': 'Llama3-8b-8192', 'messages': [{"role": "system", "content": "You are a helpful medical assistant."}, {"role": "user", "content": prompt}]}
    response = requests.post('https://api.groq.com/openai/v1/chat/completions', headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code}, {response.text}"

def generate_case_scenario(patient_data, model, api_key):
    if model == "gemini-1.5-flash-latest":
        return generate_case_scenario_gemini(patient_data, api_key)
    elif model == "openai-chat":
        return generate_case_scenario_openai(patient_data, api_key)
    elif model == "groq-model":
        return generate_case_scenario_groq(patient_data, api_key)
    else:
        return "Invalid model selected."

# select file 
def process_file(file_path, model, api_key):
    result = ""
    try:
        if file_path.endswith(".csv"):
            patient_data_df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            patient_data_df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please select a CSV or XLSX file.")

        for _, patient_data in patient_data_df.iterrows():
            case_scenario = generate_case_scenario(patient_data, model, api_key)
            result += f"Case Scenario for Patient:\n{case_scenario}\n\n"
    except Exception as e:
        messagebox.showerror("Error", str(e))
    return result

if __name__ == "__main__":
    app = ui_module.MedicalCaseUI(process_file)
    app.run()
