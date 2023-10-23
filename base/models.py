from django.db import models

class Lesson(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)

class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    lesson_id = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question = models.TextField()
    is_multiple = models.BooleanField(default=False)

class PossibleAnswer(models.Model):
    id = models.IntegerField(primary_key=True)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    possible_answer = models.TextField()
    is_correct = models.BooleanField(default=False)
