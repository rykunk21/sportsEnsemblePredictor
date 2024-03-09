"""
This is the main entry point of the program

"""
import argparse
import src.main
import warnings

def main():
    # Create the top-level parser
    parser = argparse.ArgumentParser(description='Your program description.')

    # Create subparsers
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Subparser for 'sim' command
    sim_parser = subparsers.add_parser('sim', help='Run simulator with additional arguments')
    sim_parser.add_argument('home', help='Home team')
    sim_parser.add_argument('away', help='Away team')

    # Subparser for 'pull' command
    pull_parser = subparsers.add_parser('pull', help='Pull data with additional arguments')
    pull_parser.add_argument('teams', nargs='+', type=str, help='List of team numbers for pull command')

    # Subpaser for 'update'
    update_parser = subparsers.add_parser('update', help='Update the existing list of teams or omit args to update all')
    update_parser.add_argument('teams', nargs='+', type=str, help='list of teams you wish ot update')

    # Subparser for 'slate'
    update_parser = subparsers.add_parser('slate', help='Run a whole slate')

    # Parse the arguments
    args = parser.parse_args()


    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning, module="numpy")
        
        # Call src.main.main() with the parsed arguments
        src.main.main(args)

if __name__ == '__main__':
    main()