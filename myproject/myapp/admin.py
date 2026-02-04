from django.contrib import admin
from .models import *

admin.site.register([CustomUser,Department,Doctor,Patient,Appointment])
