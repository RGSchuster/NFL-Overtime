#This program builds nested lists of divisions
#There is a large list with each year per index
#Inside that list are lists of the divisions
#Inside that list are team names

import bs4 as bs
import urllib.request
import csv

fullLeague = []
for year in range(1974,2018):
    
    sauce = urllib.request.urlopen('https://www.pro-football-reference.com/years/' + str(year) + '/index.htm').read()
    soup = bs.BeautifulSoup(sauce,'lxml')

    league = [[]]
    print(year) #allows compiling code to be visualized
    i = -1

    for eachTable in soup.find_all('tbody'):
        for xx in eachTable.find_all('tr'):
            if xx.string != None:
                #splits on the division name
                league.append([])
                i+=1
            else:
                #on team name
                (league[i]).append(xx.a.string.split()[-1])
    del league[-1] #this deletes an extra empty list is added to the end
    fullLeague.append(league)

#############
#this works for output to csv:
#
with open('divisions.csv','w') as f:
    writer = csv.writer(f)
    writer.writerows(fullLeague)
