from typing import Any, Dict, Final, Tuple, List
import os
import requests
from mimetypes import guess_type
from glob import glob
import random
import string
import datetime
from models import db, Pigeon, User, PigeonHierarchy

from passlib.hash import pbkdf2_sha256

from app import app

app.app_context().push()

VERCEL_API_URL: Final[str] = "https://blob.vercel-storage.com"
NATIONAL_ORG: Final[List[str]] = ["IF", "AU", "ATB", "NBRC", "IPB"]
COLORS: Final[List[str]] = [
    "blue",
    "black",
    "red",
    "yellow",
    "white",
    "checker",
    "barred",
    "pied",
    "grizzle",
    "t-pattern",
    "dun",
    "mealy",
]
SEX: Final[List[str]] = ["hen", "cock"]


def generate_random_letters():
    return "".join(random.choices(string.ascii_uppercase, k=3))


def generate_string_of_seven_numbers():
    # Generating a string of 7 random numbers between 0 and 9
    return "".join(random.choices("0123456789", k=7))


def generate_random_date(date1, date2):
    delta = date2 - date1
    random_days = random.randint(0, delta.days)
    return date1 + datetime.timedelta(days=random_days)


def save_image_to_blob_storage(
    image_data: bytes, file_name: str, blob_file_name: str
) -> Dict[str, Any]:
    headers = {
        "authorization": f"Bearer {os.environ.get('BLOB_READ_WRITE_TOKEN')}",
        "x-content-type": guess_type(file_name)[0],
    }

    response = requests.put(
        f"{VERCEL_API_URL}/{blob_file_name}", data=image_data, headers=headers
    ).json()
    return response


def read_image_to_bytes(file_name: str) -> bytes:
    with open(file_name, "rb") as f:
        return f.read()


# Create a test user
user = User(
    email="aw3338@drexel.edu", password=pbkdf2_sha256.hash("password"), name="Ao Wang"
)


db.session.add(user)
db.session.commit()

# Create a test pigeons
test_image_file_names = glob("static/img/test/**")

for index, file_name in enumerate(test_image_file_names):
    bytes_ = read_image_to_bytes(file_name)
    response = save_image_to_blob_storage(
        bytes_, file_name, f"user={user._id}/{os.path.basename(file_name)}"
    )
    random_date = generate_random_date(
        datetime.datetime(2020, 1, 1), datetime.datetime.now()
    )

    pigeon = Pigeon(
        user_id=user._id,
        band_id=f"{random.choice(NATIONAL_ORG)}-{datetime.datetime.now().year}-{generate_random_letters()}-{generate_string_of_seven_numbers()}",
        name=f"Pigeon {index}",
        sex=random.choice(SEX),
        color=random.choice(COLORS),
        image_url=response["url"],
        date_of_birth=str(random_date.date()),
    )
    db.session.add(pigeon)
    db.session.commit()
