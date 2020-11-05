# Generated by Django 3.1.3 on 2020-11-03 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('question_text', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, help_text='Any additional details related to this question')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('quiz_name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, help_text='Any additional details related to this quiz')),
                ('questions', models.ManyToManyField(to='quizzes.Question')),
            ],
            options={
                'verbose_name': 'Quizzes',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='quizzes.Tag'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=255)),
                ('votes', models.IntegerField(default=0, editable=False, help_text='Number of times this answer has been chosen.')),
                ('is_correct_answer', models.BooleanField(default=False, help_text='Whether or not this answer is correct.')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.question')),
            ],
        ),
    ]