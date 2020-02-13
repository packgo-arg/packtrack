#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import psycopg2 as pg
from datetime import datetime, timezone, timedelta


# In[ ]:


def calc_start_time(t):
    
    timecut = datetime.now(timezone.utc).replace(hour=15, minute=0, second=0, microsecond=0)
    
    if t <= timecut:
        return t.replace(hour=18, minute=0, second=0, microsecond=0)
    else:
        stt = t + timedelta(days=1)
        return stt.replace(hour=18, minute=0, second=0, microsecond=0)

