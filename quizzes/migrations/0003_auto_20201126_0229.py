# Generated by Django 3.1.3 on 2020-11-25 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0002_auto_20201125_1816'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='user',
            new_name='creator',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='user',
            new_name='creator',
        ),
        migrations.RenameField(
            model_name='quiz',
            old_name='user',
            new_name='creator',
        ),
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, to='quizzes.Tag'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='questions',
            field=models.ManyToManyField(blank=True, to='quizzes.Question'),
        ),
    ]