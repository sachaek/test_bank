from sqlalchemy.orm import Session

from api.db.models.account_table import Account


class AccountCrudDB:
    @staticmethod
    def get_account_by_id(db: Session, account_id: int) -> Account | None:
        return db.query(Account).filter_by(id=account_id).first()