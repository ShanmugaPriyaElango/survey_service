# Survey Management API

A Django REST Framework based Survey Management System.

This project allows:
- Admin users to create and manage surveys
- Answerer users to submit responses
- Aggregated and individual survey response views
- Role-based authorization
- MySQL database support

---

## Tech Stack

- Python 3.x
- Django
- Django REST Framework
- MySQL
- Custom Role-Based Authorization

---

## Project Structure

surveyapp/
│
├── surveys/
├── responses/
├── users/
├── manage.py
├── requirements.txt
├── .env (not committed)
└── README.md


---

## Roles

The system supports two roles:

- **admin**
  - Create surveys
  - View survey responses (individual + aggregate)
  - Access only surveys they own or shared with them

- **answerer**
  - Submit survey responses
  - View their own responses only

---

## Setup Instructions

### 1️⃣ Clone the Repository

git clone [<your-repo-url>](https://github.com/ShanmugaPriyaElango/survey_service.git)
cd surveyapp


---

### 2️⃣ Create Virtual Environment

python -m venv venv


Activate:

Windows:
venv\Scripts\activate


Linux/Mac:
source venv/bin/activate


---

### 3️⃣ Install Dependencies

pip install -r requirements.txt


---

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

DB_NAME=surveydb
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=your-secret-key
DEBUG=True


---

### 5️⃣ Configure MySQL

Create database:

CREATE DATABASE surveydb;


---

### 6️⃣ Run Migrations

python manage.py migrate


---

### 7️⃣ Run Server

python manage.py runserver


Server will start at:

http://127.0.0.1:8000/


---

## Authentication

Authentication is handled using a custom header:

X-USER-ID: <user_id>


Example using Postman:

Headers:
X-USER-ID: 1


---

## API Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/users/ | List users |
| POST | /api/users/ | Create users |

### Surveys

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/surveys/ | List surveys |
| POST | /api/surveys/ | Create survey (admin only) |
| GET | /api/surveys/<survey_id>/ | Retrieve survey |
| PUT | /api/surveys/<survey_id>/ | Update survey |

---

### Responses

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/surveys/<survey_id>/responses/ | List responses (admin only) |
| GET | /api/surveys/<survey_id>/responses/?view=aggregate | Aggregate results |
| POST | /api/surveys/<survey_id>/responses/ | Submit response (answerer only) |
| GET | /api/surveys/<survey_id>/responses/<response_id> | Retrieve response |

---

### User Responses

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/responses/?users_id=<user_id> | Get all responses by logged-in user/ created_by user_id in query_params |

---

## Aggregate View

Use:

GET /api/surveys/<survey_id>/responses/?view=aggregate


Returns:

{
"Question 1": [
  {
    "answer": "answer 1",
    "count": 2
  }
]
}


---

## Authorization Logic

- Admin can only access surveys:
  - Created by them
  - Shared with them

- Answerer can:
  - Submit only one response per survey
  - View their own responses

---

## Deployment Notes

Before deploying:

- Set `DEBUG=False`
- Use production database credentials
- Secure SECRET_KEY
- Use environment variables
- Configure allowed hosts

---

## Author

Shanmuga Priya Elango

---

## License

This project is for learning purposes.