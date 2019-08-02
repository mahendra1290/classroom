from django.db import models

class Assignment(models.Model):
    title         = models.CharField(max_length = 100)
    instructions  = models.CharField(max_length = 100)
    due_date      = models.DateTimeField()
    assigned_date = models.DateTimeField()

    def __str__(self):
        return self.title

class AssignmentsImage(models.Model):
    filename   = models.CharField(max_length = 100)
    image      = models.ImageField(upload_to = 'images/')
    assignment = models.ForeignKey(Assignment, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.image)






