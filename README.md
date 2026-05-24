# QA Automation Framework

## 📖 Overview
Pytest + Selenium framework for validating web application functionality and security.  
Generates full‑page screenshots and compiles them into DOCX reports for business users.  
Code and documentation created with **AI Copilot**.  
I am responsible for **executing the tests** and delivering reports.  

---

## 🗂️ Project Structure
```
qa-framework/
│  combine_screendumps.py       # Compile screenshots into DOCX
│  pytest                       # Pytest runner
│  pytest.ini                   # Pytest config
│  README.md                    # Documentation
│  requirements.txt             # Dependencies
│
├─reports
│  │  Final_Test_Report.docx         # Technical summary
│  │  Final_Screendump_Report.docx   # Business evidence
│  │
│  └─screenshots
│          boundary_validation.png
│          email_invalid.png
│          login_invalid.png
│          login_success.png
│          mobile_invalid.png
│          password_invalid.png
│          session_timeout.png
│          sql_injection.png
│          survey_success.png
│          xss_prevention.png
│
├─src
│  driver_setup.py              # WebDriver setup
│  __init__.py
│
└─tests
        conftest.py
        TC1_login.py
        TC2_survey.py
        TC3_login_invalid.py
        TC4_email_validation.py
        TC5_mobile_validation.py
        TC6_password_validation.py
        TC7_session_timeout.py
        TC8_sql_injection.py
        TC9_xss_prevention.py
        TC10_boundary_validation.py
```

---

## ✅ Deliverables
- **Business report** → `Final_Test_Report.docx` & `Final_Screendump_Report.docx`  
- **Screenshots** → `reports/screenshots/`  
- **Automation scripts** → TC1–TC10  

---
