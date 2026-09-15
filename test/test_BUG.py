import pytest
from models.user_dto import User
from conftest import *
from faker import Faker
fake = Faker()

class TestRegistrationBug:
    @pytest.mark.parametrize("invalid_email", [
        "vbgyt123.tby.bnj",
        "bnhjyu78@",
        "@gmail.com",
        "fgvty56@@ghyu.vbh",
        "fgth67 @cvg.bn",
    ])
    def test_registration_negative_invalid_email_BUG(self, session, registration_url, invalid_email):
        user = User("dfgrt678@gmail", "Qwerty123$")
        body = {
            "username": user.username,
            "password": user.password,
        }
        response = session.post(registration_url, json=body)
        data = response.json()
        print(response.json())
        assert response.status_code == 400
        assert data["message"]["username"] == "must be a well-formed email address"

    @pytest.mark.parametrize("invalid_password", [
            "qwerty123$",
            "QWERTY123!",
            "Qwerty!$",
            "Qwerty123",
            "Ыerty!123",
        ])
    def test_registration_negative_invalid_password_BUG(self, session, registration_url, invalid_password):
        user = User(fake.email(), "Qwer ty1$")
        body = {
            "username": user.username,
            "password": user.password,
        }
        response = session.post(registration_url, json=body)
        data = response.json()
        print(response.json())
        assert response.status_code == 400
        assert "Must contain at" in data["message"]["password"]


