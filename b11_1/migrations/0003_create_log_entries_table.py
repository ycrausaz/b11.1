from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('b11_1', '0002_create_views'),  # Make sure this matches your last migration
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('level', models.CharField(max_length=20)),
                ('message', models.TextField()),
            ],
            options={
                'db_table': 'b11_1_log_entries',
            },
        ),
    ]
