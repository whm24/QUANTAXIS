# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from QUANTAXIS.QAFetch import QA_fetch_get_stock_day, QA_fetch_get_stock_xdxr

import datetime
import pandas as pd


def QA_data_get_qfq(code, start, end):
    '使用网络数据进行复权/需要联网'
    xdxr_data = QA_fetch_get_stock_xdxr('tdx', code)
    bfq_data = QA_fetch_get_stock_day(
        'tdx', code, '1990-01-01', str(datetime.date.today())).dropna(axis=0)
    return QA_data_make_qfq(bfq_data,xdxr_data,start,end)


def QA_data_get_hfq(code, start, end):
    '使用网络数据进行复权/需要联网'
    xdxr_data = QA_fetch_get_stock_xdxr('tdx', code)
    bfq_data = QA_fetch_get_stock_day(
        'tdx', code, '1990-01-01', str(datetime.date.today())).dropna(axis=0)
    return QA_data_make_hfq(bfq_data,xdxr_data,start,end)


def QA_data_make_qfq(bfq_data,xdxr_data,start, end):
    '使用数据库数据进行复权'
    info = xdxr_data[xdxr_data['category'] == 1]
    data = pd.concat([bfq_data, info[['fenhong', 'peigu', 'peigujia',
                                      'songzhuangu']][bfq_data.index[0]:]], axis=1).fillna(0)
    data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu']
                        * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
    data['adjx'] = (data['preclose'].shift(-1) / data['close']).fillna(1)
    data['adj'] = (data['preclose'].shift(-1) /
                   data['close']).fillna(1)[::-1].cumprod()
    data['open'] = data['open'] * data['adj']
    data['high'] = data['high'] * data['adj']
    data['low'] = data['low'] * data['adj']
    data['close'] = data['close'] * data['adj']
    data['preclose'] = data['preclose'] * data['adj']
    return data[data['open'] != 0][start:end]


def QA_data_make_hfq(bfq_data, xdxr_data,start, end):
    '使用数据库数据进行复权'
    info = xdxr_data[xdxr_data['category'] == 1]
    data = pd.concat([bfq_data, info[['fenhong', 'peigu', 'peigujia',
                                      'songzhuangu']][bfq_data.index[0]:]], axis=1).fillna(0)
    data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu']
                        * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
    data['adjx'] = (data['preclose'].shift(-1) / data['close']).fillna(1)
    data['adj'] = (data['preclose'].shift(-1) /
                   data['close']).fillna(1).cumprod()
    data['open'] = data['open'] / data['adj']
    data['high'] = data['high'] / data['adj']
    data['low'] = data['low'] / data['adj']
    data['close'] = data['close'] / data['adj']
    data['preclose'] = data['preclose'] / data['adj']
    return data[data['open'] != 0][start:end]



