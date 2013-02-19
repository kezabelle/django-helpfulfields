# -*- coding: utf-8 -*-
from datetime import datetime, timedelta


def datediff(original, minutes=30):
    """
    Compares a given datetime to now to find out if it was recent.

    :param original: the original date
    :param minutes: how long ago is considered recent
    :return: whether or not it's recent
    :rtype: boolean
    """
    if not original:
        return False
    to_compare = datetime.now() - original
    recently = datetime.now() - timedelta(minutes=minutes)
    return to_compare > recently
