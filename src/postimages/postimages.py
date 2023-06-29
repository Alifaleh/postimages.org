import requests
from bs4 import BeautifulSoup
import urllib.parse
import random
import string
import magic
import os
import json
from src.postimages.headers import PostImagesHeader
from src.postimages.routes import PostImageRoute



class PostImages:
    def __init__(self, email : str, password : str, cookies : str = None) -> None:
        self.email = email
        self.password = password
        self.cookies = cookies
        self.working_gallery = False


    def _form_data(self, data_dict : dict) -> str:
        data = ""
        data_keys = data_dict.keys()
        length = len(data_keys)
        for index, item in enumerate(data_keys):
            data += f"{item}={urllib.parse.quote(data_dict[item])}"
            if not index == length - 1:
                data += '&'
        return data

    def _get_csrf(self) -> str:
        login_page_response = requests.get(PostImageRoute.login_page, headers=PostImagesHeader.login_page)
        soup = BeautifulSoup(login_page_response.text, "lxml")
        self.csrf = soup.find('input', {'name': 'csrf_hash'}).get('value')
        return self.csrf

    def is_loged_in(self):
        if self.session_key:
            return True
        return False

    def login(self) -> dict:
        self._get_csrf()
        data = self._form_data({
                'csrf_hash': self.csrf,
                'email': self.email,
                'password': self.password,
            })
        login_post_response = requests.post(PostImageRoute.login_page, headers=PostImagesHeader.login_post, data=data, allow_redirects=False)
        self.cookies = login_post_response.cookies.get_dict()
        valid_token_response = requests.get(login_post_response.headers['Location'], cookies=self.cookies, headers=PostImagesHeader.token_validator, allow_redirects=False)
        self.cookies = valid_token_response.cookies.get_dict()
        return self.cookies


    def get_galleries(self):
        galleries_response = requests.get(PostImageRoute.galleries, cookies=self.cookies, headers=PostImagesHeader.galleries)
        soup = BeautifulSoup(galleries_response.text, "lxml")
        galleries = list(map(lambda element: 
            {
                'name': element.find('h3').get('data-name'),
                'hex': element.find('h3').get('data-hex'),
                'gallery_url': element.find('a').get('href'),
            },
            soup.find_all('div', {'class': 'gallery-container'})
        ))
        return galleries
        
    def get_gallery_by_name(self, gallery_name: str) -> str:
        for gallery in self.get_galleries():
            if gallery.get('name') == gallery_name:
                return gallery
        return False

    def set_gallery_upload_token(self, working_gallery: dict) -> None:
        gallery_upload_token_response = requests.get(f"{PostImageRoute.gallery_token}/{working_gallery.get('hex')}", cookies=self.cookies, headers=PostImagesHeader.galleries)
        self.upload_token = gallery_upload_token_response.text.split('"token","')[1].split('");')[0]

    def set_working_gallery(self, gallery_name: str) -> None:
        self.working_gallery = self.get_gallery_by_name(gallery_name)
        self.set_gallery_upload_token(self.working_gallery)

    def get_current_working_gallery(self) -> dict:
        return self.working_gallery
    
    def get_upload_session(self) -> str:
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(32))

    def _form_post_data_item(self, item: dict) -> str:
        item_data = '\n------WebKitFormBoundaryODC9AjEhJ0drDGS4\n'
        for item_key in item:
            if item_key == 'Content-Disposition':
                item_data += f'{item_key}: {item[item_key]}; '
            elif item_key == 'value':
                item_data += f'\n\n{item[item_key]}'
            elif item_key == 'Content-Type':
                item_data += f'\n{item_key}: {item[item_key]}'
            else:
                item_data += f'{item_key}="{item[item_key]}"; '
        return item_data

    def _form_post_data(self, data: list) -> str:
        post_data = ''.join(
            list(map(
                lambda item: self._form_post_data_item(item),
                data,
            ))
        )
        post_data += '\n------WebKitFormBoundaryODC9AjEhJ0drDGS4--\n'
        return post_data[1:]


    def _get_image_urls(self, url: str) -> dict:
        urls_response = requests.get(url, cookies=self.cookies, headers = PostImagesHeader.token_validator)
        soup = BeautifulSoup(urls_response.text, "lxml")
        links = {'_'.join(el.find('input').get('id').split('_')[1:]): el.find('input').get('value') for el in soup.find_all('div', {'class': 'input-group'})}
        return links


    def upload_image(self, image_path: str, optimize:bool = False) -> dict:
        img_data = open(image_path, 'rb',).read().decode("latin1")
        file_content_type = magic.from_file(image_path, mime=True)
        file_name = os.path.basename(image_path)
        data = self._form_post_data([
            {
                'Content-Disposition': 'form-data',
                'name': 'token',
                'value': self.upload_token,
            },
            {
                'Content-Disposition': 'form-data',
                'name': 'upload_session',
                'value': self.get_upload_session(),
            },
            {
                'Content-Disposition': 'form-data',
                'name': 'numfiles',
                'value': '1',
            },
            {
                'Content-Disposition': 'form-data',
                'name': 'optsize',
                'value': '1' if optimize else '0',
            },
            {
                'Content-Disposition': 'form-data',
                'name': 'gallery',
                'value': self.get_current_working_gallery().get('hex'),
            },
            {
                'Content-Disposition': 'form-data',
                'name': 'expire',
                'value': '0',
            },
            {
                'Content-Disposition': 'form-data',
                'name': 'file',
                'filename': file_name,
                'Content-Type': file_content_type,
                'value': f'{img_data}',
            },
        ])
        upload_response = requests.post(PostImageRoute.upload_image, cookies=self.cookies, headers=PostImagesHeader.upload_image, data=data)
        res_json = json.loads(upload_response.text)
        if res_json['status'] == 'OK':
            return self._get_image_urls(res_json['url'])
        else:
            return False


