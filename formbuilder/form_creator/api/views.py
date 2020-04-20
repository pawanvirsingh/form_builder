from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from formbuilder.form_creator.api.serializers import FormDetailSerialiser, FormSubmissionSerialiser
from formbuilder.form_creator.models import FormTemplate, FormSubmission


class FormDetailsViewset(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = FormDetailSerialiser
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FormTemplate.objects.all()




class FormSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = FormSubmissionSerialiser
    allowed_method = ['post']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = FormSubmission.objects.all()
        return qs

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(FormSubmissionViewSet, self).get_serializer(*args, **kwargs)
