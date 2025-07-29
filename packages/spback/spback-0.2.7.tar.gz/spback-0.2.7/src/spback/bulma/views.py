from django.shortcuts import render
from django.views.generic import View

# Create your views here.


class BaseView(View):
  system_name = "Document"
  description = "Document"
  keywords = "Document"
