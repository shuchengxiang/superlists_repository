from django.conf import settings
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session
import time


class MyListsTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # 伊迪斯是已登录用户
        self.create_pre_authenticated_session('edith@example.com')

        # 她访问首页，新建一个清单
        self.browser.get(self.live_server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url

        # 她第一次看到My Lists链接
        self.browser.find_element_by_link_text('My lists').click()

        # 她看到这个页面中有她创建的清单
        # 而且清单根据第一个待办事项命名
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Reticulate splines')
        )
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # 她决定再建一个清单试试
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # 在“My List”页面，在这个新建的清单也显示出来了
        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Click cows')
        )
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # 她退出后，“My Lists”链接不见了
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('My lists'),
            []
        ))