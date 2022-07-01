from django.urls import include, path
from arike.facility.models.patients import TreatmentNotes
from arike.facility.view import CreateFacility, UpdateFacility, DetailFacility, ViewFacility, DeleteFacility
from arike.facility.views.patients import CreatePatient, UpdatePatient, ViewPatient, DetailPatient, DeletePatient, load_facilities
from arike.facility.views.family import CreateFamily, UpdateFamily, ViewFamily, DetailFamily, DeleteFamily
from arike.facility.views.disease import CreateDisease, UpdateDisease, ViewDisease, DetailDisease, DeleteDisease
from arike.facility.views.treatment import CreateTreatment, DeleteTreatment, DetailTreatment, UpdateTreatment, ViewTreatment
from arike.facility.views.home import HomeView
from arike.facility.views.visit import AddTreatmentNotes, Agenda, CreateVisit, DeleteVisit, DetailHistory, DetailVisit, PatientInfo, ViewHistoy, ViewTreatmentNotes, ViewVisit, VisitPatient
from arike.facility.viewset import FacilityViewSet
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register("api/facility", FacilityViewSet)

patient_patterns = [
  path("family/create/", CreateFamily.as_view(), name="add-family"),
  path("family/update/<int:pk>/", UpdateFamily.as_view(), name="update-family"),
  path("family/detail/<int:pk>/", DetailFamily.as_view(), name="detail-family"),
  path("family/view/", ViewFamily.as_view(), name="view-family"),
  path("family/delete/<int:pk>/", DeleteFamily.as_view(), name="delete-family"),
  path("disease/create/", CreateDisease.as_view(), name="add-disease"),
  path("disease/update/<int:pk>/", UpdateDisease.as_view(), name="update-disease"),
  path("disease/detail/<int:pk>/", DetailDisease.as_view(), name="detail-disease"),
  path("disease/view/", ViewDisease.as_view(), name="view-disease"),
  path("disease/delete/<int:pk>/", DeleteDisease.as_view(), name="delete-disease"),
  path("treatment/create/", CreateTreatment.as_view(), name="add-treatment"),
  path("treatment/update/<int:pk>/", UpdateTreatment.as_view(), name="update-treatment"),
  path("treatment/detail/<int:pk>/", DetailTreatment.as_view(), name="detail-treatment"),
  path("treatment/view/", ViewTreatment.as_view(), name="view-treatment"),
  path("treatment/delete/<int:pk>/", DeleteTreatment.as_view(), name="delete-treatment"),
  # path("filter/", FacilityFilterView.as_view())
  path("history/view", ViewHistoy.as_view(), name="history-view"),
  path("history/detail/<int:pk>", DetailHistory.as_view(), name="history-detail"),
]

patient_visit_patterns = [
  path("", VisitPatient.as_view(), name="patient_visit"),
  path("health/", PatientInfo.as_view(), name="health-info"),
  path("notes/view/", ViewTreatmentNotes.as_view(), name="treatment-notes"),
  path("notes/create/", AddTreatmentNotes.as_view(), name="add-notes"),
]

app_name = 'arike'
urlpatterns = [
  # path("facility/", SignInView.as_view(), name="login"),
  path("", HomeView.as_view(), name="homepage"),
  path("facility/create/", CreateFacility.as_view(), name='add-facility'),
  path("facility/update/<int:pk>/", UpdateFacility.as_view(), name='update-facility'),
  path("facility/detail/<int:pk>/", DetailFacility.as_view(), name='detail-facility'),
  path("facility/view/", ViewFacility.as_view(), name='view-facility'),
  path("facility/delete/<int:pk>/", DeleteFacility.as_view(), name='delete-facility'),
  path("patient/create/", CreatePatient.as_view(), name="add-patient"),
  path("patient/update/<int:pk>/", UpdatePatient.as_view(), name="update-patient"),
  path("patient/detail/<int:pk>/", DetailPatient.as_view(), name="detail-patient"),
  path("patient/view/", ViewPatient.as_view(), name="view-patient"),
  path("patient/delete/<int:pk>/", DeletePatient.as_view(), name="delete-patient"),
  path("patient/<int:pk1>/", include(patient_patterns)),
  path("visit/create/", CreateVisit.as_view(), name="add-visit"),
  # path("visit/update/<int:pk>/", UpdateVisit.as_view(), name="update-visit"),
  path("visit/detail/<int:pk>/", DetailVisit.as_view(), name="detail-visit"),
  path("visit/view/", ViewVisit.as_view(), name="view-visit"),
  path("visit/agenda/", Agenda.as_view(), name="agenda"),
  path("visit/delete/<int:pk>/", DeleteVisit.as_view(), name="delete-visit"),
  path("visit/<int:pk1>/", include(patient_visit_patterns)),
  # path("ajax/load_facilities/", load_facilities, name="ajax_facility_loader")
] + router.urls

