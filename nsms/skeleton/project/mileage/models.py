from django.db import models
from smartmin.models import SmartModel
from rapidsms.models import Connection
from django.contrib.auth.models import User

class Car(SmartModel):
    license_plate = models.CharField(max_length=8, unique=True,
                                     help_text="The license plate of this car")
    connection = models.ForeignKey(Connection,
                                   help_text="The phone number that is updating mileage for this car")


    @classmethod
    def for_connection(cls, connection):
        cars = Car.objects.filter(connection=connection)
        if cars:
            return cars[0]
        else:
            return None

    @classmethod
    def register_connection(cls, license_plate, connection):
        # should we add some kind of RapidSMS user by default?  I think so
        anon = User.objects.get(id=-1)

        license_plate = license_plate.upper()
        cars = Car.objects.filter(license_plate=license_plate)
        if cars:
            car = cars[0]
            car.connection = connection
            car.modified_by = anon
            car.save()
        else:
            car = Car.objects.create(license_plate=license_plate, connection=connection, created_by=anon, modified_by=anon)
            
        return car

    def add_mileage(self, miles, connection):
        # should we add some kind of RapidSMS user by default?  I think so
        anon = User.objects.get(id=-1)
        self.mileage_reports.create(miles=miles, connection=connection,
                                    created_by=anon, modified_by=anon)

class MileageReport(SmartModel):
    car = models.ForeignKey(Car, related_name="mileage_reports",
                            help_text="The car this mileage report is for")
    miles = models.IntegerField(help_text="How many miles were traveled on this day")
    connection = models.ForeignKey(Connection,
                                   help_text="The phone number that reported this mileage")
