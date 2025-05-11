from datetime import datetime, timedelta
from app import config, language
from app.apis.v1.web.admin_services.models import AdminServicesModel
from app.libs.utils import Utilites
# from app import language

class AdminServices(object):
    def __init__(self, user):
        self.lang = {}
        self.lang = getattr(language, config.DEFAULT_LANG)
        self.user = user
        self.model = AdminServicesModel(user)
        self.utils = Utilites()

    def createService(self, request_data):
        """
        Service to create a new service.
        """
        try:
            existing_service = self.model.getServiceBySlug(request_data["slug"])
            if existing_service:
                return {"code": 400, "msg": "Slug already exists", "data": ""}

            service_data = {
                "name": request_data["name"],
                "slug": request_data["slug"],
                "image": request_data.get("image"),
                "secrete_key": request_data.get("secrete_key"),
                "type": request_data["type"],
                "is_sub": request_data.get("is_sub", 0),
                "status": 0,  
                "date_created": datetime.now(),
                "date_updated": datetime.now()
            }

            response = self.model.createService(service_data)
            if response:
                return {"code": 201, "msg": "Service created successfully", "data": service_data}
            else:
                return {"code": 500, "msg": "Failed to create service", "data": ""}
        except Exception as e:
            print(f"Error creating service: {e}")
            return {"code": 500, "msg": "Internal server error", "data": ""}

    def approveService(self, service_id, admin_id):
        """
        Service to approve a service.
        """
        try:
            response = self.model.updateServiceStatus(service_id, 1)
            if response:
                return {"code": 200, "msg": "Service approved successfully"}
            else:
                return {"code": 500, "msg": "Failed to approve service"}
        except Exception as e:
            print(f"Error approving service: {e}")
            return {"code": 500, "msg": "Internal server error"}

    def updateServiceStatus(self, service_id, active):
        """
        Service to update the active/inactive status of a service.
        """
        try:
            new_status = 1 if active else 0
            response = self.model.updateServiceStatus(service_id, new_status)
            if response:
                return {"code": 200, "msg": "Service status updated successfully"}
            else:
                return {"code": 500, "msg": "Failed to update service status"}
        except Exception as e:
            print(f"Error updating service status: {e}")
            return {"code": 500, "msg": "Internal server error"}

    def getAllServices(self):
        """
        Service to fetch all services.
        """
        try:
            services = self.model.getAllServices()
            return {"code": 200, "msg": "Services fetched successfully", "data": services}
        except Exception as e:
            print(f"Error fetching services: {e}")
            return {"code": 500, "msg": "Internal server error", "data": []}
