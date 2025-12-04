# src/utils/generative_explainer.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

MODEL_NAME = "google/flan-t5-base"

print("🔄 Chargement du modèle génératif Flan-T5 pour l'explication médicale...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,
    device_map="auto"
)

def generate_medical_explanation(prediction: str, probabilities: dict, symptoms: str, xai_desc: str):
    prob_text = ", ".join([f"{k}: {v*100:.1f}%" for k, v in probabilities.items()])

    prompt = f"""
Tu es un expert en radiologie et en neurosciences.
Voici les informations du cas :

- Diagnostic automatique : {prediction}
- Probabilités par classe : {prob_text}
- Description XAI : {xai_desc}
- Symptômes cliniques : {symptoms}

Rédige un rapport médical clair et structuré expliquant :
1. L'interprétation du diagnostic
2. L’analyse des probabilités
3. L’analyse des zones mises en évidence par le XAI
4. Le lien avec les symptômes
5. Une conclusion médicale professionnelle et prudente
"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    output = model.generate(
        **inputs,
        max_length=380,
        temperature=0.4,
        top_p=0.9,
        no_repeat_ngram_size=3
    )

    text = tokenizer.decode(output[0], skip_special_tokens=True)
    return text.strip()
