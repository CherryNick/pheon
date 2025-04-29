from random import randint

import factory
import pytest
from passlib.context import CryptContext

from src.infra.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture
def user_factory(sync_session):
    class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = User
            sqlalchemy_session = sync_session
            sqlalchemy_session_persistence = "commit"

        id = factory.LazyFunction(lambda: randint(10**8, 10**9) + 1)
        username = factory.Faker("user_name")
        password_hash = factory.LazyAttribute(lambda _: pwd_context.hash("testpassword"))

    return UserFactory