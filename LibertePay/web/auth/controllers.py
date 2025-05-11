import json
from flask import Blueprint, jsonify, request
from app import language

from app.apis.v1.web.auth.services import webServices


web_auth = Blueprint('web_auth', __name__, url_prefix='/api/auth')

@web_auth.route('/admin/create', methods=['POST'])
def create_admin():
    """
    Endpoint for super admin to create other admins.
    """
    try:
        print("Registering Admin ...")

        middleware_response = webServices(None)
        middleware_response = middleware_response.middleWare(request.headers)

        if middleware_response["code"] != language.CODES["SUCCESS"]:
            return middleware_response  

        logged_in_admin = middleware_response["data"]
        print(f"Logged-in Admin: {logged_in_admin}")

        serv = webServices(logged_in_admin)

        request_data = request.get_json()
        print(f"Request Data: {request_data}")

        register_admin = serv.createAdmin(request_data, logged_in_admin)
        print(f"Register Admin Response: {register_admin}")
        return register_admin

    except Exception as e:
        print(f"Sign up Exception: {e}")
        return {"code": language.CODES["ERROR"], "msg": f"Sign Up Failed. Error({str(e)})"}        
    
@web_auth.route('/admin/login', methods=['POST'])
def admin_login():
    """
    Endpoint for admin login.
    """
    try:
        print("Logging Admin in ...")
        session_details = {}
        serv = webServices(session_details)
        request_method = request.method

        if request_method == "POST":
            request_data = json.loads(request.data.decode('utf-8'))
            print(request_data)
            log_admin = serv.admin_login(request_data)
            print(log_admin)
            return log_admin
        else:
            return {'code': language.CODES['ERROR', 'msg':'Method not allow : ({}).'.format(request_method)]}
    except Exception as e:
        print("Log in Exception: {}".format(e))
        return {'code': language.CODES['ERROR'], 'msg':'Log in failed. Error({})'.format(str(e))}
        raise e
    
@web_auth.route('/admin/request-password-reset', methods=['POST'])
def request_password_reset():
    """
    Endpoint to request a password reset.
    """
    try:
        request_data = request.get_json()
        if "email" not in request_data:
            return jsonify({"code": language.CODES["FAIL"], "msg": "Missing email"}), 400

        service = webServices(None)
        response = service.requestPasswordReset(request_data["email"])
        return jsonify(response), 200 if response["code"] == language.CODES["SUCCESS"] else 400
    except Exception as e:
        print(f"Password reset request error: {e}")
        return jsonify({"code": language.CODES["ERROR"], "msg": "Internal server error"}), 500

@web_auth.route('/admin/reset-password', methods=['POST'])
def reset_password():
    """
    Endpoint to reset the password.
    """
    try:
        request_data = request.get_json()
        required_fields = ["token", "new_password"]

        for field in required_fields:
            if field not in request_data:
                return jsonify({"code": language.CODES["FAIL"], "msg": f"Missing field: {field}"}), 400

        service = webServices(None)
        response = service.resetPassword(request_data["token"], request_data["new_password"])
        return jsonify(response), 200 if response["code"] == language.CODES["SUCCESS"] else 400
    except Exception as e:
        print(f"Password reset error: {e}")
        return jsonify({"code": language.CODES["ERROR"], "msg": "Internal server error"}), 500
    
    
@web_auth.route('/admin/customers', methods=['GET'])
def get_all_users():
    """
    Endpoint to fetch paginated users, accessible only by authorized admins.
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
        if logged_in_admin["role_id"] != "00":  
            return jsonify({"code": 403, "msg": "Forbidden: Admin access required"}), 403

        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 10))

        response = service.getPaginatedUsers(page, page_size)
        return jsonify(response), 200 if response["code"] == 200 else 404

    except Exception as e:
        print(f"Error fetching users: {e}")
        return jsonify({"code": 500, "msg": "Internal server error"}), 500
        
