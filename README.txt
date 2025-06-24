This ZooFlow Project Folder contains-

1. Critterscribe-Code (.py)
	The sourcecode program for Critterscribe-App

2. ZooDash-Code (.py)
	The sourcecode program for ZooDash-App

3. CritterscribeApp (.exe)
	An app for Animal Record Management for Zoo Workers. CritterScribe lets the workers of the zoo and caretakers of the various species to update and check the data regarding the meals of every animal in the area, their health check or cleanliness records, gender and age. This serves easy recording of data without making any mess or chance to forget about  anything, in an perfect and efficient manner.

4. ZooDashApp (.exe)
		One Dashboard, for Efficient Tracking, and displaying Piles of Zoo Data. ZooDash, lets the owners, admins or managers of the zoo to have a check on all the records updated by the workers, and on the stock amount of food resources and medicines they have for their animals, so that they dont find themselves in the corner at the last moment. It helps track the visiting patterns too, while registering the entries and ticket with the time and money records.

5. README File (.txt)
	Contains instructions and information regarding other files and how to run the apps properly.

6. Sample_ZooFlow_setup (.bat)
	Installs the Pawcache database and sample user accounts and other resources for displaying or running the apps, as stored in PawCache.sql and sampleuseraccounts.sql respectively. DO NOT SEPARATE THESE THREE FILES. THIS SETUP WILL ONLY WORK IF THE THREE FILES ARE TOGETHER IN SAME DIRECTORY. Before running the apps for first time on a system you must run the installer. It will ask your 'root' password once, and its totally safe so you can simply enter it.

7. PawCache (.sql)
	The database, PawCache as we call it, with its structure built on MySQL, is connected with the above applications through the well known language of python, having a clean set of separated tables for staff details, visitor tickets, animals and their info and the resources available in stock. It is designed in a way to create maximum and efficient outputs, while being easily modifiable and upgradable. The file contains the database and can be loaded into a system with MySQL using the installer.

8. sampleuseraccounts (.sql)
	Contains some sample users from sample PawCache for Project display and usage. The file contains the creation and privileges of userids and can be loaded into a system with MySQL using the installer. It only adds the users, so no user already existing on the system will be altered.

Instructions for installation and setup

Download the CritterScribeApp.exe, ZooDashApp.exe, PawCache.sql, sampleuseraccounts.sql and Sample_ZooFlow_setup.bat and keep the last three in same folder. (you may download all the files and keep them together too). Now run the setup file and enter your root password. It'll close on its own and your setup is done !
The apps (CritterscribeApp and ZooDashApp) should run properly once the installer has been run successfully first. In case of any errors, contact the developers. Now you can use the Apps on sample database.
If you have made any changes and want to reset the pawcache data, run the installer again and all the user and pawcache data will be reset. Note that the additional users (if made using add staff option of ZooDash) may not get dropped from your MySQL even if the staff_dat table is reset. So you'll have to manually drop the user if required. 

Below are some inbuilt sample logins for all four login types
1. username- imrans	password- imran	login for critterscribe as Imran Sheikh who is zookeeper/animal-caretaker/veterinary
2. username- udaans	password- udaan	login for critterscribe as Udaan Sharma who is internal shop/stall keeper
3. username- nishat	password- nisha	login for zoodash as Nisha Tiwari who is zoo manager
4. username- mikee	password- mike	login for zoodash as Mike Elipson who is zoo admin

Project details and purpose can also be read on info page in CritterScribe and ZooDash Apps. This is a sample Zoo Management system made on python and MySQL. This is an original project work made for class 12th CBSE Computer Science (083) Project work. Project is based on an average of system of common zoos in India and not according to any one zoo. All the data present in the databases are sample and fictional, and are not taken from any sources.

<this file (as well as the ZooDash App) will be updated after the project file is made, so if you are reading this line, you came in too early, and that's good, you got to see this rare line that no one else will see ever after update. Everyone who tests and tries to run this, we'll appreciate if you give reviews, suggestions or report if any bugs are found.>

Developed by Khushil Varshney
Thanks for Reading.