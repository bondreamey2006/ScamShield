import os
from google import genai

# Fallback dictionaries
MISSING_KEY_FALLBACK = {
    "english": "Explanation unavailable (API key missing).",
    "hindi": "विवरण उपलब्ध नहीं है (API कुंजी गायब है)।",
    "tamil": "விளக்கம் கிடைக்கவில்லை (API விசை இல்லை)."
}

ERROR_FALLBACK_RED = {
    "english": "Warning: Risk signals detected. Please double check before paying.",
    "hindi": "चेतावनी: जोखिम के संकेत मिले हैं। कृपया भुगतान करने से पहले दोबारा जांच लें।",
    "tamil": "எச்சரிக்கை: ஆபத்துக்கான அறிகுறிகள் கண்டறியப்பட்டுள்ளன. பணம் செலுத்துவதற்கு முன் தயவுசெய்து சரிபார்க்கவும்."
}

ERROR_FALLBACK_GREEN = {
    "english": "Verified safe merchant.",
    "hindi": "सत्यापित सुरक्षित व्यापारी।",
    "tamil": "சரிபார்க்கப்பட்ட பாதுகாப்பான வணிகர்."
}

ERROR_FALLBACK_YELLOW = {
    "english": "Unknown ID. Proceed with caution.",
    "hindi": "अज्ञात आईडी। सावधानी से आगे बढ़ें।",
    "tamil": "தெரியாத ஐடி. எச்சரிக்கையுடன் தொடரவும்."
}

def generate_explanation(verdict: str, signals: list, language: str = "english") -> str:
    """
    Calls the Gemini API to generate a plain-language explanation of the risk.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    lang_key = language.lower() if language.lower() in ["english", "hindi", "tamil"] else "english"

    if not api_key:
        return MISSING_KEY_FALLBACK[lang_key]

    try:
        client = genai.Client(api_key=api_key)
        
        # Prepare context for the prompt
        signal_details = ", ".join([f"{s.code} ({s.severity})" for s in signals])
        
        prompt = f"""
        You are ScamShield, a safety assistant for digital payments in India.
        A user scanned a UPI ID. The backend gave a verdict of '{verdict.upper()}'.
        The risk signals triggered were: {signal_details}.

        Explain this to an elderly, non-technical user in 1-2 short sentences.
        If the verdict is GREEN, assure them it's a verified safe merchant.
        If the verdict is YELLOW, tell them to proceed with caution because the ID is unknown or new.
        If the verdict is RED, warn them strongly not to pay because it has been reported by the community.

        CRITICAL: 
        - Do not use technical jargon (e.g. do not say "VPA_SINGLE_REPORT").
        - Output the final explanation strictly in {language.upper()}.
        - Keep it very concise.
        """

        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
        )
        
        return response.text.strip()
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        v = verdict.lower()
        if v == "green":
            return ERROR_FALLBACK_GREEN[lang_key]
        elif v == "yellow":
            return ERROR_FALLBACK_YELLOW[lang_key]
        else:
            return ERROR_FALLBACK_RED[lang_key]
