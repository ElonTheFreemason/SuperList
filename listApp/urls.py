from django.urls import path
from .views import (
	ListsListView,
	ListsDetailView,
	ListsCreateView,
	ListsUpdateView,
	ListsDeleteView,
	ElementsDetailView,
	ElementsUpdateView,
	ElementsDeleteView,
	ViewersDetailView,
	ViewersCreateView,
	ViewersDeleteView,
)
from . import views

urlpatterns = [
    path('', views.home, name = "list-home"),
    path('list/<int:pk>/', views.detail, name = "list-detail"),
    path('element/<int:pk>', ElementsDetailView.as_view(), name = "element-detail"),
    path('viewer/<int:pk>', ViewersDetailView.as_view(), name = "viewer-detail"),
    path('list/<int:pk>/update', ListsUpdateView.as_view(), name = "list-update"),
    path('list/<int:pk>/delete', ListsDeleteView.as_view(), name = "list-delete"),
    path('element/<int:pk>/update', ElementsUpdateView.as_view(), name = "element-update"),
    path('element/<int:pk>/delete', ElementsDeleteView.as_view(), name = "element-delete"),
    path('viewer/<int:pk>/delete', ViewersDeleteView.as_view(), name = "viewer-delete"),
    path('list/new/', ListsCreateView.as_view(), name = "list-create"),
    path('list/<int:pk>/viewer/new/', ViewersCreateView.as_view(), name = "viewer-create"),
    path('shared/', views.shared, name = "list-shared"),
]
