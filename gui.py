import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import threading
from googles import search, download_files

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Google Search GUI")
        self.master.geometry("600x500")
        self.path_dataset = None
        self.downloadpath = None
        # query
        self.query_label = tk.Label(master, text="Query")
        self.query_label.grid(row=0, column=0, padx=10, pady=10)
        self.query_entry = tk.Entry(master)
        self.query_entry.grid(row=0, column=1, padx=10, pady=10)

        # start
        self.start_label = tk.Label(master, text="start")
        self.start_label.grid(row=1, column=0, padx=10, pady=10)
        self.start_entry = tk.Entry(master)
        self.start_entry.insert(0, "0")
        self.start_entry.grid(row=1, column=1, padx=10, pady=10)

        # tld
        self.tld_label = tk.Label(master, text="tld")
        self.tld_label.grid(row=2, column=0, padx=10, pady=10)
        self.tld_entry = tk.Entry(master)
        self.tld_entry.insert(0, "com")
        self.tld_entry.grid(row=2, column=1, padx=10, pady=10)

        # tbs
        self.tbs_label = tk.Label(master, text="tbs")
        self.tbs_label.grid(row=3, column=0, padx=10, pady=10)
        self.tbs_entry = tk.Entry(master)
        self.tbs_entry.insert(0, "0")
        self.tbs_entry.grid(row=3, column=1, padx=10, pady=10)

        # safe
        self.safe_label = tk.Label(master, text="safe")
        self.safe_label.grid(row=4, column=0, padx=10, pady=10)
        self.safe_entry = tk.Entry(master)
        self.safe_entry.insert(0, "off")
        self.safe_entry.grid(row=4, column=1, padx=10, pady=10)
        
        # country
        self.country_label = tk.Label(master, text="country")
        self.country_label.grid(row=5, column=0, padx=10, pady=10)
        self.country_entry = tk.Entry(master)
        self.country_entry.grid(row=5, column=1, padx=10, pady=10)

        # user_agent
        self.user_agent_label = tk.Label(master, text="user_agent")
        self.user_agent_label.grid(row=6, column=0, padx=10, pady=10)
        self.user_agent_entry = tk.Entry(master)
        #self.user_agent_entry.insert(0, 'user_agent')
        self.user_agent_entry.grid(row=6, column=1, padx=10, pady=10)
        
        # verify_ssl
        self.verify_ssl_label = tk.Label(master, text="verify_ssl")
        self.verify_ssl_label.grid(row=7, column=0, padx=10, pady=10)
        self.verify_ssl_var = tk.IntVar()
        self.verify_ssl_var.set(True)
        self.verify_ssl_checkbox = tk.Checkbutton(
            master, variable=self.verify_ssl_var, onvalue=True, offvalue=False
        )
        self.verify_ssl_checkbox.grid(row=7, column=1, padx=10, pady=10)
        
        # num
        self.num_label = tk.Label(master, text="number of results")
        self.num_label.grid(row=0, column=3, padx=10, pady=10)
        self.num_entry = tk.Entry(master)
        self.num_entry.insert(0, 100)
        self.num_entry.grid(row=0, column=4, padx=10, pady=10)
        
        # lang
        self.lang_label = tk.Label(master, text="language")
        self.lang_label.grid(row=1, column=3, padx=10, pady=10)
        self.lang_entry = tk.Entry(master)
        self.lang_entry.insert(0, 'en')
        self.lang_entry.grid(row=1, column=4, padx=10, pady=10)
        
        # stop
        self.stop_label = tk.Label(master, text="stop")
        self.stop_label.grid(row=2, column=3, padx=10, pady=10)
        self.stop_entry = tk.Entry(master)
        self.stop_entry.insert(0, -1)
        self.stop_entry.grid(row=2, column=4, padx=10, pady=10)
        
        # pause
        self.pause_label = tk.Label(master, text="pause")
        self.pause_label.grid(row=3, column=3, padx=10, pady=10)
        self.pause_entry = tk.Entry(master)
        self.pause_entry.insert(0, 1)
        self.pause_entry.grid(row=3, column=4, padx=10, pady=10)
        
        # filetype
        self.filetype_label = tk.Label(master, text="files type")
        self.filetype_label.grid(row=4, column=3, padx=10, pady=10)
        self.filetype_entry = tk.Entry(master)
        self.filetype_entry.insert(0, "pdf")
        self.filetype_entry.grid(row=4, column=4, padx=10, pady=10)

        # path_dataset
        self.path_dataset_label = tk.Label(master, text="path to dataset")
        self.path_dataset_label.grid(row=5, column=3, padx=10, pady=10)
        self.path_dataset_button = tk.Button(master, text="Choose path", command=self.choose_path_dataset)
        self.path_dataset_button.grid(row=5, column=4, padx=10, pady=10)
        self.chosen_path_dataset_label = tk.Label(master, text="")
        self.chosen_path_dataset_label.grid(row=5, column=5, padx=10, pady=10)

        # downloadpath
        self.downloadpath_label = tk.Label(master, text="path to download folder")
        self.downloadpath_label.grid(row=6, column=3, padx=10, pady=10)
        self.downloadpath_button = tk.Button(master, text="Choose path", command=self.choose_downloadpath)
        self.downloadpath_button.grid(row=6, column=4, padx=10, pady=10)
        self.chosen_downloadpath_label = tk.Label(master, text="")
        self.chosen_downloadpath_label.grid(row=6, column=5, padx=10, pady=10)
        
        # extra_params
        self.extra_params_label = tk.Label(master, text="extra parameters")
        self.extra_params_label.grid(row=7, column=3, padx=10, pady=10)
        self.extra_params_entry = tk.Entry(master)
        self.extra_params_entry.insert(0, "filter = 0")
        self.extra_params_entry.grid(row=7, column=4, padx=10, pady=10)
        
        # search button
        self.search_button = tk.Button(master, text="Search", command=self.start_search)
        self.search_button.grid(row=8, column=0, columnspan=1, padx=10, pady=10)
        
        # download button
        self.download_button = tk.Button(master, text="Download", command=self.start_download)
        self.download_button.grid(row=9, column=0, columnspan=1, padx=10, pady=10)

        # extra_params
        self.info_label = tk.Label(master, text="0 searched link")
        self.info_label.grid(row=11, column=0, padx=10, pady=10)

    def choose_path_dataset(self):
        self.path_dataset = filedialog.askopenfilename()
        self.chosen_path_dataset_label.config(text=self.path_dataset)

    def choose_downloadpath(self):
        self.downloadpath = filedialog.askdirectory()
        self.chosen_downloadpath_label.config(text=self.downloadpath)

    def start_search(self):
        query = self.query_entry.get()
        tld = self.tld_entry.get() or "com"
        tbs = self.tbs_entry.get() or '0'
        safe = self.safe_entry.get() or 'off'
        start = int(self.start_entry.get()) or 0
        country = self.country_entry.get() or ''
        user_agent = self.user_agent_entry.get() or None
        verify_ssl = self.verify_ssl_var.get() or True
        num = int(self.num_entry.get()) or 100
        lang = self.lang_entry.get() or 'en'
        if int(self.stop_entry.get()) == -1:
            stop = None
        else:
            stop = int(self.stop_entry.get())
        pause = int(self.pause_entry.get()) or 1
        filetype = self.filetype_entry.get() or None
        path_dataset = self.path_dataset
        extra_params = dict(subString.split("=") for subString in self.extra_params_entry.get().split(";")) or {'filter': '0'}
        
        # start the thread for search function
        thread = threading.Thread(target=self.search_thread, args=(query, tld, 
            tbs, safe, start, country, user_agent, verify_ssl, num, lang, stop, pause, 
            filetype, path_dataset, extra_params))
        thread.start()


    def search_thread(self, query, tld, tbs, safe, start, country, 
                      user_agent, verify_ssl, num, lang, stop, pause, filetype, 
                      path_dataset, extra_params):
        files_count = 0
        for _ in search(query=query, tld=tld, tbs=tbs, safe=safe, start=start, country=country, 
                        user_agent=user_agent, verify_ssl=verify_ssl, num=num, 
                        lang=lang, stop=stop, pause=pause, filetype=filetype, 
                        path_dataset = path_dataset, extra_params=extra_params):
            files_count += 1
            self.info_label.config(text=f'{files_count} searched link')
            self.master.update()
    
    def start_download(self):
        dataset = self.path_dataset
        path_download = self.downloadpath

        downloadthread = threading.Thread(target=self.download_thread, args=(dataset, path_download))
        downloadthread.start()

    def download_thread(self, dataset, path_download):
        download_files(dataset, path_download)

        
root = tk.Tk()
app = GUI(root)
root.mainloop()
