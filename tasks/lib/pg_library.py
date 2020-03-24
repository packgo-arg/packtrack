#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from datetime import timezone, timedelta
from django.utils import timezone


def calc_prov(cpo, cpd):

    cparg = pd.read_excel('./tasks/lib/CP_Argentina.xlsx')
    cparg.drop(['cod_descripcion'], axis=1, inplace=True)
    a = cparg.loc[cparg['cod']==cpo, 'cod_provincia'].iloc[0]
    b = cparg.loc[cparg['cod']==cpd, 'cod_provincia'].iloc[0]
    return a, b

def calc_del_time(a ,b):
    crosst = pd.read_excel('./tasks/lib/table.xlsx', index_col='COD')
    crosst.dropna(inplace=True)
    return crosst.loc[a, b]

def calc_time(t, cpo, cpd):

    timecut = timezone.now().replace(hour=18, minute=0, second=0, microsecond=0)
    a, b = calc_prov(cpo, cpd)
    r = calc_del_time(a, b)

    if t <= timecut and a == b:
        st = timecut
        et = timezone.now().replace(hour=21, minute=0, second=0, microsecond=0)
        r = 'SAME DAY'
        return st, et, r

    elif t <= timecut:
        stt = t + timedelta(days=1)
        st = stt.replace(hour=11, minute=0, second=0, microsecond=0)
        et = st + timedelta(hours=int(r))
        return st, et, r
    else:
        stt = t + timedelta(days=2)
        st = stt.replace(hour=11, minute=0, second=0, microsecond=0)
        et = st + timedelta(hours=int(r))
        return st, et, r
