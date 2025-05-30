# Generated by Django 5.1.3 on 2025-01-14 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthAgencyBridges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_agency_bridges',
                'db_table_comment': '管控單位 - 橋梁關係中間表',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthAgencyUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_agency_users',
                'db_table_comment': '使用者隸屬於哪個單位',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Bridge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
                ('bno', models.CharField(blank=True, db_comment='橋梁編號: 同步市政府對外提供之橋梁編號， EX: 桃市府南崁橋 - 300，北市府康樂橋 - D036', max_length=10, null=True)),
                ('name', models.CharField(max_length=20)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('address_name', models.CharField(max_length=20)),
                ('id_address_name', models.CharField(max_length=20)),
                ('photo_name', models.CharField(max_length=200)),
                ('base64', models.TextField()),
                ('deleted', models.IntegerField()),
            ],
            options={
                'db_table': 'bridge',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Earthquake',
            fields=[
                ('earthquakeno', models.IntegerField(primary_key=True, serialize=False)),
                ('reportcolor', models.CharField(blank=True, max_length=10, null=True)),
                ('origintime', models.DateTimeField(blank=True, null=True)),
                ('reportcontent', models.CharField(blank=True, max_length=200, null=True)),
                ('reportimageuri', models.CharField(blank=True, max_length=200, null=True)),
                ('epicenterlocation', models.CharField(blank=True, db_column='epiCenterlocation', max_length=50, null=True)),
                ('magnitudetype', models.CharField(blank=True, max_length=10, null=True)),
                ('magnitudevalue', models.FloatField(blank=True, null=True)),
                ('shakemapimageuri', models.CharField(blank=True, max_length=200, null=True)),
                ('depthvalue', models.FloatField(blank=True, null=True)),
                ('depthtype', models.CharField(blank=True, max_length=10, null=True)),
                ('longitude', models.FloatField(null=True)),
                ('latitude', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'mearthquake',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.IntegerField()),
                ('sensor', models.IntegerField()),
                ('type', models.CharField(blank=True, max_length=20, null=True)),
                ('ip', models.IntegerField(blank=True, null=True)),
                ('sensor_location', models.CharField(blank=True, max_length=20, null=True)),
                ('detailed_location', models.CharField(blank=True, max_length=20, null=True)),
                ('cable_mass_per_length', models.FloatField(blank=True, null=True)),
                ('cable_length', models.FloatField(blank=True, null=True)),
                ('e', models.FloatField(blank=True, db_column='E', null=True)),
                ('i', models.FloatField(blank=True, db_column='I', null=True)),
                ('m', models.FloatField(blank=True, null=True)),
                ('health_alert_index', models.IntegerField(blank=True, null=True)),
                ('health_move_index', models.IntegerField(blank=True, null=True)),
                ('event_alert_index', models.IntegerField(blank=True, null=True)),
                ('event_move_index', models.IntegerField(blank=True, null=True)),
                ('cable_force_alert_index', models.IntegerField(blank=True, null=True)),
                ('cable_force_move_index', models.IntegerField(blank=True, null=True)),
                ('load_carry_capacity_alert_index', models.FloatField(blank=True, null=True)),
                ('load_carry_capacity_move_index', models.FloatField(blank=True, null=True)),
                ('effective_pier_length_alert_index', models.FloatField(blank=True, null=True)),
                ('effective_pier_length_move_index', models.FloatField(blank=True, null=True)),
                ('f_var_ref', models.FloatField(blank=True, null=True)),
                ('image_coordinate', models.CharField(blank=True, max_length=50, null=True)),
                ('current_status', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sensor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Typhoon',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('cht_name', models.CharField(blank=True, max_length=10, null=True)),
                ('eng_name', models.CharField(blank=True, max_length=50, null=True)),
                ('sea_start_datetime', models.DateTimeField(blank=True, null=True)),
                ('max_intensity', models.CharField(blank=True, max_length=3, null=True)),
                ('sea_end_datetime', models.DateTimeField(blank=True, null=True)),
                ('warning_count', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'typhoon_data',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='BridgeName',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='DataOrigin',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.DeleteModel(
            name='Mearthquake',
        ),
        migrations.DeleteModel(
            name='SensorName',
        ),
        migrations.DeleteModel(
            name='TyphoonData',
        ),
    ]
