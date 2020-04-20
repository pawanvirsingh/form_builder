from django.contrib import admin
from .models import Question, FormSubmission, FormTemplate


class FormTemplateAdmin(admin.ModelAdmin):
    list_display = ('form_link', )


# Register your models here.
admin.site.register(Question)
admin.site.register(FormSubmission)
admin.site.register(FormTemplate, FormTemplateAdmin)
