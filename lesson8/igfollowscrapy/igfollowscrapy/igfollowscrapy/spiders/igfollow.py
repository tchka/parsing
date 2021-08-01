import json
import re
from urllib.parse import quote

import scrapy
from igfollowscrapy.items import IgfollowscrapyItem
from scrapy.http import HtmlResponse


class IgfollowSpider(scrapy.Spider):
    name = 'igfollow'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']

    login_url = "https://www.instagram.com/accounts/login/ajax/"
    user_to_parse_url_template = "/%s"
    followers_url = "https://i.instagram.com/api/v1/friendships/\
    13706859777/followers/?"
    followers_query_hash = "ed2e3ff5ae8b96717476b62ef06ed8cc"

    def __init__(self, login, password, users_to_parse, **kwargs):
        super().__init__(**kwargs)
        self.login = login
        self.enc_password = password
        self.user_to_parse = users_to_parse.split(' ')

    def parse(self, response: HtmlResponse, **kwargs):
        token = self.fetch_csrf_token(response.text)
        x_instagram_ajax = self.fetch_x_instagram_ajax(response.text)
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
                "x-ig-app-id": "936619743392459",
                "x-instagram-ajax": x_instagram_ajax,
            },
        )

    def user_login(self, response: HtmlResponse):
        data = response.json()  # {'user': True, 'userId': '10248438429',
        # 'authenticated': True, 'oneTapPrompt': True, 'status': 'ok'}
        if data['authenticated']:
            for user in self.user_to_parse:
                user = user.strip()
                yield response.follow(
                    self.user_to_parse_url_template % user,
                    callback=self.parse_followers,
                    cb_kwargs={"username": user},
                )

        print('42')
        print()

    def parse_followers(self, response: HtmlResponse, username: str):
        user_id = self.fetch_user_id(response.text, username)
        basic_url = "https://i.instagram.com/api/v1/friendships\
        /%s/followers/?count=12"
        basic_url = basic_url % user_id
        url = basic_url + "&search_surface=follow_list_page"
        yield response.follow(
            url,
            callback=self.follower_data_parse,
            cb_kwargs={
                "status": "follower",
                "username": username,
                "user_id": user_id,
                "basic_url": basic_url,
                "page_number": 0,
            },
            headers={
                "x-ig-app-id": "936619743392459",
            },
        )

    def parse_following(self, response: HtmlResponse, username: str):
        user_id = self.fetch_user_id(response.text, username)
        basic_url = "https://i.instagram.com/api/v1/friendships\
        /%s/following/?count=12"
        basic_url = basic_url % user_id
        yield response.follow(
            basic_url,
            callback=self.follower_data_parse,
            cb_kwargs={
                "status": "following",
                "username": username,
                "user_id": user_id,
                "basic_url": basic_url,
                "page_number": 0,
            },
            headers={
                "x-ig-app-id": "936619743392459",
            },
        )

    def follower_data_parse(
            self, response: HtmlResponse, status,
            username, user_id, basic_url, page_number
    ):
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print("Json decode error")
            print(e)
            return
        except Exception as e:
            print(e)
            return

        print('get followers')
        print()
        try:
            users = data["users"]
        except AttributeError as e:
            print("Error during getting users")
            print(e)
            return
        except KeyError as e:
            print("Error during getting users")
            print(e)
            return

        for follow_user in users:

            try:
                follow_user_avatar = follow_user["profile_pic_url"]
            except AttributeError as e:
                print("Error during getting follower user profile_pic_url")
                print(e)
                return
            except KeyError as e:
                print("Error during getting follower user profile_pic_url")
                print(e)

            item = IgfollowscrapyItem()
            item["status"] = status
            item["username"] = username
            item["follow_user_id"] = follow_user["pk"]
            item["follow_username"] = follow_user["username"]
            item["follow_user_avatar_url"] = follow_user_avatar
            # print(item)
            yield item

        try:
            big_list = data["big_list"]
        except AttributeError as e:
            print("Error getting big_list")
            print(e)
            return
        except KeyError as e:
            print("Error getting big_list")
            print(e)
            return

        if status == "follower":
            if big_list:
                page_number += 1
                max_id = 12 * page_number
                url = basic_url + "&max_id=" + str(max_id) + \
                    "&search_surface=follow_list_page"
                yield response.follow(
                    url,
                    callback=self.follower_data_parse,
                    cb_kwargs={
                        "status": status,
                        "username": username,
                        "user_id": user_id,
                        "basic_url": basic_url,
                        "page_number": page_number,

                    },
                    headers={
                        "x-ig-app-id": "936619743392459",
                    },
                )
            else:
                basic_url = "https://i.instagram.com/api/v1\
                /friendships/%s/following/?count=12"
                basic_url = basic_url % user_id
                yield response.follow(
                    basic_url,
                    callback=self.follower_data_parse,
                    cb_kwargs={
                        "status": "following",
                        "username": username,
                        "user_id": user_id,
                        "basic_url": basic_url,
                        "page_number": 0,
                    },
                    headers={
                        "x-ig-app-id": "936619743392459",
                    },
                )
        else:
            if big_list:
                page_number += 1
                max_id = 12 * page_number
                url = basic_url + "&max_id=" + str(max_id)
                yield response.follow(
                    url,
                    callback=self.follower_data_parse,
                    cb_kwargs={
                        "status": status,
                        "username": username,
                        "user_id": user_id,
                        "basic_url": basic_url,
                        "page_number": page_number,
                    },
                    headers={
                        "x-ig-app-id": "936619743392459",
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
        str_variables = quote(str(variables).replace(" ", "")
                              .replace("'", '"'))
        return str_variables

    def fetch_x_instagram_ajax(self, text):
        matched = re.search('"rollout_hash":"\\w+"', text).group()
        return matched.split(":").pop().replace(r'"', "")
