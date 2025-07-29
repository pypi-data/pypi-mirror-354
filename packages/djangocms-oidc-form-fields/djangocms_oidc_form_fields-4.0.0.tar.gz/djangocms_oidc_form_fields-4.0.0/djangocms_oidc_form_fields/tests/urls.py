from aldryn_forms.urls import urlpatterns as aldryn_forms_urlpatterns
from cms.views import details
from django.urls import re_path

urlpatterns = []
urlpatterns.extend(aldryn_forms_urlpatterns)
urlpatterns.append(re_path(r'^(?P<slug>[0-9A-Za-z-_.//]+)/$', details, name='pages-details-by-slug'))
