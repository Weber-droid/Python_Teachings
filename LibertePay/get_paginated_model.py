    def getPaginatedUsers(self, offset, limit):
        """
        Fetch paginated users from the database.
        """
        print(f"Fetching users with offset {offset} and limit {limit}")
        condition = f"LIMIT {limit} OFFSET {offset}"
        fields = ["id", "firstname", "lastname", "email", "phone", "status"]
        return self.dbconn.select_from_table("users", fields, condition)
