"""
EduMind AI Tutor - Application Entrypoint
Delegates execution to edumind_ai_tutor.py
"""
import os
import sys

app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "edumind_ai_tutor.py")
with open(app_path, "r", encoding="utf-8") as f:
    code = compile(f.read(), app_path, "exec")
    exec(code)
