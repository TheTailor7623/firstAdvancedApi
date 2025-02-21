# Generated by Django 5.1.6 on 2025-02-19 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lifestagesareas',
            name='area',
        ),
        migrations.RemoveField(
            model_name='resourcesareas',
            name='area',
        ),
        migrations.RemoveField(
            model_name='lifestagesareas',
            name='lifestage',
        ),
        migrations.RemoveField(
            model_name='userslifestages',
            name='lifestage',
        ),
        migrations.RemoveField(
            model_name='resourceslifestages',
            name='lifestage',
        ),
        migrations.RemoveField(
            model_name='milestoneslifestages',
            name='lifestage',
        ),
        migrations.RemoveField(
            model_name='milestoneslifestages',
            name='milestone',
        ),
        migrations.RemoveField(
            model_name='milestonestasks',
            name='milestone',
        ),
        migrations.RemoveField(
            model_name='resourcesmilestones',
            name='milestone',
        ),
        migrations.RemoveField(
            model_name='milestonesprojects',
            name='milestone',
        ),
        migrations.RemoveField(
            model_name='milestonessubtasks',
            name='milestone',
        ),
        migrations.RemoveField(
            model_name='milestonesprojects',
            name='project',
        ),
        migrations.RemoveField(
            model_name='milestonessubtasks',
            name='subtask',
        ),
        migrations.RemoveField(
            model_name='milestonestasks',
            name='task',
        ),
        migrations.RemoveField(
            model_name='resourcesprojects',
            name='project',
        ),
        migrations.RemoveField(
            model_name='resourcesareas',
            name='resource',
        ),
        migrations.RemoveField(
            model_name='resourceslifestages',
            name='resource',
        ),
        migrations.RemoveField(
            model_name='resourcesmilestones',
            name='resource',
        ),
        migrations.RemoveField(
            model_name='resourcesprojects',
            name='resource',
        ),
        migrations.RemoveField(
            model_name='resourcesusers',
            name='resource',
        ),
        migrations.RemoveField(
            model_name='resourcestasks',
            name='resource',
        ),
        migrations.RemoveField(
            model_name='resourcessubtasks',
            name='resource',
        ),
        migrations.RemoveField(
            model_name='resourcessubtasks',
            name='subtask',
        ),
        migrations.RemoveField(
            model_name='resourcestasks',
            name='task',
        ),
        migrations.RemoveField(
            model_name='resourcesusers',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userslifestages',
            name='user',
        ),
        migrations.DeleteModel(
            name='AreasModel',
        ),
        migrations.DeleteModel(
            name='LifestagesAreas',
        ),
        migrations.DeleteModel(
            name='LifestagesModel',
        ),
        migrations.DeleteModel(
            name='MilestonesLifestages',
        ),
        migrations.DeleteModel(
            name='MilestonesModel',
        ),
        migrations.DeleteModel(
            name='MilestonesProjects',
        ),
        migrations.DeleteModel(
            name='MilestonesSubtasks',
        ),
        migrations.DeleteModel(
            name='MilestonesTasks',
        ),
        migrations.DeleteModel(
            name='ProjectsModel',
        ),
        migrations.DeleteModel(
            name='ResourcesAreas',
        ),
        migrations.DeleteModel(
            name='ResourcesLifestages',
        ),
        migrations.DeleteModel(
            name='ResourcesMilestones',
        ),
        migrations.DeleteModel(
            name='ResourcesProjects',
        ),
        migrations.DeleteModel(
            name='ResourcesModel',
        ),
        migrations.DeleteModel(
            name='ResourcesSubTasks',
        ),
        migrations.DeleteModel(
            name='SubTasksModel',
        ),
        migrations.DeleteModel(
            name='ResourcesTasks',
        ),
        migrations.DeleteModel(
            name='ResourcesUsers',
        ),
        migrations.DeleteModel(
            name='UsersLifestages',
        ),
    ]
