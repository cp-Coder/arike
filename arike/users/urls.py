from django.urls import path
from django.contrib.auth.views import LogoutView
from arike.users.views import DeleteUser, LoginView, CreateUser, UpdateUser, DetailUser, ViewUser, AssignFacilityUser, ChangeFacilityUser, ChangePassword

app_name = "user"
urlpatterns = [
  path("login/", LoginView.as_view(), name="login"),
  path("logout/", LogoutView.as_view(), name="logout"),
  # path("profile/", ProfileView.as_view(), name="profile"),
  path("create/", CreateUser.as_view(), name="add-user"),
  path("change/", ChangePassword.as_view(), name="change-password"),
  path("update/<int:pk>", UpdateUser.as_view(), name="update-user"),
  path("delete/<int:pk>", DeleteUser.as_view(), name="delete-user"),
  path("detail/<int:pk>", DetailUser.as_view(), name="detail-user"),
  path("assign/<int:pk>", AssignFacilityUser.as_view(), name="assign-facility"),
  path("change/<int:pk>", ChangeFacilityUser.as_view(), name="change-facility"),
  path("view/", ViewUser.as_view(), name="view-user")
]
