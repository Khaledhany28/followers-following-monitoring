from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Instagram:
    def __init__(self):

        browserDetailsfile = open("Browser Details.txt", 'r')
        browserDetails = browserDetailsfile.readlines()

        browserName = browserDetails[0][15:].strip().rstrip('\n')  # it will start from the character 15 which is the start of the real value, and will remove the white spaces and the \n
        browserPathAndProfile = browserDetails[1][15:].strip().rstrip('\n')

        # Slicing the string of the profile path to a profile name and a browser path
        browserProfile = browserPathAndProfile[browserPathAndProfile.index("User Data\\") + 10:]
        browserPath = browserPathAndProfile[:browserPathAndProfile.index("User Data\\") + 9]

        if browserName.lower() == 'chrome':  # if the browser is Chrome initialize driver with the path to the chrome directory
            options = webdriver.ChromeOptions()
            options.add_argument(f"--user-data-dir={browserPath}")  # e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
            options.add_argument(fr'--profile-directory={browserProfile}')  # Profile
            options.add_argument('--headless')
            self.driver = webdriver.Chrome(options=options)
        elif browserName.lower() == 'edge':  # if the browser is Edge initialize driver with the path to the edge directory
            options = webdriver.EdgeOptions()
            options.add_argument( f"--user-data-dir={browserPath}")  # e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
            options.add_argument(fr'--profile-directory={browserProfile}')  # Profile
            options.add_argument('--headless')
            self.driver = webdriver.Edge(options=options)
        else:
            raise ValueError("Unknown browser")
        

        self.driver.get("https://instagram.com")
        self.driver.implicitly_wait(5)
        
        # get the username of the logged in profile
        try:
            # Opens the profile of the user
            self.driver.find_element(By.XPATH, '//span [ contains( text(), "Profile" ) ]').click()
        except:
            #Opens the profile of the user but using the pfp insted on the text "profile", if the screen is small the text will not be there
            self.driver.find_element(By.XPATH, '//div [@class="x1n2onr6"]').click()

        user = self.driver.find_element(By.XPATH, '//h2 /span') # your username is the only thing with h2 tag in the page

        self.username = user.get_attribute("innerHTML")

        # get the number of followers
        try:
            numOfFollowers = self.driver.find_element(By.XPATH, "//button[contains(text(), ' followers')] /span /span")
        except:  # FOR SOME REASON instagram did change the class names in some browsers and others not IDK WHY
            numOfFollowers = self.driver.find_element(By.XPATH,  f"//a [@href = '/{self.username}/followers/'] /span /span")

        self.numOfFollowers = int(numOfFollowers.get_attribute("innerHTML"))

        # get the number of following
        try:
            numOfFollowing = self.driver.find_element(By.XPATH, "//button[contains(text(), ' following')] /span /span")
        except:  # FOR SOME REASON instagram did change the class names in some browsers and others not IDK WHY
            numOfFollowing = self.driver.find_element(By.XPATH, f"//a [@href = '/{self.username}/following/'] /span /span")

        self.numOfFollowing = int(numOfFollowing.get_attribute("innerHTML"))

    def initUsername(self, username: str):
        self.username = username

    def login(self, accUsername: str, accPassword: str):
        self.driver.get("https://www.instagram.com")  # open the login page

        usernameBox = self.driver.find_element(By.XPATH, '//input [@aria-label="Phone number, username, or email"]')
        passwordBox = self.driver.find_element(By.XPATH, '//input [@aria-label="Password"]')

        usernameBox.send_keys(accUsername)
        passwordBox.send_keys(accPassword)
        loginButton = self.driver.find_element(By.XPATH, '//button /div')
        loginButton.click()

    def getFollowers(self) -> list:
        # open the profile
        self.driver.get(f"https://www.instagram.com/{self.username}/")

        # click on the followers list to pop up
        try:
            followers = self.driver.find_element(By.XPATH, "//button[contains(text(),' followers')]")
        except:  # FOR SOME REASON instagram did change the class names in some browsers and others not IDK WHY
            followers = self.driver.find_element(By.XPATH, f"//a [@href = '/{self.username}/followers/']")

        followers.click()

        followersList = []

        # popUpWindowPath = '//div[@style="height: auto; overflow: hidden auto;"] /div [@style="display: flex; flex-direction: column; padding-bottom: 0px; padding-top: 0px; position: relative;"]'
        popUpWindowPath = '//div [@class="xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6"]'
        popUpWindow = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, popUpWindowPath)))  # the XPATH of the pop-up window that contain the list

        while len(followersList) < self.numOfFollowers:  # loop until we find all the followers

            # scroll down to load more
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight;', popUpWindow)

            followersList = self.driver.find_elements(By.XPATH, "//div [@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 x1iyjqo2 xs83m0k xeuugli x1qughib x6s0dn4 x1a02dak x1q0g3np xdl72j9'] /div /div /div/div/div /a /div /div/span")

        for i in range(len(followersList)):
            followersList[i] = followersList[i].get_attribute("innerHTML")

        return followersList

    def getFollowing(self) -> list:
        # open the profile
        self.driver.get(f"https://www.instagram.com/{self.username}/")

        # click on the followers list to pop up
        try:
            following = self.driver.find_element(By.XPATH, "//button[contains(text(),' following')]")
        except:  # FOR SOME REASON instagram did change the class names in some browsers and others not IDK WHY
            following = self.driver.find_element(By.XPATH, f"//a [@href = '/{self.username}/following/']")

        following.click()

        followingList = []

        popUpWindowPath = '//div [@class="xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6"]'
        popUpWindow = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, popUpWindowPath)))  # the XPATH of the pop-up window that contain the list

        while len(followingList) < self.numOfFollowing:  # loop until we find all the followers

            # scroll down to load more
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight;', popUpWindow)

            followingList = self.driver.find_elements(By.XPATH,  "//div [@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 x1iyjqo2 xs83m0k xeuugli x1qughib x6s0dn4 x1a02dak x1q0g3np xdl72j9'] /div /div /div/div/div /a /div /div/span")

        for i in range(len(followingList)):
            followingList[i] = followingList[i].get_attribute("innerHTML")

        return followingList
