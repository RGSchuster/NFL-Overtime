#This program builds nested lists of divisions
#There is a large list with each year per index
#Inside that list are lists of the divisions
#Inside that list are team names

import bs4 as bs
import urllib.request
import csv
import json
import pandas as pd

fullLeague = []
for year in range(1974,2019):
    
    sauce = urllib.request.urlopen('https://www.pro-football-reference.com/years/' + str(year) + '/index.htm').read()
    soup = bs.BeautifulSoup(sauce,'lxml')

    league = [[]]
    print(year,len(fullLeague)) #allows compiling code to be visualized
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
    league.pop() #deletes an extra empty list that is added to the end
    fullLeague.append(league)

print(fullLeague[0][0][0])

with open('DivisionStorage.txt','w') as outputFile:
    json.dump(fullLeague,outputFile)

#############
#this KIND OF works for output to csv:
#
##with open('divisions.csv','w',newline='') as f:
##    writer = csv.writer(f)
##    writer.writerows(fullLeague)
    

#json.load OR json.dump
