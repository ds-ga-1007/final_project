## IVF - Search Clinic Program V. 1.0.0
=======================================

The IVF - Search Clinic Program was developed as a deliverable for the “DS-GA-1007 Programming for Data Science” course, NYU’s Masters in Data Science (Fall 2016). 

IVF stands for “In Vitro Fertilization,” and is one of several infertility treatments offered to want-to-be-mothers and fathers who are not able to conceive naturally. A woman’s eggs are extracted, and then fertilization is attempted by combining her eggs with sperm in a laboratory dish. Fertilized eggs, which are called embryos, are then transferred to the woman’s uterus. The chance of pregnancy and live birth depends on many factors, including the woman’s age, her and her partner’s health, etc. (source: https://www.cdc.gov/art/artdata/index.html)

By law, fertility clinics in the US must report data on IVF and other fertility procedures to the Centers for Disease Control and Prevention (CDC). Currently, these clinic-level data are publicly available online as individual Excel files, with poorly named variables, in what one could reasonably deem as a very convoluted and incomprehensible format.

  *  http://www.cdc.gov/art/artdata/index.html
  *  http://www.cdc.gov/art/reports/archive.html
  
Our interactive program aims to make the data more accessible and user-friendly. Specifically, the user is able to do the following:

1.	Input her address, and the program generates a list of at least 10 clinics closest to the entered  address. 

2.	Choose 1 clinic from the list offered in #1 above, and compare key statistics for the chosen clinic with the performance of other IVF clinics in the same state as the chosen clinic (averages and medians). These data are reported for 2014, the most recent year available.

3.	Then, the user can view a bar chart that show how the clinic of her choice ranks relative to other clinics in the state based on either “the total number of IVF procedures” performed by each clinic or “the live birth rate (per 100 transfers)”. These data are reported for 2014, the most recent year available.

4.	Also, the user can compare the clinic’s performance overtime (2007 – 2014) with the average of all the other clinics across the country. 

To understand the output of our program, it is important to understand what data the clinics have to report to the CDC. First, note that IVF can be performed with the woman’s own eggs or donated eggs (i.e., eggs from another woman).  

**Own eggs:**  Normally, a fresh (i.e., newly extracted) egg is used for fertilization, but sometimes extracted viable eggs can be frozen and used for fertilization at a later time (“frozen eggs”). When the woman uses her own eggs, the clinics record data for **“fresh nondonor eggs”** and **“frozen nondonor eggs.”** Our program asks the woman whether she uses her own eggs, and if so, reports key statistics by age categories (< 35 years old, 35-37, 38-40, 41-42, 43-44, and > 44 years old). 

**Donor eggs:** If the woman uses donated eggs, the CDC reports two scenarios: The embryo (resulting from a successfully fertilized egg) is implanted into the woman’s uterus 2-3 days after fertilization (**“fresh embryos from donor eggs”**). Or, sometimes the woman may have chosen to freeze the embryos to use them at a later time (**“frozen embryos from donor eggs”**). The statistics that our program generates in this case are not age-specific, because the age of the woman who is trying to get pregnant is no longer relevant (it is the age of the donor that is important but it is not reported as donors normally have to be in their 20’s).

Our program generates clinic-level statistics such as:
  * Total number of cycles performed (a cycle is a treatment cycle of injections that the woman undergoes to stimulate her own eggs)
  * Cancellations per 100 cycles (e.g., because treatment fails to stimulate the woman’s eggs)
  * Number of embryo transfers attempted
  * Average number of embryos transferred (normally, more than one embryo is transferred because not all embryos turn out to be viable)
  * Pregnancies per 100 cycles (when the woman’s undergoes treatment to stimulate her own eggs)
  * Pregnancies per 100 transfers (any woman)
  * Live births per 100 cycles (when the woman’s undergoes treatment to stimulate her own eggs)
  * Live births per 100 transfers (any woman)

The user is able to explore these official IVF data depending on her age, location, and egg/embryo type.  

#### Collaborators / Team members
---------------------------------

 - Zhanna Victorovna Zhanabekova (zvz201)
 - Zahra Kadkhodaie (zk388)
 - Eduardo Fierro Farah(eff254)

#### Supervision and Evaluation
-------------------------------

 *Project subject to evaluation for program correctness*

Prof. Greg Watson (Teacher) 
Maria Elena Villalobos Ponte (Section Leader) 

#### Data
---------

All the data was downloaded from the CDC website. 

-	2014 data: https://www.cdc.gov/art/artdata/index.html, “Download the Data – Clinic Tables and Data Dictionary[XLS - 1.4 MB]”
-	Data for earlier years: https://www.cdc.gov/art/reports/archive.html

The latest update of the data was on October 26, 2016. The original files were saved in the Data Folder. 


#### Technical details
----------------------

The project was developed in **Python 3.6**
The following external libraries need to be installed for the program to run properly: 
 - Numpy (version 1.11.2 or above): https://docs.scipy.org/doc/numpy
 - Pandas (version 0.19.1 or above): https://pypi.python.org/pypi/pandas
 - Matplotlib (version 1.5.3 or above): http://matplotlib.org
 - Geopy (version 1.11.0 or above): https://pypi.python.org/pypi/geopy/1.11.0
 - Geocoder (version 1.19.0 or above): https://pypi.python.org/pypi/geocoder

The program also needs some Python standard libraries (https://docs.python.org/3/library/index.html): 
 - time: https://docs.python.org/3/library/time.html
 - os: https://docs.python.org/3/library/os.html
 - sys: https://docs.python.org/3/library/sys.html

 
 To install the above libraries, once python 3 is installed, you can run from the command line: 
 
$ pip install numpy

$ pip install pandas

$ pip install geopy

$ pip install geocoder

$ pip install  matplotlib

$ pip install pylab

 
#### Deployment
---------------

Use your operating system command line to run the package:

 $ python IVFProject.py
 
For the program to run correctly, set your working directory to the directory where the program files are located.

Else, you can change the “datadir” object in the following functions: 
-	importMyCsv in InputFunctions.py module. 
-	load_data in InputFunctions.py module.


#### Walkthrough
----------------

1.	The user inputs her main characteristics:

	1.	Her age (must be between 18 and 70) 
	2.	Whether she uses her own eggs or donor eggs (binary choice)
	3.	Whether “frozen” or “fresh” (binary choice)
		1.	If own eggs, “frozen” means “frozen eggs” and “fresh” means “fresh eggs”
		2.	If donor eggs, “frozen” means “frozen embryo” and “fresh” means “fresh embryo”

2.	The user inputs her address:
	1.	[full address], [city, state], or any other geo unit [state, county, city, country, etc.]. 

3.	The program generates a list of at least 10 clinics closest to the inputted address. 
	1.	In the case of a generic geo unit such a state, for example, the program outputs at least 10 clinics from the state’s centroid.
	2.	The list is generated from the list of clinics in the CDC 2014 file, the most recent year for which data are available.

4.	The user has to choose one clinic from the list offered above.

5.	The program generates a table where it lists key statistics for the chosen clinic, as well averages and medians of the same statistics for other IVF clinics located in the same state as the chosen clinic. These data are reported for 2014, the most recent year for which data are available.

6.	The program then asks the user whether she wants to see the ranking of all clinics in the state by either one of two variables: the total number of IVF procedures performed or the live birth rate (per 100 transfers).
	1.	Depending on what variable the user chooses, the program generates a horizontal bar plot of clinics sorted by the variable in descending order. The clinic originally chosen by the user will be marked in a different color.
	2.	These data are reported for 2014, the most recent year for which data are available.

7.	After that, the user can compare the clinic’s performance overtime (2007 – 2014) with national averages with a line plot. The national data are tailored to the group most similar to the user. For example, if the user is under 35 years old and uses her own frozen eggs, the average data presented on the plot reflects only the data related to this group of women. If the data is missing for some or all years for the selected clinic, the user is notified about the missing information.


#### Tests
----------

A module is provided with sufficient test. The test can be run using: 

$ python Tests.py


 
#### Geo referencing
--------------------

All the geo referencing for clinics was performed with the module GeoRefCities.py. IVFProject.py or any other module does not call this GeoRefCities.py. 

It's worth noting that some geo referencing was completed by hand after the code was run. 

 
#### CHANGELOG
--------------

This corresponds to the version 1.0.0 of the package "IVFsearchClinics". 

No Other versions have been developed.