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
    flash,
)
from requests.sessions import Session

from models import db, PigeonHierarchy, Pigeon

hierarchy_bp = Blueprint(
    "hierarchy",
    __name__,
)


@hierarchy_bp.route("/get/<pigeon_id>")
def get(pigeon_id):
    hierarchy = PigeonHierarchy.query.filter_by(child_id=pigeon_id).first()
    if hierarchy is None:
        return jsonify({"error": "Pigeon not found"}), 404
    return jsonify(hierarchy)


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
    flash("Pigeon hierarchy added successfully", "success")
    return redirect(url_for("pigeon.detail", id=id))


@hierarchy_bp.route("/view/<id>")
def view(id: str):
    pigeon_hierarchy = PigeonHierarchy.query.filter_by(child_id=id).first()
    if pigeon_hierarchy is None:
        return redirect(url_for("pigeon.detail", id=id))
    father = Pigeon.query.filter_by(_id=pigeon_hierarchy.father_id).first()
    mother = Pigeon.query.filter_by(_id=pigeon_hierarchy.mother_id).first()
    child = Pigeon.query.filter_by(_id=pigeon_hierarchy.child_id).first()
    return render_template("hierarchy.html", father=father, mother=mother, child=child)
