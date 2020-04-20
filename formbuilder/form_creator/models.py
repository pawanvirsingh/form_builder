import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    "Comman fields that is used in almost every table "
    id = models.UUIDField(primary_key=True, verbose_name='id', default=uuid.uuid4, editable=False)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), related_name='created_%(class)s_related',
                                   on_delete=models.SET_NULL, null=True, )
    updated_by = models.ForeignKey(get_user_model(), related_name='updated_%(class)s_related',
                                   on_delete=models.SET_NULL, null=True, )

    class Meta:
        abstract = True


class Question(BaseModel):
    """This is model for  Suestion """

    MULTIPLE_CHOICE = 'multiple-choices'
    BOOLEAN = 'bool'
    TEXT = 'text'

    TYPE_CHOICES = (
        (MULTIPLE_CHOICE, "Multiple Choice type "),
        (BOOLEAN, 'Boolean'),
        (TEXT, 'Text'),)
    question_text = models.CharField(max_length=500, null=True, blank=True)
    question_type = models.CharField(default=TEXT, choices=TYPE_CHOICES, max_length=50)
    question_options = models.TextField(null=True, blank=True, help_text="Please provide answers in comma separeted")
    order = models.IntegerField(default=0)
    placeholder = models.CharField(max_length=50, null=True, blank=True)
    help_text = models.CharField(max_length=100, null=True, blank=True)
    required = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question_text}"

    def save(self, *args, **kwargs):
        if not self.id:
            if self.question_type == self.BOOLEAN:
                self.question_options = f'{True}{False}'
        super(Question, self).save(*args, **kwargs)

    class Meta:
        ordering = ['order']


class FormTemplate(BaseModel):
    """
    This is Feed back form form data

    """
    PUBLISHED = 'published'
    DRAFT = 'draft'
    DISCARDED = 'discarded'

    STATUS_CHOICES = (
        (PUBLISHED, "Published"),
        (DRAFT, "Draft"),
        (DISCARDED, "Discarded"),
    )
    form_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    questions = models.ManyToManyField(Question)
    validity_start = models.DateTimeField(null=True, blank=True)
    vallidity_end = models.DateTimeField(null=True, blank=True)
    status = models.CharField(default=PUBLISHED, choices=STATUS_CHOICES, max_length=50)
    form_submission_response = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.form_name

    def form_link(self):
        return f'{settings.FORM_BASE_URL}/{self.pk}'


class FormSubmission(BaseModel):
    """
    This will store response submit by the User regarding  form


    response is like {"questionid":{Question:ans,"questionid":ans,}

    """
    form = models.ForeignKey(FormTemplate, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    answer = models.TextField(null=True, blank=True)
    answered_by = models.ForeignKey(get_user_model(), related_name="answered_by", null=True, blank=True,
                                    on_delete=models.SET_NULL)

    class Meta:
        unique_together = ['form', 'question', 'answered_by']

    def __str__(self):
        return f'{self.form} -- {self.answered_by}'
