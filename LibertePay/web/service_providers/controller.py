from flask import Blueprint, request, jsonify
from app import language
from app.apis.v1.web.service_providers.services import ServiceProviderService
from app.apis.v1.web.auth.services import webServices
from app.libs.logger import Logger

sms_providers = Blueprint('sms_providers', __name__, url_prefix='/api/settings/sms-provider')
logger = Logger()

@sms_providers.route('/active', methods=['PUT'])
def set_active_sms_provider():
    """
    Endpoint to set one SMS provider as active and deactivate all others.
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

        request_data = request.get_json()
        if "providerId" not in request_data:
            return jsonify({"code": 400, "msg": "Missing 'providerId' field"}), 400

        sms_service = ServiceProviderService(logged_in_admin)
        response = sms_service.set_active_sms_provider(request_data["providerId"])
        return jsonify(response), 200 if response["code"] == 200 else 500

    except Exception as e:
        logger.error(f"Error setting active SMS provider: {e}")
        return jsonify({"code": 500, "msg": "Internal server error"}), 500


@sms_providers.route('/', methods=['GET'])
def get_all_sms_providers():
    """
    Endpoint to fetch all SMS providers.
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

        sms_service = ServiceProviderService(logged_in_admin)
        response = sms_service.get_all_sms_providers()
        return jsonify(response), 200 if response["code"] == 200 else 500

    except Exception as e:
        return jsonify({"code": 500, "msg": "Internal server error"}), 500
