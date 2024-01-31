...
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="Backend APIs",
      default_version='v1',
      # description="Test description",
      description = (
         "This API powers the backend functionality of a pharmacy website, facilitating operations such as managing inventory, \n"
         "processing orders, handling user authentication, and providing access to product information.\n "
         "It offers a seamless integration between the front-end user interface and the underlying database, \n"
         "ensuring efficient and secure communication for all pharmacy-related tasks."
      ),

      # description="This API powers the backend functionality of a pharmacy website, facilitating\
      #   operations such as managing inventory, processing orders, handling user authentication, \
      #    and providing access to product information. It offers a seamless integration between \
      #       the front-end user interface and the underlying database, ensuring efficient and secure\
      #            communication for all pharmacy-related tasks.",

      # terms_of_service="https://www.google.com/policies/terms/",
      # contact=openapi.Contact(email="contact@snippets.local"),
      # license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
