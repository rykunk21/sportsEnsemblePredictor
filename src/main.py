import tkinter as tk
from src.Lib.gui import GUI
from src.Lib.simulation import MonteCarlo
from src.Lib.util import printGameResult
from src.Lib.data import LineScraper, NCAABRosterScraper, NCAABPlayerScraper, simHandler

import numpy as np
import random
import time
import os
import pickle
import json

def main(args):
    # Check the provided subcommand
    if args.command is None:
        gui = GUI()
        gui.run()

    elif args.command == 'sim':
        # Run simulator with additional arguments
        print(f"Running simulator with args: {args.home}, {args.away}")

        sim = MonteCarlo(args.home, args.away)
        prob, spreads = sim.run(10000)

        ls = LineScraper(args.home, args.away)
        game = ls.getGame()

        spread = ls.spread()
        spreadProb = sim.probability_of_value(spreads, spread)
        simResults = (np.mean(spreads), spreadProb, prob)

        printGameResult(game, simResults)



    elif args.command == 'pull':
            
        teams = args.teams

        for teamName in teams:
            file_path = f'test/teams/{teamName}.pkl'
            if os.path.exists(file_path):   
                print(f'{teamName} already in database!!!')
                continue
            team = NCAABRosterScraper(teamName) 

            print(f'Starting {teamName} Scrape')

            teamTable = {}

            for link in team.getLinks():
                name, link = link[0]

                time.sleep(15 + random.uniform(0, 10)) 
                try:
                    scraper = NCAABPlayerScraper(name, link)
                    print(f'Scraped {teamName} player: {name}')
                    table = scraper.getTable()
                    teamTable[name] = table
                except:
                    continue

            with open(f'test/teams/{teamName}.pkl', 'wb') as file:
                pickle.dump(teamTable, file)


    elif args.command == 'update':
        
        teams = args.teams
        
        
        if teams == ['.']:
            for filename in os.listdir('./test/teams'):
                team = filename.split('.')[0]
                print(f'UPDATING TEAM {team}')
                team = simHandler.updateTeam(team)
            
        else:
            for team in teams:
                simHandler.updateTeam(team)


    elif args.command == 'slate':

        games = LineScraper().getTodaysGames()

        results = []

        with open('./datasets/ncaab/mapping.json', 'r') as fp:
            mappings = json.load(fp)
        
        for home, away in games:
            print(f"Running simulator with args: {home.name}, {away.name}")
            if not simHandler.exists(home.name):
                if mappings.get(home.name):
                    home.name = mappings.get(home.name)
                else:
                    print(f'{home.name} not in known teams')
                    continue
            if not simHandler.exists(away.name):
                if mappings.get(home.name):
                    away.name = mappings.get(away.name)
                else:
                    print(f'{away.name} not in known teams')
                    continue
            
            game = (home, away)
            sim = MonteCarlo(home.name, away.name)
            prob, spreads = sim.run(10000)

            spread = home.spread

            spreadProb = sim.probability_of_value(spreads, spread)
            simResults = (np.mean(spreads), spreadProb, prob)

            results.append((home, away, simResults))

            printGameResult(game, simResults)