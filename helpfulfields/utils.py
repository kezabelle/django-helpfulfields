# -*- coding: utf-8 -*-
from datetime import datetime


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
    timediff = datetime.now() - original
    compare_to = 60 * minutes
    diff = timediff.seconds / 60
    return diff < compare_to
