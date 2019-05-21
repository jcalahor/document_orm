Document ORM implements data mapping from plain python objects into tables hosted on SQL Server 2016 (and beyond) databases. Is a "hybrid" mapper because besides supporting RDBMS storage it has NoSQL capabilities such as storing collections of objects in a single column (JSON collection) or a list of columns in a single JSON column (JSON property value)

Overview

Once you download the code in your machine, open the src folder in your favorite IDE. We suggest using Pycharm.
We will explain the content of each folder and what it means and what it contains.

core folder: contains model classes the plain python class which we are going to use. Usually this is the place where you will include your own model classes

![Alt text](/doc/images/model.png?raw=true "Optional Title")

For the porpuse to show how this framework works, we have defined a small set of classes that simulate a Entitlement System. Large companies needs to have a centralized place to report what users in the company or outside the company have acess to what computer systems and what kind of roles does a specific user has. The main classes are System, Role and User. ExternalUSer is a user that is external to the company. Contact represents a contact information for a particular system. System has a list of contacts some of them could be technical other business contact (vendor system contact or internal contact/support contact). Finally the source folder contains classes that reprensent how entitlement information is sourced into the Entitlement System, for the porpuses of example there could be 2 possible ways, export from as CSV/flat file or from a FTP push. 
