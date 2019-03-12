from selenium import webdriver
from .base import FunctionalTest


def quit_if_possible(browser):
    try: browser.quit()
    except: pass


class SharingTest(FunctionalTest):

    def test_can_share_a_list_with_another_user(self):
        # 伊迪斯是已登录用户
        self.create_pre_authenticated_session('edith@example.com')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # 她的朋友Oniciferous也在使用这个清单网站
        oni_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.create_pre_authenticated_session('oniciferous@example.com')

        # 伊迪斯访问首页，新建一个清单
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        self.add_list_item('Get help')

        # 她看到“分享这个清单”选项
        share_box = self.browser.find_element_by_css_selector(
            'input[name="sharee"]'
        )
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )