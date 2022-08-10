# """Bookings tests."""

# import datetime

# # Django
# from django.test import TestCase
# from django.test import Client

# # Django REST Framework
# # from rest_framework import status
# # from rest_framework.test import APITestCase

# # Model
# from cicerone.visits.models import Visit, VisitVariant, Rate, Price, Lang
# from cicerone.users.models import User
# from cicerone.bookings.models import Booking, BookingLine, BookingOrigin

# # from rest_framework.authtoken.models import Token


# class BookingTestModel(TestCase):
#     """Booking manager test case."""

#     def setUp(self):
#         """Test case setup."""
#         self.user = User.objects.create(
#             first_name='Bienvenido',
#             last_name='Sáez Muelas',
#             email='it@beticadigital.com',
#             username='it@beticadigital.com',
#             password='admin123',
#             is_client=True
#         )

#         self.visit = Visit.objects.create(
#             name='Visita de prueba',
#             type_visit=1
#         )

#         self.price_adult = Price.objects.create(
#             display_text='Adultos',
#             price=10,
#             subtract_quota=True
#         )

#         self.price_infantil = Price.objects.create(
#             display_text='Niños',
#             price=0
#         )

#         self.rate = Rate.objects.create(
#             description='Tarifa base'
#         )
#         self.rate.prices.add(self.price_adult)
#         self.rate.prices.add(self.price_infantil)
#         self.rate.save()

#         self.lang = Lang.objects.create(
#             lang='Español',
#             code='es'
#         )

#         self.visit_variant = VisitVariant.objects.create(
#             visit=self.visit,
#             name='Variante de visita de prueba',
#             quota_max=6,
#             base_rate=self.rate
#         )

#         self.visit_variant.langs.add(self.lang)

#         self.booking_origin = BookingOrigin.objects.create(
#             name="Web"
#         )

#         self.booking = Booking.objects.create(
#             client=self.user,
#             visit=self.visit_variant,
#             origin=self.booking_origin,
#             date=datetime.datetime.today(),
#             n_participants=5,
#             n_participants_total=5,
#             name='Bienvenido Sáez Muelas',
#             email=self.user.email,
#             phone_number="+34987654345",
#             lang=self.lang
#         )

#         for p in self.visit_variant.base_rate.prices.all():
#             booking_line = BookingLine.objects.create(
#                 booking=self.booking,
#                 n_participants=2,
#                 display_text=p.display_text,
#                 price=p.price,
#                 subtract_quota=p.subtract_quota
#             )
#             self.booking.booking_lines.add(booking_line)

#     def test_auto_generate_code_booking(self):
#         self.assertIsNotNone(self.booking.code)

#     def test_calculate_number_participant_total(self):
#         self.assertEqual(self.booking.n_participants_total,4)

#     def test_calculate_number_participant_subtract_quota(self):
#         self.assertEqual(self.booking.n_participants,2)

#     def test_calculate_booking_total(self):
#         total = 0
#         n_participants = 0
#         n_participants_total = 0
#         for line in self.booking.booking_lines.all():
#             total = total + (line.n_participants * line.price)
#             if line.subtract_quota:
#                 n_participants += line.n_participants
#             n_participants_total += line.n_participants
#         self.assertEqual(self.booking.n_participants, n_participants)
#         self.assertEqual(self.booking.n_participants_total, n_participants_total)
#         self.assertEqual(self.booking.total, total)
