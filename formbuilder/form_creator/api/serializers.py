from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from formbuilder.form_creator.models import Question, FormTemplate, FormSubmission


class FeedBackFormQuestionSerialser(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ('created_by', 'updated_by')

class FormDetailSerialiser(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = FormTemplate
        exclude = ('created_by','updated_by','status','validity_start','vallidity_end')

    def get_questions(self,obj):
        all_qestions = obj.questions.all()
        return FeedBackFormQuestionSerialser(all_qestions,many=True).data


class FormSubmissionSerialiser(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(FormSubmissionSerialiser, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = FormSubmission
        fields = '__all__'

    def validate(self, attrs):
        question = attrs.get("question")
        if question.required:
            if not attrs.get("answer"):
                raise ValidationError({"answer":"answer_cant_be blank "})
        if question.required and question.question_type in [Question.MULTIPLE_CHOICE,Question.BOOLEAN]:
            if not f"{attrs.get('answer')}" in question.question_options:
                raise ValidationError({"answer": "Question Option does not match"})
        return attrs
