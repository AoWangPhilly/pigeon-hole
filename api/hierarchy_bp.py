import os
from typing import Final, Dict, Any
from mimetypes import guess_type
from io import BytesIO
import uuid

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
from requests.sessions import Session

from models import db, PigeonHierarchy, Pigeon

hierarchy_bp = Blueprint(
    "hierarchy",
    __name__,
)


@hierarchy_bp.route("/add/<id>", methods=["POST"])
def add(id: str):
    father_id = request.form.get("father_id")
    mother_id = request.form.get("mother_id")

    if not all((father_id, mother_id)):
        return jsonify({"error": "All fields are required"}), 400

    pigeon = PigeonHierarchy.query.filter_by(child_id=id).first()
    if pigeon is not None:
        pigeon.father_id = father_id
        pigeon.mother_id = mother_id
        db.session.commit()
    else:
        pigeon = PigeonHierarchy(
            father_id=father_id,
            mother_id=mother_id,
            child_id=id,
        )
        db.session.add(pigeon)
        db.session.commit()
    return redirect(url_for("pigeon.detail", id=id))

@hierarchy_bp.route("/view/<id>")
def view(id: str):
    pigeon_hierarchy = PigeonHierarchy.query.filter_by(child_id=id).first()
    if pigeon_hierarchy is None:
        return redirect(url_for("pigeon.detail", id=id))
    return render_template("hierarchy.html", pigeon_hierarchy=pigeon_hierarchy)
