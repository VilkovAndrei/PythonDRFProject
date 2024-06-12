from rest_framework.documentation import include_docs_urls
from django.urls import path
# from docs.apps import DocsConfig


# app_name = 'docs'

urlpatterns = [
    path('docs/', include_docs_urls(title='API Documentation')),
]