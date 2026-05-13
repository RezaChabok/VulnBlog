# VulnBlog Penetration Test Report

**Version:** 1.0  
**Date:** 13/5/2026  
**Author:** Reza Chabok  
**Role:** Application Security Engineer & Penetration Tester  
**Classification:** Confidential — Personal Portfolio Project

---

## 1. Executive Summary

This report documents the findings of a full-scope web application penetration test performed against **VulnBlog**, a deliberately vulnerable blog application built with Django and Django REST Framework. The objective of this assessment was to identify, exploit, and document common web vulnerabilities aligned with **OWASP Top 10:2021**, and to demonstrate the full AppSec lifecycle — from discovery to remediation.

### Key Findings

A total of **6 vulnerabilities** were identified during this engagement:

- **2 Critical:** SQL Injection and Broken Authentication (JWT misconfiguration).
- **3 High:** Sensitive Data Exposure, Stored XSS, and Insecure Direct Object Reference (IDOR).
- **1 Medium:** Cross-Site Request Forgery (CSRF).

### Conclusion

VulnBlog in its current state (branch `main`) is critically vulnerable to common web attacks. All identified vulnerabilities have been fully remediated in a separate `secure` branch, demonstrating the ability to not only find but also fix security flaws.

---

## 2. Scope & Methodology

- **Target:** VulnBlog v1.0 (source code available, white-box assessment).
- **Scope:** All API endpoints, HTML views, and authentication mechanisms.
- **Methodology:** OWASP Testing Guide v4 with focus on OWASP Top 10:2021.
- **Tools Used:** Burp Suite, curl, Python (JWT analysis), web browser, and a custom-built API tool named **TAPRepo** for storing and managing discovered targets and their vulnerable parameters.
- **Testing Period:** [Date range]
- **Limitations:** Testing performed in an isolated local environment.

To manage and reuse discovered targets and parameters during this engagement,
I used my self-built API tool, **TAPRepo** (Target & Attack-Parameter Repository).
When an interesting endpoint or vulnerable parameter was identified
(e.g., `id`, `user_id`), it was immediately stored in TAPRepo, categorized
by vulnerability type (e.g., IDOR, SQLi). This eliminated re-work and
ensured a structured correlation between findings across different endpoints.

---

## 3. Summary of Findings

| # | Vulnerability | Severity | CVSS (approx.) | Affected Endpoint / Location |
|---|---|---|---|---|
| 1 | SQL Injection | Critical | 9.8 | `GET /api/posts/?q=` |
| 2 | Broken Authentication (JWT) | Critical | 9.0 | JWT Configuration (`settings.py`) |
| 3 | Sensitive Data Exposure | High | 7.5 | `GET /api/posts/` |
| 4 | Stored Cross-Site Scripting (XSS) | High | 7.2 | Comment section at `/post/{id}/` |
| 5 | Broken Access Control (IDOR) | High | 7.5 | `GET /api/users/{id}/profile/` |
| 6 | Cross-Site Request Forgery (CSRF) | Medium | 6.5 | `POST /post/{id}/edit/` |

---

## 4. Detailed Findings

### Finding 1: SQL Injection [CWE-89]
- **Severity:** Critical (CVSS 9.8)
- **Location:** `GET /api/posts/?q=<payload>`

**Description:**  
The post search API uses raw SQL queries without parameterization, directly concatenating user input into the query string. An attacker can inject arbitrary SQL code to access or manipulate the entire database.

**Reproduction Steps:**
1. Send a request to: `GET /api/posts/?q=' OR 1=1 --`
2. The server returns all posts from the database instead of filtered results.

**Proof of Concept:**  
![[https://raw.githubusercontent.com/RezaChabok/VulnBlog/refs/heads/main/reports/screenshots/SQLI.png]]

The discovered `q` parameter was logged into **TAPRepo** under the SQLI category for future reference and fuzzing against similar API patterns.
**Remediation:**  
Replace the raw SQL query with Django ORM: `Post.objects.filter(title__icontains=query)`.

---

### Finding 2: Broken Authentication – JWT Misconfiguration [CWE-287]
- **Severity:** Critical (CVSS 9.0)
- **Location:** JWT settings in `settings.py`

**Description:**  
Access tokens are configured with a 30-day lifetime (`ACCESS_TOKEN_LIFETIME = timedelta(days=30)`). If a token is leaked, the attacker retains unrestricted access for an entire month.

**Reproduction Steps:**
1. Obtain a valid access token via `/api/token/`.
2. Decode the token at `jwt.io` or with a Python script.
3. Observe the `exp` (expiration) field is set 30 days after `iat` (issued at).

**Proof of Concept:**  
![[https://raw.githubusercontent.com/RezaChabok/VulnBlog/refs/heads/main/reports/screenshots/BrokenAuthentication.png]]

**Remediation:**  
Reduce `ACCESS_TOKEN_LIFETIME` to 15–30 minutes. Implement token refresh with rotation and blacklisting.

---

### Finding 3: Sensitive Data Exposure [CWE-200]
- **Severity:** High (CVSS 7.5)
- **Location:** `GET /api/posts/`

**Description:**  
The `PostSerializer` includes an `author_password_hash` field that returns a hardcoded hash in the JSON response. This exposes sensitive user information to any client consuming the API.

**Reproduction Steps:**
1. Request `GET /api/posts/`.
2. Observe the `author_password_hash` field in the response.

**Proof of Concept:**  
![[https://raw.githubusercontent.com/RezaChabok/VulnBlog/refs/heads/main/reports/screenshots/SensitiveDataExposure.png]]

**Remediation:**  
Remove the `author_password_hash` field from `PostSerializer`.

---

### Finding 4: Stored Cross-Site Scripting (XSS) [CWE-79]
- **Severity:** High (CVSS 7.2)
- **Location:** Comment section at `/post/{id}/`

**Description:**  
User-submitted comments are rendered using Django's `|safe` filter, which disables HTML escaping. An attacker can store malicious JavaScript in a comment that executes in the browser of any user viewing the post.

**Reproduction Steps:**
1. Submit a comment containing `<script>alert('XSS')</script>`.
2. Navigate to the post detail page.
3. The JavaScript code executes in the browser.

**Proof of Concept:**  
![[https://raw.githubusercontent.com/RezaChabok/VulnBlog/refs/heads/main/reports/screenshots/XSS.png]]

**Remediation:**  
Remove the `|safe` filter and rely on Django's automatic HTML escaping.

---

### Finding 5: Broken Access Control (IDOR) [CWE-639]
- **Severity:** High (CVSS 7.5)
- **Location:** `GET /api/users/{id}/profile/`

**Description:**  
The user profile API does not verify whether the requesting user is authorized to view the requested profile. Changing the `user_id` parameter grants access to any user's information.

**Reproduction Steps:**
1. Log in as user A.
2. Request `GET /api/users/2/profile/` (user B's profile).
3. The server returns user B's personal data.

**Proof of Concept:**  
![[https://raw.githubusercontent.com/RezaChabok/VulnBlog/refs/heads/main/reports/screenshots/IDOR.png]]

**Remediation:**  
Validate that `request.user.id` matches the requested `user_id`.

---

### Finding 6: Cross-Site Request Forgery (CSRF) [CWE-352]
- **Severity:** Medium (CVSS 6.5)
- **Location:** `POST /post/{id}/edit/`

**Description:**  
The post editing view is decorated with `@csrf_exempt`, disabling Django's built-in CSRF protection. A malicious website can forge a request on behalf of an authenticated user to modify post content.

**Reproduction Steps:**
1. Craft a POST request to `/post/1/edit/` with `title=Hacked&content=CSRF_Attack`.
2. Send the request without any CSRF token.
3. The post is successfully modified.

**Proof of Concept:**  
![[https://raw.githubusercontent.com/RezaChabok/VulnBlog/refs/heads/main/reports/screenshots/CSRF.png]]

**Remediation:**  
Remove the `@csrf_exempt` decorator and ensure the form includes `{% csrf_token %}`.

---

## 5. Conclusion & Next Steps

This penetration test successfully identified six vulnerabilities across the OWASP Top 10:2021 in the VulnBlog application. All findings were documented with reproduction steps and remediation guidance. A fully-patched version of the application is available in the `secure` branch of the repository, demonstrating a complete DevSecOps lifecycle: **build, break, and fix.**

---

**End of Report**
