import argparse
from googles import search, download_files

# Define the command-line arguments using argparse
parser = argparse.ArgumentParser(description='Search and download files using Google Search')
parser.add_argument('query', type=str, help='Query string. Must NOT be URL-encoded.')
parser.add_argument('--tld', type=str, default='com', help='Top-level domain.')
parser.add_argument('--tbs', type=str, default='0', help='Time limits (i.e "qdr:h" => last hour, "qdr:d" => last 24 hours, "qdr:m" => last month).')
parser.add_argument('--safe', type=str, default='off', help='Safe search.')
parser.add_argument('--start', type=int, default=0, help='First result to retrieve.')
parser.add_argument('--country', type=str, default='', help='Country or region to focus the search on. Similar to changing the TLD, but does not yield exactly the same results.')
parser.add_argument('--user_agent', type=str, default=None, help='User agent for the HTTP requests. Use None for the default.')
parser.add_argument('--verify_ssl', type=bool, default=True, help='Verify the SSL certificate to prevent traffic interception attacks. Defaults to True.')
parser.add_argument('--num', type=int, default=100, help='Number of results per page.')
parser.add_argument('--lang', type=str, default='en', help='Language.')
parser.add_argument('--stop', type=int, default=None, help='Last result to retrieve. Use None to keep searching forever.')
parser.add_argument('--pause', type=float, default=1, help='Lapse to wait between HTTP requests. A lapse too long will make the search slow, but a lapse too short may cause Google to block your IP.')
parser.add_argument('--filetype', type=str, default=None, help='File type to search.')
parser.add_argument('--path_dataset', type=str, default=None, help='Path to open/save the dataset')
parser.add_argument('--extra_params', type=dict, default={'filter': '0'}, help='A dictionary of extra HTTP GET parameters, which must be URL-encoded. For example, if you don\'t want Google to filter similar results, you can set the extra_params to {\'filter\': \'0\'}, which will append \'&filter=0\' to every query.')

# Parse the arguments
args = parser.parse_args()

# Use the parsed arguments in the search and download_files functions
for url, content in search(args.query, tld=args.tld, tbs=args.tbs, safe=args.safe,
                           start=args.start, country=args.country, user_agent=args.user_agent, verify_ssl=args.verify_ssl, 
                           num=args.num, lang=args.lang, stop=args.stop, pause=args.pause, filetype=args.filetype, path_dataset=args.path_dataset, extra_params=args.extra_params):
    print(url,content)

if args.path_dataset and args.filetype:
    download_files(args.path_dataset, './files')
