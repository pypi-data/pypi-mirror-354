import requests
import base64
import json
from django.conf import settings
from django.http import HttpRequest
from nkunyim_util import Encryption


class HttpClient:

    def __init__(self, req: HttpRequest, name:str) -> None:
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            base_url = settings.SERVICES_CONFIG[name.upper()]
            user_data = None
            if req.user.is_authenticated:
                user_data = {
                    "id": str(req.user.id),
                    "username": req.user.username,
                    "nickname": req.user.nickname,
                    "phone_number": req.user.phone_number,
                    "email_address": req.user.email_address,
                    "photo_url": req.user.photo_url,
                    "is_active": req.user.is_active,
                    "is_admin": req.user.is_admin
                }
                if req.user.is_superuser:
                    user_data['is_superuser'] = req.user.is_superuser
            
            if user_data and 'id' in user_data:
                
                plain_text = json.dumps(user_data)
                
                encryption = Encryption()
                cipher_text = encryption.rsa_encrypt(plain_text=plain_text, name=name)
                
                access_token = base64.b64encode(cipher_text)
                headers['Authorization'] = f"JWT {access_token}"
                
        except KeyError as e:
            raise Exception(f"The service configuration variable {name.upper()} has not defined. Error detail: {str(e)}")

        except Exception as ex:
            raise Exception(f"Exception error occured when initializing the HttpClient. Error detail: {str(ex)}")
        
        self.base_url = base_url
        self.headers = headers


    def post(self, path: str, data: dict) -> requests.Response:
        url = self.base_url + path
        return requests.post(url=url, data=data, headers=self.headers)


    def get(self, path: str) -> requests.Response:
        url = self.base_url + path
        return requests.get(url=url, headers=self.headers)


    def put(self, path: str, data: dict) -> requests.Response:
        url = self.base_url + path
        return requests.put(url=url, data=data, headers=self.headers)


    def delete(self, path: str) -> requests.Response:
        url = self.base_url + path
        return requests.delete(url=url, headers=self.headers)