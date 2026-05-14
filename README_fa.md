# VulnBlog – یک بلاگ جنگوی عمداً آسیب‌پذیر

یک برنامهٔ تحت وب کامل ساخته‌شده با Django و Django REST Framework
است که به‌طور عمدی **شش آسیب‌پذیری از OWASP Top 10:2021** در آن تعبیه شده
است. این پروژه نمونه‌کار شخصی من برای نمایش چرخهٔ کامل امنیت نرم‌افزار
(AppSec) است: **ساختن، شکستن، و ایمن ساختن.**

## 🎯 هدف

تیم‌های نرم‌افزاری امروز به مهندسانی نیاز دارند که هم کد بزنند، هم ذهنیت
مهاجم داشته باشند. من VulnBlog را ساختم تا دقیقاً همین را ثابت کنم:

- **ساختن** یک بلاگ واقعی با Django و DRF.
- **شکستن** آن با ۶ آسیب‌پذیری مستند از OWASP Top 10.
- **ایمن ساختن** همهٔ آسیب‌پذیری‌ها در یک شاخهٔ جداگانه (`secure`).

کل این فرایند در یک گزارش تست نفوذ حرفه‌ای که داخل مخزن قرار دارد، مستند
شده است.

## 🧨 آسیب‌پذیری‌ها (OWASP Top 10)

| # | آسیب‌پذیری | شدت | محل اثر |
|---|---|---|---|
| ۱ | تزریق SQL | بحرانی | `/api/posts/?q=` |
| ۲ | احراز هویت شکسته (JWT) | بحرانی | پیکربندی JWT |
| ۳ | افشای داده‌های حساس | بالا | `/api/posts/` |
| ۴ | XSS ذخیره‌شده | بالا | بخش نظرات |
| ۵ | شکست کنترل دسترسی (IDOR) | بالا | `/api/users/{id}/profile/` |
| ۶ | CSRF | متوسط | `/post/{id}/edit/` |

تمامی شش آسیب‌پذیری شناسایی، بهره‌برداری و با مراحل بازتولید و راهکار
اصلاحی مستند شده‌اند.

## 📄 گزارش کامل تست نفوذ

گزارش کامل تست نفوذ (انگلیسی و فارسی) در پوشهٔ [`reports/`](./reports/)
موجود است. این گزارش شامل:

- خلاصهٔ مدیریتی
- روش‌شناسی (بر اساس OWASP Testing Guide)
- شرح مفصل یافته‌ها با نمره CVSS، تصاویر و راهکار اصلاحی

## 🛠️ فناوری‌ها

- **بک‌اند:** Python 3.x, Django 4.x, Django REST Framework
- **پایگاه داده:** SQLite (پیش‌فرض)
- **احراز هویت:** JWT (Simple JWT) – عمداً ضعیف شده
- **DevOps:** Docker, Docker Compose, GitHub Actions (خط لوله CI/CD برای
  اسکن امنیتی)
- **ابزارهای تست:** Burp Suite، curl، Python، و ابزار شخصی من به نام
  [TAPRepo](https://github.com/RezaChabok/TAPRepo) برای مدیریت هدف‌ها و
  پارامترهای آسیب‌پذیر.

## 📁 ساختار پروژه
VulnBlog/
├── vulnerable_app/ # پروژه اصلی جنگو
│ ├── blog/ # اپ بلاگ (مدل‌ها، نماها، APIها، قالب‌ها)
│ ├── reports/ # گزارش تست نفوذ (PDF) و تصاویر
│ ├── scripts/ # اسکریپت‌های کمکی
│ ├── Dockerfile
│ ├── docker-compose.yml
│ ├── requirements.txt
│ └── manage.py
├── .github/workflows/ # خط لوله CI/CD (اسکن امنیتی)
└── README.md


## 🚀 راه‌اندازی سریع
```bash
git clone https://github.com/RezaChabok/VulnBlog.git
cd VulnBlog
cd vulnerable_app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

## 🚀 راه‌اندازی سریع (با Docker)

```bash
git clone https://github.com/RezaChabok/VulnBlog.git
cd VulnBlog
docker-compose up --build
```
سپس به http://127.0.0.1:8000 بروید و شروع به کاوش – یا شکستن – کنید.

🔐 شاخهٔ secure
تمامی آسیب‌پذیری‌ها به‌طور کامل در شاخهٔ secure برطرف شده‌اند. دو شاخه را
مقایسه کنید تا دقیقاً ببینید چه چیزهایی تغییر کرده است:

main – آسیب‌پذیر عمدی

secure – ایمن و سخت‌شده

🧪 چطور تست کردم (و چطور TAPRepo کمک کرد)
در حین تست VulnBlog، از ابزار API شخصی خودم،
TAPRepo، برای ذخیرهٔ هر
پارامتر آسیب‌پذیر (مثلاً q برای SQLi) استفاده کردم. این کار تست مرا
ساختاریافته نگه داشت و امکان استفادهٔ مجدد از یافته‌ها در endpointهای مختلف
را فراهم کرد – رویه‌ای که آن را به هر نقش حرفه‌ای AppSec خواهم آورد.

👤 نویسنده
رضا چابک – [Github](https://github.com/RezaChabok)

📄 مجوز
[MIT](https://choosealicense.com/licenses/mit/)
