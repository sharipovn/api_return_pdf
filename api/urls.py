from django.urls import path,include
from . import views

urlpatterns = [
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('generate-ies-pdf/', views.generate_ies_pdf, name='generate_ies_pdf'),
    path('test_view/', views.test_view, name='test_view'),
    path('ies_test_view/', views.ies_test_view, name='ies_test_view'),
    path('login/',views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
