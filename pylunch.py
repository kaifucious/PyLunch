#!/usr/bin/env python
# Copyright (c) Meikell "Kai" Lamarr 2014-2015 Marathon Data Systems
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
''' 
This program will automatically fill out lunchpac web forms to order
default lunches for yourself using crontabs, in case you forget to order lunch for that
day. You do need to set the `uname`, `pwd`, and all `defaults` in the code,
as I tried to use as little raw_inputs as possible to prevent human typing
errors. If you need help, feel free to come by the Engineering room and 
talk to me. This software is under the "use-at-your-own-risk" license,
meaning if you don't understand it, grab an engineer that can read Python 
code and sit there till you do understand it. Seriously I don't wanna  
hear no crying and whining about "oh i dont understand it". Eat a snickers bar.
***P.S. Don't be coming to me trying to blame me for you screwing up your 
defaults or miscalculating your daily food limit either. 
You know how to look at the menu and spell and do math. :P
Dictated. Not Read.
The Author. 
'''

# Constants
__auth__ = "Meikell Lamarr"
__version__ = 1.0 
site_callback = "http://lunchpac.marathondata.com/login.asp"
uname = ""
pwd = ""
exit_with_errors = -1
exit_gracefully = 0
# Monday
monday_main_default = ""
monday_soup_default = ""
monday_soup_size_default = "" 
monday_comments_default = "" 
# Tuesday
tuesday_main_default = "" 
tuesday_soup_default = "" 
tuesday_soup_size_default = "" 
tuesday_comments_default = "" 
# Wednesday (Surf Taco)
wednesday_stmain_default = "" 
wednesday_stsoup_default = "" 
wednesday_stsoup_size_default = "" 
wednesday_stcomments_default = "" 
# Wednesday (Muscle Maker Grill)
wednesday_mmgmain_default = "" 
wednesday_mmgsoup_default = ""
wednesday_mmgsoup_size_default = "" 
wednesday_mmgcomments_default = ""
# Thursday (What About A Bagel)
thursday_waabmain_default = "" 
thursday_waabsoup_default = "" 
thursday_waabsoup_size_default = "" 
thursday_waabcomments_default = "" 
# Thursday (Garden Dragon)
thursday_gdmain_default = "" 
thrusday_gdsoup_default = "" 
thursday_gdsoup_size_default = "" 
thursday_gdcomments_default = "" 
# Friday
friday_main_default = "" 
friday_soup_default = "" 
friday_soup_size_default = "" 
friday_comments_default = ""


import re
import os
import sys
import logging 
import cookielib
import datetime 
from termcolor import colored, cprint
try:
    import mechanize
except ImportError:
    print(colored("[!] Mechanize was not detected on this system. To be able to run this script, you must install Mechanize. Would you like to install it now?","magenta"))
    auth = raw_input("(Y/y or N/n): ")
    if auth.lower() == "y":
        print(colored("[+] Installing Mechanize...","cyan"))
        os.system("sudo easy_install mechanize")
        print(colored("[+] Mechanize has been installed, please run this script again to start the scheduler. (It's also recommended to install `pip` if you plan on working with Python files in the future.)"))
        sys.exit(exit_gracefully)
    else:
        print(colored("[!] You have chosen not to install Mechanize. Good bye!","blue"))
        sys.exit(exit_with_errors)


def banner(): 
    '''
    Prints out a simple banner.
    '''
    print(colored("\n\t\tPyLunch, Version %.1f, %s"%(__version__, __auth__),"green"))
    print(colored("\t\t2014 Marathon Data Systems, LLC.\n","green"))


def check_defaults():
    '''
    Checks and makes sure defaults are filled in properly.
    '''
    if monday_main_default == "" or tuesday_main_default == "" or friday_main_default == "":
        print(colored("[!] One or more defaults are not set in this program. Please make sure all defaults are set, then run this program again. [lines: 0-0]","red"))
        sys.exit(exit_with_errors)
    elif wednesday_stmain_default == "" and wednesday_mmgmain_default == "":
        print(colored("[!] You have not set a defaults for either restaurant for Wednesday. Please fill the defaults correctly, and run this program again. [lines: 0-0]","red"))
        sys.exit(exit_with_errors)
    elif wednesday_stmain_default != "" and wednesday_mmgmain_default != "":
        print(colored("[!] You have set both restaurant defaults for Wednesday. Please make sure you only fill out the defaults for either Surf Taco or MMG. [lines:  0-0]","red"))
        sys.exit(exit_with_errors)
    elif thursday_waabmain_default == "" and thursday_gdmain_default == "":
        print(colored("[!] You have not set a defaults for either restaurant for Thursday. Please fill the defaults correctly, and run this program again. [lines: 0-0]","red"))
        sys.exit(exit_with_errors)
    elif thursday_waabmain_default != "" and thursday_gdmain_default != "":
        print(colored("[!] You have set both restaurant defaults for Thursday. Please make sure you only fill out the defaults for either Surf Taco or MMG. [lines:  0-0]","red"))
        sys.exit(exit_with_errors)


def print_response(response):
    '''
    View the HTML response from the browser
    '''
    print response.read()

def print_links(link):
    '''
    Prints out current HTML page links in the Terminal/Command-Line
    '''
    print(link)
    print(link.url)

def write_log(response,can_write=True):
    '''
    Writes a log to the PyLunch folder. 
    '''
    if can_write:
        response_string = str(response.read())
        pylunch_log = "pylunch.log"
        logging.basicConfig(filename=pylunch_log,
                            format='%(asctime)s %(message)s',
                            level=logging.DEBUG, 
                            )
        logging.debug(response_string)
        f = open(pylunch_log, 'rt')
        try: body = f.read()
        finally: f.close()  

def timout_regex(response):
    '''
    Searches for a regex indicating that the user can no longer place 
    lunch orders, as the time criteria has been met. If it finds a 
    match, let the user know that they can't submit orders, and exit
    gracefully. This function is really only used for manual entry, 
    obviously the script is automatic so in theory it should never not 
    order a lunch. 
    '''
    timeout_string = "all orders have been placed for today"
    response_string = str(response.read())

    if re.search(timeout_string, response_string):
        # Match Found, Time is exceeded 
        print(colored("[!] You have missed the deadline to order lunch! Please see the Marathon Data Systems Accounting department.","red"))
        write_log(response)
        sys.exit(exit_gracefully)

 

def override(*args,**kwargs):
    pass # experimental




def main(*args,**kwargs):
    '''
    Where all the magic happens. Construct a basic mechanize browser 
    and set up a cookie jar for it, and start firing off get/post requests
    until you cant fire no more.
    '''
    # Print banner 
    banner() 
    # Check defaults
    check_defaults()
    # Set Up The Browser
    mds_browser = mechanize.Browser()
    # Cookie Jar
    cookie_jar = cookielib.LWPCookieJar()
    mds_browser.set_cookiejar(cookie_jar)
    # Set up browser options
    mds_browser.set_handle_equiv(True)
    mds_browser.set_handle_redirect(True) 
    mds_browser.set_handle_referer(True)
    mds_browser.set_handle_robots(False) 
    mds_browser.set_handle_refresh(False)
    # Get the response code from the callback
    response_code = mds_browser.open(site_callback)
    # Submit the form (LunchPac Login Form)
    mds_browser.select_form(nr=0)
    mds_browser.form["UserName"] = uname
    mds_browser.form["Password"] = pwd
    response = mds_browser.submit()
    write_log(response)

    # Get the day of the week, because some days a user may have more
    # than 1 restaurant to choose from. *Note: Monday is 0, Sunday is 6.
    today = datetime.datetime.today().weekday() 

    if today == 0:  
        print(colored("[+] Today is Monday, the beginning of the work week. Time for some Grossman's Deli!","cyan"))
        #for link in mds_browser.links():
        #   print_links(link)
        # Get the Muscle Man Group URL
        print(colored("[+] Opening Grossman Deli's order submission menu...","cyan"))
        target_url = "/restaurant.asp"
        mds_browser.find_link(url=target_url)
        the_burger = mds_browser.click_link(url=target_url)
        response = mds_browser.open(the_burger)
        timout_regex(response)
        # Fill out the order form and submit it if time is still valid
        for form in mds_browser.forms():
            print(colored("[+] Placing order...","cyan"))
            mds_browser.select_form(nr=0)
            mds_browser.form["OrderItem1"] = monday_main_default
            mds_browser.form["Soup1"] = monday_soup_default
            mds_browser.form["SoupSize1"] = monday_soup_size_default
            mds_browser.form["OrderComments1"] = monday_comments_default
            response = mds_browser.submit()
            write_log(response)
            print(colored("[+] You have successfully placed an order. To review your order, please log in to LunchPac.","cyan"))
            sys.exit(exit_gracefully)  

    elif today == 1: 
        print(colored("[+] Today is Tuesday. Time for some Nino Jr's!","cyan"))
        #for link in mds_browser.links():
        #   print_links(link)
        # Get the Muscle Man Group URL 
        print(colored("[+] Opening Nino Jr's order submission menu...","cyan"))
        target_url = "/restaurant.asp"
        mds_browser.find_link(url=target_url)
        the_sandwich = mds_browser.click_link(url=target_url)
        response = mds_browser.open(the_sandwich)
        timout_regex(response)
        # Fill out the order form and submit it 
        for form in mds_browser.forms():
            print(colored("[+] Placing order...","cyan"))
            mds_browser.select_form(nr=0)
            mds_browser.form["OrderItem1"] = tuesday_main_default
            mds_browser.form["Soup1"] = tuesday_soup_default
            mds_browser.form["SoupSize1"] = tuesday_soup_size_default
            mds_browser.form["OrderComments1"] = tuesday_comments_default
            response = mds_browser.submit()
            write_log(response)
            print(colored("[+] You have successfully placed an order. To review your order, please log in to LunchPac.","cyan"))
            sys.exit(exit_gracefully)  

    elif today == 2: 
        if wednesday_stmain_default != "":
            # User is using Surf Taco's defaults
            print(colored("[+] Today is Wednesday. You have Surf Taco set as your default.","cyan"))
            #for link in mds_browser.links():
            #  print_links(link)
            # Get the Surf Taco URL
            print(colored("[+] Opening the Surf Taco order submission menu...","cyan"))
            target_url = "/default.asp?RestaurantID=11" 
            mds_browser.find_link(url=target_url)
            the_taco = mds_browser. click_link(url=target_url)
            mds_browser.open(the_taco)
            # Fill Out the Order Form and Submit it
            for form in mds_browser.forms():
                print(colored("[+] Placing order...","cyan"))
                mds_browser.select_form(nr=0)  
                mds_browser.form["OrderItem1"] = wednesday_stmain_default
                mds_browser.form["Soup1"] = wednesday_stsoup_default
                mds_browser.form["SoupSize1"] = wednesday_stsoup_size_default
                mds_browser.form["OrderComments1"] = wednesday_stcomments_default
                response = mds_browser.submit() 
                #print_response(response)
                print(colored("[+] You have successfully placed an order. To review your order, please log in to LunchPac.","cyan"))
                sys.exit(exit_gracefully)
        elif wednesday_mmgmain_default != "":
            # User is using Muscle Man Group's defaults
            print(colored("[+] Today is Wednesday. You have Muscle Man Group set as your default.","cyan"))
            #for link in mds_browser.links():
            #   print_links(link)
            # Get the Muscle Man Group URL 
            print(colored("[+] Opening the Muscle Man Group order submission menu...","cyan"))
            target_url = ""
            mds_browser.find_link(url=target_url)
            the_muscle = mds_browser.click_link(url=target_url)
            mds_browser.open(the_muscle)
            # Fill out the order form and submit it 
            for form in mds_browser.forms():
                print(colored("[+] Placing order...","cyan"))
                mds_browser.select_form(nr=0)
                mds_broswer.form["OrderItem1"] = wednesday_mmgmain_default
                mds_browser.form["Soup1"] = wednesday_mmgsoup_default
                mds_browser.form["SoupSize1"] = wednesday_mmgsoup_size_default
                mds_browser.form["OrderComments1"] = wednesday_mmgcomments_default
                response = mds_browser.submit()
                #print_response(response)
                print(colored("[+] You have successfully placed an order. To review your order, please log in to LunchPac.","cyan"))
                sys.exit(exit_gracefully)

    elif today == 3: 
        if thursday_waabmain_default != "":
            # User is using What About A Bagel's defaults
            print(colored("[+] Today is Thursday. You have What About A Bagel set as your default.","cyan"))
            #for link in mds_browser.links():
            #  print_links(link)
            # Get the What About A Bagel URL
            print(colored("[+] Opening the What About A Bagel order submission menu...","cyan"))
            target_url = "" 
            mds_browser.find_link(url=target_url)
            the_bagel = mds_browser. click_link(url=target_url)
            mds_browser.open(the_bagel)
            # Fill Out the Order Form and Submit it
            for form in mds_browser.forms():
                print(colored("[+] Placing order...","cyan"))
                mds_browser.select_form(nr=0)  
                mds_browser.form["OrderItem1"] = thursday_waabmain_default
                mds_browser.form["Soup1"] = thursday_waabsoup_default
                mds_browser.form["SoupSize1"] = thursday_waabsoup_size_default
                mds_browser.form["OrderComments1"] = thursday_waabcomments_default
                response = mds_browser.submit() 
                #print_response(response)
                print(colored("[+] You have successfully placed an order. To review your order, please log in to LunchPac.","cyan"))
                sys.exit(exit_gracefully)
        elif thursday_gdmain_default != "":
            # User is using Garden Dragon's defaults
            print(colored("[+] Today is Thursday. You have Garden Dragon set as your default.","cyan"))
            #for link in mds_browser.links():
            #   print_links(link)
            # Get the Muscle Man Group URL 
            print(colored("[+] Opening the Garden Dragon order submission menu...","cyan"))
            target_url = ""
            mds_browser.find_link(url=target_url)
            the_chinese = mds_browser.click_link(url=target_url)
            mds_browser.open(the_chinese)
            # Fill out the order form and submit it 
            for form in mds_browser.forms():
                print(colored("[+] Placing order...","cyan"))
                mds_browser.select_form(nr=0)
                mds_browser.form["OrderItem1"] = thursday_gdmain_default
                mds_browser.form["Soup1"] = thursday_gdsoup_default
                mds_browser.form["SoupSize1"] = thursday_gdsoup_size_default
                mds_browser.form["OrderComments1"] = thursday_gdcomments_default
                response = mds_browser.submit()
                #print_response(response)
                print(colored("[+] You have successfully placed an order. To review your order, please log in to LunchPac.","cyan"))
                sys.exit(exit_gracefully)

    elif today == 4: 
        print(colored("[+] Today is Friday, the end of the work week. Time for some Dominic's!","cyan"))
        #for link in mds_browser.links():
        #   print_links(link)
        # Get the Muscle Man Group URL 
        print(colored("[+] Opening the Dominic's order submission menu...","cyan"))
        target_url = "/restaurant.asp"
        mds_browser.find_link(url=target_url)
        the_pizza = mds_browser.click_link(url=target_url)
        mds_browser.open(the_pizza)
        # Fill out the order form and submit it 
        for form in mds_browser.forms():
            print(colored("[+] Placing order...","cyan"))
            mds_browser.select_form(nr=0)
            mds_brower.form["OrderItem1"] = friday_main_default
            mds_browser.form["Soup1"] = friday_soup_default
            mds_browser.form["SoupSize1"] = friday_soup_size_default
            mds_browser.form["OrderComments1"] = friday_comments_default
            response = mds_browser.submit()
            #print_response(response)
            print(colored("[+] You have successfully placed an order. To review your order, please log in to LunchPac.","cyan"))
            sys.exit(exit_gracefully) 
    else: 
        # Realistically, we shouldnt get to this point, since nobody works on Saturday and Sunday.
        # However, so those days won't be too sad and left out, we just simply print out a weekend message.
        print(colored("[+] It's the weekend, why is this program running? Go out and partayyy!"))    
        sys.exit(exit_gracefully)

if __name__ == "__main__":
    main()




