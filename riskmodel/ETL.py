# 提取各个形式数据库的类

# -*- coding: utf-8 -*-

__author__ = 'Matthew Pan'

__date__ = '2020/2/13'

""" 
connect database 

"""
from pymongo import MongoClient
import pymysql
import numpy as np
import pkg_resources
import pandas as pd


class DbRead(object):
    """从数据库中读取"""

    def __init__(self, host, port, user, password, database):
        """
        数据库连接信息
         :param host:str,IP
         :param port: int 端口
         :param user: str 用户名
         :param password: str 密码
         :param database: str or object 数据库名
        """
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._database = database

    def read_mysql(self, sql):
        """
         从mysql中获取数据
         :param sql: str, 执行的sql语句
         :return: data,iterable 数据生成器
        """
        dbConfig = {
            "host": self._host,
            "port": self._port,
            "user": self._user,
            "password": self._password,
            "db": self._database,
            "cursorclass": pymysql.cursors.DictCursor,
            "charset": "utf8"
        }

        dbMysql = pymysql.connect(**dbConfig)
        cursor = dbMysql.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        dbMysql.close()
        return data

    def read_mongodb(self, collection, findCondition):
        """
        从mongoDB中获取数据
         :param collection: object,表名
         :param findCondition: dict 查询条件
         :return: data iterable 数据生成器
        """
        conn = MongoClient(host=self._host, port=self._port)
        dbMongo = conn.get_database(name=self._database)
        dbMongo.authenticate(self._user, self._password)
        col = dbMongo.get_collection(collection)
        data = col.find(findCondition)
        conn.close()
        return data


class CsvRead(object):
    # 所有变量
    def __init__(self):
        self.all_feature = ['status_of_existing_checking_account', 'duration_in_month', 'credit_history', 'purpose',
                            'credit_amount',
                            'savings_account_and_bonds',
                            'present_employment_since', 'installment_rate_in_percentage_of_disposable_income',
                            'personal_status_and_sex', 'other_debtors_or_guarantors',
                            'present_residence_since', 'property', 'age_in_years', 'other_installment_plans',
                            'housing',
                            'number_of_existing_credits_at_this_bank', 'job',
                            'number_of_people_being_liable_to_provide_maintenance_for', 'telephone',
                            'foreign_worker']
        # 类别变量
        self.cat_col = ['purpose', 'personal_status_and_sex', 'other_debtors_or_guarantors', 'property',
                        'other_installment_plans',
                        'housing', 'telephone', 'foreign_worker']
        # 数值变量
        self.num_col = [i for i in self.all_feature if i not in self.cat_col]
        # 整型变量
        self.int_col = self.cat_col + ['status_of_existing_checking_account', 'credit_history',
                                       'savings_account_and_bonds', 'job']
        # 需要处理的数值变量
        self.sub_col = ['status_of_existing_checking_account', 'credit_history', 'savings_account_and_bonds',
                        'present_employment_since', 'job']
        # 需要替换的变量
        self.rep_dict = {
            'status_of_existing_checking_account': {4: 0},
            'savings_account_and_bonds': {5: np.nan},
            'purpose': {'A124': np.nan}
        }

    def get_data(self):
        DATA_FILE = pkg_resources.resource_filename('riskmodel', 'data/germancredit.csv')
        data = pd.read_csv(DATA_FILE, encoding='utf-8', sep=' ', header=None, names=self.all_feature + ["target"])
        return data

    def get_describe(self):
        DATA_FILE = pkg_resources.resource_filename('riskmodel', 'data/german.txt')
        with open(DATA_FILE, 'r+') as f:
            print(f.read())
