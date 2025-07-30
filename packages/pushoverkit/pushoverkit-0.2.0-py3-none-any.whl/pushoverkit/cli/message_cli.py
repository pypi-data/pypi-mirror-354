from pushoverkit import Pushover

def setup_message_cli(subparsers):
    parser = subparsers.add_parser("push", help="Push a message")

    # Required
    parser.add_argument("--token", "-t", required=True, help="Your Pushover app token")
    parser.add_argument("--user", "-u", required=True, help="User key to send the message to")
    parser.add_argument("--message", "-m", required=True, help="Message content")

    # Optional arguments
    parser.add_argument("--title", help="Message title")
    parser.add_argument("--device", "-d", help="Target a specific device")
    parser.add_argument("--html", type=int, choices=[0, 1], default=0, help="Enable HTML formatting (1 or 0)")
    parser.add_argument("--monospace", type=int, choices=[0, 1], default=0, help="Enable monospace font (1 or 0)")
    parser.add_argument("--priority", "-p", type=int, choices=[-2, -1, 0, 1, 2], default=0, help="Message priority")
    parser.add_argument("--sound", "-s", help="Override default notification sound")
    parser.add_argument("--timestamp", type=int, help="Unix timestamp for the message")
    parser.add_argument("--ttl", type=int, help="Time to live for emergency-priority messages")
    parser.add_argument("--url", help="Supplementary URL to include")
    parser.add_argument("--url-title", help="Title for the supplementary URL")
    parser.add_argument("--attachment", "-a", help="Path to a file to attach")
    parser.add_argument("--attachment-base64", help="Base64-encoded attachment data")
    parser.add_argument("--attachment-type", help="MIME type for the base64 attachment")

    parser.set_defaults(func=handle_message)

def handle_message(args):
    p = Pushover(token=args.token, default_user=args.user)
    res = p.push(
        message=args.message,
        title=args.title,
        device=args.device,
        html=args.html,
        monospace=args.monospace,
        priority=args.priority,
        sound=args.sound,
        timestamp=args.timestamp,
        ttl=args.ttl,
        url=args.url,
        url_title=args.url_title,
        attachment=args.attachment,
        attachment_base64=args.attachment_base64,
        attachment_type=args.attachment_type,
    )
    print(res)