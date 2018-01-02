#Search week by week for each season and collect wins/losses/ties
#OT games count as a tie
#Add Ws,Ls,Ts at the end

import bs4 as bs
import urllib.request
import json
import pandas as pd

def getTeamName(tr):
    #There's only one <a> tag in each table and this is only called from tables
    return tr.find('a').text.split()[-1]

def adToRecords(tr,recordTracker):
    #Adds 1 to the W/L/T for the team, defaults to 0 (then adds 1) if team is not in dictionary already
    recordTracker[getTeamName(tr)] = recordTracker.get(getTeamName(tr),0) + 1

for year in range(1974,2018): #OT was added in 1974.
    winners, losers, ties = {},{},{}
    teamNames =  {}
    #The NFL had different numbers of weeks in each season over time
    #The week number is needed to access each url
    if year <= 1977:
        weekCount = [i for i in range(1,15)] #there were 14 weeks until 1978
    elif year == 1982:
        weekCount = [1,2,11,12,13,14,15,16,17] #players strike led to a reduced season
    elif year == 1987:
        weekCount = [1,2,4,5,6,7,8,9,10,11,12,13,14,15,16] #players strike led to a reduced season
    elif year <= 1989:
        weekCount = [i for i in range(1,17)] #there were 16 weeks until 1989
    else:
        weekCount = [i for i in range(1,18)] #regular 17 week schedule as is used currently
    for week in weekCount:
        sauce = urllib.request.urlopen('https://www.pro-football-reference.com/years/' + str(year) + '/week_' + str(week) + '.htm').read()
        soup = bs.BeautifulSoup(sauce,'lxml')

        print(year,week) #Print the weeks so progress can be visualized while running

        for eachGame in soup.find_all('table', class_='teams'):
            #I check for OT first because of the way the website stores information in the tables
            OTgame = False
            for td in eachGame.find_all('td', class_='right'):
                if td.string != None: #if the game doesn't go to OT, it is reported as "none" and causes .strip() to fail
                    if td.string.strip() == 'OT':
                        OTgame = True
                        
            if week == 1:
                #Builds a dictionary of all team names. Rebuilt every loop because teams are added and removed every few years.
                for tr in eachGame.find_all('tr',['winner','loser','draw']):
                    if getTeamName(tr) not in teamNames:
                        teamNames[getTeamName(tr)] = True
            if OTgame:
                #If the game went to overtime, no need to determine actual outcome
                for tr in eachGame.find_all('tr',['winner','loser','draw']):
                    adToRecords(tr,ties)
            else:
                for tr in eachGame.find_all('tr', class_='winner'):
                    adToRecords(tr,winners)
                for tr in eachGame.find_all('tr', class_='loser'):
                    adToRecords(tr,losers)
                    
    #combine to one dictionary
    seasonRecord = dict((k,[winners.get(k,0)] + [losers.get(k,0)] + [ties.get(k,0)]) for k in teamNames.keys())
    
##    #export to csv files ##############(not in use)
##    fileName = str(year)+'.csv'
##    with open(fileName,'w') as f:
##        writer = csv.writer(f)
##        for key,value in seasonRecord.items():
##            writer.writerow([key,value])
    
    #export to json files
    fileName = 'C:\\Users\\Raphi\\Documents\\NFL-Overtime\\json files\\' + str(year) + '.json'
    df = pd.DataFrame(seasonRecord,index=['W','L','T'])
    with open(fileName,'w') as f:
        json.dump(df.to_json(),f)
