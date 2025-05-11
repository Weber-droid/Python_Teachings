import datetime
from app.libs.mysqllib import MysqlLib


class TermsModel(object):
    """
    Model for handling terms and conditions database queries.
    """
    def __init__(self, user):
        super(TermsModel, self).__init__()
        self.dbconn = MysqlLib()
        self.user = user

    def get_latest_terms(self):
        """
        Fetch the latest terms and conditions.
        """
        terms = self.dbconn.select_from_table(
            'terms_and_conditions',
            condition="WHERE status = 'Y' ORDER BY date_updated DESC LIMIT 1",  
            # order_by=""
        )
        return terms[0] if terms else None

    def save_terms(self, name, details):
        """
        Save or update the terms and conditions.
        Ensures only one record exists in the table.
        """
        data = {
            "name": name,
            "details": details,
            "status": "Y",  
            "date_updated": datetime.datetime.utcnow()
        }

        existing_terms = self.dbconn.select_from_table('terms_and_conditions', condition="LIMIT 1")
        if existing_terms:
            return self.dbconn.update_table('terms_and_conditions', data, condition="LIMIT 1")
        else:
            return self.dbconn.insert_in_table('terms_and_conditions', data)
