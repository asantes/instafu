import csv
import datetime

DATE_FORMAT = "%d-%B-%Y" #24-Agosto-2022

class Data:

	def __init__(self, likes, followers, unfollows):
		self.date = self.init_date()
		self.likes = likes
		self.followers = followers
		self.unfollows = unfollows
		
	def init_date(self):
		date = datetime.datetime.now()
		formated_date = date.strftime(DATE_FORMAT)
		return formated_date

	def set_date(self, date):
		self.date = date

	def get_csv(self):
		line = self.date+","+str(self.likes)+","+str(self.followers)+","+str(self.unfollows)
		return line
		
