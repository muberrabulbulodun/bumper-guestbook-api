# 📘 GuestBook API

This project was developed as part of a backend task assignment provided by Bumper using Django and Django REST Framework.

---

# 📄 Documentation

The detailed assignment documentation is also included in the project files.

You can additionally access it from the link below:

🔗 https://drive.google.com/file/d/1tBvvxLIFiVh7jil0tWe3lG5NnXUOYwwd/view?usp=sharing

# 🚀 Features

✅ Create guestbook entries  
✅ Unique user creation  
✅ Paginated entry listing  
✅ User-based entry statistics  
✅ Query optimizations  
✅ Validation support  
✅ Django admin panel  
✅ Automated integration tests  
✅ Coverage reporting  

---

# 🛠 Technologies

- Python
- Django
- Django REST Framework (DRF)
- SQLite
- Coverage
- Black Formatter

---

# ⚙️ Installation

## 1. Clone repository

```bash
git clone <repo_url>
cd guestbook
```

## 2. Create virtual environment

```bash
python3 -m venv .venv
```

## 3. Activate virtual environment

```bash
source .venv/bin/activate
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Run migrations

```bash
python manage.py migrate
```

## 6. Start server

```bash
python manage.py runserver
```

---

# 🔗 API Endpoints

## ➕ Create Entry

```http
POST /api/entries/create/
```

### Request Body

```json
{
  "name": "Muberra",
  "subject": "Hello",
  "message": "My first message"
}
```

---

## 📄 Get Entries

```http
GET /api/entries/
```

### Features

- 3 items per page
- ordered by latest created date
- includes username

---

## 👤 Get Users Data

```http
GET /api/users/
```

### Features

- total message count
- latest entry information
- no pagination

---

# 🧪 Tests

Run tests:

```bash
python manage.py test
```

Run coverage:

```bash
coverage run manage.py test
coverage report
```

---

# 📊 Coverage

Current coverage result:

```text
99%
```

---

# 🎥 Demo Video

The following demo video includes:

🔗 Demo Link: https://jam.dev/c/17fa0cc6-ad60-46d4-bbfa-469471bc2926

---

# 🧪 Unit & E2E Test

Integration and end-to-end test results:

🔗 Test Screenshot: https://prnt.sc/LakkMH26qjBg

---

# 📊 Coverage

Coverage result:

🔗 Coverage Screenshot: https://prnt.sc/5rAbD1uVlzpS

---

# ✅ Implemented Requirements

- User & Entry models
- Unique user creation
- Entry creation API
- Entries listing API
- Pagination support
- User-based statistics API
- Query optimizations
- Automated integration tests
- Validation checks
- Admin panel support

---
