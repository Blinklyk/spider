import url_manager, html_downloader, html_outputer, html_parser


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_rul):
        count = 1
        self.urls.add_new_url(root_rul)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print('craw %d : %s' % (count, new_url))
                html_cont = self.downloader.download(new_url)
                new_url, new_data = self.parser.parse(new_url, html_cont)
                self.urls.add_new_urls(new_url)
                self.outputer.collect_data(new_data)

                if count == 30:
                    break

                count = count + 1
            except:
                print('craw failed')

        self.outputer.output_html()


if __name__ == "__main__":
    root_rul = "https://baike.baidu.com/item/Python/407313?fr=aladdin"
    obj_spider = SpiderMain()
    obj_spider.craw(root_rul)
