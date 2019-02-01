from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip

MAX_WAIT = 10


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # 伊迪斯访问首页，不小心提交了一个空待办事项
        # 输入框中没输入内容，她就按下了回车键
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 浏览器截获了请求
        # 清单页面不会加载
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # 她在待办事项中输入了一些文字
        # 错误消失了
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        # 现在能提交了
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1：Buy milk')

        # 她有点调皮，又再次提交了一个空待办事项
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 浏览器这次也不会放行
        self.wait_for_row_in_list_table('1：Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))
        # 输入一些文字之后就能纠正这个错误
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1：Buy milk')
        self.wait_for_row_in_list_table('2：Make tea')

