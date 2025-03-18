from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin
import app.views
from VR import settings

urlpatterns = [
    path('admin/', admin.site.urls),  # This line is added to access the Django admin interface
    path('', app.views.home, name='home'),
    path('login/', app.views.login, name='login'),
    path('adddrug/', app.views.add_drug, name='add_drug'),  # Add trailing slashes for consistency
    path('drugmaster/', app.views.drug_master, name='drug_master'),
    path('adddoctor/', app.views.add_doctor, name='add_doctor'),
    path('doctormaster/', app.views.doctor_master, name='doctor_master'),
    path('assigndoctor/', app.views.assign_doctor, name='assign_doctor'),
    path('drugdoctormaster/', app.views.drug_doctor_master, name='drug_doctor_master'),
    path('searchdrug/', app.views.search_drug, name='search_drug'),
    path('viewdoctors/', app.views.view_doctors, name='view_doctors'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
