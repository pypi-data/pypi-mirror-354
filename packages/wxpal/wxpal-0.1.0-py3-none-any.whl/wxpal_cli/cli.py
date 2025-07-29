# wxpal_CLI/cli.py

import argparse
import configparser
from pathlib import Path
from .s3_handler import list_latest_forecast, download_forecast_set, list_available_days
import boto3

def WxPal_Logo():
    print("      _____                                _____         _____    ____                              ____-^-____              ")
    print("     |\    \   _____  _____      _____ ___|\    \    ___|\    \  |    |                         __-^           ^-__          ")
    print("     | |    | /    /| \    \    /    /|    |\    \  /    /\    \ |    |                      _-^                   ^-_       ")
    print("     \/     / |    ||  \    \  /    / |    | |    ||    |  |    ||    |                     //^^^^--___ < >  ___--^^^^\\\    ")
    print("     /     /_  \   \/   \____\/____/  |    |/____/||    |__|    ||    |  ____              | |_________\   /__________||     ")
    print("    |     // \  \   \   /    /\    \  |    ||    |||    .--.    ||    | |    |             |  \       / / \ \       /  |     ")
    print("    |    |/   \ |    | /    /  \    \ |    ||____|/|    |  |    ||    | |    |              \_^--____/ /   \ \____--^_/      ")
    print("    |\ ___/\   \|   /|/____/ /\ \____\|____|       |____|  |____||____|/____/|                \__^-__  \_^_/  __-^__/        ")
    print("    | |   | \______/ ||    |/  \|    ||    |       |    |  |    ||    |     ||                  \     ______     /           ")
    print("     \|___|/\ |    | ||____|    |____||____|       |____|  |____||____|_____|/                    |   | ___ |   |            ")
    print("        \(   \|____|/   \(        )/    \(           \(      )/    \(    )/                       |   |     |   |            ")
    print("         '      )/       '        '      '            '      '      '    '                         |  |     |  |             ")
    print("                '                                                                                  |  |     |  |             ")
    print("           Welcome to WxPal, G. Paladin Industries, Inc. Copyright 2025                            \__|     |__/             ")
    print("                                                                                                                             ")
    print(" !!! !!! FYI Homie, THIS IS A PROTOTYPE, NOT FOR PRODUCTION USE, SO DON'T MAKE ANY IMPORTANT DECISIONS BASED ON THIS !!! !!! ")

def load_or_prompt_credentials():
    config_path = Path.home() / '.wxpal_config'
    config = configparser.ConfigParser()

    def test_credentials(access_key, secret_key, region):
        try:
            s3 = boto3.client(
                's3',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region,
            )
            # Test basic access (adjust to match bucket if needed)
            s3.list_objects_v2(Bucket='paladinoutputs', Prefix='Data/fxx/', MaxKeys=1)
            return True
        except Exception as e:
            print(f"\n❌ Credential check failed: {e}")
            return False

    if config_path.exists():
        config.read(config_path)
        creds = config['default']
        access_key = creds.get('aws_access_key_id', '')
        secret_key = creds.get('aws_secret_access_key', '')
        region = creds.get('region', 'us-east-1')

        if test_credentials(access_key, secret_key, region):
            return access_key, secret_key, region
        else:
            print("\n🔁 Invalid credentials found. Please re-enter your AWS keys.")
            config_path.unlink()  # delete bad config to reset

    # Prompt and validate
    while True:
        print("\n🔐 WxPal Credential Setup\n")
        access_key = input("WxPal Access Key ID: ").strip()
        secret_key = input("WxPal Secret Key: ").strip()
        region = 'us-east-1'

        if test_credentials(access_key, secret_key, region):
            config['default'] = {
                'aws_access_key_id': access_key,
                'aws_secret_access_key': secret_key,
                'region': region,
            }
            with open(config_path, 'w') as f:
                config.write(f)
            return access_key, secret_key, region
        else:
            print("❌ Shoot, those credentials didn’t work. Let's try that again. Sorry playa.")


def main():
    WxPal_Logo()
    parser = argparse.ArgumentParser(description="WxPal S3 CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    parser_download = subparsers.add_parser("download", help="Download forecast files from S3")
    parser_download.add_argument("target", help="'latest' or datetime string like '0607202500'")

    parser_list = subparsers.add_parser("list", help="List available forecast days")

    args = parser.parse_args()

    if args.command == "download":
        access_key, secret_key, region = load_or_prompt_credentials()

        if args.target == "latest":
            prefix, files = list_latest_forecast(access_key, secret_key, region)
        else:
            prefix, files = list_latest_forecast(access_key, secret_key, region, datetime_code=args.target)

        if files:
            print(f"\n📦 Downloading forecast from: {prefix}")
            download_forecast_set(prefix, files, access_key, secret_key, region)
        else:
            print("\n❌ Sorry g, it looks like that joint doesn't exist")

    elif args.command == "list":
        access_key, secret_key, region = load_or_prompt_credentials()
        available_days = list_available_days(access_key, secret_key, region)
        if available_days:
            print("\n📅 Available forecast days:")
            for day in sorted(available_days, reverse=True):
                print(" -", day)
        else:
            print("\n❌ No forecasts available, sorry homie.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
