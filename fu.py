from time import sleep

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common import StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pickle
import random
import os
import os.path
import pyfiglet
import cowsay
import csv
import data
import pathlib
import re
import sys
from colorama import init
from termcolor import colored

#--collect-all pyfiglet
SLEEP_TIME = 2
MAX_UNFOLLOWS_PER_DAY = 5
DAYS_TO_UNFOLLOW = 30

MY_ID = "woollypedals"

IG_URL = "https://www.instagram.com/"
POST = "post"
REEL = "reel"
PROFILE = "profile"

# Files
CSV_FILENAME = "regestum.csv"
IMPOSTED_FOLLOWS_FILENAME = "imposted_follows.txt"
DATA_DIR = "data\\"

# Popups
CSS_COOKIE_POPUP_LOGIN = "button._a9--:nth-child(2)"
CSS_COOKIE_POPUP_NOTIS = CSS_COOKIE_POPUP_LOGIN

# Basic
XPATH_IS_PRIVATE = "//div[contains(text(),'Síguela para ver sus fotos o vídeos.')]"
CSS_NUMBER_FOLLOWERS = "li.xl565be:nth-child(2) > a:nth-child(1) > span:nth-child(1) > span:nth-child(1)"
XPATH_NOT_FOUND = "//span[contains(text(),'Es posible que el enlace que has seguido sea incorrecto o que se haya eliminado la página.')]"

# Like&Next
CSS_LIKE = "._aamw > button:nth-child(1)"
CSS_NEXT = "._aaqg._aaqh > button:nth-child(1)"

# Buttons to open lists
XPATH_BUTTON_LIST_FOLLOWERS = "//*[contains(@href, 'followers')]"
XPATH_BUTTON_LIST_LIKES = "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div[1]/a"

# Scroll lists
XPATH_LIST_FOLLOWERS = "//div[@class='_aano']"
XPATH_LIST_LIKES = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div"
HREF = "//span[@class='_aap6 _aap7 _aap8']"

# Number posts
CSS_NUMBER_POST = "._ac2a > span:nth-child(1)"
XPATH_FIRST_POST = "//div[@class='_aabd _aa8k _aanf']"

# Follow & Unfollow
XPATH_FOLLOW_BUTTON = "//div[contains(text(), 'Seguir')]"
XPATH_UNFOLLOW_BUTTON = "//div[contains(text(), 'Siguiendo')]"
XPATH_UNFOLLOW_REQUEST_BUTTON = "//div[contains(text(), 'Solicitado')]"
XPATH_UNFOLLOW_FINAL = "//button[contains(text(), 'Dejar de seguir')]"
XPATH_UNFOLLOW_FINAL_II = "//span[contains(text(), 'Dejar de seguir')]"


def make_relative_path(file_name):
    file_name_dir = DATA_DIR + file_name
    absolute_path = pathlib.Path(__file__).parent.resolve()
    relative_path = os.path.join(absolute_path, file_name_dir)

    return relative_path


def diff_dates(date_old, date_now):
    # Convert string to date object
    d1 = datetime.strptime(date_old, "%d-%B-%Y")
    d2 = datetime.strptime(date_now, "%d-%B-%Y")

    # Difference between dates in timedelta
    delta = d2 - d1
    print(f' It is been {delta.days} days')

    return delta.days


def little_pause():
    MIN_LITTLE_PAUSE = 20
    MAX_LITTLE_PAUSE = 40
    time = random.randint(MIN_LITTLE_PAUSE, MAX_LITTLE_PAUSE)
    print("\t\t\tTaking a nap of " + str(time) + "s")
    sleep(time)


def medium_pause():
    MIN_MEDIUM_PAUSE = 80
    MAX_MEDIUM_PAUSE = 120
    time = random.randint(MIN_MEDIUM_PAUSE, MAX_MEDIUM_PAUSE)
    print("\t\t\tTaking a nap of " + str(time) + "s")
    sleep(time)


def big_pause(type):

    MIN_BIG_PAUSE_I = 134
    MAX_BIG_PAUSE_I = 402
    MIN_BIG_PAUSE_II = 307
    MAX_BIG_PAUSE_II = 921
    MIN_BIG_PAUSE_III = 577
    MAX_BIG_PAUSE_III = 1731

    if(type=="1"):
        min_big_pause = MIN_BIG_PAUSE_I
        max_big_pause = MAX_BIG_PAUSE_I
    elif(type=="2"):
        min_big_pause = MIN_BIG_PAUSE_II
        max_big_pause = MAX_BIG_PAUSE_II
    else:
        min_big_pause = MIN_BIG_PAUSE_III
        max_big_pause = MAX_BIG_PAUSE_III

    time = random.randint(min_big_pause, max_big_pause)
    print(" Sleeping for " + str(time) + "s")
    sleep(time)


def read_file(file_path):
    lista = []
    with open(file_path, 'r') as f:
        for line in f:
            lista.append(line)
    return lista


def write_file(file_path, data):
    # Saving the updated list into a file
    with open(file_path, 'w') as f:
        for line in data:
            f.write(line)
    print(" The file has been updated")


def go_to(driver, target_id):
    # Go to the desired url
    print("\n Going to url -->  " + target_id)
    sleep(SLEEP_TIME)
    url = IG_URL + target_id
    driver.get(url)


def like(driver) -> bool:
    sleep(SLEEP_TIME)
    try:
        like = driver.find_element(By.CSS_SELECTOR, CSS_LIKE)
    except:
        print("\n\t\t Error finding the like button!")
        print("\t\t Not liked!")
        return False
    else:
        print("\t\tLike")
        like.click()
        return True


def next(driver) -> bool:
    sleep(SLEEP_TIME)
    try:
        next_post = driver.find_element(By.CSS_SELECTOR, CSS_NEXT)
    except:
        print("\n Error finding the next button!")
        print("\n Not next")
        return False
    else:
        next_post.click()
        return True


def is_private(driver) -> bool:
    # Returns True if private
    sleep(SLEEP_TIME + 2)
    try:
        driver.find_element(By.XPATH, XPATH_IS_PRIVATE)
        print(" This is a private account. Sleep tight")
    except:
        print(" Public profile.OK\n")
        return False

    return True


def is_profile(driver) -> bool:
    sleep(SLEEP_TIME)
    is_profile = False
    try:
        driver.find_element(By.XPATH, XPATH_NOT_FOUND)
        print(" Not Found profile")
    except:
        is_profile = True

    return is_profile


def is_to_follow(driver) -> bool:
    sleep(SLEEP_TIME+3)
    is_to_follow = True
    # The profile could've denied our request, so it doesn't appear as Stop following or Requested
    try:
        driver.find_element(By.XPATH, XPATH_FOLLOW_BUTTON)
        print(" There's no need to do anything with this profile")
        try:
            driver.find_element(By.XPATH, XPATH_UNFOLLOW_REQUEST_BUTTON)
            is_to_follow = False
        except:
            print(" ??")
    except:
        is_to_follow = False

    return is_to_follow


def open_first_post(driver):
    print("\t\tOpening first post...")
    sleep(SLEEP_TIME)
    try:
        first_post = driver.find_element(By.XPATH, XPATH_FIRST_POST)
        print("\t\tOkey, okey...First try")
        first_post.click()
    except:
        print("ERROR!")
        return 0


def get_posts_number(driver) -> int:
    sleep(SLEEP_TIME)
    try:
        number_posts = driver.find_element(By.CSS_SELECTOR, CSS_NUMBER_POST)
        numeric_string = re.sub("[^0-9]", "", number_posts.text)
        print("\t\tThere are -->  " + numeric_string + " posts")
    except Exception as e:
        print(e)
        print("\t\tUpss...Not found. We're done here")
        return -1
    else:
        return int(numeric_string)


def get_followers_number(driver) -> int:
    sleep(SLEEP_TIME+2)
    try:
        number_followers = driver.find_element(By.CSS_SELECTOR, CSS_NUMBER_FOLLOWERS)
        print(" We have " + number_followers.text + " followers")
    except:
        print(" The hell. When getting followers")
        return -1
    else:
        # This is in order to remove the coma from the text. "Ej: 2,072 to 2072", so the toString doesn't fail
        numeric_string = number_followers.text.replace(",", "")
        return int(numeric_string)


def do_imposted_follow(driver, profile):
    sleep(SLEEP_TIME)
    try:
        impost_follow = driver.find_element(By.XPATH, XPATH_FOLLOW_BUTTON)
        impost_follow.click()

        file_path = make_relative_path(IMPOSTED_FOLLOWS_FILENAME)
        try:
            with open(file_path, "a") as f:
                date = datetime.now()
                formated_date = date.strftime(data.DATE_FORMAT)
                line = profile+","+formated_date
                f.write(line+"\n")
        except:
            print("\n Error when dealing with the file " + file_path)
    except:
        print("\t\tError when doing the imposted follow!")
    else:
        print("\n\t\tLet's follow this unbelievable human being")


def unfollow(driver) -> bool:
    # Check if the unfollow-counter limit has been surpassed
    file_path_regestum = make_relative_path(CSV_FILENAME)
    first_line_regestum = read_first_line_csv(file_path_regestum)
    if (int(first_line_regestum.unfollows) >= MAX_UNFOLLOWS_PER_DAY):
        print(" We've reached the limit per unfollows today")
        return False

    # Read follow date from file
    file_path = make_relative_path(IMPOSTED_FOLLOWS_FILENAME)
    with open(file_path) as f:
        line = f.readline()
    line = line.strip()

    fields = line.split(",")
    profile = fields[0]
    follow_date = fields[1]

    # Current date
    date = datetime.now()
    now_date = date.strftime("%d-%B-%Y")

    # Get difference between dates
    diff = diff_dates(follow_date, now_date)

    go_to(driver, profile)
    is_found = is_profile(driver)

    # The profile could've denied our request, so it doesn't appear as Stop following or Requested
    is_to_be_followed = is_to_follow(driver)

    is_unfollow = False
    # If the follow was 3 months ago or older, do unfollow to the profile
    if(diff>DAYS_TO_UNFOLLOW):

        # If the profile does already exist, and we are following it or have been requested
        if is_found  and not is_to_be_followed:
            try: # Followed profile
                sleep(SLEEP_TIME)
                unfollow = driver.find_element(By.XPATH, XPATH_UNFOLLOW_BUTTON)
            except: # Follow request
                print(" It is an HYPER unbelievable request")
                sleep(SLEEP_TIME)
                unfollow = driver.find_element(By.XPATH, XPATH_UNFOLLOW_REQUEST_BUTTON)

            unfollow.click()

            # Yes I'm sure I do want to unfollow, do click. The hell...
            sleep(SLEEP_TIME)
            try:
                final_unfollow = driver.find_element(By.XPATH, XPATH_UNFOLLOW_FINAL)
            except:
                final_unfollow = driver.find_element(By.XPATH, XPATH_UNFOLLOW_FINAL_II)
                print(" Version II")
            final_unfollow.click()
            is_unfollow = True
            print(" Unfollowed")

        # Read all lines from file
        with open(file_path) as f:
            lines = f.readlines()
        # Remove first one
        lines.pop(0)
        # Write all the lines but the first one
        with open(file_path, "w") as f:
            f.writelines(lines)
        print(" We've pretty gratefully removed "+profile+ " from our following list")

    return is_unfollow


def get_profiles(driver, target, target_type):

    selector_scroll = ""
    if target_type == PROFILE:
        selector_scroll = XPATH_LIST_FOLLOWERS
    elif target_type == POST or target_type == REEL:
        selector_scroll = XPATH_LIST_LIKES

    # Scroll down the followers list
    print(" Scrolling down the list window...")
    sleep(SLEEP_TIME)
    scroll_box = driver.find_element(By.XPATH, selector_scroll)
    print(" This might take a while")
    sleep(SLEEP_TIME)

    names = []
    # Scroll down and save profiles
    last_ht, ht, i = 0, 1, 0
    while last_ht != ht:

        # Scroll down & Sleep
        print(i)
        i = i + 1
        last_ht = ht
        ht = driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);return arguments[0].scrollHeight;", scroll_box)
        sleep(random.uniform(2.2, 3.4))

        # Gather profiles in view
        if (i % 40 == 0):
            gather_names_in_view(scroll_box, names)

    print(" Scroll done :) "+str(i)+" iterations.\n Gathering all profiles")
    names = gather_names_in_view(scroll_box, names) # Get last elements

    # Remove duplicates
    names = list(dict.fromkeys(names))

    # Write a file with all the profiles
    if names:
        file_name = target.replace("/", "&")
        file_path = make_relative_path(file_name)
        print(" Saving " + str(len(names)) + " profiles in the file: " + file_name + ".txt")
        with open(file_path + ".txt", "w") as f:
            f.write("\n".join(names)+"\n")
    else:
        print(" No profiles gathered... :(")

    return names


def gather_names_in_view(scroll_box, _names):
    links = scroll_box.find_elements(By.XPATH, HREF)
    aux = [name.text for name in links if name.text != ''] # Need to filter empty string so we used name.text instead of name
    _names.extend(aux)
    extended_list = list(dict.fromkeys(_names))
    print(str(len(extended_list)))
    return extended_list


def bait_with_likes(driver, profile, chapa):
    ascii_banner = pyfiglet.figlet_format(profile)
    print(colored(ascii_banner, 'cyan', attrs=["bold"]))

    go_to(driver, profile)
    private = is_private(driver)
    likes = 0

    if not private:

        number_posts = get_posts_number(driver)
        if number_posts <= 0:
            print("\t\tIt's a trap...")
            return 0

        # Look for first post and open it
        open_first_post(driver)

        if (number_posts > 15):
            print("\t\tLet's start the charade:\n")
            likes += charade(driver, likes, chapa)

        elif (number_posts > 3):
            print("\t\tLet's start the mini charade\n")
            likes+= mini_charade(driver, likes)

        else:
            print("\t\tThe profile is ridiculous. We're out")

    else:
        #do_imposted_follow(driver, profile)
        pass

    print(colored("\t\t+-+-+-+-+-+-+-+-+-+-+-+-+-+", 'cyan'))

    return likes


def attack(driver, target_id, target_type):
    start_time = datetime.now().replace(microsecond=0)
    print("\n\n Starting at: " + start_time.strftime("%H:%M:%S"))

    selector = ""
    if target_type == PROFILE:
        selector = XPATH_BUTTON_LIST_FOLLOWERS
    elif target_type == POST or target_type == REEL:
        selector = XPATH_BUTTON_LIST_LIKES
    else:
        print("WTF???")

    type_attack = attack_menu()
    if type_attack == '0':
        return 0

    # Check if target has been attacked before
    file_name_target = target_id.replace("/", "&") + ".txt"
    file_path_target = make_relative_path(file_name_target)
    file_exists = os.path.exists(file_path_target)

    # If the list is saved in disk, we read from it. Otherwise, we go to scrap
    if not file_exists:
        go_to(driver, target_id)
        # Open list
        print(" Opening followers/likers list window")
        sleep(SLEEP_TIME+4)
        target_button = driver.find_element(By.XPATH, selector)
        target_button.click()
        profiles_list = get_profiles(driver, target_id, target_type)
    else:
        print(" This target has been scrapped before, reading from disk...\n")
        profiles_list = read_file(file_path_target)

    # We bait every profile, each apiece
    likes_count = 0
    for profile in profiles_list:

        aux_time = datetime.now().replace(microsecond=0)
        likes_profile = bait_with_likes(driver, profile.strip(), type_attack.strip())
        print("\n BAITED. We're done with " + profile.strip() + " with " + str(likes_profile) + " likes")
        likes_count = likes_count + likes_profile
        print(" We've hit " + str(likes_count) + " likes so far in this round")

        # Remove the already baited profile from the profile list
        print(" Deleting " + profile.strip() + " from list")
        aux_list = read_file(file_path_target)
        aux_list.pop(0)
        write_file(file_path_target, aux_list)

        # Delete the file when empty
        if not aux_list:
            print(" Deleting file " + file_path_target)
            os.remove(file_path_target)

        # Unfollow
        unfollowed = unfollow(driver)
        if unfollowed:
            unfollowed = 1
        else: unfollowed = 0

        # Update de Regestum
        go_to(driver, MY_ID)
        regestum_stuff(driver, likes_profile, likes_count, unfollowed)

        # Long pause
        if likes_profile:
            big_pause(type_attack)

        # Times
        last_time = datetime.now().replace(microsecond=0)
        global_time = last_time - start_time
        partial_time = last_time - aux_time

        print("\n Time spent with that profile: " + str(partial_time))
        print(" We've been running for a long time: " + str(global_time))
        print(colored("*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*\n\n", 'cyan'))


def regestum_stuff(driver, likes_profile, likes_count, unfollowed):

    my_data = data.Data(likes_profile, 0, unfollowed)

    file_path_csv = make_relative_path(CSV_FILENAME)
    csv_exists = os.path.exists(file_path_csv)
    if not csv_exists:  # Creating the file
        with open(file_path_csv, "w"):
            print(" Creating regestum.csv file")
        my_data.followers = get_followers_number(driver)
        write_line_csv(file_path_csv, my_data, False)
        print(" Writing first line ever")

    else:  # Writing first line ever (when file exists, but it's empty)
        first_line = read_first_line_csv(file_path_csv)

        if not first_line:
            print(" Writing first line ever in the rare empty file...")
            my_data.followers = get_followers_number(driver)
            write_line_csv(file_path_csv, my_data, False)

        else:
            if first_line.date == my_data.date:  # Updating current line
                print(" Updating today's line")
                my_data.date = first_line.date
                my_data.followers = first_line.followers
                aux_string = first_line.likes.replace(",", "")
                sum_likes = likes_profile + int(aux_string)
                my_data.likes = sum_likes
                aux_string_II = first_line.unfollows.replace(",", "")
                my_data.unfollows = unfollowed + int(aux_string_II)
                write_line_csv(file_path_csv, my_data, True)

            else:  # Adding a new line
                print(" Adding today's line")
                my_data.followers = get_followers_number(driver)
                write_line_csv(file_path_csv, my_data, False)


def read_first_line_csv(file_path):
    first_line = None
    with open(file_path) as file:
        csv_reader = csv.reader(file,delimiter=',')
        for row in csv_reader:
            cols = row[0].split(',')
            date = cols[0]
            likes = cols[1]
            followers = cols[2]
            unfollows = cols[3]
            first_line = data.Data(likes, followers, unfollows)
            first_line.set_date(date)
            break

    return first_line


def write_line_csv(file_path, data, update):
    row = data.get_csv()
    print(colored(" " +row, 'grey', "on_white"))

    # We read the file as a list & insert the new row in first place
    with open(file_path, 'r') as readFile:
        csv_reader = csv.reader(readFile,delimiter=',')
        lines = list(csv_reader)
        if update:
            lines.pop(0)
        lines.insert(0, [row])

    # We write the list as a file, overwritten the last version
    with open(file_path, 'w', newline='') as writeFile:
        csv_writer = csv.writer(writeFile)
        csv_writer.writerows(lines)


def attack_menu():

    option = '0'
    flag = True
    while flag:

        print("\n How mucha do you want to spam\n")
        print("\t\t 1) I just wanted to say hello")
        print("\t\t 2) Medium")
        print("\t\t 3) Hard")
        print("\t\t f) Go back!")

        option = input("\n\t Tell me: ").strip().lower()
        print("")

        if option.isalnum():

            if option == 'f':
                option = '0'
                flag = False

            elif option == '1' or option == '2' or option == '3' or option == 'f':
                flag = False

    return option


def attack_profile(driver):
    flag = False
    while not flag:
        profile = input("\n\n What profile you wanna scrap? ")
        profile = profile.strip()

        if len(profile) > 3:
            flag = True

    target_type = PROFILE
    attack(driver, profile, target_type)


def attack_post(driver):
    url = ""
    flag = False
    while not flag:
        url = input("\n\n Introduce the link to publication to be attacked: ")

        if url == "":
            print("\n Empty url...Really?")

        elif IG_URL in url:
            flag = True
        else:
            print("\n Invalid url. Try again")

    url = url.strip()
    target_id = url.replace(IG_URL, "")

    if "/p" in url:
        target_type = POST
    elif "/reel/" in url:
        target_type = REEL
    else:
        print("WTSF!!!")

    attack(driver, target_id, target_type)


def set_up(headless):
    headOption = webdriver.FirefoxOptions()
    headOption.headless = headless
    print("\n")
    if(headless):
        print(" Running headless")

    # Go to instagram.com
    print(" Loading browser...")
    headOption.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    driver = webdriver.Firefox(options=headOption)
    driver.get(IG_URL)

    # Close first & unavoidable popup
    print(" Closing cookie popup window")
    sleep(SLEEP_TIME / 2)
    for i in range(5):
        try:
            cookie_popup = driver.find_element(By.CSS_SELECTOR, CSS_COOKIE_POPUP_LOGIN)
            cookie_popup.click()
            break
        except:
            print(" Sleep & Try")
            sleep(SLEEP_TIME)

    # Delete all old cookie stuff and load the ig cookies saved previously
    print(" Loading cookies from file")
    sleep(SLEEP_TIME / 2)
    driver.delete_all_cookies()
    cookies = pickle.load(open("igcookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    # Go to instagram.com again. N E E D E D
    print(" Reloading page...")
    driver.get(IG_URL)

    # Deny notifications cookie popup
    print(" Closing cookie popup window for notifications")
    sleep(SLEEP_TIME / 2)
    for i in range(5):
        try:
            cookie_popup_notifications = driver.find_element(By.CSS_SELECTOR, CSS_COOKIE_POPUP_NOTIS)
            cookie_popup_notifications.click()
            print(" We're I N\n\n")
            break
        except:
            print(" Sleep & Try")
            sleep(SLEEP_TIME)

    # We create de "/data" directory if it does not exist
    isExist = os.path.exists("data")
    if not isExist:
        os.makedirs("data")
        print(" The data directory has been made")

    return driver


def main():
    init()

    # Console arguments
    headless = False
    n = len(sys.argv)
    if(n==2):
        arg = sys.argv[1].strip()
        if arg == "1":
            headless = True

    # Big greeting banner
    ascii_banner = pyfiglet.figlet_format("\n\tHello   old   sport!!")
    print(colored(ascii_banner, 'cyan', attrs=["bold"]))

    driver = set_up(headless)
    while True:

        menu = "\n\t What do you want to do?\n" + "-\n" + "\t 1) Attack profile\n" + "\t 2) Attack publication\n" + "\t q) Exit\n"
        cowsay.fox(menu)

        option = input("\n Introduce an option: ").lower().strip()

        if option == '1':
            attack_profile(driver)

        elif option == '2':
            attack_post(driver)

        elif option == 'q':
            print("\n Salimoh")
            os.system("CLS")
            break

        #os.system("CLS")

    if driver:
        driver.quit()

    return 69


def charade(driver, likes, length):
    # O N E   LIKE
    if length == "1":

        # 1
        next(driver)
        if like(driver):
            likes += 1
            sleep(SLEEP_TIME)

    # T H R E E   LIKES
    elif length == "2":

        # 1
        next(driver)
        if like(driver):
            likes += 1
        medium_pause()

        for x in range(5):
            next(driver)

        # 2
        if like(driver):
            likes += 1
        medium_pause()

        for x in range(8):
            next(driver)

        # 3
        if like(driver):
            likes += 1
            sleep(SLEEP_TIME)

    # F I V E   LIKES
    elif length == "3":

        # 1
        next(driver)
        if like(driver):
            likes += 1
        little_pause()

        for x in range(3):
            next(driver)

        # 2
        if like(driver):
            likes += 1
        medium_pause()

        for x in range(2):
            next(driver)

        # 3
        if like(driver):
            likes += 1
        medium_pause()

        for x in range(6):
            next(driver)

        # 4
        if like(driver):
            likes += 1
        print("\t\t\tTaking a nap of 15s")
        sleep(15)

        # 5
        next(driver)
        if like(driver):
            likes += 1
            sleep(SLEEP_TIME)

    else:
        print("WTF???")

    return likes


def mini_charade(driver, likes):

    if like(driver):
        likes += 1
    next(driver)
    medium_pause()

    if like(driver):
        likes += 1
    sleep(SLEEP_TIME)

    return likes


if __name__ == "__main__" :
    main()


