"""
	Insta bot for hypothetical follow automation to grow followers/ig presence

"""
from selenium import webdriver
import time
import random
from selenium.webdriver.common.keys import Keys


# ---------- EDIT BELOW ------------

UNAME = ''
PASS = ''
# list of accounts whose followers we want to follow
ACCOUNTS = {'LOEWE', 'Dior', 'ullajohnson', 'moncler'}

# ----------------------------------



class InstaBot:
	def __init__(self, username=UNAME, password=PASS, accounts=ACCOUNTS, following=set()):
		# create new dictionary object to remember people we've followed
		self.username = username
		self.password = password
		self.accounts = accounts
		self.following = following
		self.followed = set()

		# navigate to insta
		self.driver = webdriver.Chrome('./chromedriver')
		self.driver.get('https://www.instagram.com/')
		time.sleep(1)

		#immediately log in to home page
		self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(username)
		self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(password)
		self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
		time.sleep(7)

	def follow(self):
		# pick a random account from accounts set and search for it
		random_account = random.choice(tuple(ACCOUNTS))
		print('searching for', random_account)
		account_search = self.driver.find_element_by_xpath("//input[contains(@placeholder, 'Search')]")
		account_search.send_keys(random_account)
		time.sleep(6)
		# hit enter twice to search
		account_search.send_keys(Keys.RETURN)
		account_search.send_keys(Keys.RETURN)
		time.sleep(4)
		print('on ' + random_account + ' page... commencing follow operation ;)')
		# navigate to followers popup
		self.driver.find_element_by_xpath("//a[contains(@href, '/followers/')]").click()
		time.sleep(5)
		# scroll to bottom to activate all follow buttons in html
		popup_element = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
		time.sleep(10)
		#self.scroller(popup_element)
		for scroll in range(random.randint(1, 3)):
			# scroll down a few times
			self.scroller(popup_element)
			self.followUsers(self.following)
		self.driver.close()
		self.driver.quit()

	def scroller(self, popup_element):
		"""
			scrolls down a page - not to the very bottom
		"""
		for _ in range(1):
			print('SCROLL')
			self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeselfht;', popup_element)
			time.sleep(2)
		time.sleep(10)
		print('done SCROLLING')
		return

	def pressButtons(self, button_text):
		"""
			presses follow or unfollow buttons
		"""
		buttons = "//button[text()='{}']".format(button_text)
		follow_buttons = self.driver.find_elements_by_xpath(buttons)
		time.sleep(10)
		for butt in follow_buttons[len(follow_buttons) - 14:]:
			coin = random.randint(0, 2)
			if coin != 0:
				butt.click()
				print('followed')
				time.sleep(random.randint(1, 2))
		time.sleep(random.randint(1, 4))
		print('done pressing buttons')
		return

	def followUsers(self, following):
		"""
			checks if we've followed a user before
		"""
		print('getting names')
		users_list = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]').find_elements_by_css_selector('li')
		# print('size of users list: ', len(users_list))
		for user in users_list[-7:]:
			name = user.find_element_by_css_selector('a').get_attribute('href')
			print('USERNAME: ', name)
			follow_button = user.find_element_by_css_selector('button')
			if follow_button.text == 'Follow':
				# check if we've followed before
				if name not in following:
					# follow
					follow_button.click()
					# add name to followed
					self.followed.add(name)
			time.sleep(2)
		return


	def getNumFollowers(self):
		# retreive number of followers
		num = '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span'
		num_followers = int(self.driver.find_element_by_xpath(num).get_attribute('title').replace(',', ''))
		return num_followers

	def getNumFollowing(self):
		# retreive number of followers
		num = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'
		num_following = int(self.driver.find_element_by_xpath(num).get_attribute('title').replace(',', ''))
		return num_following

	def findSimilarAccounts(self):
		# searches with hashtags to find similar accounts and add them to our accounts set
		# print(' ')
		pass

	def massUnfollow(self):
		# go to my account page
		self.driver.get('https://www.instagram.com/' + self.username + '/')
		time.sleep(2)
		#num_scrolls = self.getNumFollowing() / 7 + 25
		num_scrolls = 1041 / 7 + 25
		time.sleep(7)
		# navigates to my following list
		self.driver.find_element_by_xpath("//a[contains(@href, '/following/')]").click()
		time.sleep(7)
		f = open('dont_unfollow_2.txt', 'r+')
		dont_unfollow = set(line.rstrip('\n') for line in f)
		# iterate through all accounts, unfollow
		popup_element = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
		# scroll and unfollow incrementally
		for _ in range(int(num_scrolls)):
			print('SCROLL')
			self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeselfht;', popup_element)
			time.sleep(1)
			# get list of elements, unfollow
			users_list = popup_element.find_elements_by_css_selector('li')
			for user in users_list:
				name = user.find_element_by_css_selector('a').get_attribute('href')
				unfollow_button = user.find_element_by_css_selector('button')
				time.sleep(2)
				if unfollow_button.text == 'Following':
					# check if we've followed before
					if name not in dont_unfollow:
						# unfollow
						unfollow_button.click()
						time.sleep(1)
						# confirm unfollow
						unfollow_popup = self.driver.find_element_by_xpath("//div[contains(@role, 'dialog')]")
						confirm_unfollow_button = unfollow_popup.find_element_by_xpath("//button[contains(text(), 'Unfollow')]")
						confirm_unfollow_button.click()

		f.close()



	def generateNewPost(self):
		print(' ')



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ ACTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_your_followers():
	self = InstaBot()
	f = open('dont_unfollow_2.txt', 'w')
	self.driver.get(UNAME)
	time.sleep(4)
	self.driver.find_element_by_xpath("//a[contains(@href, '/followers/')]").click()
	time.sleep(6)
	# scroll to bottom
	num_scrolls = self.getNumFollowers() / 7 + 25
	popup_element = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]')
	for _ in range(int(num_scrolls)):
		self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeselfht;', popup_element)
		time.sleep(1)
	time.sleep(5)
	# # # # # #
	users_list = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]').find_elements_by_css_selector('li')
	users_ = []
	for user in users_list:
		name = user.find_element_by_css_selector('a').get_attribute('href')
		users_.append(name)

	time.sleep(30)
	f.write('\n'.join(str(usr) for usr in users_))
	f.close()


def go_follow():
	f = open('following.txt', 'r+')
	following = set(line.rstrip('\n') for line in f)
	self = InstaBot(UNAME, PASS, ACCOUNTS, following)
	self.follow()
	f.close()
	f2 = open('following.txt', 'a+')
	f2.write('\n'.join(str(usr) for usr in self.followed))
	f2.write('\n')
	f2.close()

def go_unfollow():
	self = InstaBot()
	time.sleep(10)
	self.massUnfollow()

if __name__ == '__main__':
	go_follow()  # TODO: change specs on follow function
	#get_your_followers()
	#go_unfollow()
