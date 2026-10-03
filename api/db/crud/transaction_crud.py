from sqlalchemy.orm import Session

from api.db.models.transaction_table import Transaction


class TransactionCrudDB:
    @staticmethod
    def get_transactions_to_account(db: Session, to_account_id: int, transaction_type: str) -> list[Transaction]:
        return db.query(Transaction).filter_by(to_account_id=to_account_id,
                                               transaction_type=transaction_type).all()
