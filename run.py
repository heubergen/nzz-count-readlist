from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import date
import time
import os.path

# User preferences
opsheadless = 1 # 0 show browser during running, 1 run browser in headless mode
opsnzzuser = "YOUR_USERNAME" # add your nzz.ch username
opsnzzpwd =  "YOUR_PASSWORD" # add your nzz.ch password
opsoutputpathfile = "CHOOSE_PATH" # path of the file you want to write the results into, add / at the end
opsoutputnamefile = "CHOOSE_NAME" # name of the file you want to write the results into

# System preferences, should not be changed unless you know what to do
opsnzzloginsite = "https://login.nzz.ch/?target=https%3A%2F%2Fwww.nzz.ch%2F&action=login"
opsnzzlistsite = "https://www.nzz.ch/meine-nzz/merkliste"
opsnzzloginfield = "input#c1-login-field"
opsnzzpwdfield = "input#c1-password-field"
opsnzzmorebutton = "button.button--loadmore"
opsnzztagname = "article"
opsnumberclicks = 3
opsoutputtypefile = ".csv"
opslogtypefile = ".log"
opsoutputfiletowrite = (opsoutputpathfile + opsoutputnamefile + opsoutputtypefile)
countartold = 0
countartnew = 0
countartfin = 1


# Functions
def addentry_tofile():
    myfile.write(str(today) + "," + str(countartfin) + "\n")

def addheader_tofile():
    myfile.write("DATE,COUNT" + "\n")

# Start script
edgeop = webdriver.EdgeOptions()
if opsheadless == 1:
    edgeop.add_argument('headless')
elif opsheadless == 0:
    pass
else:
    print("Invalid options, please choose 0 or 1")

driver = webdriver.Edge(options=edgeop)

# Login to site
driver.get(opsnzzloginsite)
elemuser = driver.find_element(By.CSS_SELECTOR, opsnzzloginfield)
elemuser.clear()
elemuser.send_keys(opsnzzuser)
elempwd = driver.find_element(By.CSS_SELECTOR, opsnzzpwdfield)
elempwd.clear()
elempwd.send_keys(opsnzzpwd)
elempwd.send_keys(Keys.RETURN)

# Switch to read list and count number of articles
time.sleep(5)
driver.get(opsnzzlistsite)
time.sleep(3)
elemmore = driver.find_element(By.CSS_SELECTOR, opsnzzmorebutton)
today = date.today()
while countartfin != countartnew:
    currentnumberofclicks = 0
    while currentnumberofclicks < opsnumberclicks:
        elemmore.click()
        time.sleep(0.5)
        currentnumberofclicks += 1
    countartold = countartnew
    countartnew = len(driver.find_elements(By.TAG_NAME, opsnzztagname))
    countartfin = countartold

# Write final number into file
if os.path.exists(opsoutputfiletowrite):
    with open(opsoutputfiletowrite, "+a") as myfile:
        addentry_tofile()

else:
    with open(opsoutputfiletowrite, "a") as myfile:
        addheader_tofile()
        addentry_tofile()

# End script
driver.close()
