from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey,JSON,DateTime
from super_models.database import Base


class IdBox(Base):
    __tablename__ = 'id_box'

    name = Column(String(32), primary_key=True)
    value = Column(BigInteger, nullable=False)