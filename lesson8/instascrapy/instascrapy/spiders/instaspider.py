import copy
import json
import re
from urllib.parse import quote

import scrapy
from instascrapy.items import InstascrapyItem
from scrapy.http import HtmlResponse


class InstaspiderSpider(scrapy.Spider):
    name = 'instaspider'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']

    login_url = "https://www.instagram.com/accounts/login/ajax/"
    user_to_parse_url_template = "/%s"
    post_getting_url = "/graphql/query/?query_hash=%s&variables=%s"
    post_query_hash = "8c2a529969ee035a5063f2fc8602a0fd"

    def __init__(self, login, password, users_to_parse, **kwargs):
        super().__init__(**kwargs)
        self.login = login
        self.enc_password = password
        self.user_to_parse = users_to_parse

    def parse(self, response: HtmlResponse, **kwargs):
        token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.login_url,
            method="POST",
            callback=self.user_login,
            formdata={
                "username": self.login,
                "enc_password": self.enc_password,
            },
            headers={
                "X-CSRFToken": token,
            },
        )

    def user_login(self, response: HtmlResponse):
        data = response.json()  # {'user': True, 'userId': '10248438429',
        # 'authenticated': True, 'oneTapPrompt': True, 'status': 'ok'}
        if data['authenticated']:
            yield response.follow(
                self.user_to_parse_url_template % self.user_to_parse,
                callback=self.user_data_parse,
                cb_kwargs={"username": self.user_to_parse},
            )
        print('42')
        print()

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {
            "id": user_id,
            "first": 12,
        }
        str_variables = self.make_str_variables(variables)
        url = self.post_getting_url % (self.post_query_hash, str_variables)
        print("TO POSTS!")
        print()
        yield response.follow(
            url,
            callback=self.post_parse,
            cb_kwargs={
                # глубокое копирование
                "variables": copy.deepcopy(variables),
                "username": username,
            },
        )

    def post_parse(self, response: HtmlResponse, variables, username):
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print("Json decode error")
            print(e)
            return
        except Exception as e:
            print(e)
            return

        try:
            data = data["data"]["user"]["edge_owner_to_timeline_media"]
        except AttributeError as e:
            print("Error during getting edge_owner_to_timeline_media")
            print(e)
            return
        except KeyError as e:
            print("Error during getting edge_owner_to_timeline_media")
            print(e)
            return

        try:
            edges = data["edges"]
        except AttributeError as e:
            print("Error during getting page_info")
            print(e)
            return
        except KeyError as e:
            print("Error during getting page_info")
            print(e)
            return

        for edge in edges:
            node = edge["node"]
            item = InstascrapyItem()
            item["id"] = node["id"]
            item["user_id"] = variables["id"]
            item["username"] = username
            item["image_url"] = node["display_url"]
            item["likes"] = node["edge_media_preview_like"]["count"]
            item["metadata"] = node
            yield item

        try:
            page_info = data["page_info"]
        except AttributeError as e:
            print("Error during getting page_info")
            print(e)
            return
        except KeyError as e:
            print("Error during getting page_info")
            print(e)
            return

        if page_info["has_next_page"]:
            variables["after"] = page_info["end_cursor"]
            str_variables = self.make_str_variables(variables)
            url = self.post_getting_url % (self.post_query_hash, str_variables)
            yield response.follow(
                url,
                callback=self.post_parse,
                cb_kwargs={
                    # глубокое копирование
                    "variables": copy.deepcopy(variables),
                    "username": username,
                },
            )

    def fetch_csrf_token(self, text):
        matched = re.search('"csrf_token":"\\w+"', text).group()
        return matched.split(":").pop().replace(r'"', "")

    def fetch_user_id(self, text, username):
        matched = re.search('{"id":"\\d+","username":"%s"}'
                            % username, text).group()
        return json.loads(matched).get("id")

    def make_str_variables(self, variables):
        str_variables = quote(
            str(variables).replace(" ", "").replace("'", '"'))
        return str_variables
