import argparse
from .helper import main_deploy
from .database_helper import update_schema_flow
from .utils import send_email

VALID_PROJECTS = ["backoffice", "websites", "flightbite"]
VALID_UPDATE_TARGETS = ["master database","log database","logs database","client database"]
VALID_ENVS = {
    "staging": "staging",
    "uat": "uat",
    "production": "prod",
    "prod": "prod",
    "live": "prod"
}

VALID_PREPOSITIONS = ["to", "on"]

def deploy(env, project):
    print(f"🚀 Deploying '{project}' to environment '{env}'")
    main_deploy(env, project)

def update_database(target, env):
    print(f"🔄 Updating '{target}' on '{env}'")
    update_schema_flow(target,env)
    #send_email("Staging", "Database", "1. Schema applied to database\n2. Point2", "Backoffice")

def main():
    parser = argparse.ArgumentParser(prog="mini", description="Zikomo Mini CLI Assistant, developed by Imran A. Shah")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy a project")
    deploy_parser.add_argument("project", choices=VALID_PROJECTS, help="Project to deploy")
    deploy_parser.add_argument("preposition", choices=VALID_PREPOSITIONS, help="'to' or 'on'")
    deploy_parser.add_argument("environment", choices=VALID_ENVS.keys(), help="Target environment")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update client systems")
    update_parser.add_argument("target", nargs=2, help="Update target (e.g., client database)")
    update_parser.add_argument("preposition", choices=VALID_PREPOSITIONS, help="'to' or 'on'")
    update_parser.add_argument("environment", choices=VALID_ENVS.keys(), help="Target environment")

    args = parser.parse_args()

    if args.command == "deploy":
        env = VALID_ENVS[args.environment.lower()]
        deploy(env, args.project)

    elif args.command == "update":
        env = VALID_ENVS[args.environment.lower()]
        target = " ".join(args.target).lower()
        
        if target not in VALID_UPDATE_TARGETS:
            print(f"❌ Unsupported update target: '{target}'")
            return
        
        update_database(target, env)

# MAIN
if __name__ == "__main__":
    main()
