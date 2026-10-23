"""Interactive launcher for the safe defensive command center."""
from command_center import OmniSecCommandCenter

def main() -> int:
    OmniSecCommandCenter().cmdloop()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
