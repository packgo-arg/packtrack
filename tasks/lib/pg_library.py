#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import psycopg2 as pg
from datetime import datetime, timezone, timedelta
from django.utils import timezone
import os, sys
# In[ ]:


def calc_start_time(t):

    timecut = timezone.now().replace(hour=18, minute=0, second=0, microsecond=0)

    if t <= timecut:
        return t.replace(hour=21, minute=0, second=0, microsecond=0)
    else:
        stt = t + timedelta(days=1)
        return stt.replace(hour=21, minute=0, second=0, microsecond=0)

def calc_end_time(st, cpo, cpd):

	crosst = pd.read_excel('./tasks/lib/table.xlsx', index_col='COD')
	crosst.dropna(inplace=True)
	cparg = pd.read_excel('./tasks/lib/CP_Argentina.xlsx')
	cparg.drop(['cod_descripcion'], axis=1, inplace=True)

	a = cparg.loc[cparg['cod']==cpo, 'cod_provincia'].iloc[0]
	b = cparg.loc[cparg['cod']==cpd, 'cod_provincia'].iloc[0]
	r = int(crosst.loc[a, b])
	et = st + timedelta(hours=r)
	return et, r
