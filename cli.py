import os
from argparse import ArgumentParser
from pathlib import Path

from dotenv import load_dotenv
from farcaster import Warpcast


DEFAULT_FILE_PATH = "./.farcaster_graph.txt"
SEEN_USERS = {}


def get_client() -> Warpcast:
    """Get instance of Warpcast client"""
    load_dotenv(".env")

    try:
        api_key = os.environ["FARCASTER_MNEMONIC"]
    except KeyError:
        raise ValueError("Missing env var `FARCASTER_MNEMONIC`")

    return Warpcast(mnemonic=api_key)


def get_following_data(c: Warpcast, fid: int) -> str:
    following = {
        user.fid: (user.username or user.display_name)
        for user in c.get_all_following(fid).users
    }
    SEEN_USERS.update(following)

    try:
        current_username = SEEN_USERS[fid]
    except KeyError:
        current_username = c.get_user(fid).username

    return " ".join([str(fid), current_username] + list(following.values())) + "\n"


def get_starting_fid(file_name: Path):
    fp = Path(file_name)
    if not fp.exists():
        return 1

    for line in open(fp, "r"):
        pass

    return int(line.split()[0])


def pull_following(start_fid: int, file_name: str, c: Warpcast):
    while True:
        if start_fid % 100 == 0:
            print(f"Pulling followers for fid: {start_fid}")

        following = get_following_data(c, start_fid)

        with open(file_name, "a") as f:
            f.write(following)

        start_fid += 1


def main():
    parser = ArgumentParser(description="Process some integers.")

    # Add the optional output file path argument
    # The `nargs='?'` makes the argument optional
    parser.add_argument(
        "--output_file_path", type=str, nargs="?", help="Optional output file path"
    )

    parser.add_argument("--test", action="store_true")

    # Parse the command line arguments
    args = parser.parse_args()
    client = get_client()

    if args.test:
        assert client.get_healthcheck()
        print("Passed Healthcheck")
        return

    file_path = args.output_file_path or DEFAULT_FILE_PATH
    starting_fid = get_starting_fid(file_path)

    print(f"Starting from fid: {starting_fid}")
    pull_following(starting_fid, file_path, client)


if __name__ == "__main__":
    main()
