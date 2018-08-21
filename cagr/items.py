# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Campus(scrapy.Item):
    id = scrapy.Field(serializer=int)
    code = scrapy.Field(serializer=str)


class College(scrapy.Item):
    code = scrapy.Field(serializer=str)
    name = scrapy.Field(serializer=str)


class Department(scrapy.Item):
    code = scrapy.Field(serializer=str)
    name = scrapy.Field(serializer=str)


class Program(scrapy.Item):
    id = scrapy.Field(serializer=int)
    name = scrapy.Field(serializer=str)


class Course(scrapy.Item):
    code = scrapy.Field(serializer=str)
    campus = scrapy.Field(serializer=str)
    name = scrapy.Field(serializer=str)
    load = scrapy.Field(serializer=int)


class Professor(scrapy.Item):
    id = scrapy.Field(serializer=int)
    name = scrapy.Field()


class Class(scrapy.Item):
    code = scrapy.Field(serializer=str)
    term = scrapy.Field(serializer=str)
    course_id = scrapy.Field(serializer=str)
    capacity = scrapy.Field(serializer=int)
    enrolled = scrapy.Field(serializer=int)
    special = scrapy.Field(serializer=int)
    pending = scrapy.Field(serializer=int)
    remaining = scrapy.Field(serializer=int)
    professors = scrapy.Field()
    schedule = scrapy.Field()
