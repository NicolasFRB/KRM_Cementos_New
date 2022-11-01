from celery import shared_task
from krm.celery import app as celery_app
import datetime

# import the logging library
import logging

from krm.evaluations.models import ControlTest
from krm.evaluations_krm.models import RiskTestInherent, RiskTestResidual


# Get an instance of a logger
logger = logging.getLogger(__name__)


@celery_app.task
def risk_test_send_notification_expert(rt_pk):
    logger.info(
        "Comienzo de envío de mail de notificación para el experto del test de riesgo inherente: {}".format(rt_pk))
    try:
        rt = RiskTestInherent.objects.get(pk=rt_pk)
    except RiskTestInherent.DoesNotExist:
        logger.error("Test de Riesgo no encontradoa con pk: %s" % rt_pk)
        return

    rt.sent_email_notification_expert()


@celery_app.task
def risk_test_send_notification_evaluator(rt_pk):
    logger.info(
        "Comienzo de envío de mail de notificación para el evaluador del test de riesgo residual: {}".format(rt_pk))
    try:
        rt = RiskTestResidual.objects.get(pk=rt_pk)
    except RiskTestResidual.DoesNotExist:
        logger.error("Test de Riesgo no encontradoa con pk: %s" % rt_pk)
        return

    rt.send_email_notification_evaluator()
