from django.contrib import admin
from .models import Status
from .forms import StatusForm


# Register your models here.
class StatusAdmin(admin.ModelAdmin):
    list_display = ['user', '__str__', 'image']
    form = StatusForm

    # class Meta:
    #     model = Status


admin.site.register(Status, StatusAdmin)
