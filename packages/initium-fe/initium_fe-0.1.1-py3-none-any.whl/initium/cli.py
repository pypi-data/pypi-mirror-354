import argparse
from .generator import generate_project

def main():
    parser = argparse.ArgumentParser(description='Festo Project Bootstrap')
    parser.add_argument('name', help='Project name')
    parser.add_argument('type', choices=['plc', 'hmi', 'ros', 'bioreactor'], 
                        help='Project type')
    parser.add_argument('--remote', action='store_true', 
                        help='Create remote GitLab project')
    
    args = parser.parse_args()
    generate_project(args.name, args.type, args.remote)

if __name__ == '__main__':
    main() 