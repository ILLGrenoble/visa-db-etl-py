# Visa Database ETL Python Library

This project contains the source code for the Python library to be used to load data into the database of the VISA platform.

VISA (Virtual Infrastructure for Scientific Analysis) makes it simple to create compute instances on facility cloud infrastructure to analyse your experimental data using just your web browser.

See the [User Manual](https://visa.readthedocs.io/en/latest/) for deployment instructions and end user documentation.

## Description

The ETL Process is an application, running independently to VISA, that is used to push data into the VISA database.

Data includes User Office information (users, proposals, experiments, instruments) and roles of different users depending on their function at the site.

The Extraction and Transformation parts of the process are left to the administrators of VISA who have access to the local facility data sources. This library helps in the creation of the ETL Process at each site by providing the load aspect of the process.

## How to populate with the CSV source

The CSV source is an example of how to develop a source for the Visa ETL.

To run it, simply modify the code to update the connection parameters, and comment or uncomment the call to `clean()` (for performance reasons, if you have a lot a data or it is the first time you load the data)
The CSV files must be in the csv_data/ folder below the code, and have the same name as the function.

## How to create a loader

- create a python 3 module
- instanciate class Loader with an asyncpg Connection object
- Init schema by loading schema.sql and/or call `Loader.clean()` if necessary
- call the methods in the order specified in CSV_source.py (inverse from the method `Loader.clean()`)
- each method expect an iterable. It can be a list, list comprehension, sequence, generator ...
- each element of the iterable must be a dictionnary, with the column name as the key, and the value as a string
- the loader is asynchronous, it must be run with `asyncio.run()`
- every other details is up to you (where you get you data from )

## Acknowledgements

<img src="https://github.com/panosc-eu/panosc/raw/master/Work%20Packages/WP9%20Outreach%20and%20communication/PaNOSC%20logo/PaNOSClogo_web_RGB.jpg" width="200px"/> 

VISA has been developed as part of the Photon and Neutron Open Science Cloud (<a href="http://www.panosc.eu" target="_blank">PaNOSC</a>)

<img src="https://github.com/panosc-eu/panosc/raw/master/Work%20Packages/WP9%20Outreach%20and%20communication/images/logos/eu_flag_yellow_low.jpg"/>

PaNOSC has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No 823852.
