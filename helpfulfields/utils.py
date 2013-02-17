# -*- coding: utf-8 -*-
from datetime import datetime


def datediff(original, minutes=30):
    if not original:
        return False
    timediff = datetime.now() - original
    compare_to = 60 * minutes
    diff = timediff.seconds / 60
    return diff < compare_to
