Document ORM implements data mapping from plain python objects into tables hosted on SQL Server 2016 (and beyond) databases. Is a "hybrid" mapper because besides supporting RDBMS storage it has NoSQL capabilities such as storing collections of objects in a single column (JSON collection) or a list of columns in a single JSON column (JSON property value)

Overview

Once you download the code in your machine, open the src folder in your favorite IDE. We suggest using Pycharm.
We will explain the content of each folder and what it means and what it contains.

core folder: contains model classes the plain python class which we are going to use. Usually this is the place where you will include your own model classes

![Alt text](/doc/images/model.png?raw=true "structure")

For the porpuse to show how this framework works, we have defined a small set of classes that simulate a Entitlement System. Large companies needs to have a centralized place to report what users in the company or outside the company have acess to what computer systems and what kind of roles does a specific user has. The main classes are System, Role and User. ExternalUSer is a user that is external to the company. Contact represents a contact information for a particular system. System has a list of contacts some of them could be technical other business contact (vendor system contact or internal contact/support contact). Finally the source folder contains classes that reprensent how entitlement information is sourced into the Entitlement System, for the porpuses of example there could be 2 possible ways, export from as CSV/flat file or from a FTP push. 

db folder: contains the db class which is the entry point for storage it contains methods to store, retrieve and delete entitities. db alone cannot do any job without the help of helper classes. These helper classes are generated by the generation tool which are located in the db_generator folder

db_generator folder: contains the logic and code generation that creates the source code on python and stored procedures needed to store the objects defined by the model. Once all the setup is properly configured we use generator.py to perform the generation.
Use db_generator.cfg to setup to connection string to a sql server database and target_folder to specify where we want to store the generated source code. We need to store them under the db folder. Make sure to create an empty database and point to that db in the connection_string. The file generation_spec.py is the heart of the generation. it specifies how to map the object fields into column tables, it also specifies the relation ship between tables so the corresponding constraints will be created on the db.

Data types are sql types however under the System table there is a column named Contacts, this is a special kind of column which is a JSON column (will be created as varchar(max) on sql server), it specifies that a collection of objects will be stored in this column and they will be serialized into a JSON collection

The image below show details of the configuration entries that define the mapping.

![Alt text](/doc/images/generation_spec1.png?raw=true "structure")

The screenshot below show setup for a family of objects that are stored on the same target SQL table. Child specific fields are stored in a common JSON field.
![Alt text](/doc/images/generation_spec2.png?raw=true "structure")

Running the generator.

Onces setup is complete, we use generator.py to run the generation of the pieces of code that will allow us to store the entities. The screenshot below shows the code (stored procedures and python modules) that are created.

![Alt text](/doc/images/generated_code.png?raw=true "structure")

test folder: The db_tests module contains different set of sample tests that we can apply to the generated code. The samples are illustrative for the different features that the framework support. This is also sample code of how to use the framework and how you can adopt it to your own system
