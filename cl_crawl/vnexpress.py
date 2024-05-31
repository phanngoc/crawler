from calendar import c
import re
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import dateparser
import helper as crawl

from DrissionPage import ChromiumOptions, ChromiumPage
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def createChromeDriver():
    try:
        #os.system('rm -rf /tmp/DrissionPage/userData_9222/Default')
        options = ChromiumOptions()
        # options.set_paths('/usr/bin/google-chrome')

        arguments = [
            "-no-first-run",
            "-force-color-profile=srgb",
            "-metrics-recording-only",
            "-password-store=basic",
            "-use-mock-keychain",
            "-export-tagged-pdf",
            "-no-default-browser-check",
            "-disable-background-mode",
            "-enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions",
            "-disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage",
            "-deny-permission-prompts",
            "-disable-gpu",

        ]

        for argument in arguments:
            options.set_argument(argument)

        driver = ChromiumPage(options)

        return driver
    except Exception as e:
        print(f'setup_chromium exception: {str(e)}')

def scroll_and_wait(driver):
    """Scrolls down the page smoothly and waits for data to load."""
    scroll_script = """
        var scroll = document.body.scrollHeight;
        var i = 0;
        function scrollit(i) {
            window.scrollBy({top: scroll, left: 0, behavior: 'smooth'});
            i++;
            if (i < 2) {
                setTimeout(scrollit, 500, i);
            }
        }
        scrollit(i);
    """
    driver.run_js(scroll_script)

def use_soup(driver, selector):
    """Return a BeautifulSoup object of the current page."""
    elem = driver.ele(selector, timeout=2).html
    return BeautifulSoup(elem, 'html.parser')

driver = createChromeDriver()

class VnexpressCrawler():
    base_url = 'https://vnexpress.net'
    page = 1
    daily = False # if exist in database will kill process.

    def __init__(self):
        pass

    def get_response(self, url, params = {}):
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'GET, HEAD, POST, PUT, DELETE, TRACE, OPTIONS, PATCH',
            'Access-Control-Allow-Headers': """X-Real-IP,X-AGENT,Pragma,X-REFERER,X-AUTH-TOKEN,Accept-Encoding,channel,X-XSS-Protection,X-Content-Type-Options,Strict-Transport-Security,Content-Type,Authorization,Accept,Origin,User-Agent,DNT,Cache-Control,X-Mx-ReqToken,Keep-Alive,X-Requested-With,If-Modified-Since,token-id""",
            'Content-Encoding': 'gzip'
        }
        # Make an HTTP GET request to the API endpoint using the requests library
        response = requests.get(url, params=params, headers=headers)
        return response
    
    def get_page_detail(self, url, params = {}):
        if url.startswith(self.base_url) == False:
            url = self.base_url + url

        print('get_page_detail:', url, params)

        driver.get(url, timeout=2)
        driver.wait.load_start()
        scroll_and_wait(driver)
        time.sleep(2)

        publishdate_elem =  use_soup(driver, "xpath://div[@class='header-content width_common']//span[@class='date']")
        if publishdate_elem:
            publishDate = publishdate_elem.text
            publishDate = publishDate.strip()
            publishDate = dateparser.parse(publishDate)
        else:
            publishDate = None

        content_detail_elem = use_soup(driver, "xpath://article[@class='fck_detail ']")

        content_detail = ''
        if content_detail_elem:
            content_detail = content_detail_elem.text

        driver.wait.ele_displayed('xpath://div[@class="box-category__list-news"]')
        soup = use_soup(driver, 'xpath://div[@class="box-category__list-news"]')
        tagsElem = soup.select('h4.item-tag > a')
        print('tagsElems', tagsElem)
        # Extract the text and href from each tag
        tags_data = []
        for tag in tagsElem:
            tag_text = tag.get_text(strip=True)
            tags_data.append(tag_text)
            print(f'Tag: {tag_text}')

        return {
            'date': publishDate,
            'content': content_detail,
            'tags_data': tags_data
        }

    def crawl_html(self, url, params = {}):
        print('start:crawl_html:', url, params)
        response = self.get_response(url, params)
        if response.status_code // 100 == 2:
            content_html = response.content

            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(content_html, 'html.parser')

            # Find the title element
            title_elements = soup.select('.title-news a')
            if title_elements is None or len(title_elements) == 0:
                return False

            for title_element in title_elements:
                title = title_element.get_text()
                link = title_element['href']

                print("Title:", title)
                print("Link:", link)
                try:
                    data_detail = self.get_page_detail(link, {})
                    item = {
                        'domain': 'https://vnexpress.net/kinh-doanh',
                        'title': title,
                        'url': link,
                        'date': data_detail['date'] if 'date' in data_detail else None,
                        'content': data_detail['content'] if 'content' in data_detail else None,
                        'data': {
                            'tags': data_detail['tags_data'] if 'tags_data' in data_detail else None,
                        },
                    }

                    if self.daily:
                        # print('daily:', item)
                        crawl.create_article(item)
                    else:
                        crawl.create_article(item, True)
                except Exception as e:
                    print('error:', e)
        else:
            # If unsuccessful, print the status code and reason for failure
            print(f"Request failed with status code {response.status_code}: {response.reason}")
            return False

    def run(self, page = {"from": None, "to": None}, daily = False):
        self.daily = daily
        page_from = 1 if page['from'] is None else page['from']
        page_to = -1 if page['to'] is None else page['to']
        while (True):
            isSuccess = self.crawl_html('https://vnexpress.net/kinh-doanh-p' + str(page_from), {})
            # break
            if isSuccess == False or page_to == page_from:
                break
            page_from += 1


VnexpressCrawler().run(daily=True)
