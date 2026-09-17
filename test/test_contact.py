from dataclasses import asdict
from faker import Faker
import random
import pytest
from config import *
fake = Faker()

class TestContacts:

    @pytest.mark.smoke
    def test_add_contact_positive(self, session, add_contact_url, auth_headers, random_contact):
        response = session.post(
            add_contact_url,
            headers=auth_headers,
            json=asdict(random_contact)
        )
        print(response.json()["message"])
        assert response.status_code == 200
        assert "Contact was added" in response.json()["message"]

    @pytest.mark.smoke
    def test_get_all_contacts_positive(self, session, add_contact_url, auth_headers):
        response = session.get(
            add_contact_url,
            headers=auth_headers
        )
        print(response.json())
        assert response.status_code == 200
        assert isinstance(response.json()["contacts"], list)

    def test_get_all_contacts_negative_wrong_token(self, session, add_contact_url, auth_headers):
        headers = {"Authorization": "Lorem ipsum dolor sit amet"}
        response = session.get(
            add_contact_url,
            headers=headers
        )
        print(response.json())
        assert response.status_code == 401
        assert response.json()["error"] == "Unauthorized"

    @pytest.mark.smoke
    def test_update_contact_positive(self, session, add_contact_url, auth_headers, create_contact):
        contact_id = create_contact
        print(">>> Contact ID:", contact_id)
        res1 = session.get(add_contact_url, headers=auth_headers)
        print(">>> This is Contac BEFOR UPDATE: ", res1.json())

        updated_contact = {
            "id": contact_id,
            "name": fake.name(),
            "lastName": fake.last_name(),
            "email": fake.email(),
            "phone": "0172365517778",
            "address": "address_Lorem",
            "description": "text",
        }

        response = session.put(add_contact_url, headers=auth_headers, json=updated_contact)
        print(">>> This is MESSAGE of UPDATE: ", response.json())

        assert response.status_code == 200
        assert "Contact was updated" in response.json()["message"]

        res = session.get(add_contact_url, headers=auth_headers)
        print(">>> Here are ONLY HEADERS AFTER UpDate: ", res.json())
        assert res.json()["contacts"][0]["address"] == "address_Lorem"
        assert res.json()["contacts"][0]["phone"] == "0172365517778"

    # 2. Variante, um ein Feld zu verändern:
    @pytest.mark.smoke
    def test_update_contact_one_field_positive(self, session, add_contact_url, auth_headers, create_contact):

        contact_id = create_contact

        res1 = session.get(add_contact_url, headers=auth_headers).json()["contacts"][0]
        print(">>> ПЕРВЫЙ запрос GET: ", res1)
        res1["name"] = "Robert" #veränderten nur den Namen

        response = session.put(add_contact_url, headers=auth_headers, json=res1)
        print(">>> UPDATE: ПОДТВЕРЖДЕНИЕ, сообщение: ", response.json())

        assert response.status_code == 200
        assert "Contact was updated" in response.json()["message"]
        assert res1["name"] == "Robert"

        res = session.get(add_contact_url, headers=auth_headers)
        print(">>> ПОСЛЕ UPDATE, сам файл JSON: ", res.json())

    @pytest.mark.smoke
    def test_update_contact_one_field_second_positive(self, session, add_contact_url, auth_headers, create_contact_return_contact):
        contact = create_contact_return_contact
        print(">> CONTACT: ", contact)

        # Adresse ändern:
        contact["address"] = "New Address"
        response = session.put(add_contact_url, headers=auth_headers, json=contact)
        print(">> ONLY MESSAGE" , response.json())
        print(">> ПОСЛЕ UPDATE: ", contact)

        assert response.status_code == 200
        assert "Contact was updated" in response.json()["message"]

    @pytest.mark.smoke
    def test_delete_contact_positive(self, session, add_contact_url, auth_headers, create_contact):
        contact_id = create_contact
        response = session.delete(f"{add_contact_url}/{contact_id}", headers=auth_headers)
        print(">> ONLY MESSAGE" , response.json())
        assert response.status_code == 200
        assert "Contact was deleted" in response.json()["message"]




