import json
import time
from datetime import datetime
from bs4 import BeautifulSoup
from cl_crawl import helper
from cl_crawl.helper import request_get

class CrawlDantri:
    baseUrl = 'https://dantri.com.vn'
    url = 'https://dantri.com.vn/api/newest/get-more-newest-article/{sessionId}/{offsetNext}/{offsetPrev}.htm'
    offsetCurrent = 12
    offsetPrev = 12
    isDupArticle = False
    isLastResult = False

    def __init__(self, is_update = False):
        self.is_update = is_update

    def get_page_detail(self, url, params = {}):
        url = self.baseUrl + url
        headers = {}
        response = request_get(url, params, headers)
        if response.status_code // 100 == 2:
            content_html = response.text
            print('content_html', content_html[:100])
            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(content_html, 'html.parser')
            # Find the title element
            publishdate_elem = soup.find('time',  class_='author-time')
            content_detail_elem = soup.find('div', class_='singular-content')
            print('publishdate_elem', publishdate_elem)
            if publishdate_elem:
                publishDate = publishdate_elem.get('datetime')
                publishDate = publishDate.strip()
                print('publishDate', publishDate)
                publishDate = datetime.strptime(publishDate, "%Y-%m-%d %H:%M")
            else:
                publishDate = None

            content_detail = content_detail_elem.get_text() if content_detail_elem else None

            return {
                'date': publishDate,
                'content': content_detail
            }
        else:
            # If unsuccessful, print the status code and reason for failure
            print(f"Request failed with status code {response.status_code}: {response.reason}")
            return {}

    def crawl_html(self, url, params = {}):
        print('crawl_html', url, params)
        response = request_get(url, params)

        if response.status_code // 100 == 2:
            content_html = response.content
            # json parse
            content_json = json.loads(content_html)
            self.offsetCurrent = content_json['offset']
            self.offsetPrev = content_json['offset']
            html = content_json['data']
            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Find the title element and check last result.
            title_elements = soup.select('.article-thumb a')

            if title_elements is None or title_elements is []:
                self.isLastResult = True

            for title_element in title_elements:
                title = title_element.find('img').get('alt')
                link = title_element['href']

                print("Title:", title)
                print("Link:", link)

                data_detail = self.get_page_detail(link, {})
                # print('data_detail', data_detail)
                item = {
                    'domain': self.baseUrl,
                    'title': title,
                    'url': link,
                    'date': data_detail['date'] if 'date' in data_detail else None,
                    'content': data_detail['content'] if 'content' in data_detail else None,
                }
                self.isDupArticle = helper.create_article(item, self.is_update)
        else:
            # If unsuccessful, print the status code and reason for failure
            print(f"Request failed with status code {response.status_code}: {response.reason}")
            return False

    def run(self, is_update = False, sessionId = ''):
        while (True):
            url_crawl = self.url.format(sessionId=sessionId, offsetNext=self.offsetCurrent, offsetPrev=self.offsetPrev)
            print('url_crawl', url_crawl, self.isLastResult)
            self.crawl_html(url_crawl, {})
            if (self.isDupArticle and not is_update) or self.isLastResult:
                break
            # set timeout before next request
            time.sleep(1)

# obj = CrawlDantri()
# obj.run(True, '638421102809130000')