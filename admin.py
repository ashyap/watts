from django.contrib import admin
from .models import Company, Employee, EmployeeLog

admin.site.register(Company);
admin.site.register(Employee);
admin.site.register(EmployeeLog);
