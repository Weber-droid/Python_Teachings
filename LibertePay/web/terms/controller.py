from flask import Blueprint, request, jsonify
from app import language
from app.apis.v1.web.terms.services import TermsService
from app.apis.v1.web.auth.services import webServices
from app.libs.logger import Logger

terms = Blueprint('terms', __name__, url_prefix='/api/terms')
logger = Logger()

@terms.route('/', methods=['GET'])
def get_terms():
    """
    Endpoint to fetch the active terms and conditions.
    """
    try:
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"code": 401, "msg": "Unauthorized: Missing token"}), 401

        service = webServices(None)
        middleware_response = service.middleWare({"Authorization": token})

        if middleware_response["code"] != language.CODES["SUCCESS"]:
            return jsonify(middleware_response), 401

        logged_in_admin = middleware_response["data"]
        if logged_in_admin["role_id"] not in ["00", "01", "02"]: 
            return jsonify({"code": 403, "msg": "Forbidden: Admin access required"}), 403

        terms_service = TermsService(logged_in_admin)
        response = terms_service.get_terms()
        return jsonify(response), 200 if response["code"] == 200 else 404

    except Exception as e:
        return jsonify({"code": 500, "msg": "Internal server error"}), 500


@terms.route('/', methods=['POST', 'PUT'])
def save_terms():
    """
    Endpoint to save or update the terms and conditions.
    """
    try:
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"code": 401, "msg": "Unauthorized: Missing token"}), 401

        service = webServices(None)
        middleware_response = service.middleWare({"Authorization": token})

        if middleware_response["code"] != language.CODES["SUCCESS"]:
            return jsonify(middleware_response), 401

        logged_in_admin = middleware_response["data"]
        if logged_in_admin["role_id"] not in ["00"]:  
            return jsonify({"code": 403, "msg": "Forbidden: Super admin access required"}), 403

        request_data = request.get_json()
        required_fields = ["name", "details"]
        for field in required_fields:
            if field not in request_data:
                return jsonify({"code": 400, "msg": f"Missing '{field}' field"}), 400

        terms_service = TermsService(logged_in_admin)
        response = terms_service.save_terms(request_data["name"], request_data["details"])
        return jsonify(response), 200 if response["code"] == 200 else 500

    except Exception as e:
        return jsonify({"code": 500, "msg": "Internal server error"}), 500
