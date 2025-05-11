from datetime import datetime, timedelta
from app import config, language
from app.apis.v1.web.auth.models import AuthenticationModel
from app.libs.sms import SMS
from app.libs.utils import Utilites
from passlib.hash import sha256_crypt

class webServices(object):
    def __init__(self, user):
        self.lang = {}
        self.lang = getattr(language, config.DEFAULT_LANG)
        self.user = user
        self.sms = SMS
        self.utils = Utilites()
        self.model = AuthenticationModel(user)

    def middleWare(self, request_value):
        print("In Middleware")
        print("Request value:", request_value)
        
        request_header = dict(request_value)
        print("Request header:", request_header)
        
        auth_header = request_header.get('Authorization', None)
        if not auth_header:
            print("No Authorization header found")
            return {"code": language.CODES['FAIL'], "msg": "Authorization header missing", "data": ""}
            
        try:
            # Handle both "Bearer token" and just "token" formats
            if ' ' in auth_header:
                access_token = auth_header.split()[1]
            else:
                access_token = auth_header
                
            print("Extracted access token:", access_token)
            
            admin = self.model.middleWareAdmin(access_token)
            print("Admin data:", admin)
            
            if not admin:
                print("User not found in database")
                return {"code": language.CODES['FAIL'], "msg": "User Not Exist", "data": ""}
                
            if admin[0]["expire_date"] == "":
                print("Expire date is null")
                return {"code": language.CODES['FAIL'], "msg": "Login Required", "data": ""}
                
            if admin[0]["expire_date"] < datetime.now():
                print("Token has expired")
                return {"code": language.CODES['FAIL'], "msg": "Token Expired", "data": ""}
                
            if admin[0]["expire_date"] < datetime.now() + timedelta(days=1):
                print("Extending token expiration")
                updateData = {
                    "expire_date": datetime.now() + timedelta(days=1)
                }
                updateMiddleAdmin = self.model.updateMiddleWare(updateData, access_token)
                print("Token extension result:", updateMiddleAdmin)
                
            return {"code": language.CODES['SUCCESS'], "msg": "Success", "data": admin[0]}
            
        except Exception as e:
            print("Error in middleware:", str(e))
            return {"code": language.CODES['FAIL'], "msg": f"Authorization Failed: {str(e)}", "data": ""}



    def createAdmin(self, request_data, logged_in_admin):
        print("In register Admin...")

        if logged_in_admin.get("role_id") != "00":
            return {"code": language.CODES["FAIL"], "msg": "Unauthorised access. Must be a super admin to add admins."}

        name = request_data.get("name")
        email =  request_data.get("email")
        phone_number = request_data.get("phone_number")
        password = request_data.get("password")
        role_id = request_data.get("role_id")

        if not all ([name, email, phone_number, password, role_id]):
            return {"code": language.CODES["FAILS"], "msg":"Invalid data", "data": ""}
        
        if role_id not in ["01", "02"]:
            return {"code": language.CODES["FAIL"], "msg":"Invalid role_id, Must be 01 or 02"}

        role = self.model.getRoleById(role_id)
        if not role:
            role_name = "Maker" if role_id == "01" else "Checker"
            self.model.createRole({"role_id": role_id, "role_name": role_name})
            print(f"Role {role_name} added to roles table.")

        password_check = self.utils.password_complexity_check(password)
        print(password_check)
        if not password_check["password_ok"]:
            return {"code":language.CODES["FAIL"], "msg":"Password not secure enough", "data": password_check }
        
        is_email = self.model.getAdminByEmail(email)
        if is_email:
            print("There is a user")
            return {"code": language.CODES["FAIL"], "msg": "An admin with this email already exist", "data": ""}
        
        is_number = self.model.getAdminByPhoneNumber(phone_number)
        if is_number:
            return {"code": language.CODES["FAIL"], "msg":"An admin with this phone number exist", "data":""}
        
        admin_data = {
            "name": name,
            "email": email,
            "phone_number": phone_number,
            "password": sha256_crypt.hash(password),
            "role_id": role_id 
        }

        add_admin = self.model.createAdmin(admin_data)
        if add_admin:
            return {"code": language.CODES["SUCCESS"], "msg":"Registration successful", "data":""}
        else:
            return {"code": language.CODES["FAIL"], "msg": "Registration failed", "data":""}


    def admin_login(self, request_data):
        """
        Admin login method.
        """
        try:
            print("Logging Admin in ...")
            email = request_data.get("email")
            password = request_data.get("password")

            if not email or not password:
                return {"code": language.CODES["FAIL"], "msg": "Invalid data", "data": ""}

            print(f"Fetching admin with email: {email}")
            getAdmin = self.model.getAdminByEmail(email)
            print(f"Admin fetched: {getAdmin}")

            if not getAdmin:
                return {"code": language.CODES["FAIL"], "msg": "Admin with this email does not exist", "data": {}}

            print("Verifying password...")
            verify_pass = sha256_crypt.verify(password, getAdmin['password'])
            print(f"Password verification result: {verify_pass}")

            if verify_pass:
                print("Generating access token...")
                access_token = self.utils.generateUniqueID(1000000, 9999999)
                login_data = {
                    "access_token": access_token,
                    "expire_date": datetime.now() + timedelta(days=1),
                    "last_login": datetime.now()
                }
                print(f"Updating admin login data: {login_data}")
                update_admin = self.model.updateAdmin(login_data, email, getAdmin['id'])
                print(f"Update result: {update_admin}")
                return {"code": language.CODES["SUCCESS"],"msg": "Login successful","data": {"access_token": access_token,"name": getAdmin['name'],"email": getAdmin['email'],"role_id": getAdmin['role_id']}}
            else:
                print("Incorrect password")
                return {"code": language.CODES["FAIL"], "msg": self.lang["Invalid login"], "data": ""}
        except Exception as e:
            print(f"Log in Exception: {e}")
            return {"code": language.CODES["FAIL"], "msg": "Incorrect Password", "data": ""}
        

    def requestPasswordReset(self, email):
        """
        Service to handle password reset requests.
        """
        try:
            admin = self.model.getAdminByEmail(email)
            if not admin:
                return {"code": language.CODES["FAIL"], "msg": "Admin not found", "data": ""}

            token = self.utils.generateUniqueID(1000000, 9999999)
            expiration = datetime.now() + timedelta(minutes=30)

            self.model.save_reset_token(admin["id"], token, expiration)

            reset_link = f"https://your-admin-app.com/reset-password?token={token}"

            subject = "Password Reset Request"
            recipient = email
            msg = f"""
            <p>Hello,</p>
            <p>Click the link below to reset your password:</p>
            <p><a href="{reset_link}">{reset_link}</a></p>
            <p>This link will expire in 30 minutes.</p>
            <p>If you did not request a password reset, please ignore this email.</p>
            """
            email_sent = self.utils.sendEmailSendGrid(subject, recipient, msg)
            if not email_sent:
                return {"code": language.CODES["FAIL"], "msg": "Failed to send password reset email", "data": ""}

            return {"code": language.CODES["SUCCESS"], "msg": "Password reset link sent to email", "data": {"token": token}}
        except Exception as e:
            print(f"Password reset request error: {e}")
            return {"code": language.CODES["FAIL"], "msg": "Internal server error", "data": ""}

    def resetPassword(self, token, new_password):
        """
        Service to handle password reset.
        """
        try:
            reset_token = self.model.get_reset_token(token)
            if not reset_token:
                return {"code": language.CODES["FAIL"], "msg": "Invalid or expired token", "data": ""}

            if datetime.now() > reset_token["expiration"]:
                return {"code": language.CODES["FAIL"], "msg": "Token has expired", "data": ""}

            hashed_password = sha256_crypt.hash(new_password)

            admin_id = reset_token["admin_id"]
            update_result = self.model.updateAdminPassword(admin_id, hashed_password)
            if not update_result:
                return {"code": language.CODES["FAIL"], "msg": "Failed to reset password", "data": ""}

            self.model.invalidate_reset_token(token)

            return {"code": language.CODES["SUCCESS"], "msg": "Password reset successful", "data": ""}
        except Exception as e:
            print(f"Password reset error: {e}")
            return {"code": language.CODES["FAIL"], "msg": "Internal server error", "data": ""}
        
    def getPaginatedUsers(self, page, page_size):
        """
        Service to fetch paginated users.
        """
        try:
            offset = (page - 1) * page_size
            users = self.model.getPaginatedUsers(offset, page_size)

            if not users:
                return {"code": 404, "msg": "No users found", "data": []}

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

            return {
                "code": 200,
                "msg": "Users fetched successfully",
                "data": formatted_users,
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_users": len(users)  
                }
            }
        except Exception as e:
            print(f"Error fetching paginated users: {e}")
            return {"code": 500, "msg": "Internal server error", "data": []}
