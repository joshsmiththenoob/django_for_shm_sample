# Generated by Django 5.1.3 on 2025-03-19 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_alter_weatherdailyhistorydata_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='EngineeringFirm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'engineering_firm',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LocalEarthquake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earthquakeno', models.IntegerField()),
                ('reportcolor', models.CharField(blank=True, max_length=10, null=True)),
                ('origintime', models.DateTimeField(blank=True, null=True)),
                ('reportcontent', models.CharField(blank=True, max_length=200, null=True)),
                ('reportimageuri', models.CharField(blank=True, max_length=200, null=True)),
                ('epicenterlocation', models.CharField(blank=True, db_column='epiCenterlocation', max_length=50, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('magnitudetype', models.CharField(blank=True, max_length=10, null=True)),
                ('magnitudevalue', models.FloatField(blank=True, null=True)),
                ('shakemapimageuri', models.CharField(blank=True, max_length=200, null=True)),
                ('depthvalue', models.FloatField(blank=True, null=True)),
                ('depthtype', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'local_earthquake',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StructureDailyHistoryData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.IntegerField()),
                ('mid', models.IntegerField(blank=True, null=True)),
                ('time', models.DateTimeField()),
                ('max_health', models.FloatField(blank=True, null=True)),
                ('up_health', models.FloatField(blank=True, null=True)),
                ('mid_health', models.FloatField(blank=True, null=True)),
                ('down_health', models.FloatField(blank=True, null=True)),
                ('min_health', models.FloatField(blank=True, null=True)),
                ('max_seismic', models.FloatField(blank=True, null=True)),
                ('up_seismic', models.FloatField(blank=True, null=True)),
                ('mid_seismic', models.FloatField(blank=True, null=True)),
                ('down_seismic', models.FloatField(blank=True, null=True)),
                ('min_seismic', models.FloatField(blank=True, null=True)),
                ('max_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('up_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('mid_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('down_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('min_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('max_bandwidth', models.FloatField(blank=True, null=True)),
                ('up_bandwidth', models.FloatField(blank=True, null=True)),
                ('mid_bandwidth', models.FloatField(blank=True, null=True)),
                ('down_bandwidth', models.FloatField(blank=True, null=True)),
                ('min_bandwidth', models.FloatField(blank=True, null=True)),
                ('max_cable_force', models.FloatField(blank=True, null=True)),
                ('up_cable_force', models.FloatField(blank=True, null=True)),
                ('mid_cable_force', models.FloatField(blank=True, null=True)),
                ('down_cable_force', models.FloatField(blank=True, null=True)),
                ('min_cable_force', models.FloatField(blank=True, null=True)),
                ('max_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('up_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('mid_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('down_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('min_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('max_damping_ratio', models.FloatField(blank=True, null=True)),
                ('up_damping_ratio', models.FloatField(blank=True, null=True)),
                ('mid_damping_ratio', models.FloatField(blank=True, null=True)),
                ('down_damping_ratio', models.FloatField(blank=True, null=True)),
                ('min_damping_ratio', models.FloatField(blank=True, null=True)),
                ('max_frequency_variance', models.FloatField(blank=True, null=True)),
                ('up_frequency_variance', models.FloatField(blank=True, null=True)),
                ('mid_frequency_variance', models.FloatField(blank=True, null=True)),
                ('down_frequency_variance', models.FloatField(blank=True, null=True)),
                ('min_frequency_variance', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'structure_daily_history_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StructureEarthquakeEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_marker', models.CharField(max_length=10)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('max_health', models.FloatField(blank=True, null=True)),
                ('up_health', models.FloatField(blank=True, null=True)),
                ('mid_health', models.FloatField(blank=True, null=True)),
                ('down_health', models.FloatField(blank=True, null=True)),
                ('min_health', models.FloatField(blank=True, null=True)),
                ('max_seismic', models.FloatField(blank=True, null=True)),
                ('up_seismic', models.FloatField(blank=True, null=True)),
                ('mid_seismic', models.FloatField(blank=True, null=True)),
                ('down_seismic', models.FloatField(blank=True, null=True)),
                ('min_seismic', models.FloatField(blank=True, null=True)),
                ('max_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('up_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('mid_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('down_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('min_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('max_bandwidth', models.FloatField(blank=True, null=True)),
                ('up_bandwidth', models.FloatField(blank=True, null=True)),
                ('mid_bandwidth', models.FloatField(blank=True, null=True)),
                ('down_bandwidth', models.FloatField(blank=True, null=True)),
                ('min_bandwidth', models.FloatField(blank=True, null=True)),
                ('max_cable_force', models.FloatField(blank=True, null=True)),
                ('up_cable_force', models.FloatField(blank=True, null=True)),
                ('mid_cable_force', models.FloatField(blank=True, null=True)),
                ('down_cable_force', models.FloatField(blank=True, null=True)),
                ('min_cable_force', models.FloatField(blank=True, null=True)),
                ('max_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('up_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('mid_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('down_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('min_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('max_damping_ratio', models.FloatField(blank=True, null=True)),
                ('up_damping_ratio', models.FloatField(blank=True, null=True)),
                ('mid_damping_ratio', models.FloatField(blank=True, null=True)),
                ('down_damping_ratio', models.FloatField(blank=True, null=True)),
                ('min_damping_ratio', models.FloatField(blank=True, null=True)),
                ('max_frequency_variance', models.FloatField(blank=True, null=True)),
                ('up_frequency_variance', models.FloatField(blank=True, null=True)),
                ('mid_frequency_variance', models.FloatField(blank=True, null=True)),
                ('down_frequency_variance', models.FloatField(blank=True, null=True)),
                ('min_frequency_variance', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'structure_earthquake_event',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StructureFinalFloodResistance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('freq_var_ratio', models.FloatField(blank=True, null=True)),
                ('health_var_ratio', models.FloatField(blank=True, null=True)),
                ('cable_force_var_ratio', models.FloatField(blank=True, null=True)),
                ('load_carry_capacity_var_ratio', models.FloatField(blank=True, null=True)),
                ('max_during_freq_var_ratio', models.FloatField(blank=True, null=True)),
                ('max_during_health_var_ratio', models.FloatField(blank=True, null=True)),
                ('max_during_bridge_var_ratio', models.FloatField(blank=True, null=True)),
                ('post_event_health', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'structure_final_flood_resistance',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StructureFinalSeismicResistance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('freq_var_ratio', models.FloatField(blank=True, null=True)),
                ('health_var_ratio', models.FloatField(blank=True, null=True)),
                ('cable_force_var_ratio', models.FloatField(blank=True, null=True)),
                ('load_carry_capacity_var_ratio', models.FloatField(blank=True, null=True)),
                ('max_during_freq_var_ratio', models.FloatField(blank=True, null=True)),
                ('max_during_health_var_ratio', models.FloatField(blank=True, null=True)),
                ('max_during_bridge_var_ratio', models.FloatField(blank=True, null=True)),
                ('post_event_health', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'structure_final_seismic_resistance',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StructureFloodResistance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.BigIntegerField(blank=True, null=True)),
                ('freq_var_ratio', models.FloatField(blank=True, null=True)),
                ('health_var_ratio', models.FloatField(blank=True, null=True)),
                ('cable_force_var_ratio', models.FloatField(blank=True, null=True)),
                ('load_carry_capacity_var_ratio', models.TextField(blank=True, null=True)),
                ('max_during_freq_var_ratio', models.TextField(blank=True, null=True)),
                ('max_during_health_var_ratio', models.TextField(blank=True, null=True)),
                ('max_during_bridge_var_ratio', models.TextField(blank=True, null=True)),
                ('post_event_health', models.FloatField(blank=True, null=True)),
                ('bid', models.BigIntegerField(blank=True, null=True)),
                ('mid', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'structure_flood_resistance',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StructureHourlyHistoryData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.IntegerField()),
                ('mid', models.IntegerField(blank=True, null=True)),
                ('time', models.DateTimeField()),
                ('max_health', models.FloatField(blank=True, null=True)),
                ('up_health', models.FloatField(blank=True, null=True)),
                ('mid_health', models.FloatField(blank=True, null=True)),
                ('down_health', models.FloatField(blank=True, null=True)),
                ('min_health', models.FloatField(blank=True, null=True)),
                ('max_seismic', models.FloatField(blank=True, null=True)),
                ('up_seismic', models.FloatField(blank=True, null=True)),
                ('mid_seismic', models.FloatField(blank=True, null=True)),
                ('down_seismic', models.FloatField(blank=True, null=True)),
                ('min_seismic', models.FloatField(blank=True, null=True)),
                ('max_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('up_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('mid_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('down_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('min_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('max_bandwidth', models.FloatField(blank=True, null=True)),
                ('up_bandwidth', models.FloatField(blank=True, null=True)),
                ('mid_bandwidth', models.FloatField(blank=True, null=True)),
                ('down_bandwidth', models.FloatField(blank=True, null=True)),
                ('min_bandwidth', models.FloatField(blank=True, null=True)),
                ('max_cable_force', models.FloatField(blank=True, null=True)),
                ('up_cable_force', models.FloatField(blank=True, null=True)),
                ('mid_cable_force', models.FloatField(blank=True, null=True)),
                ('down_cable_force', models.FloatField(blank=True, null=True)),
                ('min_cable_force', models.FloatField(blank=True, null=True)),
                ('max_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('up_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('mid_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('down_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('min_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('max_damping_ratio', models.FloatField(blank=True, null=True)),
                ('up_damping_ratio', models.FloatField(blank=True, null=True)),
                ('mid_damping_ratio', models.FloatField(blank=True, null=True)),
                ('down_damping_ratio', models.FloatField(blank=True, null=True)),
                ('min_damping_ratio', models.FloatField(blank=True, null=True)),
                ('max_frequency_variance', models.FloatField(blank=True, null=True)),
                ('up_frequency_variance', models.FloatField(blank=True, null=True)),
                ('mid_frequency_variance', models.FloatField(blank=True, null=True)),
                ('down_frequency_variance', models.FloatField(blank=True, null=True)),
                ('min_frequency_variance', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'structure_hourly_history_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StructureMinuteHistoryData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.IntegerField()),
                ('mid', models.IntegerField(blank=True, null=True)),
                ('time', models.DateTimeField()),
                ('max_health', models.FloatField(blank=True, null=True)),
                ('up_health', models.FloatField(blank=True, null=True)),
                ('mid_health', models.FloatField(blank=True, null=True)),
                ('down_health', models.FloatField(blank=True, null=True)),
                ('min_health', models.FloatField(blank=True, null=True)),
                ('max_seismic', models.FloatField(blank=True, null=True)),
                ('up_seismic', models.FloatField(blank=True, null=True)),
                ('mid_seismic', models.FloatField(blank=True, null=True)),
                ('down_seismic', models.FloatField(blank=True, null=True)),
                ('min_seismic', models.FloatField(blank=True, null=True)),
                ('max_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('up_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('mid_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('down_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('min_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('max_bandwidth', models.FloatField(blank=True, null=True)),
                ('up_bandwidth', models.FloatField(blank=True, null=True)),
                ('mid_bandwidth', models.FloatField(blank=True, null=True)),
                ('down_bandwidth', models.FloatField(blank=True, null=True)),
                ('min_bandwidth', models.FloatField(blank=True, null=True)),
                ('max_cable_force', models.FloatField(blank=True, null=True)),
                ('up_cable_force', models.FloatField(blank=True, null=True)),
                ('mid_cable_force', models.FloatField(blank=True, null=True)),
                ('down_cable_force', models.FloatField(blank=True, null=True)),
                ('min_cable_force', models.FloatField(blank=True, null=True)),
                ('max_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('up_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('mid_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('down_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('min_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('max_damping_ratio', models.FloatField(blank=True, null=True)),
                ('up_damping_ratio', models.FloatField(blank=True, null=True)),
                ('mid_damping_ratio', models.FloatField(blank=True, null=True)),
                ('down_damping_ratio', models.FloatField(blank=True, null=True)),
                ('min_damping_ratio', models.FloatField(blank=True, null=True)),
                ('max_frequency_variance', models.FloatField(blank=True, null=True)),
                ('up_frequency_variance', models.FloatField(blank=True, null=True)),
                ('mid_frequency_variance', models.FloatField(blank=True, null=True)),
                ('down_frequency_variance', models.FloatField(blank=True, null=True)),
                ('min_frequency_variance', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'structure_minute_history_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StructureTyphoonEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_marker', models.CharField(max_length=10)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('max_health', models.FloatField(blank=True, null=True)),
                ('up_health', models.FloatField(blank=True, null=True)),
                ('mid_health', models.FloatField(blank=True, null=True)),
                ('down_health', models.FloatField(blank=True, null=True)),
                ('min_health', models.FloatField(blank=True, null=True)),
                ('max_seismic', models.FloatField(blank=True, null=True)),
                ('up_seismic', models.FloatField(blank=True, null=True)),
                ('mid_seismic', models.FloatField(blank=True, null=True)),
                ('down_seismic', models.FloatField(blank=True, null=True)),
                ('min_seismic', models.FloatField(blank=True, null=True)),
                ('max_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('up_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('mid_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('down_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('min_centroid_frequency', models.FloatField(blank=True, null=True)),
                ('max_bandwidth', models.FloatField(blank=True, null=True)),
                ('up_bandwidth', models.FloatField(blank=True, null=True)),
                ('mid_bandwidth', models.FloatField(blank=True, null=True)),
                ('down_bandwidth', models.FloatField(blank=True, null=True)),
                ('min_bandwidth', models.FloatField(blank=True, null=True)),
                ('max_cable_force', models.FloatField(blank=True, null=True)),
                ('up_cable_force', models.FloatField(blank=True, null=True)),
                ('mid_cable_force', models.FloatField(blank=True, null=True)),
                ('down_cable_force', models.FloatField(blank=True, null=True)),
                ('min_cable_force', models.FloatField(blank=True, null=True)),
                ('max_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('up_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('mid_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('down_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('min_load_carry_capacity', models.FloatField(blank=True, null=True)),
                ('max_damping_ratio', models.FloatField(blank=True, null=True)),
                ('up_damping_ratio', models.FloatField(blank=True, null=True)),
                ('mid_damping_ratio', models.FloatField(blank=True, null=True)),
                ('down_damping_ratio', models.FloatField(blank=True, null=True)),
                ('min_damping_ratio', models.FloatField(blank=True, null=True)),
                ('max_frequency_variance', models.FloatField(blank=True, null=True)),
                ('up_frequency_variance', models.FloatField(blank=True, null=True)),
                ('mid_frequency_variance', models.FloatField(blank=True, null=True)),
                ('down_frequency_variance', models.FloatField(blank=True, null=True)),
                ('min_frequency_variance', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'structure_typhoon_event',
                'managed': False,
            },
        ),
        migrations.AlterModelTable(
            name='weatherstation',
            table='weather_station',
        ),
    ]
