import requests
import json
import re
import os
from openai import OpenAI
from typing import Dict, Any

# =========================
# OpenAI Client
# =========================
# client = OpenAI( api_key=os.getenv("OPENAI_API_KEY"))  # in environment 

# =========================
# Diagnosis List (Fixed)
# =========================
DIAGNOSIS_LIST = [
    "Asthma",
    "URTI",
    "ACOS",
    "UACS",
    "Rhinnites (Allergic Rhintes)",
    "COPD",
    "Bronchiectasis",
    "Bronchiolitis",
    "Flu",
    "Pneumonia",
    "LRTI",
    "ILD",
    "AECB",
    "AECOPD",
    "Tracheobronchites",
    "Rhinisinusutes and (chronic allergic rhinisinusutes)",
    "CAP",
    "Post flu",
    "P edema",
    "OSA",
    "Empyema",
    "GERD",
    "Psycho/anxiety"
]

# =========================
# Prompt Builder
# =========================
def build_prompt(patient_data: Dict[str, Any]) -> str:
    return f"""
You are a medical clinical decision support assistant.
You analyze structured patient data and select the MOST LIKELY diagnosis
ONLY from a predefined diagnosis list.

Patient data (JSON):
{json.dumps(patient_data, indent=2)}

Allowed diagnosis list (choose ONLY ONE):
{json.dumps(DIAGNOSIS_LIST, indent=2)}

Instructions:
1. Analyze symptoms, duration, cough characteristics, smoking exposure,
   past medical history, family history, and pregnancy status.
2. Choose ONE diagnosis strictly from the list.
3. Do not invent symptoms or diagnosis.
4. If data is insufficient, choose the closest diagnosis and lower confidence.
5. Do NOT recommend treatment.
6. This is NOT a definitive diagnosis.

CRITICAL OUTPUT RULES (DO NOT VIOLATE):
- supporting_evidence MUST be an array of STRING only.
- Each item must be a plain human-readable sentence.
- DO NOT return objects or key-value structures.
- confidence MUST be ONE of the following strings exactly:
  "Low", "Medium", or "High"
- Any violation makes the output invalid.

Return ONLY valid JSON in the following format:

{{
   "final_diagnosis": "One diagnosis EXACTLY as written in the allowed list",
   "confidence": "Low | Medium | High",
   "supporting_evidence": [
    "Evidence sentence 1",
    "Evidence sentence 2",
    "Evidence sentence 3"
  ]
}}
"""

# =========================
# Main AI Function
# =========================
def analyze_patient(patient_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sends patient data to the LLM and returns structured diagnosis result.
    """

    prompt = build_prompt(patient_data)

    print("📨 Sending prompt to AI model...\n")
    print(prompt)
    print("\n==============================\n")

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "temperature": 0,
            "stream": False
        },
        timeout=120
    )

    # ✅ 
    if response.status_code != 200:
        print("❌ AI request failed")
        print(response.text)
        raise RuntimeError("AI service error")

    data = response.json()

    # 
    print("🧠 RAW AI RESPONSE:")
    print(json.dumps(data, indent=2))
    print("\n==============================\n")

    # ✅ Ollama   
    if "response" not in data:
        raise KeyError("Missing 'response' field in AI output")

    raw_text = data["response"]

    print("📄 RAW TEXT FROM MODEL:")
    print(raw_text)
    print("\n==============================\n")

    #   JSON 
    output = extract_json(raw_text)

    print("✅ FINAL PARSED OUTPUT:")
    print(json.dumps(output, indent=2))
    print("\n==============================\n")

    return output

def analyze_patient3(patient_data: Dict[str, Any]) -> Dict[str, Any]:
    
    """
    Sends patient data to the LLM and returns structured diagnosis result.
    """

    prompt = build_prompt(patient_data)

    print(" Sending prompt to AI model...")
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "temperature": 0,
            "stream": False
        }
    )

    result = response.json()["response"]
    print("befor result")
    print(result)
    print("after result")
    output = extract_json(result)
    print(output)
    ##print(json.dumps(output, indent=2))
    ##print("after output")
    return output
'''
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
            temperature=0,
        )

        # =========================
        # Extract text safely
        # =========================
        output_text = response.output_text
        print("🤖 Raw AI output:")
        print(output_text)

        # =========================
        # Parse JSON
        # =========================
        result = json.loads(output_text)

        return {
            "status": "success",
            "result": result
        }

    except json.JSONDecodeError:
        print("❌ Failed to parse AI response as JSON")
        return {
            "status": "error",
            "message": "Invalid AI response format"
        }

    except Exception as e:
        print("❌ AI service error:", str(e))
        return {
            "status": "error",
            "message": str(e)
        } 
    '''

def extract_json(text: str):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in LLM response")
    return json.loads(match.group())

def analyze_patient_():
    print("*****analyze_patient_*************-----------")
    patient_data = {
    "age": 63,
    "gender": "female",
    "smoking": "no",
    "marital_status": "married",
    "previous_symptoms":"chronic intermittent cough 5 months ago and Hypertension",
    "family_history": "no respiratory diseases",
    "location": {"country": "Syria", "city": ""},
    "clinical_measurements": "Bp:14/8, BMI: 44",
    "current_symptoms":"intermittent cough, nasal congestion, afebrile, tight breathing",
    }

    prompt = f"""
    You are a senior pulmonologist.

    Task:
    Classify the patient's condition into exactly ONE disease.

    Rules:
    - Base your decision ONLY on patient data
    - Choose strictly ONE diagnosis from the list
    - No assumptions beyond the data
    - Prefer chronic overlap diseases when symptoms are recurrent

    Diagnosis list:
    ["Asthma","URTI","ACOS","UACS","Rhinnites (Allergic Rhintes)","COPD",
    "Bronchiectasis","Bronchiolitis","Flu","Pneumonia","LRTI","ILD","AECB",
    "AECOPD","Tracheobronchites","Rhinisinusutes and (chronic allergic rhinisinusutes)",
    "CAP","Post flu","P edema","OSA","Empyema","GERD","Psycho/anxiety"]

    Patient data:
    {json.dumps(patient_data, indent=2)}

    Output ONLY valid JSON:
    {{
    "final_diagnosis": "",
    "confidence": 0.0,
    "supporting_evidence": [
      "Evidence item 1",
      "Evidence item 2",
      "Evidence item 3"
  ]
}}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "temperature": 0,
            "stream": False
        }
    )

    result = response.json()["response"]
    print("befor result")
    print(result)
    print("after result")
    output = extract_json(result)
    print(json.dumps(output, indent=2))
    print(output)
    print("after output")
    return output

    #result = json.loads(response.choices[0].message.content)
    #print(result)



## ollama serve

## ollama pull phi3:medium
## ollama pull phi3:mini
## ollama pull mistral
## ollama pull llama3
## ollama pull qwen2.5



'''
def analyze_patient(patient):
    # مثال مبدئي
    cough = patient.cough_details
    symptoms = patient.main_symptoms

    risk_score = 0

    if cough.get("hemoptysis"):
        risk_score += 3
    if "Asthma" in patient.past_medical_history:
        risk_score += 2
    if "Current smoker" in patient.smoking_exposure:
        risk_score += 2

    return {
        "risk_level": "High" if risk_score >= 4 else "Moderate",
        "risk_score": risk_score,
        "summary": "Possible respiratory condition detected",
        "recommendation": "Consult a pulmonologist"
    }
'''