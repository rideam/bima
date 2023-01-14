from tortoise import fields, models


class Users(models.Model):
    id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    fullname = fields.CharField(max_length=50, null=True)
    password = fields.CharField(max_length=128, null=True)
    access_level = fields.ForeignKeyField("models.AccessLevels", related_name="users")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


class AccessLevels(models.Model):
    id = fields.UUIDField(pk=True)
    type = fields.CharField(max_length=50)
    menu = fields.JSONField(null=True)


class Regions(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


class Crops(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


class Farmers(models.Model):
    id = fields.UUIDField(pk=True)
    wallet = fields.CharField(max_length=225)
    address = fields.TextField()
    user = fields.ForeignKeyField("models.Users", related_name="farmers")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


class Farms(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255)
    address = fields.TextField()
    width = fields.IntField()
    length = fields.IntField()
    region = fields.ForeignKeyField("models.Regions", related_name="farms")
    farmer = fields.ForeignKeyField("models.Farmers", related_name="farms")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


class Weather(models.Model):
    id = fields.UUIDField(pk=True)
    timestamp = fields.IntField()
    temperature = fields.FloatField(precision=2, default=0.0)
    humidity = fields.FloatField(precision=2, default=0.0)
    soil_moisture = fields.FloatField(precision=2, default=0.0)
    farm = fields.ForeignKeyField("models.Farms", related_name="weather")
    crop = fields.ForeignKeyField("models.Crops", related_name="weather")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


class StrikeEvents(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255)
    temperature = fields.FloatField(precision=2, default=0.0)
    humidity = fields.FloatField(precision=2, default=0.0)
    soil_moisture = fields.FloatField(precision=2, default=0.0)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


class Policies(models.Model):
    id = fields.UUIDField(pk=True)
    start_date = fields.DatetimeField()
    end_date = fields.DatetimeField()
    premium = fields.IntField()
    crop = fields.ForeignKeyField("models.Crops", related_name="policies")
    farmers = fields.ManyToManyField("models.Farmers", related_name="policies")
    strike_events = fields.ManyToManyField("models.StrikeEvents", related_name="policies")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
