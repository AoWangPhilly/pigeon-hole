import os
from typing import Final, Dict, Any
from mimetypes import guess_type
from io import BytesIO
import uuid
import datetime

import requests
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session,
)

from models import PigeonHierarchy, db, Pigeon

pigeon_bp = Blueprint(
    "pigeon",
    __name__,
)

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


def read_image_from_blob_storage(blob_file_name: str) -> BytesIO:
    headers = {
        "authorization": f"Bearer {os.environ.get('BLOB_READ_WRITE_TOKEN')}",
        "prefix": blob_file_name,
    }
    response = requests.get(VERCEL_API_URL, headers=headers).json()
    return response


@pigeon_bp.route("/get/<pigeon_id>")
def get(pigeon_id):
    pigeon = Pigeon.query.filter_by(_id=pigeon_id).first()
    if pigeon is None:
        return jsonify({"error": "Pigeon not found"}), 404
    return jsonify(pigeon)


@pigeon_bp.route("/view")
def view():
    # filter for user only
    if session.get("user") is None:
        return redirect(url_for("auth.login"))

    nameFilter = request.args.get("name")
    if nameFilter:
        page = db.paginate(
            Pigeon.query.filter_by(user_id=session.get("user").get("_id"))
            .filter(
                Pigeon.name.icontains(nameFilter),
            )
            .order_by(Pigeon.name),
            per_page=6,
        )
    else:
        page = db.paginate(
            Pigeon.query.filter_by(user_id=session.get("user").get("_id")).order_by(
                Pigeon.name
            ),
            per_page=6,
        )
    is_empty = (
        Pigeon.query.filter_by(user_id=session.get("user").get("_id")).first() is None
    )
    return render_template(
        "view.html",
        is_empty=is_empty,
        page=page,
        session=session,
        name=request.args.get("name", ""),
    )


@pigeon_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html", session=session)

    user_id = session.get("user").get("_id")
    band_id = request.form.get("bandID")
    name = request.form.get("name")
    sex = request.form.get("sex")
    color = request.form.get("color")
    date_of_birth = request.form.get("dateOfBirth")
    image_data = request.files["image"]

    band_id_exist = Pigeon.query.filter_by(band_id=band_id).first()
    if band_id_exist:
        return render_template(
            "add.html", session=session, error="Band ID already exists"
        )

    blob_storage_response = save_image_to_blob_storage(
        image_data=image_data.read(),
        file_name=image_data.filename,
        blob_file_name=f"pigeon_images/user={user_id}/band_id={band_id}/{uuid.uuid4()}.png",
    )
    url = blob_storage_response.get("url")
    pigeon = Pigeon(
        user_id=user_id,
        band_id=band_id,
        name=name,
        sex=sex,
        color=color,
        date_of_birth=date_of_birth,
        image_url=url,
    )
    db.session.add(pigeon)
    db.session.commit()

    return redirect(url_for("pigeon.view"))


@pigeon_bp.route("/<id>")
def detail(id):
    if not session.get("user"):
        return redirect(url_for("auth.login"))

    pigeons = Pigeon.query.filter_by(user_id=session.get("user").get("_id"))
    pigeon = pigeons.filter_by(_id=id).first()

    cocks = pigeons.filter(
        Pigeon.sex == "cock",
        Pigeon._id != id,
        Pigeon.date_of_birth < pigeon.date_of_birth,
    ).all()
    hens = pigeons.filter(
        Pigeon.sex == "hen",
        Pigeon._id != id,
        Pigeon.date_of_birth < pigeon.date_of_birth,
    ).all()
    pigeon_hierarchy = PigeonHierarchy.query.filter_by(child_id=id).first()

    return render_template(
        "detail.html",
        pigeon=pigeon,
        cocks=cocks,
        hens=hens,
        session=session,
        pigeon_hierarchy=pigeon_hierarchy,
    )


@pigeon_bp.route("/delete/<id>")
def delete(id):
    pigeon = Pigeon.query.filter_by(_id=id).first()
    db.session.delete(pigeon)
    db.session.commit()
    return redirect(url_for("pigeon.view"))


@pigeon_bp.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "GET":
        pigeon = Pigeon.query.filter_by(_id=id).first()
        return render_template("edit.html", pigeon=pigeon)

    pigeon = Pigeon.query.filter_by(_id=id).first()
    user_id = session.get("user").get("_id")
    band_id = request.form.get("bandID")
    name = request.form.get("name")
    sex = request.form.get("sex")
    color = request.form.get("color")
    date_of_birth = request.form.get("dateOfBirth")
    image_data = request.files["image"]

    if pigeon.sex == "cock":
        hierarchy = PigeonHierarchy.query.filter_by(father_id=id).first()
    else:
        hierarchy = PigeonHierarchy.query.filter_by(mother_id=id).first()
    child_pigeon = Pigeon.query.filter_by(_id=hierarchy.child_id).first()

    if hierarchy and pigeon.sex == "cock" and sex == "hen":
        return render_template(
            "edit.html",
            error=f"Pigeon is already father to {child_pigeon.band_id}",
            pigeon=pigeon,
        )
    else:
        return render_template(
            "edit.html",
            error=f"Pigeon is already mother to {child_pigeon.band_id}",
            pigeon=pigeon,
        )

    pigeon.user_id = user_id
    pigeon.band_id = band_id
    pigeon.name = name
    pigeon.sex = sex
    pigeon.color = color
    pigeon.date_of_birth = date_of_birth

    try:
        db.session.commit()
    except:
        return (
            render_template("edit.html", error="Band ID is not unique", pigeon=pigeon),
            400,
        )

    if image_data:
        blob_storage_response = save_image_to_blob_storage(
            image_data=image_data.read(),
            file_name=image_data.filename,
            blob_file_name=f"pigeon_images/user={user_id}/band_id={band_id}/{uuid.uuid4()}.png",
        )
        url = blob_storage_response.get("url")

        pigeon.image_url = url
        db.session.commit()

    return redirect(url_for("pigeon.detail", id=id))
