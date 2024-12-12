from celery import shared_task
from krm.celery import app as celery_app
import datetime

# import the logging library
import logging

from krm.evaluations.models import ControlTest


# Get an instance of a logger
logger = logging.getLogger(__name__)


@celery_app.task
def control_test_send_notification_control_owner(ct_pk, notif_type):
    logger.info(
        "Comienzo de envío de mail de notificación para control owner para el control test: {}".format(ct_pk))
    try:
        ct = ControlTest.objects.get(pk=ct_pk)
    except ControlTest.DoesNotExist:
        logger.error("Control Test no encontradoa con pk: %s" % ct_pk)
        return

    ct.sent_notification_control_owner(notif_type)


@celery_app.task
def control_test_send_notification_control_supervisor(ct_pk, notif_type):
    logger.info(
        "Comienzo de envío de mail de notificación para control supervisor para el control test: {}".format(ct_pk))
    try:
        ct = ControlTest.objects.get(pk=ct_pk)
    except ControlTest.DoesNotExist:
        logger.error("Control Test no encontradoa con pk: %s" % ct_pk)
        return

    ct.sent_notification_control_supervisor(notif_type)
