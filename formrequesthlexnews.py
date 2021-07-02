# scrapy shell "https'://www1.hkexnews.hk/search/titlesearch.xhtml?lang=en"

from scrapy.http import FormRequest

data = {'lang': 'EN',
		'category': '0',
		'market': 'SEHK',
		'searchType': '1',
		't1code': '-2',
		't2Gcode': '-2',
		't2code': '-2',
		'stockId': '-1',
		'from': '20201023',
		'to': '20201123',
		'MB-Daterange': '0',
		'title': ''}
		
page = FormRequest('https://www1.hkexnews.hk/search/titlesearch.xhtml?lang=en',
					formdata=data)
					
yield(page)