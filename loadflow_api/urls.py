"""
URL configuration for loadflow_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from loadflow.views import run_load_flow
from django.urls import path
from loadflow.views import BusListView, LineListView, LoadListView, LoadFlowAnalysisView, BusDetailView, LineDetailView, LoadDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buses/', BusListView.as_view(), name='bus-list'),
    path('buses/<int:pk>/', BusDetailView.as_view(), name='bus-detail'),  # ✅ Allows GET, PUT, PATCH, DELETE
    path('lines/', LineListView.as_view(), name='line-list'),
    path('lines/<int:pk>/', LineDetailView.as_view(), name='line-detail'),  # ✅ Allows GET, PUT, PATCH, DELETE
    path('loads/', LoadListView.as_view(), name='load-list'),
    path('loads/<int:pk>/', LoadDetailView.as_view(), name='load-detail'),  # ✅ Allows GET, PUT, PATCH, DELETE
    path('loadflow/', LoadFlowAnalysisView.as_view(), name='loadflow-analysis'),
    path('loadflow/run/', run_load_flow, name='run_load_flow'),
]
