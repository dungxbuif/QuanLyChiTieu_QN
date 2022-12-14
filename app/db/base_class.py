import re
from uuid import uuid4

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


def pluralize(noun: str):
    if re.search('[sxz]$', noun):
         return re.sub('$', 'es', noun)
    elif re.search('[^aeioudgkprt]h$', noun):
        return re.sub('$', 'es', noun)
    elif re.search('[aeiou]y$', noun):
        return re.sub('y$', 'ies', noun)
    else:
        return noun + 's'

@as_declarative()
class Base:
    id=Column(String, primary_key=True, index=True,default=str(uuid4()))
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        carmalCase_to_snakecase=re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
        return pluralize(carmalCase_to_snakecase)

    created_at=Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))
    creator=Column(Integer, nullable=True,)
