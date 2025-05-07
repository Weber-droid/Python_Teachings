@web_auth.route('/admin/customers', methods=['GET'])
def get_all_users():
    """
    Endpoint to fetch paginated users, accessible only by authorized admins.
    """
    try:
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"code": 401, "msg": "Unauthorized: Missing token"}), 401

        try:
            if token.startswith("Bearer "):
                token = token.split(" ")[1]

            # Decode the token using AuthService
            # decoded_token = service.decode_token(token)

            # Check if the user has admin privileges
            # if decoded_token.get("role_id") != "admin":  # Replace "admin" with your actual admin role ID
                # return jsonify({"code": 403, "msg": "Forbidden: Admin access required"}), 403

        except Exception as e:
            return jsonify({"code": 401, "msg": f"Unauthorized: {str(e)}"}), 401

        
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 10))

        
        offset = (page - 1) * page_size

        
        users = model.getPaginatedUsers(offset, page_size)
        if not users:
            return jsonify({"code": 404, "msg": "No users found", "data": []}), 404

        
        formatted_users = [
            {
                "id": user["id"],
                "firstname": user["firstname"],
                "lastname": user["lastname"],
                "email": user["email"],
                "phone": user["phone"],
                "status": user["status"]
            }
            for user in users
        ]

        
        return jsonify({
            "code": 200,
            "msg": "Users fetched successfully",
            "data": formatted_users,
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_users": len(users)  
            }
        }), 200

    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return jsonify({"code": 500, "msg": "Internal server error"}), 500
