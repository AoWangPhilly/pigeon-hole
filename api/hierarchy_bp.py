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

from models import db, Pigeon

hierarchy_bp = Blueprint(
    "hierarchy",
    __name__,
)
