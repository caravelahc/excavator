# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
from cagr.items import Campus, Class, Course, Professor
from scrapy.exceptions import DropItem


class DedupPipeline():
    def __init__(self):
        self.courses_seen = set()
        self.professors_seen = set()

    def process_item(self, item, spider):
        if isinstance(item, Course):
            if item['code'] in self.courses_seen:
                raise DropItem(f'Duplicate course found: {item["code"]}')
            else:
                self.courses_seen.add(item['code'])
        elif isinstance(item, Professor):
            if item['id'] in self.professors_seen:
                raise DropItem(f'Duplicate professor found: {item["id"]}')
            else:
                self.professors_seen.add(item['id'])
        return item


class PgsqlPipeline():
    def __init__(self, host, user, password, dbname):
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            host=settings.get('DATABASE_HOST'),
            user=settings.get('POSTGRES_USER'),
            password=settings.get('POSTGRES_PASSWORD'),
            dbname=settings.get('POSTGRES_DB'),
        )

    def open_spider(self, spider):
        self.connection = psycopg2.connect(host=self.host,
                                           user=self.user,
                                           password=self.password,
                                           dbname=self.dbname)

        with open('schema.sql') as fp, self.connection.cursor() as cursor:
            cursor.execute(fp.read())
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        with self.connection.cursor() as cursor:
            if isinstance(item, Campus):
                cursor.execute("""
                    INSERT INTO campi(id, code)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                """, (item['id'], item['code']))
            elif isinstance(item, Course):
                cursor.execute("""
                    INSERT INTO courses(code, campus_id, name, load)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (item['code'], spider.campus, item['name'], item['load']))
            elif isinstance(item, Class):
                cursor.execute("""
                    INSERT INTO classes(code, term, course_id, capacity, enrolled, special, pending, remaining)
                    SELECT %s, %s, c.id, %s, %s, %s, %s, %s FROM courses c WHERE c.code = %s
                    ON CONFLICT ON CONSTRAINT classes_uniq DO UPDATE
                        SET capacity = excluded.capacity,
                            enrolled = excluded.enrolled,
                            special = excluded.special,
                            pending = excluded.pending,
                            remaining = excluded.remaining
                    RETURNING id
                """, (item['code'], item['term'], item['capacity'],
                      item['enrolled'], item['special'], item['pending'],
                      item['remaining'], item['course_id']))
                class_id, *_ = cursor.fetchone()
                for professor_id in item['professors']:
                    cursor.execute("""
                        INSERT INTO classes_professors(class_id, professor_id)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING
                    """, (class_id, professor_id))
            elif isinstance(item, Professor):
                cursor.execute("""
                    INSERT INTO professors(id, name)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                """, (item['id'], item['name']))

        self.connection.commit()
        return item
