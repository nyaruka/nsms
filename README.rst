NyarukaSMS
----------------------------------------

NyarumaSMS aims to provide a quick start for a basic python based SMS app using the tools Nyaruka uses to build its systems.  This includes setting up rapidsms, rapidsms-httprouter, smartmin and our parsing and localization libraries.  

Getting Started
----------------

To get started, follow these steps::

  % virtualenv env
  % ./env/bin/activate
  % pip install nsms
  % start-nsms [project-name]
  % pip install -r pip-requires.txt
  % cd [project-name]
  % python manage.py syncdb
  % python manage.py migrate
  % python manage.py runserver

Sample Application
-------------------

NSMS comes with a simple SMS application to track the mileage on vehicles.  The SMS format for the application is as follows.

Registering Cars
~~~~~~~~~~~~~~~~

Each user of the system much register the car they are using, they do so by sending::

  car [license plate]

This register a car to the phone.  From now on all mileage reports will be associated with the car with the passed in license plate.  The license plate must be 8 characters.

Adding Mileage Reports
~~~~~~~~~~~~~~~~~~~~~~~

Once a user has registered their car, they can report mileage by sending the message::

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
