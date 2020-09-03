import time

from celery import shared_task


# @shared_task
# def sum(a, b):
#     time.sleep(5)
#     print("SUMA:", a + b)
#     return a + b


@shared_task
def async_reference_changed