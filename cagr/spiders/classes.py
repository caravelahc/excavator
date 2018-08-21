# -*- coding: utf-8 -*-
import logging
from pprint import pformat
from urllib import parse

import scrapy
from cagr.items import Class, Course, Professor

log = logging.getLogger(__name__)


class ClassesSpider(scrapy.Spider):
    name = 'classes'
    allowed_domains = ['cagr.sistemas.ufsc.br']

    def __init__(self, campus=None, term=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.campus = campus
        self.term = term
        self.initial_form = None

    def start_requests(self):
        def init(response):
            self.initial_form = response

            for opt in response.css('[id="formBusca:selectCampus"] option'):
                id = opt.css('::attr(value)').extract_first().strip()
                name = opt.css('::text').extract_first().strip()[5:]
                if name == self.campus:
                    self.logger.info(f'Found campus {name} ID {id}')
                    return scrapy.FormRequest.from_response(
                        response, 'formBusca', formdata={
                            'AJAXREQUEST': '_viewRoot',
                            'formBusca:selectCampus': id,
                            'formBusca:selectSemestre': self.term,
                        },
                        callback=self.parse, dont_filter=True)


        yield scrapy.Request(url=parse.urlunparse((
            'https', # scheme
            'cagr.sistemas.ufsc.br', # netloc
            '/modules/comunidade/cadastroTurmas/index.xhtml', # path
            '', '', '', # params, query, fragment
        )), callback=init)

    def parse(self, response):
        current_page = response.css('.rich-datascr-act::text').extract_first()
        self.logger.info(f'Parsing page {current_page}')

        page_buttons = response.css('.rich-datascr-act + .rich-datascr-inact')
        if len(page_buttons) > 0:
            yield scrapy.FormRequest.from_response(
                        self.initial_form, 'formBusca', formdata={
                            'AJAXREQUEST': '_viewRoot',
                            'formBusca:dataScroller1': 'fastforward',
                        },
                        callback=self.parse, dont_filter=True)

        for row in response.xpath('//*[@id="formBusca:dataTable:tb"]/*'):
            cells = row.xpath('./*')

            yield Course(
                code=cells[3].css('::text').extract_first().strip(),
                campus=self.campus,
                name=cells[5].css('::text').extract_first().strip(),
                load=int(cells[6].css('::text').extract_first()),
            )

            professors = set()
            for professor in cells[13].xpath('./*[@href]'):
                *_, lattes_id = professor.css('::attr(href)').extract_first().split('/')
                lattes_id = int(lattes_id)

                name = professor.css('::text').extract_first().strip()

                yield Professor(id=lattes_id, name=name)
                professors.add(lattes_id)

            remaining = cells[10].css('::text').extract_first()
            pending = cells[11].css('::text').extract_first()

            yield Class(
                code=cells[4].css('::text').extract_first(),
                term=self.term,
                course_id=cells[3].css('::text').extract_first(),
                capacity=int(cells[7].css('::text').extract_first()),
                enrolled=int(cells[8].css('::text').extract_first()),
                special=int(cells[9].css('::text').extract_first()),
                remaining=int(remaining) if remaining != 'LOTADA' else 0,
                pending=int(pending) if pending is not None else 0,
                # schedule=?,
                professors=list(professors),
            )
