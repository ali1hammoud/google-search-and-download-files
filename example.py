from googles import search, download_files

#query to search
query = 'multi agents systems multi-wheeled robots'

for url, content in search(query, tld="com", tbs='0', safe='off',
                        start=0, country='',user_agent=None, verify_ssl=True, 
                        num=100, lang='en', stop=1, pause=1, filetype='pdf', 
                        path_dataset= 'dataset.csv', extra_params={'filter': '0'}):
    print(url,content)

download_files('dataset.csv', './files')