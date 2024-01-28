from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
import sys

SLEEP_TIME = 4
USERPASS_FILENAME = "userpassword.txt"

CSS_FIRST_POPUP = "button._a9--:nth-child(2)"
CSS_SECOND_POPUP = "button._acan:nth-child(4)"
CSS_LAST_POPUP = "button._a9--:nth-child(1)"


def read_userpass():
	try:
		with open(USERPASS_FILENAME) as f:
			userpass = f.readline()
	except FileNotFoundError:
		print(f"File {USERPASS_FILENAME} not found!", file=sys.stderr)
		print(" File "+USERPASS_FILENAME+ "not found. Do the following:\n")
		print("\t I) Make a file with the name "+USERPASS_FILENAME)
		print("\t II) Write your username & password in the first line")
		print("\tIII) Splite your username & password with a comma like this:")
		print("\n\t\t username,password")
		return

	if userpass:
		aux = userpass.strip()
		return aux.split(",")
	else:
		print(" You are an idiot")
		return


#Read username & password from file
userpass = read_userpass()
username = userpass[0]
password = userpass[1]

headOption = webdriver.FirefoxOptions()
headOption.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"

#Go to instagram.com
driver = webdriver.Firefox(options=headOption)
driver.get("https://www.instagram.com")
sleep(SLEEP_TIME)

#Close first & unavoidable popup 
cookie_popup = driver.find_element(By.CSS_SELECTOR, CSS_FIRST_POPUP)
cookie_popup.click()
sleep(SLEEP_TIME)

#Find text inputs and fill them with username & password
username_input = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
username_input.send_keys(username)
password_input.send_keys(password)

#Click on submit
login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
login_button.click()

#Accept auto login cookie popup
sleep(SLEEP_TIME)
for i in range(5):
	try:
		cookie_popup_autologin = driver.find_element(By.CSS_SELECTOR, CSS_SECOND_POPUP)
		cookie_popup_autologin.click()
		break
	except:
		print(" Error when looking for the auto login popup. Attempt number "+str(i))
		sleep(SLEEP_TIME)

#Deny notifications cookie popup
sleep(SLEEP_TIME)
for i in range (5):
	try:
		cookie_popup_notifications = driver.find_element(By.CSS_SELECTOR, CSS_LAST_POPUP)
		cookie_popup_notifications.click()
		break
	except:
		print(" Error when looking for the last popup...Attempt number "+str(i))
		sleep(SLEEP_TIME)

#Save cookies & exit
pickle.dump(driver.get_cookies() , open("igcookies.pkl","wb"))
driver.quit()




