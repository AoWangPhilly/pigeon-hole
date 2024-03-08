# Pigeon Hole

## Group Members:

- Brian Chen (bc844@drexel.edu)
- Ao Wang (aw3338@drexel.edu)

## User Description

Pigeon Hole is a dedicated platform for pigeon racers catering to professionals and passionate hobbyists. Users meticulously manage their racing pigeon fleet by inputting details such as band IDs, names, sexes, and birthdates. The application offers a visually rich pedigree generator to explore intricate family trees and racing achievements. Pigeon Hole addresses time constraints and organizational challenges, providing a user-friendly platform for streamlined data management and informed decision-making, ultimately optimizing racing outcomes.

## System Description

Pigeon Hole provides a user-friendly platform, empowering pigeon racers to manage their racing pigeon fleet meticulously. The application allows racers to input and organize detailed information for each bird, including band IDs, names, sexes, and dates of birth. With its visually rich pedigree generator, the app enables racers to explore the intricate family trees of their pigeons, showcasing lineage and racing achievements. This feature enhances understanding of each bird's genetic background, aiding in strategic breeding decisions for improved racing performance. Pigeon Hole is a comprehensive tool for enthusiasts, offering a convenient and insightful resource for managing and optimizing their pigeon racing experience.

## Tech Stack

- User Interface:
  - HTML
  - CSS
  - JavaScript
  - jQuery
- Styling/Interaction: Bootstrap
- Web Framework: Flask
- Database:
  - Postgres
  - Vercel Blob Storage
- Data Validation:
  - Flask-WTF
- Deployment: Vercel (https://pigeon-hole-nu.vercel.app/)

## Plugins Used

Since we used Flask, there are many available plugins to the framework.

- Flask WTF: Extension that integrates the WTForms library, which provides useful features for creating and handling forms in a simple way for a Flask web application.
- Flask SQLAlchemy: Extension for Flask allowing support for SQLAlchemy an Object Relational Mapper (ORM) that gives application developers the full power and flexibility of SQL.

## Run Application

1. Create Python Environment using `python3 -m venv venv`
2. Activate environment `source venv/bin/activate`
3. Install libraries, `pip install -r requirements.txt`
4. Follow directions in `env.example`
5. Run program, `python3 app.py`
