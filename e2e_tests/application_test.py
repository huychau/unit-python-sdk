import os
import unittest
from datetime import timedelta
from unit import Unit
from unit.models.application import *

token = os.environ.get('TOKEN')
client = Unit("https://api.s.unit.sh", token)

def create_individual_application():
    request = CreateIndividualApplicationRequest(
        FullName("Jhon", "Doe"), date.today() - timedelta(days=20*365),
        Address("1600 Pennsylvania Avenue Northwest", "Washington", "CA", "20500", "US"), "jone.doe1@unit-finance.com",
        Phone("1", "2025550108"),
        ssn="000000003",
        device_fingerprints=[device_fingerprint]
    )

    return client.applications.create(request)

def test_create_individual_application():
    app = create_individual_application()
    assert app.data.type == "individualApplication"

def test_create_business_application():
    request = CreateBusinessApplicationRequest(
        name="Acme Inc.",
        address=Address("1600 Pennsylvania Avenue Northwest", "Washington", "CA", "20500", "US"),
        phone=Phone("1", "9294723497"), state_of_incorporation="CA", entity_type="Corporation", ein="123456789",
        officer=Officer(full_name=FullName("Jone", "Doe"), date_of_birth=date.today() - timedelta(days=20 * 365),
                           address=Address("950 Allerton Street", "Redwood City", "CA", "94063", "US"),
                           phone=Phone("1", "2025550108"), email="jone.doe@unit-finance.com", ssn="000000005"),
        contact=BusinessContact(full_name=FullName("Jone", "Doe"), email="jone.doe@unit-finance.com", phone=Phone("1", "2025550108")),
        beneficial_owners=[
            BeneficialOwner(
                FullName("James", "Smith"), date.today() - timedelta(days=20*365),
                Address("650 Allerton Street","Redwood City","CA","94063","US"),
                Phone("1","2025550127"),"james@unit-finance.com",ssn="574567625"),
              BeneficialOwner(FullName("Richard","Hendricks"), date.today() - timedelta(days=20 * 365),
              Address("470 Allerton Street", "Redwood City", "CA", "94063", "US"),
              Phone("1", "2025550158"), "richard@unit-finance.com", ssn="574572795")
        ]
    )

    response = client.applications.create(request)
    assert response.data.type == "businessApplication"

def test_list_and_get_applications():
    response = client.applications.list()
    for app in response.data:
        assert app.type == "businessApplication" or app.type == "individualApplication"
        res = client.applications.get(app.id)
        assert res.data.type == "businessApplication" or res.data.type == "individualApplication"

