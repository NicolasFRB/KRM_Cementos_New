# from celery import shared_task
# from krm.celery import app as celery_app
# import datetime

# # import the logging library
# import logging

# from krm.users.models import User


# # Get an instance of a logger
# logger = logging.getLogger(__name__)


# @celery_app.task
# def send_welcome_email(user_pk):
#     """ Tarea que se encargará de enviar un email de bienvenida a KRC Tool """

#     logger.info(
#         "Comienzo de envío de mail de bienvenida para el usuario: {}".format(user_pk))
#     try:
#         user = User.objects.get(pk=user_pk)
#     except Booking.DoesNotExist:
#         logger.error("Usuario no encontradoa con pk: %s" % user_pk)
#         return

#     user.send_welcome_email()


# @celery_app.task
# def send_email_remember_password(user_pk):
#     """ Tarea que se encargará de enviar un email de rescordar contraseña de KRC Tool """

#     logger.info(
#         "Comienzo de envío de mail de recordar contraseña para el usuario: {}".format(user_pk))
#     try:
#         user = User.objects.get(pk=user_pk)
#     except Booking.DoesNotExist:
#         logger.error("Usuario no encontradoa con pk: %s" % user_pk)
#         return

#     user.send_email_remember_password()
