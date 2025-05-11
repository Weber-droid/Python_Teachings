from flask import Blueprint, request, jsonify
from app.apis.v1.web.admin_services.services import AdminServices
from app import language
from app.apis.v1.web.auth.services import webServices

admin_services = Blueprint('admin_services', __name__, url_prefix='/api/admin')

@admin_services.route('/add-services', methods=['POST'])
def create_service():
    """
    Endpoint for maker or super admin to create a new service.
    """
    try:
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"code": 401, "msg": "Unauthorized: Missing token"}), 401

        if token.startswith("Bearer "):
            token = token.split(" ")[1]

        service = webServices(None)
        middleware_response = service.middleWare({"Authorization": f"Bearer {token}"})

        if middleware_response["code"] != language.CODES["SUCCESS"]:
            return jsonify(middleware_response), 401

        logged_in_admin = middleware_response["data"]
        if logged_in_admin["role_id"] not in ["00", "01"]: 
            return jsonify({"code": 403, "msg": "Forbidden: Maker or Super Admin access required"}), 403

        request_data = request.get_json()
        required_fields = ["name", "slug", "type"]

        for field in required_fields:
            if field not in request_data:
                return jsonify({"code": 400, "msg": f"Missing field: {field}"}), 400

        admin_service = AdminServices(logged_in_admin)
        response = admin_service.createService(request_data)
        return jsonify(response), 201 if response["code"] == 201 else 400

    except Exception as e:
        print(f"Service creation error: {e}")
        return jsonify({"code": 500, "msg": "Internal server error"}), 500

@admin_services.route('/services/approve', methods=['POST'])
def approve_service():
    """
    Endpoint for checker or super admin to approve a service.
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
        if logged_in_admin["role_id"] not in ["00", "02"]:  
            return jsonify({"code": 403, "msg": "Forbidden: Checker or Super Admin access required"}), 403

        request_data = request.get_json()
        required_fields = ["service_id"]

        for field in required_fields:
            if field not in request_data:
                return jsonify({"code": 400, "msg": f"Missing field: {field}"}), 400

        admin_service = AdminServices(logged_in_admin)
        response = admin_service.approveService(request_data["service_id"], logged_in_admin["id"])
        return jsonify(response), 200 if response["code"] == 200 else 500

    except Exception as e:
        print(f"Service approval error: {e}")
        return jsonify({"code": 500, "msg": "Internal server error"}), 500

@admin_services.route('/services/<int:service_id>/status', methods=['PUT'])
def update_service_status(service_id):
    """
    Endpoint to update the active/inactive status of a service.
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
        if logged_in_admin["role_id"] != "00": 
            return jsonify({"code": 403, "msg": "Forbidden: Admin access required"}), 403

        request_data = request.get_json()
        if "active" not in request_data:
            return jsonify({"code": 400, "msg": "Missing 'active' field"}), 400

        admin_service = AdminServices(logged_in_admin)
        response = admin_service.updateServiceStatus(service_id, request_data["active"])
        return jsonify(response), 200 if response["code"] == 200 else 500

    except Exception as e:
        print(f"Service status update error: {e}")
        return jsonify({"code": 500, "msg": "Internal server error"}), 500


@admin_services.route('/fetch-services', methods=['GET'])
def get_all_services():
    """
    Endpoint to fetch all services.
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

        admin_service = AdminServices(logged_in_admin)
        response = admin_service.getAllServices()
        return jsonify(response), 200 if response["code"] == 200 else 500
    except Exception as e:
        print(f"Error fetching services: {e}")
        return jsonify({"code": 500, "msg": "Internal server error"}), 500
