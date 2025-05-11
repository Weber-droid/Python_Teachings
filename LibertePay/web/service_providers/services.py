from app import config, language
from app.apis.v1.web.service_providers.models import ServiceProviderModel
from app.libs.utils import Utilites


class ServiceProviderService(object):
    def __init__(self, user):
        self.lang = {}
        self.lang = getattr(language, config.DEFAULT_LANG)
        self.user = user
        self.utils = Utilites
        self.model = ServiceProviderModel(user)
        

    def set_active_sms_provider(self, provider_id):
        """
        Service to set one SMS provider as active and deactivate all others.
        """
        try:
            current_active_provider = self.model.get_active_sms_provider()
            if current_active_provider and current_active_provider["id"] == provider_id:
                return {"code": 200, "msg": "Provider is already active"}

            provider = self.model.get_sms_provider_by_id(provider_id)
            if not provider:
                return {"code": 400, "msg": "Invalid provider ID"}

            self.model.deactivate_all_sms_providers()
            response = self.model.activate_sms_provider(provider_id)
            if response:
                return {"code": 200, "msg": "SMS provider activated successfully"}
            else:
                return {"code": 500, "msg": "Failed to activate SMS provider"}
        except Exception as e:
            return {"code": 500, "msg": "Internal server error"}

    def get_all_sms_providers(self):
        """
        Service to fetch all SMS providers.
        """
        try:
            providers = self.model.get_all_sms_providers()
            return {"code": 200, "msg": "SMS providers fetched successfully", "data": providers}
        except Exception as e:
            return {"code": 500, "msg": "Internal server error", "data": []}
