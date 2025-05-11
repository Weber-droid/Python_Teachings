from app import config, language
from app.apis.v1.web.terms.models import TermsModel
from app.libs.utils import Utilites

class TermsService(object):
    def __init__(self, user):
        self.lang = {}
        self.lang = getattr(language, config.DEFAULT_LANG)
        self.user = user
        self.model = TermsModel(user)
        self.utils = Utilites

    def get_terms(self):
        """
        Service to fetch the active terms and conditions.
        """
        try:
            terms = self.model.get_latest_terms()
            if not terms:
                return {"code": 404, "msg": "Terms and conditions not found"}
            return {"code": 200, "msg": "Terms fetched successfully", "data": terms}
        except Exception as e:
            return {"code": 500, "msg": "Internal server error", "data": []}

    def save_terms(self, name, details):
        """
        Service to save or update the terms and conditions.
        """
        try:
            sanitized_details = Utilites.sanitize_html(details)

            response = self.model.save_terms(name, sanitized_details)
            if response:
                return {"code": 200, "msg": "Terms updated successfully"}
            else:
                return {"code": 500, "msg": "Failed to update terms"}
        except Exception as e:
            return {"code": 500, "msg": "Internal server error"}
