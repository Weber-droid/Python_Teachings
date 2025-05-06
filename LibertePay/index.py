@web_auth.route('/admin/create', methods=['POST'])
def create_admin():
    """
    Endpoint for super admin to create other admins.
    """
    try:
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"code": 401, "msg": "Unauthorized: Missing token"}), 401

        try:
            if token.startswith("Bearer "):
                token = token.split(" ")[1]
            decoded_token = service.decode_token(token)
            if decoded_token.get("role_id") != "00":  # Ensure only super admin can create admins
                return jsonify({"code": 403, "msg": "Forbidden: Super admin access required"}), 403
        except Exception as e:
            return jsonify({"code": 401, "msg": f"Unauthorized: {str(e)}"}), 401

        request_data = request.get_json()
        required_fields = ["name", "email", "phone_number", "password", "role_id"]

        for field in required_fields:
            if field not in request_data:
                logger.error(f"Admin creation failed: Missing field {field}.")
                return jsonify({"code": 400, "msg": f"Missing field: {field}"}), 400

        if request_data["role_id"] not in ["01", "02"]:  # 01 for maker, 02 for checker
            logger.error(f"Admin creation failed: Invalid role ID {request_data['role_id']}.")
            return jsonify({"code": 400, "msg": "Invalid role ID"}), 400

        hashed_password = service.hash_password(request_data["password"])

        admin_data = {
            "name": request_data["name"],
            "email": request_data["email"],
            "phone_number": request_data["phone_number"],
            "password": hashed_password,
            "role_id": request_data["role_id"]
        }

        response = model.createAdmin(admin_data)
        if response:
            return jsonify({"code": 201, "msg": "Admin created successfully"}), 201
        else:
            return jsonify({"code": 500, "msg": "Failed to create admin"}), 500

    except Exception as e:
        logger.error(f"Admin creation error: {e}")
        return jsonify({"code": 500, "msg": "Internal server error"}), 500
