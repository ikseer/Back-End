# from django.contrib.auth import get_user_model
# from django.urls import reverse

# from .test_setup import *

# User=get_user_model()


# class PatientDeleteTestCase(TestSetup):
#     def setUp(self) -> None:
#         super().setUp()
#         self.staff, self.staff_token = self.create_staff()


#     def test_delete_patient(self):
#         patient, patient_token = self.create_patient()

#         url='/accounts/patient/{}/'.format(patient.id)
#         response = self.client.delete(
#             url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(Patient.objects.count(), 0)
#         self.assertEqual(len( Patient.deleted_objects.all()), 1)
#     def test_delete_patient_hard(self):
#         patient, patient_token = self.create_patient()
#         self.assertEqual(Patient.objects.count(), 1)
#         url='/accounts/patient/{}/?method=hard'.format(patient.id)
#         response = self.client.delete(
#             url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)

#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(Patient.objects.count(), 0)
#         self.assertEqual(len( Patient.deleted_objects.all()), 0)
#     def test_delete_patient_restore(self):
#         patient, patient_token = self.create_patient()

#         url='/accounts/patient/{}/'.format(patient.id)
#         response = self.client.delete(
#             url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
#         self.assertEqual(response.status_code, 204)


#         url=reverse('patient-restore',kwargs={'pk':patient.id})
#         response = self.client.post(
#             url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(Patient.objects.count(), 1)
#         self.assertEqual(len( Patient.deleted_objects.all()), 0)
#     def test_delete_hard_after_soft(self):
#         patient, patient_token = self.create_patient()
#         self.assertEqual(Patient.objects.count(), 1)
#         url='/accounts/patient/{}/?method=soft'.format(patient.id)
#         response = self.client.delete(
#             url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)

#         self.assertEqual(response.status_code, 204)
#         url=reverse('deleted-patient-delete',kwargs={'pk':patient.id})
#         response = self.client.delete(
#             url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)

#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(Patient.objects.count(), 0)
#         self.assertEqual(len( Patient.deleted_objects.all()), 0)
#     def test_delete_patient_get_deleted(self):
#         patient, patient_token = self.create_patient()

#         url='/accounts/patient/{}/'.format(patient.id)
#         response = self.client.delete(
#             url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
#         self.assertEqual(response.status_code, 204)

#         url=reverse('patient-get-deleted')
#         response = self.client.get(
#             url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
#         self.assertEqual(response.status_code, 200)
#         # print(response.data)
#         self.assertEqual(len(response.data['results']), 1)
# class DoctorDeleteTestCase(TestSetup):
#     def setUp(self) -> None:
#         super().setUp()
#         self.staff, self.staff_token = self.create_staff()
#         self.doctor, self.doctor_token = self.create_doctor()

#     def test_delete_doctor(self):
#         url='/accounts/doctor/{}/'.format(self.doctor.id)
#         response = self.client.delete(
#             url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(Doctor.objects.count(), 0)
#         self.assertEqual(len( Doctor.deleted_objects.all()), 1)
#     def test_delete_doctor_hard(self):
#         self.assertEqual(Doctor.objects.count(), 1)
#         url='/accounts/doctor/{}/?method=hard'.format(self.doctor.id)
#         response = self.client.delete(
#             url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)

#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(Doctor.objects.count(), 0)
#         self.assertEqual(len( Doctor.deleted_objects.all()), 0)
#     def test_delete_doctor_restore(self):
#         self.assertEqual(Doctor.objects.count(), 1)
#         url='/accounts/doctor/{}/'.format(self.doctor.id)
#         response = self.client.delete(
#             url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
#         self.assertEqual(response.status_code, 204)
#         url=reverse('doctor-restore',kwargs={'pk':self.doctor.id})
#         response = self.client.post(
#             url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(Doctor.objects.count(), 1)
#         self.assertEqual(len( Doctor.deleted_objects.all()), 0)
#     def test_delete_hard_after_soft(self):
#         self.assertEqual(Doctor.objects.count(), 1)
#         url='/accounts/doctor/{}/?method=soft'.format(self.doctor.id)
#         response = self.client.delete(
#             url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
#         self.assertEqual(response.status_code, 204)
#         url=reverse('deleted-doctor-delete',kwargs={'pk':self.doctor.id})
#         response = self.client.delete(
#             url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(Doctor.objects.count(), 0)
#         self.assertEqual(len( Doctor.deleted_objects.all()), 0)
#     def test_delete_doctor_get_deleted(self):
#         self.assertEqual(Doctor.objects.count(), 1)
#         url='/accounts/doctor/{}/'.format(self.doctor.id)
#         response = self.client.delete(
#             url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
#         self.assertEqual(response.status_code, 204)
#         url=reverse('doctor-get-deleted')
#         response = self.client.get(
#             url, format='json', HTTP_AUTHORIZATION='Bearer ' + self.staff_token)
#         self.assertEqual(response.status_code, 200)
#         # print(response.data)
#         self.assertEqual(len(response.data['results']), 1)
