import pytest
from rest_framework import APIClient

client = APIClient()

@pytest.mark.django_db
def test_create_collection():
    payload = {
        'title' : 'Test',
        'description' : 'Test'
        
    }
