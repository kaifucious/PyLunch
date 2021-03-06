@info 
PyLunch 

@credits 
Meikell "Kai" Lamarr 
Marathon Data Systems, 2014™

@supported_platforms
Mac OS 10.8+ 

@dependencies 
CronTabs
Python 2.7+ 

@setup 
In order to run PyLunch automatically, you must set up CronTabs on your Mac. In order 
to get this setup, open up a terminal and use:

env EDITOR=nano crontab -e 

This will open up a nano editor, where you can add Cron jobs at. The Cron syntax is 

*	*	*	*	*	sudo python /path/to/script

where the first asterisk is for specifying the minute of the run (0-59), the second asterisk 
is for specifying the hour of the run (0-23), the third asterisk is for specifying the day of the month of the run (0-31), the fourth asterisk is for specifying the month of the run (1-12),
and the fifth asterisk is for specifying the day of the week (where Sunday is equal to 0, and Saturday is equal to 6). You can replace the path/to/script placeholder with the path to the pylunch program, which is probably /users/your_username/pylunch/pylunch.py

@usage
Say you wanted to run PyLunch everyday at 09:00 AM - you would use the following sequence:

00	9	*	*	*

or if you wanted to run the script once a week on Wednesday, you could use the following sequence:

*	*	*	*	3

Although you can make the sequence whatever you want, it's wise to choose a sequece that will order at least an half hour before the lunch cutoff. For instance, if you ran a Cron at 9:00 A.M., since the cutoff for most days is 9:30 A.M. this will ensure that you have a default lunch "on hold" (you can always change it until the cutuff). If you do not change it, the default will be in place already. 

After you're done configuring the CronTab, to save the tab press Control + O (to write the file), then Enter to accept the new file name, and then Control + X (to exit nano).

To delete the CronTab, just open up the crontab with:

env EDITOR=nano crontab -e

and delete it and resave. 

To see a list of all CronTabs, use:

crontab -l 

To see if the CronTab successfully executed the program, use: 

mail

To delete all mail in the CronTab mailbox, use:

cd /var/mail 

and delete the lone file 

@additional_help
To get more help on the PyLunch module itself, open up a terminal window and start a Python environment:

python 

After the environment starts, import the pylunch module and call help() on it: 

import pylunch 
help(pylunch)

The doc string should explain what's going on. If you still don't understand, contact me and I'll try and help you out. 

REMEMBER TO ADD YOUR OWN USERNAME AND PASSWORD LOGIN TO PYLUNCH.PY OR NOTHING WILL WORK!!!


--------------------------
Happy Lunch Ordering! 
>>> Hack the Gibson




