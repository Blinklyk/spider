from bs4 import BeautifulSoup
import re
import urllib.parse



class HtmlParser(object):
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_url = self._get_new_url(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_url, new_data

    def _get_new_url(self, page_url, soup):
        new_urls = set()
        # /view/123.htm
        links = soup.find_all('a', href=re.compile(r'/item/*'))
        for link in links:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        # < dd class ="lemmaWgt-lemmaTitle-title" > < h1 > Python < / h1 >
        res_data = {}

        res_data['url'] = page_url

        title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find('h1')
        move = dict.fromkeys((ord(c) for c in u"\xa0\n\t"))
        title_cont = title_node.get_text().translate(move)
        res_data['title'] = title_cont

        # < div class ="lemma-summary" label-module="lemmaSummary" >
        summary_node = soup.find('div', class_="lemma-summary")
        move = dict.fromkeys((ord(c) for c in u"\xa0\u02c8\xb2"))
        summary_cont = summary_node.get_text().translate(move)
        res_data['summary'] = summary_cont

        return res_data




