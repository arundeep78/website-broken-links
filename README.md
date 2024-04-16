# Find broken links easily

Find broken links in your website with easy to use web interface.

Streamlit application to find broken links in your website.
It is a wrapper around muffet, a Go library for finding broken links.

## Run using Docker

Run the Docker image using `docker run -p 8501:8501 arundeep78/website-broken-links`

## Usage

1. Enter the URL of the website you want to scan
3. Click the "Scan" button
4. Wait for the scan to complete
5. View the results in the web interface

## Features

- Find broken links in your website
- Easy to use web interface
- Provides easy summaries of the errors and success links
- Provide top 3 error codes and broken links
- Broken links list categorized in internal and external links
- Provides comparison of total links vs unique broken links
- Download broken links table for internal, external or complete set
- Supports max requests rate limit
- Supports ignoring TLS certificate checks


## Limitations - what may come next

- Only supports HTTP and HTTPS protocols
- Does not support custom headers
- Does not support custom user agent
- Does not support custom request timeout
- Does not support custom request retries
- Does not support custom request delay
- Support to customize scan for certian file types or ignore certain files


## Be careful

Default rate limit is set to '20'. It may be too high depending on your website infrastructure or DDoS attack configuration.

## Issue

If you find any issue, please create an issue. This will help to improve the project.

## Disclaimer

This project is not affiliated with or endorsed by the official website.
