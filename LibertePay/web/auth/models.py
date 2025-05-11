from app.libs.mysqllib import MysqlLib

class AuthenticationModel(object):
    def __init__(self, user):
        super(AuthenticationModel, self).__init__()
        self.dbconn = MysqlLib()
        self.user = user

    def middleWareAdmin(self, access_token):
        print("In Get Authorized Admin")

        admin = self.dbconn.select_from_table('admin', condition="WHERE access_token = '{}'"
                                             .format(access_token))
        return admin
    
    def updateMiddleWare(self, request_value, access_token):
        print("Update Middle Ware")

        updateMiddle = self.dbconn.update_table('admin', request_value, condition="WHERE access_token = '{}'"
                                                .format(access_token))
        return updateMiddle


    def updateAdmin(self, request_data, email, admin_id):
        print("In Update Admin")

        updateAdmin = self.dbconn.update_table('admin', request_data, condition="WHERE email = '{}' and id = {}"
                                              .format(email, admin_id))
        return updateAdmin

    def getRoleById(self, role_id):
        """
        Fetch a role by role_id.
        """
        print(f"Fetching role with ID: {role_id}")
        role = self.dbconn.select_from_table('roles', condition="WHERE role_id = '{}'".format(role_id))
        return role[0] if len(role) > 0 else None
    
    def createRole(self, role_data):
        """
        Insert a new role into the roles table.
        """
        print(f"Inserting role: {role_data}")
        return self.dbconn.insert_in_table('roles', role_data)

    def createAdmin(self, admin_data):
        """
        Insert a new admin into the database.
        """
        print(f"Creating admin with email: {admin_data['email']}")
        result = self.dbconn.insert_in_table('admin', admin_data)
        return result

    def getAdminByEmail(self, email):
        """
        Fetch an admin by email.
        """
        print(f"Fetching admin with email: {email}")
        admin = self.dbconn.select_from_table('admin', condition="WHERE email = '{}'".format(email))
        return admin[0] if len(admin) > 0 else None
    
    def getAdminByPhoneNumber (self, phone_number):
        """
        Fetch an admin by phone number
        """
        print(f"Fetching admin with phone number: {phone_number}")
        admin = self.dbconn.select_from_table('admin', condition="WHERE phone_number = '{}'".format(phone_number))
        return admin[0] if len(admin) > 0 else None
    
    def save_reset_token(self, admin_id, token, expiration):
        """
        Save the password reset token and expiration for an admin.
        """
        data = {
            "admin_id": admin_id,
            "token": token,
            "expiration": expiration
        }
        return self.dbconn.insert_in_table('password_reset_tokens', data)

    def get_reset_token(self, token):
        """
        Fetch a reset token from the database.
        """
        result = self.dbconn.select_from_table('password_reset_tokens', condition="WHERE token = '{}'".format(token))
        return result[0] if len(result) > 0 else None

    def invalidate_reset_token(self, token):
        """
        Invalidate a reset token after use.
        """
        return self.dbconn.delete_from_table('password_reset_tokens', condition="WHERE token = '{}'".format(token))

    def updateAdminPassword(self, admin_id, hashed_password):
        """
        Update the admin's password in the database.
        """
        print(f"Updating password for admin with ID: {admin_id}")
        request_data = {"password": hashed_password}
        return self.dbconn.update_table("admin", request_data, condition="WHERE id = '{}'".format(admin_id))
    
    def getPaginatedUsers(self, offset, limit):
        """
        Fetch paginated users from the database.
        """
        print(f"Fetching users with offset {offset} and limit {limit}")
        condition = f"LIMIT {limit} OFFSET {offset}"
        fields = ["id", "firstname", "lastname", "email", "phone", "status"]
        return self.dbconn.select_from_table("users", fields, condition)


    
