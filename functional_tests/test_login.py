from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
import time
import os
import imaplib

from .base import FunctionalTest

# TEST_EMAIL = 'shuchengxiang@dongao.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # 伊迪斯访问这个很棒的超级列表网站
        # 第一次注意到导航栏中有“登录”区域
        # 看到要求输入电子邮件地址，她便输入了
        if self.staging_server:
            test_email = 'shuchengxiang@dongao.com'
        else:
            test_email = 'shuchengxiang@dongao.com'
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # 出现一条消息，告诉她邮件已经发出
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # 她查看邮件，看到一条消息
        body = self.wait_for_email(test_email, SUBJECT)

        # 邮件中有个URL链接
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # 她点击了链接
        self.browser.get(url)

        # 她登录了！
        self.wait_to_be_logged_in(email=test_email)

        # 现在她要退出
        self.browser.find_element_by_link_text('Log out').click()

        # 她退出了
        self.wait_to_be_logged_out(email=test_email)

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertIn(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = imaplib.IMAP4_SSL('mail.dongao.com')
        try:
            username = test_email
            password = os.environ.get('DONGAO_PASSWORD')
            inbox.login(username, password)
            while time.time() - start < 60:
                # 获取最新的10封邮件
                inbox.select()
                typ, data = inbox.search(None, 'ALL')
                for num in data[0].split()[-1:]:
                    typ, lines = inbox.fetch(num, '(RFC822)')
                    if f'Subject: {subject}' in lines[0][1].decode('utf-8'):
                        email_id = num
                        body = ''.join(lines[0][1].decode('utf-8'))
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.store(email_id, '+FLAGS', '\\Deleted')
                inbox.expunge()
            inbox.close()
            inbox.logout()
