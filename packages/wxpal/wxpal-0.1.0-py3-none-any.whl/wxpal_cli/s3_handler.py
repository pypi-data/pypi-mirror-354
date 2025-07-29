# WxPal_CLI/s3_handler.py

import boto3
import fnmatch
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError

BUCKET_NAME = "paladinoutputs"
FOLDER_PREFIX = "Data/fxx/"

def validate_credentials(access_key, secret_key, region):
    try:
        boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        ).list_buckets()
        return True
    except Exception as e:
        print(f"❌ Credential check failed: {e}")
        return False

def list_available_days(access_key, secret_key, region):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=FOLDER_PREFIX, Delimiter="/")
        folders = [
            cp["Prefix"].replace(FOLDER_PREFIX, "").strip("/")
            for cp in response.get("CommonPrefixes", [])
        ]
        return folders
    except ClientError as e:
        print(f"Error listing folders: {e}")
        return []

def list_latest_forecast(access_key, secret_key, region, datetime_code=None):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    if datetime_code:
        try:
            dt = datetime.strptime(datetime_code, "%m%d%Y%H")
            folder = f"{dt.year}_{dt.month}_{dt.day}"  # NOT zero padded
        except ValueError:
            print("⚠️ Invalid datetime_code format. Use MMDDYYYYHH.")
            return None, []
    else:
        try:
            response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=FOLDER_PREFIX, Delimiter="/")
            folders = [
                cp["Prefix"].replace(FOLDER_PREFIX, "").strip("/")
                for cp in response.get("CommonPrefixes", [])
            ]
            if not folders:
                return None, []
            folder = sorted(folders)[-1]  # latest unpadded folder
        except ClientError as e:
            print(f"Error listing folders: {e}")
            return None, []

    # Match file names with padded format
    parts = folder.split("_")
    if len(parts) != 3:
        print(f"⚠️ Unexpected folder format: {folder}")
        return None, []

    folder_padded = f"{int(parts[0]):04}_{int(parts[1]):02}_{int(parts[2]):02}"
    full_prefix = f"{FOLDER_PREFIX}{folder}/"  # Use original folder name

    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=full_prefix)
        contents = response.get("Contents", [])
    except ClientError as e:
        print(f"Error listing files: {e}")
        return None, []

    files = []
    for obj in contents:
        key = obj["Key"]
        if fnmatch.fnmatch(key, f"{full_prefix}log_{folder_padded}_*_*.nc"):
            files.append(key.split("/")[-1])

    return full_prefix, sorted(files)

def download_forecast_set(prefix, files, access_key, secret_key, region, out_dir="."):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    for file in files:
        out_path = f"{out_dir}/{file}"
        s3.download_file(BUCKET_NAME, f"{prefix}{file}", out_path)
        print(f"✅ Downloaded: {out_path}")
