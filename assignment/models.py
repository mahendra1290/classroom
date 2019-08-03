from django.db import models

class Assignment(models.Model):
    title = models.CharField(max_length=100)
    instructions = models.CharField(max_length=100)
    due_date = models.DateField(null=True)
    pub_date = models.DateField(null=True)

    def __str__(self):
        return self.title

class AssignmentsFile(models.Model):
    filename   = models.CharField(max_length = 100)
    file       = models.FileField(upload_to = 'images/')
    assignment = models.ForeignKey(Assignment, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.file)






