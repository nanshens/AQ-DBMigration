import glob
import hashlib
import os
import sqlite3
import uuid
from collections import Counter
from datetime import datetime
import mysql.connector
import psycopg2
from loguru import logger

from aq_dbmigration.db_constant import DBConstant
from aq_dbmigration.db_record import DBRecord
from aq_dbmigration.migration_config import MigrationConfig


class DBMigration(object):

    def __init__(self, config:MigrationConfig):
        self.config:MigrationConfig = config
        self.conn = None
        self.__init_conn()
        self.__init()

    def __execute_sql(self, sql, params=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        self.conn.commit()
        cursor.close()

    def __find_all_sql(self, sql, params=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def __init_conn(self):
        if self.config.db_type == DBConstant.Type.PostgreSQL:
            self.conn = psycopg2.connect(
                dbname=self.config.db_name, user=self.config.db_user, password=self.config.db_password,
                host=self.config.db_host, port=self.config.db_port
            )
        elif self.config.db_type in [DBConstant.Type.MariaDB, DBConstant.Type.MySql]:
            self.conn = mysql.connector.connect(
                database=self.config.db_name, user=self.config.db_user, password=self.config.db_password,
                host=self.config.db_host, port=self.config.db_port
            )
        elif self.config.db_type == DBConstant.Type.SQLite:
            self.conn = sqlite3.connect(self.config.db_name)

    def __init(self):
        self.__execute_sql(DBConstant.get_init_sql(self.config.db_type))

        base_line = self.__find_all_sql(f"select * from {DBConstant.get_table_name(self.config.db_type)} where file_path='{DBConstant.BASE_LINE}';")
        if len(base_line) == 0:
            self.__execute_sql(f"insert into {DBConstant.get_table_name(self.config.db_type)} values (%s, '{self.config.base_line}', 'V{self.config.base_line}', '', '{DBConstant.BASE_LINE}', %s, 0, 0);",
                               (str(uuid.uuid4()), datetime.now()))

    def __find_all_records(self):
        result = self.__find_all_sql(f"select * from {DBConstant.get_table_name(self.config.db_type)};")
        records = []
        for row in result:
            records.append(DBRecord.of_db(row))
        return records

    def __find_all_files(self):
        if not os.path.exists(self.config.sql_directory): return []
        sql_files = glob.glob(os.path.join(self.config.sql_directory, '*.sql'))
        return sql_files

    def __generate_md5(self, content, file_path):
        md5_hash = hashlib.md5()
        md5_hash.update(content.encode('utf-8'))
        md5_hash.update(file_path.encode('utf-8'))
        return md5_hash.hexdigest()

    def __find_db_records(self, file_path, records):
        for record in records:
            if file_path == record.file_path:
                return record
        return None

    def __get_base_line(self, records):
        return [record for record in records if record.file_path == DBConstant.BASE_LINE][0]

    def __insert_record(self, record):
        sql = f"insert into {DBConstant.get_table_name(self.config.db_type)} values (%s, '{record.sequence}', '{record.version}', '{record.description}', '{record.file_path}', %s, {record.execution_time}, '{record.check_value}');"
        self.__execute_sql(sql, (str(uuid.uuid4()), datetime.now()))


    def migration(self):
        records = self.__find_all_records()
        base_line = self.__get_base_line(records)
        file_records = []
        files = self.__find_all_files()

        for file_path in files:
            file_name = os.path.basename(file_path)
            splits = file_name.split('__')

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                md5 = self.__generate_md5(content, file_path)
                file_records.append(DBRecord.of_file(splits[0].replace("V", ""), splits[0], splits[1], file_path, md5, content))

        version_list = [o.version for o in file_records]
        version_count = Counter(version_list)
        duplicate_versions = [version for version, count in version_count.items() if count > 1]

        if len(duplicate_versions) > 0:
            raise Exception(f"AQ-DBMigration ERROR: duplicate versions {str(duplicate_versions)}")

        sorted_file_records = sorted(file_records, key=lambda record: (record.main_sequence, record.sub_sequence))

        logger.info("AQ-DBMigration START")
        for file_record in sorted_file_records:
            if base_line.sub_sequence == 0 and file_record.main_sequence <= base_line.main_sequence: continue
            if base_line.sub_sequence != 0 and (file_record.main_sequence < base_line.main_sequence or file_record.main_sequence == base_line.main_sequence and file_record.sub_sequence <= base_line.sub_sequence): continue

            record = self.__find_db_records(file_record.file_path, records)

            if record is None:
                st = datetime.now()
                self.__execute_sql(file_record.content)
                et = datetime.now()
                file_record.execution_time = (et - st).seconds
                self.__insert_record(file_record)
                logger.info(f"AQ-DBMigration EXECUTE {file_record.file_path}")
                continue

            if record.check_value != file_record.check_value:
                raise Exception(f"AQ-DBMigration ERROR: check value error: db is {record.check_value}, but file is {file_record.check_value}")

        logger.info("AQ-DBMigration END")