from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import date
import time
import os.path

# User preferences
opheadless = 1 # 0 show browser during running, 1 run browser in headless mode
opnzzuser = "YOUR_USERNAME" # add your nzz.ch username
opnzzpwd =  "YOUR_PASSWORD" # add your nzz.ch password
opoutputpathfile = "CHOOSE_PATH" # path of the file you want to write the results into, add / at the end
opoutputnamefile = "CHOOSE_NAME" # name of the file you want to write the results into

# System preferences, should not be changed unless you know what to do
opnzzloginsite = "https://login.nzz.ch/?target=https%3A%2F%2Fwww.nzz.ch%2F&action=login"
opnzzlistsite = "https://www.nzz.ch/meine-nzz/merkliste"
opnzzloginfield = "input#c1-login-field"
opnzzpwdfield = "input#c1-password-field"
opnzzmorebutton = "button.button--loadmore"
opnzztagname = "article"
opnumberclicks = 3
opoutputtypefile = ".csv"
oplogtypefile = ".log"
opoutputfiletowrite = (opoutputpathfile + opoutputnamefile + opoutputtypefile)
countartold = 0
countartnew = 0
countartfin = 1
today = date.today()

# Functions
def addentry_tofile():
    myfile.write(str(today) + "," + str(countartfin) + "\n")

def addheader_tofile():
    myfile.write("DATE,COUNT" + "\n")

# Check first if output file doesn't include an entry for today already
if os.path.exists(opoutputfiletowrite):
    with open(opoutputfiletowrite) as myfile:
        if str(today) in myfile.read():
            print("Already an entry for today, exiting script")
            exit()            
        else:
            pass
else:
    pass

# Start script
edgeop = webdriver.EdgeOptions()
if opheadless == 1:
    edgeop.add_argument('headless')
elif opheadless == 0:
    pass
else:
    print("Invalid options, please choose 0 or 1")

driver = webdriver.Edge(options=edgeop)

# Login to site
driver.get(opnzzloginsite)
elemuser = driver.find_element(By.CSS_SELECTOR, opnzzloginfield)
elemuser.clear()
elemuser.send_keys(opnzzuser)
elempwd = driver.find_element(By.CSS_SELECTOR, opnzzpwdfield)
elempwd.clear()
elempwd.send_keys(opnzzpwd)
elempwd.send_keys(Keys.RETURN)

# Switch to read list and count number of articles
time.sleep(5)
driver.get(opnzzlistsite)
time.sleep(3)
elemmore = driver.find_element(By.CSS_SELECTOR, opnzzmorebutton)
while countartfin != countartnew:
    currentnumberofclicks = 0
    while currentnumberofclicks < opnumberclicks:
        elemmore.click()
        time.sleep(0.5)
        currentnumberofclicks += 1
    countartold = countartnew
    countartnew = len(driver.find_elements(By.TAG_NAME, opnzztagname))
    countartfin = countartold

# Write final number into file
if os.path.exists(opoutputfiletowrite):
    with open(opoutputfiletowrite, "+a") as myfile:
        addentry_tofile()

else:
    with open(opoutputfiletowrite, "a") as myfile:
        addheader_tofile()
        addentry_tofile()

# End script
driver.close()
