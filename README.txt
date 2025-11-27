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

Download the CritterScribeApp.exe, ZooDashApp.exe, PawCache.sql, sampleuseraccounts.sql and Sample_ZooFlow_setup.bat and keep the last three in same folder. (you may download all the files and keep them together too). Now run the installer setup file and enter your root password. It'll close on its own and your setup is done !

In case you get some error after putting the root password in setup, or if setup runs successfully but the apps don't run, follow the below steps-

- go to your MySQL command line and confirm if you are putting the correct password and it is working.

- if you are sure you are putting correct password but it still doesn't enter, open 'MySQL Installer - Community' on your system and reconfigure MySQL server.
- follow the steps, enter your root password when needed and after it finishes, your MySQL will work fine again. If it rejects your password there, then your password is incorrect. You might need to remember it or reinstall MySQL.

- If password is not an issue, then search and open 'edit the system environment variables' settings on your windows (or similar setting for other operating systems)
- select environment variables, then select 'Path' variable in the list and click edit.
- check if there is a path to bin directory of MySQL (example- C:\Program Files\MySQL\MySQL Server 8.0\bin). If not, locate the bin folder in your system (it could be in different drive or sequence of directories or could be same as the example) and add the path.
- Apply all the settings and close the dialogues, refresh your system and try running the installer setup file once more.

The apps (CritterscribeApp and ZooDashApp) should run properly once the installer setup file has been run successfully first. In case of any other errors, contact the developer. Now you can use the apps on a sample database.
If you have made any changes and want to reset the pawcache data, run the installer again and all the user and pawcache data will be reset. Note that the additional users (if made using add staff option of ZooDash) may not get dropped from your MySQL even if the staff_dat table is reset. So you'll have to manually drop the user if required. 

Below are some inbuilt sample logins for all four login types
1. username- imrans	password- imran	login for critterscribe as Imran Sheikh who is zookeeper/animal-caretaker/veterinary
2. username- udaans	password- udaan	login for critterscribe as Udaan Sharma who is internal shop/stall keeper
3. username- nishat	password- nisha	login for zoodash as Nisha Tiwari who is zoo manager
4. username- mikee	password- mike	login for zoodash as Mike Elipson who is zoo admin

Project details and purpose can also be read on info page in CritterScribe and ZooDash Apps. This is a sample Zoo Management system made on python and MySQL. This is an original work made for class 12th CBSE Computer Science (083) Project. Project is based on an average of system of common zoos in India and not according to any one zoo. All the data present in the databases are sample and fictional, and are not taken from any sources.

Developed by Khushil Varshney

Thanks for checking out my project.


