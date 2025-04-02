# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User


class Agency(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    photo_name = models.CharField(max_length=200, blank=True, null=True)
    base64 = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'agency'


class AuthAgencyBridges(models.Model):
    agency = models.ForeignKey(Agency, models.DO_NOTHING)
    bridge = models.ForeignKey('Bridge', models.DO_NOTHING)
    class Meta:
        managed = False
        db_table = 'auth_agency_bridges'
        unique_together = (('agency', 'bridge'),)
        db_table_comment = '管控單位 - 橋梁關係中間表'


class AuthAgencyUsers(models.Model):
    agency = models.ForeignKey(Agency, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_agency_users'
        unique_together = (('agency', 'user'),)
        db_table_comment = '使用者隸屬於哪個單位'

class WeatherStation(models.Model):
    id = id = models.IntegerField(primary_key=True)
    station_id = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=10)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    deleted = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weather_station'


class Bridge(models.Model):
    type = models.CharField(max_length=20)
    bno = models.CharField(max_length=10, blank=True, null=True, db_comment='橋梁編號: 同步市政府對外提供之橋梁編號， EX: 桃市府南崁橋 - 300，北市府康樂橋 - D036')
    name = models.CharField(max_length=20)
    longitude = models.FloatField()
    latitude = models.FloatField()
    address_name  = models.CharField(max_length=20)
    id_address_name  = models.CharField(max_length=20)
    photo_name = models.CharField(max_length=200)
    base64 = models.TextField()
    station_id = models.ForeignKey(WeatherStation, models.DO_NOTHING, db_column='station_id', to_field= 'station_id', blank=True, null=True)
    health_alert_index = models.FloatField()
    health_move_index = models.FloatField()
    event_alert_index = models.FloatField()
    event_move_index = models.FloatField()
    deleted = models.IntegerField()
    health_alert_index =  models.FloatField(blank=True, null=True)
    health_move_index =  models.FloatField(blank=True, null=True)


    # Django ORM: ManyToMany Field
    bridges = models.ManyToManyField(
        'Bridge', 
        through='AuthAgencyBridges', 
        related_name='agencies'
    )

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'bridge'

class EngineeringFirm(models.Model):
    name = models.CharField(max_length=20)
    agency = models.ForeignKey(Agency, models.DO_NOTHING, db_comment="該工程顧問公司屬於哪個管理單位")
    
    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'engineering_firm'



class BridgeData(models.Model):
    bid = models.IntegerField()
    sensor = models.IntegerField()
    mid = models.IntegerField(blank=True, null=True)
    createtime = models.DateTimeField()
    health = models.FloatField(blank=True, null=True)
    seismic = models.FloatField(blank=True, null=True)
    centroid_frequency = models.FloatField(blank=True, null=True)
    bandwidth = models.FloatField(blank=True, null=True)
    cable_force = models.FloatField(blank=True, null=True)
    load_carry_capacity = models.FloatField(blank=True, null=True)
    damping_ratio = models.FloatField(blank=True, null=True)
    frequency_variance = models.FloatField(blank=True, null=True)
    time2 = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bridge_data'
        unique_together = (('bid', 'sensor', 'createtime'),)


class DailyHistoryData(models.Model):
    bid = models.IntegerField()
    sensor = models.IntegerField()
    mid = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField()
    max_health = models.FloatField(blank=True, null=True)
    up_health = models.FloatField(blank=True, null=True)
    mid_health = models.FloatField(blank=True, null=True)
    down_health = models.FloatField(blank=True, null=True)
    min_health = models.FloatField(blank=True, null=True)
    max_seismic = models.FloatField(blank=True, null=True)
    up_seismic = models.FloatField(blank=True, null=True)
    mid_seismic = models.FloatField(blank=True, null=True)
    down_seismic = models.FloatField(blank=True, null=True)
    min_seismic = models.FloatField(blank=True, null=True)
    max_centroid_frequency = models.FloatField(blank=True, null=True)
    up_centroid_frequency = models.FloatField(blank=True, null=True)
    mid_centroid_frequency = models.FloatField(blank=True, null=True)
    down_centroid_frequency = models.FloatField(blank=True, null=True)
    min_centroid_frequency = models.FloatField(blank=True, null=True)
    max_bandwidth = models.FloatField(blank=True, null=True)
    up_bandwidth = models.FloatField(blank=True, null=True)
    mid_bandwidth = models.FloatField(blank=True, null=True)
    down_bandwidth = models.FloatField(blank=True, null=True)
    min_bandwidth = models.FloatField(blank=True, null=True)
    max_cable_force = models.FloatField(blank=True, null=True)
    up_cable_force = models.FloatField(blank=True, null=True)
    mid_cable_force = models.FloatField(blank=True, null=True)
    down_cable_force = models.FloatField(blank=True, null=True)
    min_cable_force = models.FloatField(blank=True, null=True)
    max_load_carry_capacity = models.FloatField(blank=True, null=True)
    up_load_carry_capacity = models.FloatField(blank=True, null=True)
    mid_load_carry_capacity = models.FloatField(blank=True, null=True)
    down_load_carry_capacity = models.FloatField(blank=True, null=True)
    min_load_carry_capacity = models.FloatField(blank=True, null=True)
    max_damping_ratio = models.FloatField(blank=True, null=True)
    up_damping_ratio = models.FloatField(blank=True, null=True)
    mid_damping_ratio = models.FloatField(blank=True, null=True)
    down_damping_ratio = models.FloatField(blank=True, null=True)
    min_damping_ratio = models.FloatField(blank=True, null=True)
    max_frequency_variance = models.FloatField(blank=True, null=True)
    up_frequency_variance = models.FloatField(blank=True, null=True)
    mid_frequency_variance = models.FloatField(blank=True, null=True)
    down_frequency_variance = models.FloatField(blank=True, null=True)
    min_frequency_variance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'daily_history_data'
        unique_together = (('bid', 'sensor', 'time'),)


class EarthquakeEvent(models.Model):
    bid = models.IntegerField()
    sensor = models.IntegerField()
    mid = models.IntegerField(blank=True, null=True)
    event_id = models.IntegerField()
    time_marker = models.CharField(max_length=10)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    max_health = models.FloatField(blank=True, null=True)
    up_health = models.FloatField(blank=True, null=True)
    mid_health = models.FloatField(blank=True, null=True)
    down_health = models.FloatField(blank=True, null=True)
    min_health = models.FloatField(blank=True, null=True)
    max_seismic = models.FloatField(blank=True, null=True)
    up_seismic = models.FloatField(blank=True, null=True)
    mid_seismic = models.FloatField(blank=True, null=True)
    down_seismic = models.FloatField(blank=True, null=True)
    min_seismic = models.FloatField(blank=True, null=True)
    max_centroid_frequency = models.FloatField(blank=True, null=True)
    up_centroid_frequency = models.FloatField(blank=True, null=True)
    mid_centroid_frequency = models.FloatField(blank=True, null=True)
    down_centroid_frequency = models.FloatField(blank=True, null=True)
    min_centroid_frequency = models.FloatField(blank=True, null=True)
    max_bandwidth = models.FloatField(blank=True, null=True)
    up_bandwidth = models.FloatField(blank=True, null=True)
    mid_bandwidth = models.FloatField(blank=True, null=True)
    down_bandwidth = models.FloatField(blank=True, null=True)
    min_bandwidth = models.FloatField(blank=True, null=True)
    max_cable_force = models.FloatField(blank=True, null=True)
    up_cable_force = models.FloatField(blank=True, null=True)
    mid_cable_force = models.FloatField(blank=True, null=True)
    down_cable_force = models.FloatField(blank=True, null=True)
    min_cable_force = models.FloatField(blank=True, null=True)
    max_load_carry_capacity = models.FloatField(blank=True, null=True)
    up_load_carry_capacity = models.FloatField(blank=True, null=True)
    mid_load_carry_capacity = models.FloatField(blank=True, null=True)
    down_load_carry_capacity = models.FloatField(blank=True, null=True)
    min_load_carry_capacity = models.FloatField(blank=True, null=True)
    max_damping_ratio = models.FloatField(blank=True, null=True)
    up_damping_ratio = models.FloatField(blank=True, null=True)
    mid_damping_ratio = models.FloatField(blank=True, null=True)
    down_damping_ratio = models.FloatField(blank=True, null=True)
    min_damping_ratio = models.FloatField(blank=True, null=True)
    max_frequency_variance = models.FloatField(blank=True, null=True)
    up_frequency_variance = models.FloatField(blank=True, null=True)
    mid_frequency_variance = models.FloatField(blank=True, null=True)
    down_frequency_variance = models.FloatField(blank=True, null=True)
    min_frequency_variance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'earthquake_event'


class FinalFloodResistance(models.Model):
    bid = models.IntegerField()
    sensor = models.IntegerField()
    mid = models.ForeignKey('Model', models.DO_NOTHING, db_column='mid', blank=True, null=True)
    event = models.ForeignKey('Typhoon', models.DO_NOTHING)
    freq_var_ratio = models.FloatField(blank=True, null=True)
    health_var_ratio = models.FloatField(blank=True, null=True)
    cable_force_var_ratio = models.FloatField(blank=True, null=True)
    load_carry_capacity_var_ratio = models.FloatField(blank=True, null=True)
    post_event_health = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'final_flood_resistance'
        unique_together = (('bid', 'sensor', 'event'),)


class FinalSeismicResistance(models.Model):
    bid = models.IntegerField()
    sensor = models.IntegerField()
    mid = models.ForeignKey('Model', models.DO_NOTHING, db_column='mid', blank=True, null=True)
    event = models.ForeignKey('Earthquake', models.DO_NOTHING)
    freq_var_ratio = models.FloatField(blank=True, null=True)
    health_var_ratio = models.FloatField(blank=True, null=True)
    cable_force_var_ratio = models.FloatField(blank=True, null=True)
    load_carry_capacity_var_ratio = models.FloatField(blank=True, null=True)
    post_event_health = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'final_seismic_resistance'
        unique_together = (('bid', 'sensor', 'event'),)


class Earthquake(models.Model):
    earthquakeno = models.IntegerField(primary_key=True)
    reportcolor = models.CharField(max_length=10, blank=True, null=True)
    origintime = models.DateTimeField(blank=True, null=True)
    reportcontent = models.CharField(max_length=200, blank=True, null=True)
    reportimageuri = models.CharField(max_length=200, blank=True, null=True)
    epicenterlocation = models.CharField(db_column='epiCenterlocation', max_length=50, blank=True, null=True)  # Field name made lowercase.
    magnitudetype = models.CharField(max_length=10, blank=True, null=True)
    magnitudevalue = models.FloatField(blank=True, null=True)
    shakemapimageuri = models.CharField(max_length=200, blank=True, null=True)
    depthvalue = models.FloatField(blank=True, null=True)
    depthtype = models.CharField(max_length=10, blank=True, null=True)
    longitude = models.FloatField(null= True)
    latitude = models.FloatField(null= True)
    information_base64 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'earthquake'


class MinuteHistoryData(models.Model):
    bid = models.IntegerField()
    sensor = models.IntegerField()
    mid = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField()
    max_health = models.FloatField(blank=True, null=True)
    up_health = models.FloatField(blank=True, null=True)
    mid_health = models.FloatField(blank=True, null=True)
    down_health = models.FloatField(blank=True, null=True)
    min_health = models.FloatField(blank=True, null=True)
    max_seismic = models.FloatField(blank=True, null=True)
    up_seismic = models.FloatField(blank=True, null=True)
    mid_seismic = models.FloatField(blank=True, null=True)
    down_seismic = models.FloatField(blank=True, null=True)
    min_seismic = models.FloatField(blank=True, null=True)
    max_centroid_frequency = models.FloatField(blank=True, null=True)
    up_centroid_frequency = models.FloatField(blank=True, null=True)
    mid_centroid_frequency = models.FloatField(blank=True, null=True)
    down_centroid_frequency = models.FloatField(blank=True, null=True)
    min_centroid_frequency = models.FloatField(blank=True, null=True)
    max_bandwidth = models.FloatField(blank=True, null=True)
    up_bandwidth = models.FloatField(blank=True, null=True)
    mid_bandwidth = models.FloatField(blank=True, null=True)
    down_bandwidth = models.FloatField(blank=True, null=True)
    min_bandwidth = models.FloatField(blank=True, null=True)
    max_cable_force = models.FloatField(blank=True, null=True)
    up_cable_force = models.FloatField(blank=True, null=True)
    mid_cable_force = models.FloatField(blank=True, null=True)
    down_cable_force = models.FloatField(blank=True, null=True)
    min_cable_force = models.FloatField(blank=True, null=True)
    max_load_carry_capacity = models.FloatField(blank=True, null=True)
    up_load_carry_capacity = models.FloatField(blank=True, null=True)
    mid_load_carry_capacity = models.FloatField(blank=True, null=True)
    down_load_carry_capacity = models.FloatField(blank=True, null=True)
    min_load_carry_capacity = models.FloatField(blank=True, null=True)
    max_damping_ratio = models.FloatField(blank=True, null=True)
    up_damping_ratio = models.FloatField(blank=True, null=True)
    mid_damping_ratio = models.FloatField(blank=True, null=True)
    down_damping_ratio = models.FloatField(blank=True, null=True)
    min_damping_ratio = models.FloatField(blank=True, null=True)
    max_frequency_variance = models.FloatField(blank=True, null=True)
    up_frequency_variance = models.FloatField(blank=True, null=True)
    mid_frequency_variance = models.FloatField(blank=True, null=True)
    down_frequency_variance = models.FloatField(blank=True, null=True)
    min_frequency_variance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'minute_history_data'
        unique_together = (('bid', 'sensor', 'time'),)


class Model(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'model'


class QuartileData(models.Model):
    bid = models.IntegerField()
    sensor = models.IntegerField()
    mid = models.ForeignKey(Model, models.DO_NOTHING, db_column='mid', blank=True, null=True)
    time = models.DateTimeField()
    max_health = models.FloatField(blank=True, null=True)
    up_health = models.FloatField(blank=True, null=True)
    mid_health = models.FloatField(blank=True, null=True)
    down_health = models.FloatField(blank=True, null=True)
    min_health = models.FloatField(blank=True, null=True)
    max_seismic = models.FloatField(blank=True, null=True)
    up_seismic = models.FloatField(blank=True, null=True)
    mid_seismic = models.FloatField(blank=True, null=True)
    down_seismic = models.FloatField(blank=True, null=True)
    min_seismic = models.FloatField(blank=True, null=True)
    max_centroid_frequency = models.FloatField(blank=True, null=True)
    up_centroid_frequency = models.FloatField(blank=True, null=True)
    mid_centroid_frequency = models.FloatField(blank=True, null=True)
    down_centroid_frequency = models.FloatField(blank=True, null=True)
    min_centroid_frequency = models.FloatField(blank=True, null=True)
    max_bandwidth = models.FloatField(blank=True, null=True)
    up_bandwidth = models.FloatField(blank=True, null=True)
    mid_bandwidth = models.FloatField(blank=True, null=True)
    down_bandwidth = models.FloatField(blank=True, null=True)
    min_bandwidth = models.FloatField(blank=True, null=True)
    max_cable_force = models.FloatField(blank=True, null=True)
    up_cable_force = models.FloatField(blank=True, null=True)
    mid_cable_force = models.FloatField(blank=True, null=True)
    down_cable_force = models.FloatField(blank=True, null=True)
    min_cable_force = models.FloatField(blank=True, null=True)
    max_load_carry_capacity = models.FloatField(blank=True, null=True)
    up_load_carry_capacity = models.FloatField(blank=True, null=True)
    mid_load_carry_capacity = models.FloatField(blank=True, null=True)
    down_load_carry_capacity = models.FloatField(blank=True, null=True)
    min_load_carry_capacity = models.FloatField(blank=True, null=True)
    max_damping_ratio = models.FloatField(blank=True, null=True)
    up_damping_ratio = models.FloatField(blank=True, null=True)
    mid_damping_ratio = models.FloatField(blank=True, null=True)
    down_damping_ratio = models.FloatField(blank=True, null=True)
    min_damping_ratio = models.FloatField(blank=True, null=True)
    max_frequency_variance = models.FloatField(blank=True, null=True)
    up_frequency_variance = models.FloatField(blank=True, null=True)
    mid_frequency_variance = models.FloatField(blank=True, null=True)
    down_frequency_variance = models.FloatField(blank=True, null=True)
    min_frequency_variance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quartile_data'
        unique_together = (('bid', 'sensor', 'time'),)


class Sensor(models.Model):
    bid = models.ForeignKey(Bridge, models.DO_NOTHING, db_column='bid', related_name='sensors')
    sensor = models.IntegerField()
    type = models.CharField(max_length=20, blank=True, null=True)
    ip = models.IntegerField(blank=True, null=True)
    sensor_location = models.CharField(max_length=20, blank=True, null=True)
    detailed_location = models.CharField(max_length=20, blank=True, null=True)
    cable_mass_per_length = models.FloatField(blank=True, null=True)
    cable_length = models.FloatField(blank=True, null=True)
    elasticity = models.FloatField(blank=True, null=True)  
    inertia = models.FloatField(blank=True, null=True)  
    mass = models.FloatField(blank=True, null=True)
    span =  models.FloatField(blank=True, null=True)
    nearest_pier_distance =  models.FloatField(blank=True, null=True)
    health_alert_index = models.IntegerField(blank=True, null=True)
    health_move_index = models.IntegerField(blank=True, null=True)
    event_alert_index = models.IntegerField(blank=True, null=True)
    event_move_index = models.IntegerField(blank=True, null=True)
    bridge_alert_index = models.FloatField(blank=True, null=True)
    bridge_move_index = models.FloatField(blank=True, null=True)
    image_x = models.FloatField(max_length=50, blank=True, null=True)
    image_y = models.FloatField(max_length=50, blank=True, null=True)
    f_var_ref = models.FloatField(blank=True, null=True)
    current_status = models.IntegerField(blank=True, null=True)
    deleted = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'sensor'
        unique_together = (('bid', 'sensor'),)


class Typhoon(models.Model):
    id = models.IntegerField(primary_key=True)
    cht_name = models.CharField(max_length=10, blank=True, null=True)
    eng_name = models.CharField(max_length=50, blank=True, null=True)
    sea_start_datetime = models.DateTimeField(blank=True, null=True)
    max_intensity = models.CharField(max_length=3, blank=True, null=True)
    sea_end_datetime = models.DateTimeField(blank=True, null=True)
    warning_count = models.IntegerField(blank=True, null=True)
    track_base64 = models.TextField(blank=True, null=True)
    information_base64 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'typhoon'


class TyphoonEvent(models.Model):
    bid = models.IntegerField()
    sensor = models.IntegerField()
    mid = models.ForeignKey(Model, models.DO_NOTHING, db_column='mid', blank=True, null=True)
    event = models.ForeignKey(Typhoon, models.DO_NOTHING)
    time_marker = models.CharField(max_length=10)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    max_health = models.FloatField(blank=True, null=True)
    up_health = models.FloatField(blank=True, null=True)
    mid_health = models.FloatField(blank=True, null=True)
    down_health = models.FloatField(blank=True, null=True)
    min_health = models.FloatField(blank=True, null=True)
    max_seismic = models.FloatField(blank=True, null=True)
    up_seismic = models.FloatField(blank=True, null=True)
    mid_seismic = models.FloatField(blank=True, null=True)
    down_seismic = models.FloatField(blank=True, null=True)
    min_seismic = models.FloatField(blank=True, null=True)
    max_centroid_frequency = models.FloatField(blank=True, null=True)
    up_centroid_frequency = models.FloatField(blank=True, null=True)
    mid_centroid_frequency = models.FloatField(blank=True, null=True)
    down_centroid_frequency = models.FloatField(blank=True, null=True)
    min_centroid_frequency = models.FloatField(blank=True, null=True)
    max_bandwidth = models.FloatField(blank=True, null=True)
    up_bandwidth = models.FloatField(blank=True, null=True)
    mid_bandwidth = models.FloatField(blank=True, null=True)
    down_bandwidth = models.FloatField(blank=True, null=True)
    min_bandwidth = models.FloatField(blank=True, null=True)
    max_cable_force = models.FloatField(blank=True, null=True)
    up_cable_force = models.FloatField(blank=True, null=True)
    mid_cable_force = models.FloatField(blank=True, null=True)
    down_cable_force = models.FloatField(blank=True, null=True)
    min_cable_force = models.FloatField(blank=True, null=True)
    max_load_carry_capacity = models.FloatField(blank=True, null=True)
    up_load_carry_capacity = models.FloatField(blank=True, null=True)
    mid_load_carry_capacity = models.FloatField(blank=True, null=True)
    down_load_carry_capacity = models.FloatField(blank=True, null=True)
    min_load_carry_capacity = models.FloatField(blank=True, null=True)
    max_damping_ratio = models.FloatField(blank=True, null=True)
    up_damping_ratio = models.FloatField(blank=True, null=True)
    mid_damping_ratio = models.FloatField(blank=True, null=True)
    down_damping_ratio = models.FloatField(blank=True, null=True)
    min_damping_ratio = models.FloatField(blank=True, null=True)
    max_frequency_variance = models.FloatField(blank=True, null=True)
    up_frequency_variance = models.FloatField(blank=True, null=True)
    mid_frequency_variance = models.FloatField(blank=True, null=True)
    down_frequency_variance = models.FloatField(blank=True, null=True)
    min_frequency_variance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'typhoon_event'
        unique_together = (('bid', 'sensor', 'event', 'time_marker'),)


class WeatherData(models.Model):
    id = models.IntegerField(primary_key=True)
    station_id = models.ForeignKey(WeatherStation, models.DO_NOTHING, db_column='station_id', to_field= 'station_id', blank=True, null=True)
    time = models.DateTimeField()
    temperature = models.FloatField(blank=True, null=True)
    wind_speed = models.FloatField(blank=True, null=True)
    wind_direction = models.FloatField(blank=True, null=True)
    precipitation = models.FloatField(blank=True, null=True)
    acc_precipitation = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weather_data'


class WeatherDailyHistoryData(models.Model):
    id = models.IntegerField(primary_key=True)
    station_id = models.CharField(unique=True, max_length=50)
    time = models.DateTimeField()
    max_temperature = models.FloatField(blank=True, null=True)
    up_temperature = models.FloatField(blank=True, null=True)
    mid_temperature = models.FloatField(blank=True, null=True)
    down_temperature = models.FloatField(blank=True, null=True)
    min_temperature = models.FloatField(blank=True, null=True)
    max_wind_speed = models.FloatField(blank=True, null=True)
    up_wind_speed = models.FloatField(blank=True, null=True)
    mid_wind_speed = models.FloatField(blank=True, null=True)
    down_wind_speed = models.FloatField(blank=True, null=True)
    min_wind_speed = models.FloatField(blank=True, null=True)
    max_wind_direction = models.FloatField(blank=True, null=True)
    up_wind_direction = models.FloatField(blank=True, null=True)
    mid_wind_direction = models.FloatField(blank=True, null=True)
    down_wind_direction = models.FloatField(blank=True, null=True)
    min_wind_direction = models.FloatField(blank=True, null=True)
    max_precipitation = models.FloatField(blank=True, null=True)
    up_precipitation = models.FloatField(blank=True, null=True)
    mid_precipitation = models.FloatField(blank=True, null=True)
    down_precipitation = models.FloatField(blank=True, null=True)
    min_precipitation = models.FloatField(blank=True, null=True)
     
    class Meta:
        managed = False
        db_table = 'weather_daily_history_data'


class LocalEarthquake(models.Model):
    earthquakeno = models.IntegerField()
    reportcolor = models.CharField(max_length=10, blank=True, null=True)
    origintime = models.DateTimeField(blank=True, null=True)
    reportcontent = models.CharField(max_length=200, blank=True, null=True)
    reportimageuri = models.CharField(max_length=200, blank=True, null=True)
    epicenterlocation = models.CharField(db_column='epiCenterlocation', max_length=50, blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    magnitudetype = models.CharField(max_length=10, blank=True, null=True)
    magnitudevalue = models.FloatField(blank=True, null=True)
    shakemapimageuri = models.CharField(max_length=200, blank=True, null=True)
    depthvalue = models.FloatField(blank=True, null=True)
    depthtype = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'local_earthquake'


class StructureDailyHistoryData(models.Model):
    bid = models.IntegerField()
    mid = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField()
    max_health = models.FloatField(blank=True, null=True)
    up_health = models.FloatField(blank=True, null=True)
    mid_health = models.FloatField(blank=True, null=True)
    down_health = models.FloatField(blank=True, null=True)
    min_health = models.FloatField(blank=True, null=True)
    max_seismic = models.FloatField(blank=True, null=True)
    up_seismic = models.FloatField(blank=True, null=True)
    mid_seismic = models.FloatField(blank=True, null=True)
    down_seismic = models.FloatField(blank=True, null=True)
    min_seismic = models.FloatField(blank=True, null=True)
    max_centroid_frequency = models.FloatField(blank=True, null=True)
    up_centroid_frequency = models.FloatField(blank=True, null=True)
    mid_centroid_frequency = models.FloatField(blank=True, null=True)
    down_centroid_frequency = models.FloatField(blank=True, null=True)
    min_centroid_frequency = models.FloatField(blank=True, null=True)
    max_bandwidth = models.FloatField(blank=True, null=True)
    up_bandwidth = models.FloatField(blank=True, null=True)
    mid_bandwidth = models.FloatField(blank=True, null=True)
    down_bandwidth = models.FloatField(blank=True, null=True)
    min_bandwidth = models.FloatField(blank=True, null=True)
    max_cable_force = models.FloatField(blank=True, null=True)
    up_cable_force = models.FloatField(blank=True, null=True)
    mid_cable_force = models.FloatField(blank=True, null=True)
    down_cable_force = models.FloatField(blank=True, null=True)
    min_cable_force = models.FloatField(blank=True, null=True)
    max_load_carry_capacity = models.FloatField(blank=True, null=True)
    up_load_carry_capacity = models.FloatField(blank=True, null=True)
    mid_load_carry_capacity = models.FloatField(blank=True, null=True)
    down_load_carry_capacity = models.FloatField(blank=True, null=True)
    min_load_carry_capacity = models.FloatField(blank=True, null=True)
    max_damping_ratio = models.FloatField(blank=True, null=True)
    up_damping_ratio = models.FloatField(blank=True, null=True)
    mid_damping_ratio = models.FloatField(blank=True, null=True)
    down_damping_ratio = models.FloatField(blank=True, null=True)
    min_damping_ratio = models.FloatField(blank=True, null=True)
    max_frequency_variance = models.FloatField(blank=True, null=True)
    up_frequency_variance = models.FloatField(blank=True, null=True)
    mid_frequency_variance = models.FloatField(blank=True, null=True)
    down_frequency_variance = models.FloatField(blank=True, null=True)
    min_frequency_variance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'structure_daily_history_data'
        unique_together = (('bid', 'time'),)


class StructureEarthquakeEvent(models.Model):
    bid = models.ForeignKey(Bridge, models.DO_NOTHING, db_column='bid')
    mid = models.ForeignKey(Model, models.DO_NOTHING, db_column='mid', blank=True, null=True)
    event = models.ForeignKey(Earthquake, models.DO_NOTHING)
    time_marker = models.CharField(max_length=10)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    max_health = models.FloatField(blank=True, null=True)
    up_health = models.FloatField(blank=True, null=True)
    mid_health = models.FloatField(blank=True, null=True)
    down_health = models.FloatField(blank=True, null=True)
    min_health = models.FloatField(blank=True, null=True)
    max_seismic = models.FloatField(blank=True, null=True)
    up_seismic = models.FloatField(blank=True, null=True)
    mid_seismic = models.FloatField(blank=True, null=True)
    down_seismic = models.FloatField(blank=True, null=True)
    min_seismic = models.FloatField(blank=True, null=True)
    max_centroid_frequency = models.FloatField(blank=True, null=True)
    up_centroid_frequency = models.FloatField(blank=True, null=True)
    mid_centroid_frequency = models.FloatField(blank=True, null=True)
    down_centroid_frequency = models.FloatField(blank=True, null=True)
    min_centroid_frequency = models.FloatField(blank=True, null=True)
    max_bandwidth = models.FloatField(blank=True, null=True)
    up_bandwidth = models.FloatField(blank=True, null=True)
    mid_bandwidth = models.FloatField(blank=True, null=True)
    down_bandwidth = models.FloatField(blank=True, null=True)
    min_bandwidth = models.FloatField(blank=True, null=True)
    max_cable_force = models.FloatField(blank=True, null=True)
    up_cable_force = models.FloatField(blank=True, null=True)
    mid_cable_force = models.FloatField(blank=True, null=True)
    down_cable_force = models.FloatField(blank=True, null=True)
    min_cable_force = models.FloatField(blank=True, null=True)
    max_load_carry_capacity = models.FloatField(blank=True, null=True)
    up_load_carry_capacity = models.FloatField(blank=True, null=True)
    mid_load_carry_capacity = models.FloatField(blank=True, null=True)
    down_load_carry_capacity = models.FloatField(blank=True, null=True)
    min_load_carry_capacity = models.FloatField(blank=True, null=True)
    max_damping_ratio = models.FloatField(blank=True, null=True)
    up_damping_ratio = models.FloatField(blank=True, null=True)
    mid_damping_ratio = models.FloatField(blank=True, null=True)
    down_damping_ratio = models.FloatField(blank=True, null=True)
    min_damping_ratio = models.FloatField(blank=True, null=True)
    max_frequency_variance = models.FloatField(blank=True, null=True)
    up_frequency_variance = models.FloatField(blank=True, null=True)
    mid_frequency_variance = models.FloatField(blank=True, null=True)
    down_frequency_variance = models.FloatField(blank=True, null=True)
    min_frequency_variance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'structure_earthquake_event'
        unique_together = (('bid', 'event', 'time_marker'),)


class StructureFinalFloodResistance(models.Model):
    bid = models.ForeignKey(Bridge, models.DO_NOTHING, db_column='bid')
    mid = models.ForeignKey(Model, models.DO_NOTHING, db_column='mid', blank=True, null=True)
    event = models.ForeignKey('Typhoon', models.DO_NOTHING)
    freq_var_ratio = models.FloatField(blank=True, null=True)
    health_var_ratio = models.FloatField(blank=True, null=True)
    cable_force_var_ratio = models.FloatField(blank=True, null=True)
    load_carry_capacity_var_ratio = models.FloatField(blank=True, null=True)
    max_during_freq_var_ratio = models.FloatField(blank=True, null=True)
    max_during_health_var_ratio = models.FloatField(blank=True, null=True)
    max_during_bridge_var_ratio = models.FloatField(blank=True, null=True)
    post_event_health = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'structure_final_flood_resistance'
        unique_together = (('bid', 'event'),)


class StructureFinalSeismicResistance(models.Model):
    bid = models.ForeignKey(Bridge, models.DO_NOTHING, db_column='bid')
    mid = models.ForeignKey(Model, models.DO_NOTHING, db_column='mid', blank=True, null=True)
    event = models.ForeignKey(Earthquake, models.DO_NOTHING)
    freq_var_ratio = models.FloatField(blank=True, null=True)
    health_var_ratio = models.FloatField(blank=True, null=True)
    cable_force_var_ratio = models.FloatField(blank=True, null=True)
    load_carry_capacity_var_ratio = models.FloatField(blank=True, null=True)
    max_during_freq_var_ratio = models.FloatField(blank=True, null=True)
    max_during_health_var_ratio = models.FloatField(blank=True, null=True)
    max_during_bridge_var_ratio = models.FloatField(blank=True, null=True)
    post_event_health = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'structure_final_seismic_resistance'
        unique_together = (('bid', 'event'),)


class StructureFloodResistance(models.Model):
    event_id = models.BigIntegerField(blank=True, null=True)
    freq_var_ratio = models.FloatField(blank=True, null=True)
    health_var_ratio = models.FloatField(blank=True, null=True)
    cable_force_var_ratio = models.FloatField(blank=True, null=True)
    load_carry_capacity_var_ratio = models.TextField(blank=True, null=True)
    max_during_freq_var_ratio = models.TextField(blank=True, null=True)
    max_during_health_var_ratio = models.TextField(blank=True, null=True)
    max_during_bridge_var_ratio = models.TextField(blank=True, null=True)
    post_event_health = models.FloatField(blank=True, null=True)
    bid = models.BigIntegerField(blank=True, null=True)
    mid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'structure_flood_resistance'


class StructureHourlyHistoryData(models.Model):
    bid = models.IntegerField()
    mid = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField()
    max_health = models.FloatField(blank=True, null=True)
    up_health = models.FloatField(blank=True, null=True)
    mid_health = models.FloatField(blank=True, null=True)
    down_health = models.FloatField(blank=True, null=True)
    min_health = models.FloatField(blank=True, null=True)
    max_seismic = models.FloatField(blank=True, null=True)
    up_seismic = models.FloatField(blank=True, null=True)
    mid_seismic = models.FloatField(blank=True, null=True)
    down_seismic = models.FloatField(blank=True, null=True)
    min_seismic = models.FloatField(blank=True, null=True)
    max_centroid_frequency = models.FloatField(blank=True, null=True)
    up_centroid_frequency = models.FloatField(blank=True, null=True)
    mid_centroid_frequency = models.FloatField(blank=True, null=True)
    down_centroid_frequency = models.FloatField(blank=True, null=True)
    min_centroid_frequency = models.FloatField(blank=True, null=True)
    max_bandwidth = models.FloatField(blank=True, null=True)
    up_bandwidth = models.FloatField(blank=True, null=True)
    mid_bandwidth = models.FloatField(blank=True, null=True)
    down_bandwidth = models.FloatField(blank=True, null=True)
    min_bandwidth = models.FloatField(blank=True, null=True)
    max_cable_force = models.FloatField(blank=True, null=True)
    up_cable_force = models.FloatField(blank=True, null=True)
    mid_cable_force = models.FloatField(blank=True, null=True)
    down_cable_force = models.FloatField(blank=True, null=True)
    min_cable_force = models.FloatField(blank=True, null=True)
    max_load_carry_capacity = models.FloatField(blank=True, null=True)
    up_load_carry_capacity = models.FloatField(blank=True, null=True)
    mid_load_carry_capacity = models.FloatField(blank=True, null=True)
    down_load_carry_capacity = models.FloatField(blank=True, null=True)
    min_load_carry_capacity = models.FloatField(blank=True, null=True)
    max_damping_ratio = models.FloatField(blank=True, null=True)
    up_damping_ratio = models.FloatField(blank=True, null=True)
    mid_damping_ratio = models.FloatField(blank=True, null=True)
    down_damping_ratio = models.FloatField(blank=True, null=True)
    min_damping_ratio = models.FloatField(blank=True, null=True)
    max_frequency_variance = models.FloatField(blank=True, null=True)
    up_frequency_variance = models.FloatField(blank=True, null=True)
    mid_frequency_variance = models.FloatField(blank=True, null=True)
    down_frequency_variance = models.FloatField(blank=True, null=True)
    min_frequency_variance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'structure_hourly_history_data'
        unique_together = (('bid', 'time'),)


class StructureMinuteHistoryData(models.Model):
    bid = models.IntegerField()
    mid = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField()
    max_health = models.FloatField(blank=True, null=True)
    up_health = models.FloatField(blank=True, null=True)
    mid_health = models.FloatField(blank=True, null=True)
    down_health = models.FloatField(blank=True, null=True)
    min_health = models.FloatField(blank=True, null=True)
    max_seismic = models.FloatField(blank=True, null=True)
    up_seismic = models.FloatField(blank=True, null=True)
    mid_seismic = models.FloatField(blank=True, null=True)
    down_seismic = models.FloatField(blank=True, null=True)
    min_seismic = models.FloatField(blank=True, null=True)
    max_centroid_frequency = models.FloatField(blank=True, null=True)
    up_centroid_frequency = models.FloatField(blank=True, null=True)
    mid_centroid_frequency = models.FloatField(blank=True, null=True)
    down_centroid_frequency = models.FloatField(blank=True, null=True)
    min_centroid_frequency = models.FloatField(blank=True, null=True)
    max_bandwidth = models.FloatField(blank=True, null=True)
    up_bandwidth = models.FloatField(blank=True, null=True)
    mid_bandwidth = models.FloatField(blank=True, null=True)
    down_bandwidth = models.FloatField(blank=True, null=True)
    min_bandwidth = models.FloatField(blank=True, null=True)
    max_cable_force = models.FloatField(blank=True, null=True)
    up_cable_force = models.FloatField(blank=True, null=True)
    mid_cable_force = models.FloatField(blank=True, null=True)
    down_cable_force = models.FloatField(blank=True, null=True)
    min_cable_force = models.FloatField(blank=True, null=True)
    max_load_carry_capacity = models.FloatField(blank=True, null=True)
    up_load_carry_capacity = models.FloatField(blank=True, null=True)
    mid_load_carry_capacity = models.FloatField(blank=True, null=True)
    down_load_carry_capacity = models.FloatField(blank=True, null=True)
    min_load_carry_capacity = models.FloatField(blank=True, null=True)
    max_damping_ratio = models.FloatField(blank=True, null=True)
    up_damping_ratio = models.FloatField(blank=True, null=True)
    mid_damping_ratio = models.FloatField(blank=True, null=True)
    down_damping_ratio = models.FloatField(blank=True, null=True)
    min_damping_ratio = models.FloatField(blank=True, null=True)
    max_frequency_variance = models.FloatField(blank=True, null=True)
    up_frequency_variance = models.FloatField(blank=True, null=True)
    mid_frequency_variance = models.FloatField(blank=True, null=True)
    down_frequency_variance = models.FloatField(blank=True, null=True)
    min_frequency_variance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'structure_minute_history_data'
        unique_together = (('bid', 'time'),)


class StructureTyphoonEvent(models.Model):
    bid = models.ForeignKey(Bridge, models.DO_NOTHING, db_column='bid')
    mid = models.ForeignKey(Model, models.DO_NOTHING, db_column='mid', blank=True, null=True)
    event = models.ForeignKey('Typhoon', models.DO_NOTHING)
    time_marker = models.CharField(max_length=10)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    max_health = models.FloatField(blank=True, null=True)
    up_health = models.FloatField(blank=True, null=True)
    mid_health = models.FloatField(blank=True, null=True)
    down_health = models.FloatField(blank=True, null=True)
    min_health = models.FloatField(blank=True, null=True)
    max_seismic = models.FloatField(blank=True, null=True)
    up_seismic = models.FloatField(blank=True, null=True)
    mid_seismic = models.FloatField(blank=True, null=True)
    down_seismic = models.FloatField(blank=True, null=True)
    min_seismic = models.FloatField(blank=True, null=True)
    max_centroid_frequency = models.FloatField(blank=True, null=True)
    up_centroid_frequency = models.FloatField(blank=True, null=True)
    mid_centroid_frequency = models.FloatField(blank=True, null=True)
    down_centroid_frequency = models.FloatField(blank=True, null=True)
    min_centroid_frequency = models.FloatField(blank=True, null=True)
    max_bandwidth = models.FloatField(blank=True, null=True)
    up_bandwidth = models.FloatField(blank=True, null=True)
    mid_bandwidth = models.FloatField(blank=True, null=True)
    down_bandwidth = models.FloatField(blank=True, null=True)
    min_bandwidth = models.FloatField(blank=True, null=True)
    max_cable_force = models.FloatField(blank=True, null=True)
    up_cable_force = models.FloatField(blank=True, null=True)
    mid_cable_force = models.FloatField(blank=True, null=True)
    down_cable_force = models.FloatField(blank=True, null=True)
    min_cable_force = models.FloatField(blank=True, null=True)
    max_load_carry_capacity = models.FloatField(blank=True, null=True)
    up_load_carry_capacity = models.FloatField(blank=True, null=True)
    mid_load_carry_capacity = models.FloatField(blank=True, null=True)
    down_load_carry_capacity = models.FloatField(blank=True, null=True)
    min_load_carry_capacity = models.FloatField(blank=True, null=True)
    max_damping_ratio = models.FloatField(blank=True, null=True)
    up_damping_ratio = models.FloatField(blank=True, null=True)
    mid_damping_ratio = models.FloatField(blank=True, null=True)
    down_damping_ratio = models.FloatField(blank=True, null=True)
    min_damping_ratio = models.FloatField(blank=True, null=True)
    max_frequency_variance = models.FloatField(blank=True, null=True)
    up_frequency_variance = models.FloatField(blank=True, null=True)
    mid_frequency_variance = models.FloatField(blank=True, null=True)
    down_frequency_variance = models.FloatField(blank=True, null=True)
    min_frequency_variance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'structure_typhoon_event'
        unique_together = (('bid', 'event', 'time_marker'),)
