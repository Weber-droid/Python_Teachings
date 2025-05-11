import datetime
from app.libs.mysqllib import MysqlLib

class AdminServicesModel(object):
    def __init__(self, user):
        self.dbconn = MysqlLib()
        self.user = user

    def getServiceBySlug(self, slug):
        """
        Fetch a service by its slug.
        """
        print(f"Fetching service with slug: {slug}")
        condition = f"WHERE slug = '{slug}'"
        service = self.dbconn.select_from_table('services', condition=condition)
        return service[0] if service else None

    def createService(self, service_data):
        """
        Insert a new service into the database.
        """
        print(f"Creating service: {service_data['name']}")
        return self.dbconn.insert_in_table('services', service_data)

    def updateServiceStatus(self, service_id, status):
        """
        Update the status of a service.
        """
        print(f"Updating service status for ID: {service_id}")
        update_data = {
            "status": status,
            "date_updated": datetime.datetime.utcnow()
        }
        condition = f"WHERE id = {service_id}"
        return self.dbconn.update_table('services', update_data, condition)

    def getAllServices(self):
        """
        Fetch all services from the database.
        """
        return self.dbconn.select_from_table("services")
