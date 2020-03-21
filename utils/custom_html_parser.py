from html.parser import HTMLParser


class CustomHtmlParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.json = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for attr in attrs:
                if attr[0] == 'src':
                    self.json.append(
                        {'src': attr[1], 'type': CustomHtmlParser.getUrlType(attr[1])})

    def error(self, message):
        pass

    @staticmethod
    def getUrlType(source: str):
        if source[:10] == 'data:image':
            return 'base64'
        return 'url'
