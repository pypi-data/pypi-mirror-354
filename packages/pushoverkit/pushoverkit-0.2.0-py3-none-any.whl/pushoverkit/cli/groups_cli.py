from pushoverkit.groups import Groups

def setup_groups_cli(subparsers):
    parser = subparsers.add_parser("groups", help="Manage groups")
    group_subparsers = parser.add_subparsers(dest="group_command", required=True)

    # create
    create = group_subparsers.add_parser("create", help="Create a new group")
    create.add_argument("--token", "-t", required=True)
    create.add_argument("--name", "-n", required=True)
    create.set_defaults(func=handle_create)

    # rename
    rename = group_subparsers.add_parser("rename", help="Rename a group")
    rename.add_argument("--token", "-t", required=True)
    rename.add_argument("--group-key", "-g", required=True)
    rename.add_argument("--name", "-n", required=True)
    rename.set_defaults(func=handle_rename)

    # list-groups
    list_groups = group_subparsers.add_parser("list-groups", help="List all groups")
    list_groups.add_argument("--token", "-t", required=True)
    list_groups.set_defaults(func=handle_list_groups)

    # list-users
    list_users = group_subparsers.add_parser("list-users", help="List users in a group")
    list_users.add_argument("--token", "-t", required=True)
    list_users.add_argument("--group-key", "-g", required=True)
    list_users.set_defaults(func=handle_list_users)

    # add-user
    add_user = group_subparsers.add_parser("add-user", help="Add user to group")
    add_user.add_argument("--token", "-t", required=True)
    add_user.add_argument("--group-key", "-g", required=True)
    add_user.add_argument("--user", "-u", required=True)
    add_user.add_argument("--device", "-d")
    add_user.add_argument("--memo", "-m")
    add_user.set_defaults(func=handle_add_user)

    # remove-user
    remove_user = group_subparsers.add_parser("remove-user", help="Remove user from group")
    remove_user.add_argument("--token", "-t", required=True)
    remove_user.add_argument("--group-key", "-g", required=True)
    remove_user.add_argument("--user", "-u", required=True)
    remove_user.add_argument("--device", "-d")
    remove_user.set_defaults(func=handle_remove_user)

    # disable-user
    disable_user = group_subparsers.add_parser("disable-user", help="Disable user in group")
    disable_user.add_argument("--token", "-t", required=True)
    disable_user.add_argument("--group-key", "-g", required=True)
    disable_user.add_argument("--user", "-u", required=True)
    disable_user.add_argument("--device", "-d")
    disable_user.set_defaults(func=handle_disable_user)

    # enable-user
    enable_user = group_subparsers.add_parser("enable-user", help="Enable user in group")
    enable_user.add_argument("--token", "-t", required=True)
    enable_user.add_argument("--group-key", "-g", required=True)
    enable_user.add_argument("--user", "-u", required=True)
    enable_user.add_argument("--device", "-d")
    enable_user.set_defaults(func=handle_enable_user)

# Handlers

def handle_create(args):
    g = Groups(token=args.token)
    print(g.create(name=args.name))

def handle_rename(args):
    g = Groups(token=args.token)
    print(g.rename(group_key=args.group_key, name=args.name))

def handle_list_groups(args):
    g = Groups(token=args.token)
    print(g.list_groups())

def handle_list_users(args):
    g = Groups(token=args.token)
    print(g.list_users(group_key=args.group_key))

def handle_add_user(args):
    g = Groups(token=args.token)
    print(g.add_user(group_key=args.group_key, user=args.user, device=args.device, memo=args.memo))

def handle_remove_user(args):
    g = Groups(token=args.token)
    print(g.remove_user(group_key=args.group_key, user=args.user, device=args.device))

def handle_disable_user(args):
    g = Groups(token=args.token)
    print(g.disable_user(group_key=args.group_key, user=args.user, device=args.device))

def handle_enable_user(args):
    g = Groups(token=args.token)
    print(g.enable_user(group_key=args.group_key, user=args.user, device=args.device))