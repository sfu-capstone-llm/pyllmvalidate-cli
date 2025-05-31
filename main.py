import argparse


def main():
    args = parseArgs()
    print(args)


def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", action="store")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
