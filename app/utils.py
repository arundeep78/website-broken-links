import base64
from enum import IntEnum, StrEnum
import json
import PIL.Image
from urllib3.util import parse_url
import subprocess
import requests
import os
import shutil
import pandas as pd

MUFFET_PATH = "MUFFET_PATH"
LAST_PROCESSED_WEBSITE = "LAST_PROCESSED_WEBSITE"
OUTPUT_FILE = './output/output.json'


# create a frozen enum with values INTERNAL and EXTERNAL equaling to 0 and 1 respectively

class LinkOrigin(StrEnum):
    INTERNAL = "Internal"
    EXTERNAL = "External"


def set_last_processed_website(url):
    os.environ[LAST_PROCESSED_WEBSITE] = url

def get_last_processed_website():
    return os.environ.get(LAST_PROCESSED_WEBSITE)

def get_muffet_path():
    return os.environ.get(MUFFET_PATH)

def is_valid_url(url):

    # Check if the URL starts with http:// or https://``
    if not (url.startswith('http://') or url.startswith('https://')):
        return False
    
    # Check if the URL is well-formed
    try:
        result = parse_url(url)
        return all([result.scheme, result.host])
    except ValueError:
        return False
 

# with urllib library check if the url returns success or not

def is_url_accessible(url):
    # Check if the URL is accessible
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def set_search_tool_path():
    # If muffet isn't on PATH, check a couple other likely spots
    muffet_path = shutil.which("muffet")
    if not muffet_path:
        if shutil.os.path.isfile("/muffet"):
            muffet_path = "/muffet"
        elif shutil.os.path.isfile("./muffet"):
            muffet_path = shutil.os.path.realpath("./muffet")
        else:
            raise Exception("Couldn't find muffet")
    os.environ[MUFFET_PATH] = muffet_path

def get_muffet_search_results(url, show_success:bool, ignore_verify_tls:bool, rate_limit:int=None):

    # Run muffet and capture the output
    # prepare the command to run muffet
    muffet_command = [
        get_muffet_path(),
        "--timeout=30",
        "--color=always",
        "--buffer-size=8192",
        "--format=json",
    ]

    # add the show_success and ignore_verify_tls flags if provided
    if show_success:
        muffet_command.append("--verbose")

    if ignore_verify_tls:
        muffet_command.append("--skip-tls-verification")

    if rate_limit:
        muffet_command.append(f"--rate-limit={rate_limit}")

    # add the url to the command
    muffet_command.append(url)
    print(muffet_command)

    proc = subprocess.run(  muffet_command,
                            capture_output=True

                        )
    
    # store results in a file called 'output.json'
    save_output(proc.stdout.decode('utf-8'))

    # with open(OUTPUT_FILE, 'w') as f:
    #     f.write(proc.stdout.decode('utf-8'))

    # Return the JSON output

    data = json.loads(proc.stdout.decode('utf-8'))
    
    return data

def save_output(data):
    '''
    save outoput to a file called 'output.json'
    '''

    # check if OUTPUT_FILE exists, if path does not exists then create it

    OUTPUT_DIR=os.path.dirname(OUTPUT_FILE)
    if not os.path.exists(OUTPUT_DIR):
        try:
            os.makedirs(OUTPUT_DIR)
        except Exception as e:
            print(f"An error occurred while creating directory '{OUTPUT_DIR}'. Error: {str(e)}")

    with open(OUTPUT_FILE, 'w') as f:
        f.write(data)
      

def process_website(url, show_success:bool, ignore_verify_tls:bool, rate_limit:int):
    '''
    Process the website given as a url using the muffet tool using the provided input paramters.
    parse the generated output. create a dataframe and returns dataframe as output

    Parameters:

        url (str): The URL of the website to process.
        show_success (bool): Whether to show successful URLs.
        verify_tls (bool): Whether to verify TLS certificates. 
        rate_limit (int): The rate limit in HTTP requests per second for the website.

    Returns:
        DataFrame: A dataframe containing the results of the website processing.

    Example:

    results = process_website("http://example.com", show_success=True, verify_tls=False)

    print(results)

    '''

    # validate input values

    # check if the URL is valid
    assert is_valid_url(url), "URL must be valid"

    # check if the URL is accessible
    assert is_url_accessible(url), "URL must be accessible"

    # set last process url as an environment variable called 'last_tested_website'
    set_last_processed_website(url)

    # set the search tool path
    set_search_tool_path()  

    # Run muffet and capture the output
    data = get_muffet_search_results(url, show_success, ignore_verify_tls, rate_limit)

    # Create a dataframe from the parsed JSON
    df = pd.json_normalize(data, record_path=['links'], meta=['url'],meta_prefix='parent_')

    if len(df) ==0:
        return df

    # Add link_origin column and mark it external or internal link based on the url
    df['link_origin'] = LinkOrigin.INTERNAL

    df['link_origin']= df['link_origin'].where(df['url'].str.startswith(url), LinkOrigin.EXTERNAL)


    # Return the results
    return df    

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="broken_links.csv">Download complete results as csv file</a>'
    return href


