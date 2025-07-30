from pushoverkit.teams import Teams

def setup_teams_cli(subparsers):
    parser = subparsers.add_parser("teams", help="Manage Pushover Teams")
    team_subparsers = parser.add_subparsers(dest="team_command", required=True)

    # add-user
    add_user = team_subparsers.add_parser("add-user", help="Add a user to your team")
    add_user.add_argument("--team-token", "-t", required=True, help="Your team's API token")
    add_user.add_argument("--email", "-e", required=True, help="Email of the user to add")
    add_user.add_argument("--name", "-n", help="Full name of the user")
    add_user.add_argument("--password", "-p", help="Set a password (optional)")
    add_user.add_argument("--instant", "-i", action="store_true", help="Enable Instant Login link")
    add_user.add_argument("--admin", "-a", action="store_true", help="Add user as administrator")
    add_user.add_argument("--group", "-g", help="Assign user to a specific Delivery Group")
    add_user.set_defaults(func=handle_add_user)

    # remove-user
    remove_user = team_subparsers.add_parser("remove-user", help="Remove a user from your team")
    remove_user.add_argument("--team-token", "-t", required=True, help="Your team's API token")
    remove_user.add_argument("--email", "-e", required=True, help="Email of the user to remove")
    remove_user.set_defaults(func=handle_remove_user)


def handle_add_user(args):
    t = Teams(team_token=args.team_token)
    result = t.add_user(
        email=args.email,
        name=args.name,
        password=args.password,
        instant=args.instant,
        admin=args.admin,
        group=args.group
    )
    print(result)


def handle_remove_user(args):
    t = Teams(team_token=args.team_token)
    result = t.remove_user(email=args.email)
    print(result)