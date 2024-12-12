from celery import shared_task
from krm.celery import app as celery_app
import datetime

# import the logging library
import logging

from krm.evaluations.models import ControlTest
from krm.evaluations_krm.models import RiskTestInherent, RiskTestResidual
from krm.questionnaires.models import QuestionTest

# Get an instance of a logger
logger = logging.getLogger(__name__)


@celery_app.task
def question_test_send_notification(qt_pk, notif_type):
    logger.info(
        "Comienzo de envío de mail de notificación para el usuario para completar cuestionarios del test de pregunta: {}".format(qt_pk))
    try:
        qt = QuestionTest.objects.get(pk=qt_pk)
    except QuestionTest.DoesNotExist:
        logger.error("Test de Pregunta no encontradoa con pk: %s" % qt_pk)
        return

    qt.send_email_notification(notif_type)
