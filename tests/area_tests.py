import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from catproofapi.models import Area

class AreaTests(APITestCase):

    fixtures = ['areas', 'user', 'token']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    # def test_create_area(self):
    #     url = "/areas"

    #     data = {
    #         "label": "Food"
    #     }

    #     response = self.client.post(url, data, format='json')

    #     json_response = json.loads(response.content)

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     self.assertEqual(json_response["label"], "Food")
    #     self.assertEqual(json_response["id"], 5)

    def test_get_area(self):
        area = Area()
        area.label = "Furniture"
        area.save()

        response = self.client.get(f"/areas/{area.id}")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(json_response["label"], "Furniture")
        self.assertEqual(json_response["id"], area.id)
        
    # def test_get_areas(self):
    #     response = self.client.get("/areas")

    #     json_response = json.loads(response.content)

    #     self.assertEqual(response.status_code,status.HTTP_200_OK)

    #     self.assertEqual(json_response[0]["label"], "Furniture")
    #     self.assertEqual(json_response[1]["label"], "Toys")
    #     self.assertEqual(json_response[2]["label"], "Litter-Box")
    #     self.assertEqual(json_response[3]["label"], "Cat Proof")

    

    # def test_delete_area(self):
    #     area = Area()
    #     area.label = "Furniture"
    #     area.save()
        
    #     response = self.client.delete(f"/areas/{area.id}")
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     response = self.client.get(f"/areas/{area.id}")
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)