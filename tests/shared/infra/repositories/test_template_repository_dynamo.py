""" import os

import pytest

from src.shared.infra.repositories.template_repository_dynamo import TemplateRepositoryDynamo
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_TemplateRepositoryDynamo:
    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_create_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = TemplateRepositoryDynamo()
        user_repository_mock = UserRepositoryMock()
        resp = user_repository.create_user(user_repository_mock.users[0])

        assert user_repository_mock.users[0].email == resp.email

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = TemplateRepositoryDynamo()
        user_repository_mock = UserRepositoryMock()
        resp = user_repository.get_user(user_repository_mock.users[0].user_id)

        assert user_repository_mock.users[0].email == resp.email

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_delete_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = TemplateRepositoryDynamo()
        user_repository_mock = UserRepositoryMock()
        resp = user_repository.delete_user(user_repository_mock.users[0].user_id)

        assert user_repository_mock.users[0].email == resp.email

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_get_all_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = TemplateRepositoryDynamo()
        user_repository_mock = UserRepositoryMock()
        resp = user_repository.get_all_user()

        assert len(user_repository_mock.users) == len(resp)

    @pytest.mark.skip(reason="Needs dynamoDB")
    def test_update_user(self):
        os.environ["STAGE"] = "TEST"

        user_repository = TemplateRepositoryDynamo()
        user_repository_mock = UserRepositoryMock()
        updated = user_repository_mock.users[0].model_copy(update={"password_hash": "novo_hash"})
        resp = user_repository.update_user(updated)

        assert resp.password_hash == "novo_hash"
 """
