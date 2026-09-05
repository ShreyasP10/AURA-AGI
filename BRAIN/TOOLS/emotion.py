"""
4. Emotion-aware — detect tone from text (Groq) + adapt AVA persona
Uses Groq openai/gpt-oss-20b to classify emotion, then inject into INSTRUCTIONS
"""
import os
from dotenv import load_dotenv; load_dotenv()
try:
    from groq import Groq
    _g=Groq(api_key=os.environ.get("GROQ_AI")) if os.environ.get("GROQ_AI") else None
    from functools import lru_cache
@lru_cache(maxsize=128)
def detect_emotion(text: str) -> str:
        if not _g: return "neutral"
        try:
            r=_g.chat.completions.create(model="openai/gpt-oss-20b", messages=[
                {"role":"system","content":"Classify emotion in one word: happy, sad, angry, anxious, excited, neutral. Only output the word."},
                {"role":"user","content":text}], max_tokens=5)
            emo=r.choices[0].message.content.strip().lower().split()[0]
            return emo if emo in ["happy","sad","angry","anxious","excited","neutral"] else "neutral"
        except: return "neutral"

    def adapt_prompt(base_prompt: str, emotion: str) -> str:
        tones={"happy":"Be upbeat and celebratory. ","sad":"Be gentle and empathetic. ","angry":"Be calm and de-escalating. ","anxious":"Be reassuring and steady. ","excited":"Be energetic and fun. ","neutral":""}
        return tones.get(emotion,"")+base_prompt
except ImportError:
    from functools import lru_cache
@lru_cache(maxsize=128)
def detect_emotion(t): return "neutral"
    def adapt_prompt(b,e): return b

if __name__=="__main__":
    print(detect_emotion("I just got accepted!"))
