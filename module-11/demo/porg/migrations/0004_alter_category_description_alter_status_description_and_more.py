# Generated by Django 5.1.6 on 2025-03-09 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('porg', '0003_category_status_task_delete_todoitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(null=True),
        ),
    ]
