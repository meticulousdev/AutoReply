import sys
from PyQt5.QtWidgets import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
import time


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # ID and PASSWORD
        self.id_edit: QLineEdit = QLineEdit(self)
        self.id_edit.move(80, 20)
        self.pw_edit: QLineEdit = QLineEdit(self)
        self.pw_edit.move(80, 60)
        self.reply_edit: QLineEdit = QLineEdit(self)
        self.reply_edit.move(80, 100)

        id_label: QLabel = QLabel('ID:', self)
        id_label.move(20, 20)
        pw_label: QLabel = QLabel('PW:', self)
        pw_label.move(20, 60)
        reply_label: QLabel = QLabel('RE:', self)
        reply_label.move(20, 100)

        # START and CONTINUE Button
        self.start_button: QPushButton = QPushButton('START', self)
        self.start_button.move(300, 30)
        self.continue_button: QPushButton = QPushButton('CONTINUE', self)
        self.continue_button.move(300, 80)

        self.setWindowTitle('Auto Reply')
        self.setGeometry(500, 500, 500, 200)
        self.center()
        self.show()

        # START button clicked
        self.start_button.clicked.connect(self.auto_reply)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def auto_reply(self):
        driver = webdriver.Edge("msedgedriver.exe")

        url = "https://www.naver.com/"
        driver.get(url)

        try:
            login_big_button_xpath = '//a[@class="link_login"]'
            login_big_button = driver.find_element_by_xpath(login_big_button_xpath)
            login_big_button.click()

            id_xpath = '//input[@id="id"]'
            pw_xpath = '//input[@id="pw"]'
            id_section = driver.find_element_by_xpath(id_xpath)
            pw_section = driver.find_element_by_xpath(pw_xpath)

            my_id = self.id_edit.text()
            my_pw = self.pw_edit.text()

            id_section.click()
            pyperclip.copy(my_id)
            id_section.send_keys(Keys.CONTROL, 'v')
            time.sleep(0.5)

            pw_section.click()
            pyperclip.copy(my_pw)
            pw_section.send_keys(Keys.CONTROL, 'v')
            time.sleep(0.5)

            login_button = driver.find_element_by_class_name("btn_global")
            login_button.click()

            driver.get("{link}")
            time.sleep(0.5)
            driver.get("{link}")
            time.sleep(0.5)

            driver.switch_to.frame('cafe_main')
            article_list = driver.find_elements_by_css_selector('div.inner_list > a.article')
            article_urls = [article.get_attribute('href') for article in article_list]

            driver.get(article_urls[11])
            time.sleep(0.5)

            idx = 0
            iframes = driver.find_elements_by_tag_name('iframe')
            for i, iframe in enumerate(iframes):
                try:
                    print('%d번째 iframe 입니다.' % i)
                    driver.switch_to.frame(iframes[i])
                    print(driver.page_source)

                    if len(driver.page_source) > 100:
                        print(len(driver.page_source))
                        idx = i

                    # 원래 frame으로 돌아옵니다.
                    driver.switch_to.default_content()
                except:
                    # exception이 발생했다면 원래 frame으로 돌아옵니다.
                    driver.switch_to.default_content()

                    # 몇 번째 frame에서 에러가 났었는지 확인합니다.
                    print('pass by except : iframes[%d]' % i)

                    # 다음 for문으로 넘어갑니다.
                pass

            driver.switch_to.frame(iframes[idx])
            reply_area = driver.find_elements_by_css_selector('textarea')[0]
            reply_area.send_keys(self.reply_edit.text())

            reply_button = driver.find_elements_by_class_name('btn_register')[0]
            reply_button.click()

        except:
            driver.quit()

        # driver.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
