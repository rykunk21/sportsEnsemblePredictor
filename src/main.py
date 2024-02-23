import tkinter as tk
from src.Lib.gui import GUI
from src.Lib.simulation import MonteCarlo
from src.Lib.util import Game, convertline
from src.Lib.data import LineScraper, NCAABRosterScraper, NCAABPlayerScraper
import numpy as np
import random
import time
import os
import pickle

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

        spread = ls.spread()
        home_ml_odds, away_ml_odds = ls.getMoneyLineOdds()
        home_spread_odds, away_spread_odds = ls.getSpreadOdds()

        spreadProb = sim.probability_of_value(spreads, spread)
        home_team = sim.game.home
        away_team = sim.game.away

        fieldWidth = max(
            len(home_team + ' cover:'), 
            len(home_team + ' ML:'), 
            len(away_team + ' cover'), 
            len(away_team + ' ML:'),
            len(f'Spread {np.mean(spreads):.2f}')
        )
       

        print('-' * (fieldWidth + 30))
        print('{:^{width}}|{:^15}|{:^15}'.format(f'Spread {np.mean(spreads):.2f}', 'Prob', 'Diff', width=fieldWidth))
        print('-' * (fieldWidth + 30))  # Adjust the total width as needed

        print('{:<{width}}|{:^15.2f}|{:^15.2f}'.format(
            f'{home_team} cover:', spreadProb, 
            spreadProb - convertline(home_spread_odds), width=fieldWidth)
        )
        
        print('{:<{width}}|{:^15.2f}|{:^15.2f}'.format(
            f'{home_team} ML:', prob, 
            prob - convertline(home_ml_odds), width=fieldWidth)
        )
        
        print('{:<{width}}|{:^15.2f}|{:^15.2f}'.format(
            f'{away_team} cover', 1 - spreadProb, 
            (1 - spreadProb) - convertline(away_spread_odds), width=fieldWidth)
        )
        
        print('{:<{width}}|{:^15.2f}|{:^15.2f}'.format(
            f'{away_team} ML:', 1 - prob, 
            (1 - prob) - convertline(away_ml_odds), width=fieldWidth)
        )


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

                time.sleep(45 + random.uniform(0, 30)) 
                try:
                    scraper = NCAABPlayerScraper(name, link)
                    print(f'Scraped {teamName} player: {name}')
                    table = scraper.getTable()
                    teamTable[name] = table
                except:
                    continue

            with open(f'test/teams/{teamName}.pkl', 'wb') as file:
                pickle.dump(teamTable, file)