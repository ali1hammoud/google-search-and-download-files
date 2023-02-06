# Google Search and files download
A Python script that allows you to search Google from terminal and GUI, create a dataset to save the results.

## Features
- Search the given query string using Google.
- Downloading files from google results
- Use of parameters such as query string, top level domain, language, time limits, safe search, number of results, start and stop result, pause between requests, country or region, file type, extra parameters, user agent, and SSL verification.
- Run in terminal and gui.
- Results are returned as a generator of URLs.

## Usage
To use the Google Search script, simply call the search function and pass in your desired parameters.

Here's an example of searching for the query "Python":

```python
from googles import search
for url, title in search("Python", tld="com", num=10, stop=20, pause=2):
    print(url, title)
```
or from terminal:
```
>python main.py -h
```
or using GUI:
```
>python gui.py
```
## Parameters
The following parameters can be passed to the search function:

- `query` (str): Query string. Must NOT be URL-encoded.
- `tld` (str): Top-level domain.
- `lang` (str): Language.
- `tbs` (str): Time limits (i.e "qdr:h" => last hour, "qdr:d" => last 24 hours, "qdr:m" => last month).
- `safe` (str): Safe search.
- `num` (int): Number of results per page.
- `start` (int): First result to retrieve.
- `stop` (int): Last result to retrieve. Use None to keep searching forever.
- `pause` (float): Lapse to wait between HTTP requests. A lapse too long will make the search slow, but a lapse too short may cause Google to block your IP.
- `country` (str): Country or region to focus the search on. Similar to changing the TLD, but does not yield exactly the same results.
- `filetype` (str): File type to search.
- `extra_params` (dict): A dictionary of extra HTTP GET parameters, which must be URL-encoded. For example, if you don't want Google to filter similar results, you can set the extra_params to {'filter': '0'}, which will append '&filter=0' to every query.
- `user_agent` (str): User agent for the HTTP requests. Use None for the default.
- `verify_ssl` (bool): Verify the SSL certificate to prevent traffic interception attacks. Defaults to True.
- `path_dataset` (str): Path to open/save the dataset.

## Credits
This repository is based on the work of ![Mario Vilas](https://github.com/MarioVilas/googlesearch).
