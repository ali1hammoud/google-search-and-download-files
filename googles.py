#!/usr/bin/env python

import os
import random
import sys
import time
import ssl
import requests
import hashlib

if sys.version_info[0] > 2:
    from http.cookiejar import LWPCookieJar
    from urllib.request import Request, urlopen, urlretrieve
    from urllib.parse import quote_plus, urlparse, parse_qs
else:
    from cookielib import LWPCookieJar
    from urllib import quote_plus
    from urllib2 import Request, urlopen, urlretrieve
    from urlparse import urlparse, parse_qs

try:
    from bs4 import BeautifulSoup
    is_bs4 = True
except ImportError:
    from BeautifulSoup import BeautifulSoup
    is_bs4 = False

__all__ = [

    # Main search function.
    'search',

    # Shortcut for downloading files.
    'download',

    # Miscellaneous utility functions.
    'get_random_user_agent', 'get_tbs',
]

# URL templates to make Google searches.
url_home = "https://www.google.%(tld)s/"
url_search = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&" \
             "btnG=Google+Search&tbs=%(tbs)s&safe=%(safe)s&" \
             "cr=%(country)s"
url_next_page = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&" \
                "start=%(start)d&tbs=%(tbs)s&safe=%(safe)s&" \
                "cr=%(country)s"
url_search_num = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&" \
                 "num=%(num)d&btnG=Google+Search&tbs=%(tbs)s&safe=%(safe)s&" \
                 "cr=%(country)s"
url_next_page_num = "https://www.google.%(tld)s/search?hl=%(lang)s&" \
                    "q=%(query)s&num=%(num)d&start=%(start)d&tbs=%(tbs)s&" \
                    "safe=%(safe)s&cr=%(country)s"
url_parameters = (
    'hl', 'q', 'num', 'btnG', 'start', 'tbs', 'safe', 'cr')

# Cookie jar. Stored at the user's home folder.
# If the cookie jar is inaccessible, the errors are ignored.
home_folder = os.getenv('HOME')
if not home_folder:
    home_folder = os.getenv('USERHOME')
    if not home_folder:
        home_folder = '.'   # Use the current folder on error.
cookie_jar = LWPCookieJar(os.path.join(home_folder, '.google-cookie'))
try:
    cookie_jar.load()
except Exception:
    pass

# Default user agent, unless instructed by the user to change it.
#USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'

# Load the list of valid user agents from the install folder.
# The search order is:
#   * user_agents.txt.gz
#   * user_agents.txt
#   * default user agent
try:
    install_folder = os.path.abspath(os.path.split(__file__)[0])
    try:
        user_agents_file = os.path.join(install_folder, 'user_agents.txt.gz')
        import gzip
        fp = gzip.open(user_agents_file, 'rb')
        try:
            user_agents_list = [_.strip() for _ in fp.readlines()]
        finally:
            fp.close()
            del fp
    except Exception:
        user_agents_file = os.path.join(install_folder, 'user_agents.txt')
        with open(user_agents_file) as fp:
            user_agents_list = [_.strip() for _ in fp.readlines()]
except Exception:
    user_agents_list = [USER_AGENT]


# Get a random user agent.
def get_random_user_agent():
    """
    Get a random user agent string.

    :rtype: str
    :return: Random user agent string.
    """
    return random.choice(user_agents_list)


# Helper function to format the tbs parameter.
def get_tbs(from_date, to_date):
    """
    Helper function to format the tbs parameter.

    :param datetime.date from_date: Python date object.
    :param datetime.date to_date: Python date object.

    :rtype: str
    :return: Dates encoded in tbs format.
    """
    from_date = from_date.strftime('%m/%d/%Y')
    to_date = to_date.strftime('%m/%d/%Y')
    return 'cdr:1,cd_min:%(from_date)s,cd_max:%(to_date)s' % vars()

# Helper function to extract the title of the link
def extract_title(lst):
    title = []
    for item in lst:
        if '>' in item and '</' in item:
            start = item.index('>') + 1
            end = item.index('</')
            title.append(item[start:end])
            break
    return title

# Request the given URL and return the response page, using the cookie jar.
# If the cookie jar is inaccessible, the errors are ignored.
def get_page(url, user_agent=None, verify_ssl=True):
    """
    Request the given URL and return the response page, using the cookie jar.

    :param str url: URL to retrieve.
    :param str user_agent: User agent for the HTTP requests.
        Use None for the default.
    :param bool verify_ssl: Verify the SSL certificate to prevent
        traffic interception attacks. Defaults to True.

    :rtype: str
    :return: Web page retrieved for the given URL.

    :raises IOError: An exception is raised on error.
    :raises urllib2.URLError: An exception is raised on error.
    :raises urllib2.HTTPError: An exception is raised on error.
    """
    if user_agent is None:
        user_agent = USER_AGENT
    request = Request(url)
    request.add_header('User-Agent', user_agent)
    cookie_jar.add_cookie_header(request)
    if verify_ssl:
        response = urlopen(request)
    else:
        context = ssl._create_unverified_context()
        response = urlopen(request, context=context)
    cookie_jar.extract_cookies(response, request)
    html = response.read()
    response.close()
    try:
        cookie_jar.save()
    except Exception:
        pass
    return html


# Filter links found in the Google result pages HTML code.
# Returns None if the link doesn't yield a valid result.
def filter_result(link):
    try:

        # Decode hidden URLs.
        if link.startswith('/url?'):
            o = urlparse(link, 'http')
            link = parse_qs(o.query)['q'][0]

        # Valid results are absolute URLs not pointing to a Google domain,
        # like images.google.com or googleusercontent.com for example.
        # TODO this could be improved!
        o = urlparse(link, 'http')
        if o.netloc and 'google' not in o.netloc:
            return link

    # On error, return None.
    except Exception:
        pass


# Returns a generator that yields URLs.
def search(query, tld='com', lang='en', tbs='0', safe='off', num=10, start=0,
           stop=None, pause=2.0, country='', filetype=None ,extra_params=None,
           user_agent=None, verify_ssl=True, path_dataset = None):
    """
    Search the given query string using Google.

    :param str query: Query string. Must NOT be url-encoded.
    :param str tld: Top level domain.
    :param str lang: Language.
    :param str tbs: Time limits (i.e "qdr:h" => last hour,
        "qdr:d" => last 24 hours, "qdr:m" => last month).
    :param str safe: Safe search.
    :param int num: Number of results per page.
    :param int start: First result to retrieve.
    :param int stop: Last result to retrieve.
        Use None to keep searching forever.
    :param float pause: Lapse to wait between HTTP requests.
        A lapse too long will make the search slow, but a lapse too short may
        cause Google to block your IP. Your mileage may vary!
    :param str country: Country or region to focus the search on. Similar to
        changing the TLD, but does not yield exactly the same results.
        Only Google knows why...
    :para str filetype: File type to search.
    :param dict extra_params: A dictionary of extra HTTP GET
        parameters, which must be URL encoded. For example if you don't want
        Google to filter similar results you can set the extra_params to
        {'filter': '0'} which will append '&filter=0' to every query.
    :param str user_agent: User agent for the HTTP requests.
        Use None for the default.
    :param bool verify_ssl: Verify the SSL certificate to prevent
        traffic interception attacks. Defaults to True.

    :rtype: generator of str
    :return: Generator (iterator) that yields found URLs.
        If the stop parameter is None the iterator will loop forever.
    """
    # Set of hashes for the results found.
    # This is used to avoid repeated results.
    hashes = []
    if path_dataset:
        with open(path_dataset, 'r') as dataset:
            data = dataset.readlines()
            if data:
                for line in data:
                    hashes.append(line.split(',')[0])

    # Count the number of links yielded.
    count = 0

    # Prepare the search string.
    if filetype:
        query = quote_plus(f'filetype:{filetype} {query}')
    else:
        query = quote_plus(query)

    # If no extra_params is given, create an empty dictionary.
    # We should avoid using an empty dictionary as a default value
    # in a function parameter in Python.
    if not extra_params:
        extra_params = {}

    # Check extra_params for overlapping.
    for builtin_param in url_parameters:
        if builtin_param in extra_params.keys():
            raise ValueError(
                'GET parameter "%s" is overlapping with \
                the built-in GET parameter',
                builtin_param
            )

    # Grab the cookie from the home page.
    get_page(url_home % vars(), user_agent, verify_ssl)

    # Prepare the URL of the first request.
    if start:
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()
    else:
        if num == 10:
            url = url_search % vars()
        else:
            url = url_search_num % vars()

    # Loop until we reach the maximum result, if any (otherwise, loop forever).
    while not stop or count < stop:

        # Remeber last count to detect the end of results.
        last_count = count

        # Append extra GET parameters to the URL.
        # This is done on every iteration because we're
        # rebuilding the entire URL at the end of this loop.
        for k, v in extra_params.items():
            k = quote_plus(k)
            v = quote_plus(v)
            url = url + ('&%s=%s' % (k, v))

        # Sleep between requests.
        # Keeps Google from banning you for making too many requests.
        time.sleep(pause)

        # Request the Google Search results page.
        html = get_page(url, user_agent, verify_ssl)

        # Parse the response and get every anchored URL.
        if is_bs4:
            soup = BeautifulSoup(html, 'html.parser')
        else:
            soup = BeautifulSoup(html)
        try:
            anchors = soup.find(id='search').findAll('a')
            # Sometimes (depending on the User-agent) there is
            # no id "search" in html response...
        except AttributeError:
            # Remove links of the top bar.
            gbar = soup.find(id='gbar')
            if gbar:
                gbar.clear()
            anchors = soup.findAll('a')
        file_counter = len(hashes)+1
        # Process every anchored URL.
        for a in anchors:

            # Get the URL from the anchor tag.
            try:
                link = a['href']
            except KeyError:
                continue

            # Filter invalid links and links pointing to Google itself.
            link = filter_result(link)
            if not link:
                continue

            # Discard repeated results.
            h = hashlib.sha256(bytes(link, "utf-8")).hexdigest()
            if h in hashes:
                continue
            hashes.append(h)
            extracted_title = extract_title([str(x) for x in a.contents])
            extracted_title = ''.join(extracted_title)
            
            filename = 'dataset.csv'
            if path_dataset:
                filename = path_dataset
            with open(filename, 'a') as dataset:
                if filetype:
                    dataset.write(f'{h},{extracted_title},{link},File N-{file_counter}\n')
                    file_counter += 1
                else:
                    dataset.write(f'{h},{extracted_title},{link}\n')
            # Yield the result.
            yield link, extracted_title

            # Increase the results counter.
            # If we reached the limit, stop.
            count += 1
            if stop and count >= stop:
                return

        # End if there are no more results.
        if last_count == count:
            break

        # Prepare the URL for the next request.
        start += num
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()

def download_files(dataset, download_path):
    urls = []
    filenames = []
    with open(dataset, 'r') as dataset_file:
        data = dataset_file.readlines()
        for line in data:
            urls.append(line.split(',')[2])
            filenames.append(line.split(',')[3][:-1])

    for url, filename in zip(urls, filenames):
        response = requests.get(url)
        with open(f'{download_path}/{filename}.pdf', "wb") as file:
                file.write(response.content)