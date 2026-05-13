# VulnBlog – A Deliberately Vulnerable Django Blog

VulnBlog is a full-stack web application built with Django and Django REST
Framework, intentionally riddled with **six OWASP Top 10:2021
vulnerabilities**. It serves as my personal portfolio piece to demonstrate
the complete Application Security (AppSec) lifecycle: **build, break, and
fix.**

## 🎯 Purpose

Modern software teams need engineers who can not only write code but also
think like an attacker. I created VulnBlog to prove exactly that:

- **Build** a realistic Django + DRF blog.
- **Break** it with 6 documented OWASP Top 10 vulnerabilities.
- **Fix** all vulnerabilities in a separate `secure` branch.

The entire process is documented in a professional penetration test report
included in this repository.

## 🧨 Vulnerabilities (OWASP Top 10)

| # | Vulnerability | Severity | Affected Endpoint |
|---|---|---|---|
| 1 | SQL Injection | Critical | `/api/posts/?q=` |
| 2 | Broken Authentication (JWT) | Critical | JWT Configuration |
| 3 | Sensitive Data Exposure | High | `/api/posts/` |
| 4 | Stored XSS | High | Comment section |
| 5 | Broken Access Control (IDOR) | High | `/api/users/{id}/profile/` |
| 6 | CSRF | Medium | `/post/{id}/edit/` |

All six vulnerabilities were identified, exploited, and documented with
reproduction steps and remediation advice.

## 📄 Full Penetration Test Report

A complete penetration test report (English & Persian) is available in the
[`reports/`](./reports/) directory. The report includes:

- Executive summary
- Methodology (OWASP Testing Guide)
- Detailed findings with CVSS scores, screenshots, and remediation

## 🛠️ Tech Stack

- **Backend:** Python 3.x, Django 4.x, Django REST Framework
- **Database:** SQLite (default)
- **Auth:** JWT (Simple JWT) – deliberately weakened
- **DevOps:** Docker, Docker Compose, GitHub Actions (CI/CD for security
  scanning)
- **Tools used in testing:** Burp Suite, curl, Python, and my own
  [TAPRepo](https://github.com/RezaChabok/TAPRepo) for managing targets and
  vulnerable parameters.

## 📁 Project Structure

VulnBlog/
├── vulnerable_app/ # Main Django project
│ ├── blog/ # Blog app (models, views, APIs, templates)
│ ├── reports/ # Penetration test report (PDF) and screenshots
│ ├── scripts/ # Helper scripts
│ ├── Dockerfile
│ ├── docker-compose.yml
│ ├── requirements.txt
│ └── manage.py
├── .github/workflows/ # CI/CD pipeline (security scan)
└── README.md

text

## 🚀 Quick Start

```bash
git clone https://github.com/RezaChabok/VulnBlog.git
cd VulnBlog
cd vulnerable_app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Visit http://127.0.0.1:8000 and start exploring – or breaking.

🔐 The secure Branch
All vulnerabilities have been completely fixed in the secure branch.
Compare the branches to see exactly what changed:

main – vulnerable by design

secure – hardened and safe

🧪 How I Tested It (And How TAPRepo Helped)
While testing VulnBlog, I used my own API tool,
TAPRepo, to store every
vulnerable parameter I found (e.g., q for SQLi). This kept my testing
structured and allowed me to reuse findings across different endpoints – a
practice I would bring to any real-world AppSec role.

👤 Author
Reza Chabok – GitHub

📄 License
MIT
