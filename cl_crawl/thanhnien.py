import requests
from bs4 import BeautifulSoup
import dateparser
from cl_crawl import helper

class CrawlThanhNien:
    base_url = 'https://thanhnien.vn'
    page = 1
    daily = False # if exist in database will kill process.

    def __init__(self):
        pass

    def get_response(self, url, params = {}):
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'GET, HEAD, POST, PUT, DELETE, TRACE, OPTIONS, PATCH',
            'Access-Control-Allow-Headers': 'X-Real-IP,X-AGENT,Pragma,X-REFERER,X-AUTH-TOKEN,Accept-Encoding,channel,X-XSS-Protection,X-Content-Type-Options,Strict-Transport-Security,Content-Type,Authorization,Accept,Origin,User-Agent,DNT,Cache-Control,X-Mx-ReqToken,Keep-Alive,X-Requested-With,If-Modified-Since,token-id',
            'Content-Encoding': 'gzip'
        }
        # Make an HTTP GET request to the API endpoint using the requests library
        response = requests.get(url, params=params, headers=headers)
        return response
    
    def get_page_detail(self, url, params = {}):
        url = self.base_url + url
        print('get_page_detail', url, params)
        response = self.get_response(url, params)
        if response.status_code // 100 == 2:
            content_html = response.content
            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(content_html, 'html.parser')
            # Find the title element
            publishdate_elem = soup.find('div', attrs={'data-role': 'publishdate'})
            content_detail_elem = soup.find('div', attrs={'class': 'detail__cmain-main'})

            if publishdate_elem:
                publishDate = publishdate_elem.get_text()
                publishDate = publishDate.strip()
                publishDate = dateparser.parse(publishDate)
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
        response = self.get_response(url, params)
        if response.status_code // 100 == 2:
            content_html = response.content

            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(content_html, 'html.parser')

            # Find the title element
            title_elements = soup.find_all('a', class_='box-category-link-title')
            if title_elements is None or title_elements is []:
                return False

            for title_element in title_elements:
                title = title_element.get_text()
                link = title_element['href']

                print("Title:", title)
                print("Link:", link)

                data_detail = self.get_page_detail(link, {})

                item = {
                    'domain': 'https://thanhnien.vn/kinh-te.htm',
                    'title': title,
                    'url': link,
                    'date': data_detail['date'] if 'date' in data_detail else None,
                    'content': data_detail['content'] if 'content' in data_detail else None,
                }

                if self.daily:
                    isDup = helper.create_article(item, False)
                    if isDup is False:
                        return False
                else:
                    helper.create_article(item, True)
        else:
            # If unsuccessful, print the status code and reason for failure
            print(f"Request failed with status code {response.status_code}: {response.reason}")
            return False

    def run(self, page = {"from": None, "to": None}, daily = False):
        self.daily = daily
        page_from = 1 if page['from'] is None else page['from']
        page_to = -1 if page['to'] is None else page['to']
        while (True):
            isSuccess = self.crawl_html('https://thanhnien.vn/timelinelist/18549/' + str(page_from) + '.htm', {})
            if isSuccess == False or page_to == page_from:
                break
            page_from += 1
