@info 
PyLunch 
Marathon Data Systems, 2014™

@credits 
Meikell "Kai" Lamarr 

@supported_platforms
Mac OS 10.8+ 

@dependencies 
CronTabs
Python 2.7+ 

@help 
In order to run PyLunch automatically, you must set up CronTabs on your Mac. In order 
to get this setup, open up a terminal and use:

env EDITOR=nano crontab -e 

This will open up a nano editor, where you can add cron jobs at. The cron syntax is 

*	*	*	*	*	[path/to/script]

where the first asterisk is for specifying the minute of the run (0-59), the second asterisk 
is for specifying the hour of the run (0-23), the third asterisk is for specifying the day of the month of the run (0-31), the fourth asterisk is for specifying the month of the run (1-12),
and the fifth asterisk is for specifying the day of the week (Where Sunday is equal to 0, and Saturday is equal to 6). You can replace the [path/to/script] with the path to the pylunch program, which is probably /users/your_username/pylunch/pylunch.py

Say you wanted to run PyLunch everyday at 09:30 AM - you would use the following sequence:

30	9	*	*	*

or if you wanted to run the script once a week on Wednesday, you could use the following sequence:

*	*	*	*	3

Although you can make the sequence whatever you want, it's wise to choose a sequece that will order a couple of minutes (if not exactly 1 minute) before 9:30 AM, as this is the general cutoff time for lunch orders during the week. 

After you're done configuring the CronTab, to save the tab press Control + O (to write the file), then Enter to accept the new file name, and then Control + X (to exit nano).

To delete the CronTab, just open up the crontab with:

env EDITOR=nano crontab -e

and delete it and resave. 

To see a list of all CronTabs, use:

crontab -l 

To get more help on the PyLunch module itself, open up a terminal window and start a Python environment:

python 

After the environment starts, import the pylunch module and call hep() on it: 

import pylunch 
help(pylunch)

The doc string should explain what's going on. If you still don't understand, contact me and I'll help you out. 

REMEMBER TO ADD YOUR OWN USERNAME AND PASSWORD LOGIN TO PYLUNCH.PY OR NOTHING WILL WORK!!!


--------------------------
Happy Lunch Ordering! 
>>> Hack the Gibson




