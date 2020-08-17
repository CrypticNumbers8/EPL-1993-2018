import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#read csv file
epl_csv = pd.read_csv("C:/Users/arvin/OneDrive/Desktop/Sublime/EPL_Set.csv")

all_teams = epl_csv['HomeTeam'].unique().tolist()
print(all_teams)
lent = len(all_teams)
print(f"Choose your club from the above List of {lent} clubs:")

club = input("Your Club Name?")
print("Your chosen Club is: " + club)


def team_played_or_not(club,season):
	Team_Home1 = epl_csv[epl_csv['HomeTeam'] == club]
	all_seasons = list(Team_Home1['Season'].unique())
	if season not in all_seasons:
		print("SORRY! This team didnt play in the Premier league on the given season ,TRY AGAIN!!")
		return 0
	else:
		print("Your Team Played in the Prem! Below are the Plots:")
		return 1


def team_and_season(club, season, homeplot = 0, awayplot = 0, pointplot = 1):

	#if (club didn't play that season):
		#print('%s did not play in the season %s', club, season)

		flag = team_played_or_not(club,season)

		if flag == 0:
			return 0

	#else:

		Team_home = epl_csv[epl_csv['HomeTeam'] == club] #HomeGame DATAFRAME
		#print(Team_home.info())
		Team_away = epl_csv[epl_csv['AwayTeam'] == club] #AwayGame DATAFRAME


		seasons = list(Team_home['Season'].unique())
		#print(seasons)

		no_of_home_wins = [] #list of no of home wins each season
		no_of_away_wins = [] #list of no of away wins each season

		for i in seasons:
			x = Team_home[Team_home['Season'] == i]
			count_home = 0
			for j in x['FTR']:
				if j == 'H':
					count_home += 1

			no_of_home_wins.append(count_home)

		for j in seasons:
			y = Team_away[Team_away['Season'] == j]
			count_away = 0
			for i in y['FTR']:
				if i == 'A':
					count_away += 1

			no_of_away_wins.append(count_away)


		#print(no_of_home_wins)
		#print(no_of_away_wins)

		#data frame containing home and away win records
		data_home_away = pd.DataFrame({'Seasons':seasons, 'Victory at home': no_of_home_wins, 'Victory at away':no_of_away_wins}) 
		#print(data_home_away)

		if homeplot == 1:
			plt.figure(figsize =  (16,9))

			sns.barplot(x = data_home_away['Seasons'], y = data_home_away['Victory at home'])
			plt.xticks(rotation = 45)
			plt.xlabel('Seasons')
			plt.ylabel('# of wins at home')
			plt.title('HOME WINS') # no of home wins vs season

			plt.grid()
			plt.show()

		if awayplot  == 1:
			plt.figure(figsize =  (16,9))

			sns.barplot(x = data_home_away['Seasons'], y = data_home_away['Victory at away'])
			plt.xticks(rotation = 45)
			plt.xlabel('Seasons')
			plt.ylabel('# of wins at away grounds')
			plt.title('AWAY WINS') #no of away wins vs season
			plt.grid()
			plt.show()

		# 2017-18 season performances

		filter_season = epl_csv['Season'] == season
		filter_Team_home = epl_csv['HomeTeam'] == club
		filter_Team_away=epl_csv['AwayTeam']==club
		Team_whole=epl_csv[filter_Team_home | filter_Team_away] #complete Team DF
		Team_year = Team_whole[filter_season] #2017-18 Team DF
		#print(Team_year)

		points_home = [] #points won in home fixtures
		for i in Team_year[Team_year['HomeTeam'] == club].loc[:,'FTR']:
			if i == 'H':
				points_home.append(3)
			elif i == 'D':
				points_home.append(1)
			else:
				points_home.append(0)

		points_away = [] #points won in away fixtures
		for j in Team_year[Team_year['AwayTeam'] == club].loc[:,'FTR']:
			if j == 'A':
				points_away.append(3)
			elif j == 'D':
				points_away.append(1)
			else:
				points_away.append(0)

		#print(points_home)
		#print(points_away)

		Team_home_year = Team_year[Team_year['HomeTeam'] == club]
		Team_home_year['Point'] = points_home #add new column points

		Team_away_year = Team_year[Team_year['AwayTeam'] == club]
		Team_away_year['Point'] = points_away #add new column points

		#print(Team_home_year)
		#print(Team_away_year)

		datetime = pd.to_datetime(Team_home_year['Date'], errors = 'coerce')
		Team_home_year['date'] = datetime
		Team_home_year= Team_home_year.set_index('date') #add index date
		#print(Team_home_year)

		datetime1 = pd.to_datetime(Team_away_year['Date'], errors = 'coerce')
		Team_away_year['date'] = datetime1
		Team_away_year = Team_away_year.set_index('date') #add index date
		#print(Team_away_year)


		merge = pd.concat([Team_home_year,Team_away_year], axis = 0) #merge home and away DF
		merge.sort_values(by = ['date'], inplace = True, ascending = True)
		#print(merge)

		point = []
		counter = 0
		for k in merge['Point']:
			counter += k
			point.append(counter)

		merge['Cumulative Points'] = point #Total points after that gameweek
		#print(merge)
		merge.drop(columns = ['Point'])
		weeks = [ i for i in range(1,39)]
		merge['Gameweek'] = weeks
		print(merge)


		#pointplot for season performance
		plt.figure(figsize = (24,15))
		sns.pointplot(x = 'Gameweek', y = 'Cumulative Points', data = merge, color = 'Blue', alpha = 0.8)

		plt.grid()
		plt.show()

team_and_season('Chelsea', '2010-11')

'''
club1 = str(input("Select your club:"))
season1 = str(input("Select season"))
homeplot = bool(input("Do you want to see home victories : 0 for NO or 1 for YES"))
awayplot = bool(input("Do you want to see away victories : 0 for NO or 1 for YES"))
ptplot = bool(input('Do you want to see performance of club in the season? 0 for NO or 1 for YES'))


team_and_season(club1, season1,homeplot,awayplot,ptplot)
'''