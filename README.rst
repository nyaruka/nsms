Base Package / Module for RapidSMS Apps
----------------------------------------

This package aims to provide a base RapidSMS app with the best practices we use at Nyaruka.  Many projects will be able to clone this RapidSMS app as a beginning then modify to fit their needs.

This application provides a sample SMS app to track the mileage on vehicles.  The SMS format for the application is as follows.


Registering Cars
~~~~~~~~~~~~~~~~

  car [license plate]

This register a car to the phone.  From now on all mileage reports will be associated with the car with the passed in license plate.  The license plate must be 8 characters.

Adding Mileage Reports
~~~~~~~~~~~~~~~~~~~~~~~

  miles [mileage (integer)]

This records a new mileage report for the car associated with this connection.  If the connetion has not registered a car then this will be an error.


Best Practices
===============

This application aims to demonstrate the following best practices:
 
* Comprehensive unit coverage.  We aim for 100% unit test coverage of our apps, and so should you.  This app shows you how easily that can be done
* DRY. We use Smartmin to allow us to add a lot of functionality without adding much code
* Language Templates.  We let our customers edit the translations for all our messages through a web UI, including using standard Django templates for formatting.
* Tolerant Parsing.  Though still a work in progress, our rapidsms_parser module provides an easy way to programmatically parse SMS messages and give good error messaging in the process.
* User Management.  We provide our customers with basic user management, using groups and SmartMin permissions to easily manage these.
