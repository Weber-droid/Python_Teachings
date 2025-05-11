import datetime
from app.libs.mysqllib import MysqlLib

class ServiceProviderModel(object):
    """
    Model for handling SMS provider-related database queries.
    """

    def __init__(self, user):
        super(ServiceProviderModel, self).__init__()
        self.dbconn = MysqlLib()
        self.user = user

    def get_active_sms_provider(self):
        """
        Fetch the currently active SMS provider.
        """
        condition = "WHERE status = 1"
        provider = self.dbconn.select_from_table('service_providers', condition=condition)
        return provider[0] if provider else None
    
    def get_sms_provider_by_id(self, provider_id):
        """
        Fetch an SMS provider by its ID.
        """
        condition = f"WHERE id = '{provider_id}'"
        provider = self.dbconn.select_from_table('service_providers', condition=condition)
        return provider[0] if provider else None

    def deactivate_all_sms_providers(self):
        """
        Deactivate all SMS providers.
        """
        update_data = {"status": 0}
        return self.dbconn.update_table('service_providers', update_data)

    def activate_sms_provider(self, provider_id):
        """
        Activate a specific SMS provider by its ID.
        """
        update_data = {"status": 1, "date_updated": datetime.datetime.utcnow()}
        condition = f"WHERE id = '{provider_id}'"
        return self.dbconn.update_table('service_providers', update_data, condition=condition)
    
    def get_all_sms_providers(self):
        """
        Fetch all SMS providers from the database.
        """
        providers = self.dbconn.select_from_table('service_providers')
        return providers
