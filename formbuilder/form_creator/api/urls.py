from rest_framework.routers import SimpleRouter

from formbuilder.form_creator.api import views

router = SimpleRouter()
router.register('get-form', views.FormDetailsViewset, basename='form-detail')
router.register('submit-form', views.FormSubmissionViewSet, basename='submit-form')


