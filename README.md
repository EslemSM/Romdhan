Romdhan Journey API

Romdhan Journey is a digital initiative and RESTful web service designed to support spiritual and daily practices during the holy month of Ramadhan. Developed as a project for Tunis Business School, this API provides a centralized platform for religious content, personalized tracking, and cultural resources tailored to the Tunisian context.

📖 Table of Contents
Overview

Features

Tech Stack

Project Structure

Database Architecture

Installation

Testing

🌟 Overview
The API aims to bridge tradition and innovation by providing structured, accessible, and culturally relevant religious content. It focuses on supporting spiritual consistency, promoting healthy daily habits through recipes, and maintaining cultural relevance for Tunisian users.



✨ Features
The API is organized into several modular resources:


User Management: Secure registration, login, and profile management using JWT-based authentication.



Spiritual Content: Centralized access to:

Prayers and Prayer Times (calculated via the praytimes library).



Supplications (Doua) and Adhkar.


Ahadith and Quran Tafsir (integrated via external APIs like AlQuran Cloud).



Khatma Tracking: Tools to monitor Quran reading progress and completion status.



Recipe Management: Culturally appropriate and health-oriented Ramadhan recipes.



Personalization: Users can create personal content (User Douas/Adhkar) and save favorites for quick access.


🛠 Tech Stack

Framework: Flask 




Database: MySQL (relational) with SQLAlchemy ORM 





Authentication: JSON Web Tokens (JWT) via Flask-JWT-Extended 



Data Validation: Marshmallow 



API Documentation: Flask-Smorest (OpenAPI support) 

📂 Project Structure
Plaintext

├── models/             # Database models (SQLAlchemy) [cite: 158]
├── resources/          # RESTful API endpoints [cite: 159]
├── schemas/            # Data validation/serialization (Marshmallow) [cite: 160]
└── app.py              # Application entry point and configuration 
📊 Database Architecture
The system utilizes a relational model to maintain data integrity and support complex user relationships.


Key Relationships:


User to Content: A one-to-many relationship exists between users and their personalized entries (Douas, Adhkar, and Recipes).



Favorites: Linking tables for users to bookmark specific spiritual content and recipes.


Khatma: Direct association with users to track individual reading progress.

🚀 Installation
Clone the repository:

Bash

git clone https://github.com/your-username/romdhan-journey-api.git
cd romdhan-journey-api
Install the required dependencies:

Bash

pip install Flask flask-restful flask-smorest flask-sqlalchemy
pip install Flask-JWT-Extended marshmallow marshmallow-sqlalchemy
pip install PyMySQL praytimes
``` [cite: 152, 153, 154, 155]

Configure the Database: Ensure your MySQL server is running and update the URI in app.py.

Run the Application:

Bash

python app.py
🧪 Testing
Functionality, reliability, and authorization are validated using Insomnia. Tests include verifying protected endpoints (Favorites, Khatma) and ensuring data integrity across spiritual resources.




Developed by: Islem Smiai Supervised by: Mr. Ben Messaoud Montassar Institution: Tunis Business School 



Would you like me to generate a specific requirements.txt file or a sample .env configuration for this repository?
