from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage


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
        self.browser = oni_browser
        self.create_pre_authenticated_session('oniciferous@example.com')

        # 伊迪斯访问首页，新建一个清单
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Get help')

        # 她看到“分享这个清单”选项
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )

        # 她分享自己的清单之后，页面更新了
        # 提示已经分享给Oniciferous
        list_page.share_list_with('oniciferous@example.com')

        # 现在Oniciferous在他的浏览器中访问清单页面
        self.browser = oni_browser
        MyListsPage(self).go_to_my_lists_page()

        # 他看到了伊迪斯分享的清单
        self.browser.find_element_by_link_text('Get help').click()

        # 在清单页面，Oniciferous看到这个清单属于伊迪斯
        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(),
            'edith@example.com'
        ))

        # 他在这个清单中添加一个待办事项
        list_page.add_list_item('Hi Edith!')

        # 伊迪斯刷新页面后，看到Oniciferous添加的内容
        self.browser = edith_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Hi Edith!', 2)
