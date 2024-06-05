import requests
from bs4 import BeautifulSoup
import dateparser
from helper import helper

class VnEconomySpider():
    base_url = 'https://vneconomy.vn'
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

        try:
            response = self.get_response(url, params)
            if response.status_code // 100 == 2:
                content_html = response.content
                soup = BeautifulSoup(content_html, 'html.parser')
                # Find the title element
                publishdate_elem = soup.select_one('.detail__header .detail__meta')
                if publishdate_elem:
                    publishDateTxt = publishdate_elem.get_text()
                    publishDateTxt = publishDateTxt.strip()
                    publishDate = dateparser.parse(publishDateTxt, date_formats=['%H:%M %d/%m/%Y'])
                    print('publishDate', publishDateTxt, publishDate.month)
                else:
                    publishDate = None

                content_detail_elem = soup.select_one('.detail__content')

                content_detail = ''
                if content_detail_elem:
                    content_detail = content_detail_elem.get_text()

                        # Find all elements with the class "a.tag-item"
                tag_items = soup.find_all('a', {'class': 'tag-item'})
                # Extract the tags and merge them into a list
                tag_list = [tag.text for tag in tag_items]

                return {
                    'date': publishDate,
                    'content': content_detail,
                    'tags': tag_list
                }            
            else:
                # If unsuccessful, print the status code and reason for failure
                print(f"Request failed with status code {response.status_code}: {response.reason}")
                return {}
        except Exception as e:
            print('get_page_detail:e:', e)
            return {}

    def crawl_html(self, url, params = {}):
        print('start:crawl_html:', url, params)
        response = self.get_response(url, params)
        if response.status_code // 100 == 2:
            content_html = response.content

            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(content_html, 'html.parser')

            # Find the title element
            title_elements = soup.select('.zone--featured .zone__content .col-lg-9 .story--featured .story__title a')
            if title_elements is None or len(title_elements) == 0:
                return False

            for title_element in title_elements:
                title = title_element.get_text()
                link = title_element['href']

                print("Title:", title)
                print("Link:", link)
                data_detail = self.get_page_detail(link, {})
                item = {
                    'domain': self.base_url + '/chung-khoan.htm',
                    'title': title,
                    'url': link,
                    'date': data_detail['date'] if 'date' in data_detail else None,
                    'content': data_detail['content'] if 'content' in data_detail else None,
                    'data': data_detail['tags'] if 'tags' in data_detail else None,
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
        page = page_from
        while (True):
            isSuccess = self.crawl_html('https://vneconomy.vn/chung-khoan.htm?trang=' + str(page), {})
            if isSuccess == False or page_to == page:
                break
            page += 1