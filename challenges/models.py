from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField
from django.conf import settings

class DescriptionField(models.TextField):
    pass

class Question(models.Model):
    title = models.CharField(max_length=100)
    question_text = models.CharField(max_length=200)
    description = DescriptionField()
    sample_code = models.TextField()
    answer_code = models.TextField()
    test_expression = ArrayField(models.CharField(max_length=30, blank=True), null=True, default=list)
    test_value = ArrayField(models.CharField(max_length=30, blank=True), null=True, default=list)
    max_score = models.FloatField(default=100.)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    due_date = models.DateTimeField('due date')
    # sample_file = models.FileField(null=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    class Meta:
        unique_together = ['question', 'user']

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trial = models.PositiveIntegerField(default=0)
    answer_code = models.TextField(blank=True)
    test_value = ArrayField(models.CharField(max_length=30, blank=True), null=True, default=list)
    score = models.FloatField(default=0)
    pub_date = models.DateTimeField('date updated', auto_now_add=True)


    def __str__(self):
        return self.question.title + "_" + self.user.student_id



