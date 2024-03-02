from typing import Any, Dict, Final
import os
import requests
from mimetypes import guess_type
from glob import glob

from models import db, Pigeon, User, PigeonHierarchy

VERCEL_API_URL: Final[str] = "https://blob.vercel-storage.com"


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
    email="aw3338@drexel.edu",
    password="password",
    name="Ao Wang"
)


db.session.add(user)
db.session.commit()

# Create a test pigeons
test_image_file_names = glob("static/img/test/**")

for file_name in test_image_file_names:
    bytes_ = read_image_to_bytes(file_name)
    response = save_image_to_blob_storage(
        bytes_, file_name, f"user={user.id}/{os.path.basename(file_name)}"
    )
