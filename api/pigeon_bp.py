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
    flash,
)

from models import PigeonHierarchy, db, Pigeon
from forms import AddPigeonForm, EditPigeonForm

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
    if session.get("user") is None:
        return redirect(url_for("auth.login"))

    form = AddPigeonForm()
    if request.method == "POST" and form.validate_on_submit():
        user_id = session.get("user").get("_id")
        band_id = form.band_id.data
        name = form.name.data
        sex = form.sex.data
        color = form.color.data
        date_of_birth = form.date_of_birth.data
        image_data = form.image.data

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

        success_message = f"{name} has been added successfully"
        flash(success_message, "success")
        return redirect(url_for("pigeon.view"))
    return render_template("add.html", session=session, form=form)


@pigeon_bp.route("/<id>")
def detail(id):
    if session.get("user") is None:
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
    if session.get("user") is None:
        return redirect(url_for("auth.login"))

    pigeon = Pigeon.query.filter_by(_id=id).first()
    db.session.delete(pigeon)
    db.session.commit()

    delete_message = f"{pigeon.name} has successfully been removed."
    flash(delete_message, "danger")
    return redirect(url_for("pigeon.view"))


@pigeon_bp.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    if session.get("user") is None:
        return redirect(url_for("auth.login"))

    pigeon = Pigeon.query.filter_by(_id=id).first()
    form = EditPigeonForm()
    if request.method == "POST" and form.validate_on_submit():
        user_id = session.get("user").get("_id")
        image_data = form.image.data
        band_id = form.band_id.data

        pigeon.band_id = band_id
        pigeon.name = form.name.data
        pigeon.sex =  form.sex.data
        pigeon.color = form.color.data
        pigeon.date_of_birth = form.date_of_birth.data

        if image_data:
            blob_storage_response = save_image_to_blob_storage(
                image_data=image_data.read(),
                file_name=image_data.filename,
                blob_file_name=f"pigeon_images/user={user_id}/band_id={band_id}/{uuid.uuid4()}.png",
            )
            url = blob_storage_response.get("url")

            pigeon.image_url = url

        db.session.commit()
        flash(f"{pigeon.name} has been updated successfully", "success")
        return redirect(url_for("pigeon.detail", id=id))

    form.color.data = pigeon.color
    form.sex.data = pigeon.sex
    return render_template("edit.html", pigeon=pigeon, form=form)
