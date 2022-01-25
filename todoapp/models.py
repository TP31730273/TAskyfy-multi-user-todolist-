from django.db import models

# Create your models here.

class Department(models.Model):
    Name = models.CharField(max_length=30,null=True,default='')
    JObTitles = models.TextField(max_length=300)
    class Meta:
        db_table = 'Department'
    
    def __str__(self):
        return self.Name

class Master(models.Model):
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=12)
    IsActive = models.BooleanField(default=False)

    class Meta:
        db_table = 'master'
    
    def __str__(self):
        return self.Email

choice_gender=(
    ('m','male'),
    ('f','female'),
)

class Profile(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True,default='')
    FullName = models.CharField(max_length=30,null=True,default='')
    JobTitle = models.CharField(max_length=30,null=True,default='')
    Mobile = models.CharField(max_length=10,null=True,default='')
    Birthdate = models.DateField(auto_created=True,default='1999-08-01')
    RefID = models.CharField(max_length=30,default='')
    Gender = models.CharField(max_length=10,null=True,choices=choice_gender)
    Country = models.CharField(max_length=10,null=True,default='')
    State = models.CharField(max_length=25,null=True,default='')
    City = models.CharField(max_length=25,null=True,default='')
    Address = models.TextField(max_length=150,null=True,default='')

    class Meta:
        db_table = 'profile'
    
    def __str__(self):
        return self.Master.Email

class profile_pic(models.Model):
    Master = models.ForeignKey(Master,on_delete=models.CASCADE)
    Img = models.FileField(upload_to="images",null=True)

    class Meta:
        db_table = 'profile_pic'
    
    def __str__(self):
        return self.Master.Email
        
class connection(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=100,default='')
    class Meta:
        db_table = 'connection'

    def __str__(self):
        return self.Master.Email
        
class connectionRequet(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'connectionRequet'

    
class ToDo(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    # profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Title = models.TextField(max_length=150)
    Tags = models.TextField(max_length=150)
    Deadline = models.DateTimeField(auto_created=True)
    Description = models.TextField(max_length=150)
    Iscomplete=models.BooleanField(default=False)

    class Meta:
        db_table = 'ToDO'
    
    def __str__(self):
        return self.master.Email

class ToDoMember(models.Model):
    todo = models.ForeignKey(ToDo, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ToDoMember'

    def __str__(self):
        return self.todo.Title

class ToDOparticipant(models.Model):
    todo = models.ForeignKey(ToDo, on_delete=models.CASCADE)
    Connection = models.ForeignKey(connection, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ToDoParticipant' 
    
    def __str__(self):
        return self.Connection.profile.FullName