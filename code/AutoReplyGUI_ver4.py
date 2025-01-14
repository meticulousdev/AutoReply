import sys
from PyQt5.QtWidgets import *

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import pyperclip
import time
from bs4 import BeautifulSoup


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # START and CONTINUE Button
        self.time_edit: QLineEdit = QLineEdit(self)
        self.time_edit.move(180, 50)

        time_label: QLabel = QLabel('TIME:', self)
        time_label.move(120, 55)

        # START and CONTINUE Button
        self.start_button: QPushButton = QPushButton('START', self)
        self.start_button.move(100, 100)
        self.continue_button: QPushButton = QPushButton('CONTINUE', self)
        self.continue_button.move(300, 100)

        self.setWindowTitle('Auto Reply')
        self.setGeometry(500, 500, 500, 200)
        self.center()
        self.show()

        # START button clicked
        self.start_button.clicked.connect(self.start_edge_browser)
        self.continue_button.clicked.connect(self.auto_reply)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start_edge_browser(self):
        self.driver = webdriver.Edge("msedgedriver.exe")

        url = "https://www.naver.com/"
        self.driver .get(url)

        login_big_button_xpath = '//a[@class="link_login"]'
        login_big_button = self.driver .find_element_by_xpath(login_big_button_xpath)
        login_big_button.click()

    def auto_reply(self):
        try:
            self.driver.get("https://cafe.naver.com/campingkan")
            time.sleep(0.5)
            self.driver.get("https://cafe.naver.com/ArticleList.nhn?search.clubid=29118241&search.boardtype=L")
            time.sleep(0.5)

            self.driver.switch_to.frame('cafe_main')

            article_num = 21
            article_time_table = self.driver.find_elements_by_css_selector('td.td_date')
            article_time = article_time_table[article_num]
            test = 0

            while test == 0:
                if article_time.text >= self.time_edit.text():
                    article_list = self.driver.find_elements_by_css_selector('div.inner_list > a.article')
                    article_urls = [article.get_attribute('href') for article in article_list]

                    self.driver.get(article_urls[article_num])
                    time.sleep(0.15)

                    idx = 0
                    iframes = self.driver.find_elements_by_tag_name('iframe')
                    for i, iframe in enumerate(iframes):
                        try:
                            print('%d번째 iframe 입니다.' % i)
                            self.driver.switch_to.frame(iframes[i])
                            print(self.driver.page_source)

                            if len(self.driver.page_source) > 100:
                                print(len(self.driver.page_source))
                                idx = i

                            # 원래 frame으로 돌아옵니다.
                            self.driver.switch_to.default_content()
                        except:
                            # exception이 발생했다면 원래 frame으로 돌아옵니다.
                            self.driver.switch_to.default_content()

                            # 몇 번째 frame에서 에러가 났었는지 확인합니다.
                            print('pass by except : iframes[%d]' % i)

                            # 다음 for문으로 넘어갑니다.
                        pass

                    self.driver.switch_to.frame(iframes[idx])
                    reply_area = self.driver.find_elements_by_css_selector('textarea')[0]
                    reply_area.send_keys("8")

                    reply_button = self.driver.find_elements_by_class_name('btn_register')[0]
                    reply_button.click()

                    test = 1
                else:
                    self.driver.get(self.driver.current_url)
                    time.sleep(0.05)

                    self.driver.switch_to.frame('cafe_main')
                    article_time_table = self.driver.find_elements_by_css_selector('td.td_date')
                    article_time = article_time_table[article_num]

                    print(article_time.text, self.time_edit.text())
                    print(article_time.text >= self.time_edit.text())
                    print()

        except:
            self.driver.quit()

        # driver.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
