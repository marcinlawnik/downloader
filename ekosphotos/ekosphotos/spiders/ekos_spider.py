import scrapy
import json
import re

from ekosphotos.items import EkosItem
from scrapy import log


class EkosSpider(scrapy.Spider):
    name = "ekos"
    allowed_domains = ["ekos.edu.pl"]
    range = range(1,2) # 28146 the end number should be +1 as the function definition is -1 so range 1,2 gives 1 result
    base_url = 'http://ekos.edu.pl/liceum/photogallery.php?photo_id='
    start_urls = [base_url + str(s) for s in range]
    
    def parse(self, response):
        #scrapy.log.start('scrapy.log', 'INFO', False)
        
        item = EkosItem()
        #title of album
        item['album'] = ''.join(response.xpath('/html/body/table[3]/tr/td[2]/table[2]/tr[1]/td/table/tr/td[1]/a[2]/text()').extract())
        #relative file path
        item['image'] = ''.join(response.xpath('/html/body/table[3]/tr/td[2]/table[2]/tr[1]/td/div[1]/a/img/@src').extract())
        #extracted description
        description = ''.join(response.xpath('/html/body/table[3]/tr/td[2]/table[2]/tr[1]/td/div[2]').extract())
        item['description'] = description
        #date
        dateregex = '[0-9]{2}-[0-9]{2}-[0-9]{4}'
        regexmatch = re.search(dateregex, description)
        if regexmatch:
            s = regexmatch.start()
            e = regexmatch.end()
            item['date'] = ''.join(i for i in description[s:e] if i.isdigit() or i in ('-'))
        else:
            item['date'] = 'UNMATCHED'
        #year
        yearregex = '-[0-9]{4}'
        regexmatch = re.search(yearregex, description)
        if regexmatch:
            s = regexmatch.start()
            e = regexmatch.end()
            item['year'] = ''.join(i for i in description[s:e] if i.isdigit())
        else:
            item['year'] = 'UNMATCHED'
        #uploader
        uploaderregex = '>[a-zA-Z]*_[a-zA-Z]*<'
        regexmatch = re.search(uploaderregex, description)
        if regexmatch:
            s = regexmatch.start()
            e = regexmatch.end()
            item['uploader'] = ''.join(i for i in description[s:e] if i.isalpha() or i in ('_'))
        else:
            item['uploader'] = 'UNMATCHED'
        #width
        widthregex = '[0-9]{2,4}\sx'
        regexmatch = re.search(widthregex, description)
        if regexmatch:
            s = regexmatch.start()
            e = regexmatch.end()
            #filter found match for digits
            item['width'] = ''.join(i for i in description[s:e] if i.isdigit())
        else:
            item['width'] = 'UNMATCHED'
        #height
        heightregex = 'x\s[0-9]{2,4}\s'
        regexmatch = re.search(heightregex, description)
        if regexmatch:
            s = regexmatch.start()
            e = regexmatch.end()
            item['height'] = ''.join(i for i in description[s:e] if i.isdigit())
        else:
            item['height'] = 'UNMATCHED'
        #views
        viewsregex = '[0-9]{1,8}\\n'
        regexmatch = re.search(viewsregex, description)
        if regexmatch:
            s = regexmatch.start()
            e = regexmatch.end()
            item['views'] = ''.join(i for i in description[s:e] if i.isdigit())
        else:
            item['views'] = 'UNMATCHED'
        #photo_id the gallery number
        item['photo_id'] = ''.join(i for i in response.url if i.isdigit())
        #logs
        #scrapy.log.msg(json.dumps(vars(item), sort_keys = True, indent = 4), "INFO")
        yield item
		