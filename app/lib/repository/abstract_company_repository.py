from abc import abstractmethod
from app.lib.models.company_model import Company

class AbstractCompanyRepository:

    @abstractmethod
    def get_company_by_phone_number(self, phone_number: str) -> Company:
        pass
