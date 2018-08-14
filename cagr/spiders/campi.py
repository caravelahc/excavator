# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from cagr.items import Campus


class CampiSpider(scrapy.Spider):
    name = 'campi'
    allowed_domains = ['cagr.sistemas.ufsc.br']
    start_urls = [parse.urlunparse((
        'https', # scheme
        'cagr.sistemas.ufsc.br', # netloc
        '/modules/comunidade/cadastroTurmas/index.xhtml', # path
        '', '', '', # params, query, fragment
    ))]

    def parse(self, response):
        for opt in response.css('[id="formBusca:selectCampus"] option'):
            id = opt.css('::attr(value)').extract_first().strip()
            abbrev = opt.css('::text').extract_first().strip()[5:]

            yield Campus(id=int(id), abbrev=abbrev)
