import os
import sys

# Ensure server package is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.database import SessionLocal, engine, Base
from server.models import Exam, User
from server.routers.auth import get_password_hash
import shutil
import zipfile

Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()

    # 1. Create a default user
    if not db.query(User).filter(User.username == "student").first():
        print("Creating default user 'student' with password 'password'")
        hashed_pwd = get_password_hash("password")
        user = User(username="student", hashed_password=hashed_pwd)
        db.add(user)

    # Create dummy user Yuval
    if not db.query(User).filter(User.username == "Yuval").first():
        print("Creating user 'Yuval' with password '19-07'")
        hashed_pwd_yuval = get_password_hash("19-07")
        user_yuval = User(username="Yuval", hashed_password=hashed_pwd_yuval)
        db.add(user_yuval)

    # 2. Seed Exams
    base_data_dir = os.path.join(os.getcwd(), "Digital-Psychometric-Data")
    exam_dirs = ["Exams", "FullExams"]

    exam_password = "1234"
    hashed_exam_pwd = get_password_hash(exam_password)

    count = 0

    # Ensure server/zips directory exists
    zip_storage = os.path.join(os.getcwd(), "server", "zips")
    os.makedirs(zip_storage, exist_ok=True)

    for version in exam_dirs:
        version_path = os.path.join(base_data_dir, version)
        if not os.path.exists(version_path):
            continue

        for language in os.listdir(version_path):
            lang_path = os.path.join(version_path, language)
            if not os.path.isdir(lang_path): continue

            for year in os.listdir(lang_path):
                year_path = os.path.join(lang_path, year)
                if not os.path.isdir(year_path): continue

                # Look for directories that might be exams (e.g. "1", "2", "3")
                # and verify they contain answers.txt
                for item in os.listdir(year_path):
                    item_path = os.path.join(year_path, item)
                    if os.path.isdir(item_path):
                        if "answers.txt" in os.listdir(item_path):
                            # This is an exam folder
                            exam_name = f"{language}-{year}-{item}"
                            zip_filename = f"{exam_name}.zip"
                            zip_path = os.path.join(zip_storage, zip_filename)

                            # Zip it if not exists
                            if not os.path.exists(zip_path):
                                print(f"Zipping {item_path} to {zip_path}")
                                shutil.make_archive(zip_path.replace('.zip',''), 'zip', item_path)

                            # Add to DB
                            title = exam_name

                            existing = db.query(Exam).filter(Exam.title == title).first()
                            if not existing:
                                print(f"Adding exam: {title}")
                                exam = Exam(
                                    title=title,
                                    name=title,
                                    version=version,
                                    language=language,
                                    year=year,
                                    quarter=item,
                                    filename=zip_path, # Server serves this
                                    file_path=zip_path,
                                    password_hash=hashed_exam_pwd,
                                    is_premium=False
                                )
                                db.add(exam)
                                count += 1

    db.commit()
    print(f"Seeded {count} exams.")
    db.close()

if __name__ == "__main__":
    seed()
