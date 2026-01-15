🩸 HemoVital – AI Powered Blood Donation System

HemoVital is a web-based healthcare platform designed to streamline blood donation management by intelligently connecting donors, hospitals, and patients through a centralized and secure system. The platform focuses on reducing emergency response time, improving donor coordination, and ensuring reliable access to life-saving blood supplies.

🚀 Key Features

🧠 AI-assisted donor matching based on blood group, location, and eligibility

🏥 Hospital and blood bank request management

🧍 Donor registration, availability tracking, and donation history

🔐 Secure authentication with role-based access control

📊 Dashboard for monitoring requests and responses

📩 Email notifications and alerts

🗂 Modular and scalable backend architecture

🧩 Problem Statement

In emergency medical situations, hospitals and patients often face delays in finding suitable blood donors due to manual coordination, outdated records, and lack of real-time availability. This leads to inefficient communication, increased response time, and avoidable risks to patient lives.

💡 Solution

HemoVital provides a digital platform where donors, hospitals, and administrators can interact seamlessly. The system intelligently identifies eligible donors and facilitates faster blood request fulfillment while maintaining data accuracy, transparency, and security.

🏗️ System Architecture

Frontend: HTML, CSS, Bootstrap, JavaScript

Backend: Python, Django (MVT Architecture)

Database: PostgreSQL (Production), SQLite (Local Development)

AI Integration: Donor eligibility logic & prediction services

Deployment: Railway with Gunicorn

Security: Environment-based configuration, secure authentication

👥 User Roles

Donor: Register, manage profile, receive donation requests

Hospital/Blood Bank: Raise blood requests, track responses

Admin: Monitor system activity, manage users and data

🔐 Security & Best Practices

Sensitive data managed via environment variables

API keys and credentials never committed to source code

Secure session and CSRF protection enabled

Logs, local databases, and secrets excluded using .gitignore


⚙️ Setup Instructions (Local)
# Clone repository
git clone https://github.com/gauravmatrix/Hemo_Vital.git
cd Hemo_Vital

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver

🌍 Deployment

The application is deployed on Railway, using Gunicorn and PostgreSQL for production-ready hosting. Environment variables are managed securely through Railway’s dashboard.

📌 Future Enhancements

Mobile application support

Advanced AI-based donor prediction

Geo-location based emergency alerts

Analytics for blood demand trends

👨‍💻 Author

Gaurav Kumar
Full Stack Developer
<<<<<<< HEAD
GitHub: https://github.comgauravmatrix
=======
GitHub: https://github.com/gauravmatrix
>>>>>>> 0c473c5b3c401d3e4d03e215c5b98b671ea001dc
