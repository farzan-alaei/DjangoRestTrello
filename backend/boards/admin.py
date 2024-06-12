from django.contrib import admin
from boards.models import Board, List, Task, Comment, Label

# Register your models here.
admin.site.register(Board)
admin.site.register(List)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Label)
