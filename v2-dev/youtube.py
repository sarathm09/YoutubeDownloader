import os, tkMessageBox, pafy, time, pickle, urllib
from ttk import Progressbar, Style
from Tkinter import *


class YoutubeScript:
    def __init__(self):
        self.totDownloadSize = 0
        self.completedSize = 0
        self.saveData = {
            "url": "",
            "title": "",
            "selected": [],
            "completed": [],
            "savetype": ""
        }

    def initUi(self):

        self.ipGui = Tk()
        self.ipGui.wm_title("YtD by T90")
        self.ipGui.wm_minsize(700, 150)

        self.titleFrame = Frame(self.ipGui, height=100, width=500, relief=RAISED, bg="#555")
        self.titleFrame.pack(fill=BOTH)
        titleLabel = Label(self.titleFrame, text="Youtube Downloader Script", bg="#555", fg="#fff", font=("Arial", 16))
        subTitleLabel = Label(self.titleFrame, text="By T90", bg="#555", fg="#ddd")
        titleLabel.pack(fill=X, side=TOP, pady=3)
        subTitleLabel.pack(fill=X, side=BOTTOM)

        self.ipFrame = Frame(self.ipGui, height=200, width=500, relief=RAISED, bg="#bbb")
        self.ipFrame.pack(fill=BOTH, padx=3, pady=3)
        self.urlBox = Entry(self.ipFrame, relief=RAISED, fg="#777")
        self.urlBox.focus()
        self.urlBtn = Button(self.ipFrame, text="Download", height=2, bg="#777", fg="#eee", command=self.startDownload)
        self.urlBox.pack(fill=BOTH, padx=20, pady=10)
        self.urlBtn.pack(fill=BOTH, padx=50, pady=10)

        # self.urlBox.insert(0, "https://www.youtube.com/playlist?list=PLYvPGplh5--N1zwtg_5-z3kVW9U92FUc2")

        self.selectVidsFrame = Frame(self.ipGui, bg="#bbb")

        selectLabel = Label(self.selectVidsFrame, text="Select videos to be downloaded and click on Start.", bg="#bbb")
        self.vidsListBox = Listbox(self.selectVidsFrame, bg="#bbb", relief=RAISED, selectmode=EXTENDED,
                                   selectbackground="#888", selectforeground="#fff", borderwidth=1,
                                   highlightthickness=0, activestyle="none")
        self.selectVidsBtn = Button(self.selectVidsFrame, text="Start", height=2, bg="#777", fg="#eee",
                                    command=self.selectVids)
        selectLabel.pack(fill=X, padx=3, pady=3)
        self.vidsListBox.pack(fill=X, padx=10, pady=10)
        self.selectVidsBtn.pack(fill=X, padx=50, pady=10)

        self.progFrame = Frame(self.ipGui, height=200, width=500, relief=SUNKEN, bg="#bbb")

        self.titleInProgFrame = Frame(self.progFrame, bg="#bbb")
        self.status1InProgFrame = Frame(self.progFrame, bg="#bbb")
        self.status2InProgFrame = Frame(self.progFrame, bg="#bbb")
        self.progInProgFrame = Frame(self.progFrame, bg="#bbb")

        self.vidTitleLabel = Label(self.titleInProgFrame, text="Fetching videos, please wait...", bg="#bbb", fg="#333")

        self.thisVidCompletedTitle = Label(self.status1InProgFrame, text="Completed:", bg="#bbb", fg="#333",
                                           justify="right")
        self.thisVidCompletedText = Label(self.status1InProgFrame, text="0 MB", bg="#bbb", fg="#333", justify="left")
        self.thisVidSizeTitle = Label(self.status1InProgFrame, text="Size:", bg="#bbb", fg="#333", justify="right")
        self.thisVidSizeText = Label(self.status1InProgFrame, text="calculating", bg="#bbb", fg="#333", justify="left")
        self.totVidCompletedTitle = Label(self.status1InProgFrame, text="Total downloaded:", bg="#bbb", fg="#333",
                                          justify="right")
        self.totVidCompletedText = Label(self.status1InProgFrame, text="0 MB", bg="#bbb", fg="#333", justify="left")
        self.totVidSizeTitle = Label(self.status1InProgFrame, text="Total Size:", bg="#bbb", fg="#333", justify="right")
        self.totVidSizeText = Label(self.status1InProgFrame, text="calculating", bg="#bbb", fg="#333", justify="left")
        self.curSpeedTitle = Label(self.status2InProgFrame, text="Speed:", bg="#bbb", fg="#333", justify="right")
        self.curSpeedText = Label(self.status2InProgFrame, text="0 mbps", bg="#bbb", fg="#333", justify="left")
        self.vidLengthTitle = Label(self.status2InProgFrame, text="Video duration:", bg="#bbb", fg="#333",
                                    justify="right")
        self.vidLengthText = Label(self.status2InProgFrame, text="calculating", bg="#bbb", fg="#333", justify="left")
        self.etaTitle = Label(self.status2InProgFrame, text="ETA:", bg="#bbb", fg="#333", justify="right")
        self.etaText = Label(self.status2InProgFrame, text="calculating", bg="#bbb", fg="#333", justify="left")
        self.timeTakenTitle = Label(self.status2InProgFrame, text="Time Taken:", bg="#bbb", fg="#333", justify="right")
        self.timeTakenText = Label(self.status2InProgFrame, text="calculating", bg="#bbb", fg="#333", justify="left")

        self.totProgLabel = Label(self.progInProgFrame, text="Total Progress", bg="#bbb", fg="#333")
        s = Style()
        s.theme_use('alt')
        s.configure("grey.Horizontal.TProgressbar", foreground='#eee', background='#888')
        self.indiProg = Progressbar(self.progInProgFrame, style="grey.Horizontal.TProgressbar", orient='horizontal',
                                    mode='determinate', maximum=100)
        self.totProg = Progressbar(self.progInProgFrame, style="grey.Horizontal.TProgressbar", orient='horizontal',
                                   mode='determinate', maximum=100)
        self.openDownloadFolderBtn = Button(self.progInProgFrame, text="Open Download Location", height=2, bg="#777",
                                            fg="#eee", command=self.openDownloadFolder)

        self.titleInProgFrame.pack(fill=BOTH, expand=1)
        self.status1InProgFrame.pack(fill=BOTH, expand=1)
        self.status2InProgFrame.pack(fill=BOTH, expand=1)
        self.progInProgFrame.pack(fill=BOTH, expand=1)

        self.vidTitleLabel.pack(fill=BOTH, expand=1, padx=50, pady=10, side=TOP)

        self.thisVidCompletedTitle.pack(fill=BOTH, expand=1, side=LEFT)
        self.thisVidCompletedText.pack(fill=BOTH, expand=1, side=LEFT)
        self.thisVidSizeTitle.pack(fill=BOTH, expand=1, side=LEFT)
        self.thisVidSizeText.pack(fill=BOTH, expand=1, side=LEFT)
        self.totVidCompletedTitle.pack(fill=BOTH, expand=1, side=LEFT)
        self.totVidCompletedText.pack(fill=BOTH, expand=1, side=LEFT)
        self.totVidSizeTitle.pack(fill=BOTH, expand=1, side=LEFT)
        self.totVidSizeText.pack(fill=BOTH, expand=1, side=LEFT)

        self.curSpeedTitle.pack(fill=BOTH, expand=1, side=LEFT)
        self.curSpeedText.pack(fill=BOTH, expand=1, side=LEFT)
        self.vidLengthTitle.pack(fill=BOTH, expand=1, side=LEFT)
        self.vidLengthText.pack(fill=BOTH, expand=1, side=LEFT)
        self.etaTitle.pack(fill=BOTH, expand=1, side=LEFT)
        self.etaText.pack(fill=BOTH, expand=1, side=LEFT)
        self.timeTakenTitle.pack(fill=BOTH, expand=1, side=LEFT)
        self.timeTakenText.pack(fill=BOTH, expand=1, side=LEFT)

        self.indiProg.pack(fill=BOTH, expand=1, padx=50, pady=10)
        self.totProgLabel.pack(fill=BOTH, expand=1)
        self.totProg.pack(fill=BOTH, expand=1, padx=50, pady=10)
        self.openDownloadFolderBtn.pack(fill=BOTH, expand=1, padx=90, pady=10)

    def saveData(self, status="auto"):
        self.saveData['url'] = self.url
        self.saveData['title'] = self.pafy['title']
        self.saveData['savetype'] = status
        self.saveData['selected'] = self.selectedIndexList
        self.saveData['completed'] = self.completedVids

        pickle.dump(self.saveData, "saves/saveFile_" + str(int(time.time())))

    def getUrlandStart(self):
        try:
            urllib.urlretrieve("http://youtube.com/favicon.ico", "favicon.ico")
            self.initUi()
            self.ipGui.iconbitmap(r'favicon.ico')
            self.ipGui.mainloop()
        except Exception as e:
            print e.message
            root = Tk()
            root.withdraw()
            tkMessageBox.showerror("Connectivity Issues",
                                   "Connectivity issue detected. "
                                   "Please make sure that you are connected to the Internet and then restart the app.")
            exit(0)

    def startDownload(self):
        if not os.path.exists("downloads"):
            os.mkdir("downloads")
        self.urlBtn.config(text="Loading...")

        self.ipGui.update()
        self.url = self.urlBox.get()
        if "watch" in self.url and "list" in self.url:
            parts = self.url.split("&")
            for part in parts:
                if "list=" in part:
                    self.url = "https://www.youtube.com/playlist?" + part
                    break
        self.ipFrame.pack_forget()
        if "playlist" in self.url:
            self.selectVidsFrame.pack(fill=BOTH, padx=3, pady=3)
            self.vidsListBox.focus()
            self.pafy = pafy.get_playlist(self.url)
            self.ipGui.wm_title(self.pafy['title'])
            self.vidsObjs = []
            i = 0
            for vid in self.pafy['items']:
                self.vidsObjs.append(vid)
                i += 1
                self.vidsListBox.insert(END, str(i) + ". " + vid['playlist_meta']['title'] + " [" + str(
                    round(int(vid['playlist_meta']['length_seconds']) / 60, 2)) + "min]")

    def selectVids(self):
        items = self.vidsListBox.curselection()
        self.selectedIndexList = items
        if len(items) == 0:
            tkMessageBox.showerror("No video selected",
                                   "No videos selected.\nPlease select some videos and press start. "
                                   "Select multiple videos using Shift/Ctrl.")
            return
        self.selectedList = []
        for item in items:
            self.selectedList.append(self.vidsObjs[item])
        self.selectVidsFrame.pack_forget()
        self.progFrame.pack(fill=BOTH, padx=3, pady=3)
        self.selectVidsBtn.config(text="Fetching videos, please wait...")
        self.ipGui.update()
        self.downloadPlaylist()

    def downloadPlaylist(self):
        self.startTime = time.time()
        self.completedVids = []
        if not os.path.exists("downloads/playlists"):
            os.mkdir("downloads/playlists")

        safePlaylistTitle = self.winStringFormat(self.pafy['title'])

        if not os.path.exists("downloads/playlists/" + safePlaylistTitle):
            os.mkdir("downloads/playlists/" + safePlaylistTitle)

        self.dwnldgVidNum = -1
        for vid in self.selectedList:
            self.totDownloadSize += vid['pafy'].getbest().get_filesize()
        self.totProgLabel.config(
                text="Total Progress")
        for vid in self.selectedList:
            self.dwnldgVidNum += 1
            best = vid['pafy'].getbest()
            index = self.vidsObjs.index(vid)

            safeTitle = self.winStringFormat(vid['pafy'].title + "." + best.extension)
            self.vidDuration = vid['pafy'].duration
            self.vidTitleLabel.config(text=vid['pafy'].title)
            best.download(quiet=True, filepath="downloads/playlists/" + safePlaylistTitle + "/" + str(
                index + 1) + ". " + safeTitle, callback=self.updateProg)
            self.totProgLabel.config(
                text="Completed " + str(self.dwnldgVidNum) + " of " + str(len(self.selectedList)) + " videos.")
            self.completedSize += best.get_filesize()
            self.completedVids.append(index)
        tkMessageBox.showinfo("Completed", "Successfully completed download.")
        self.openDownloadFolder()

    def updateProg(self, total, recvd, ratio, rate, eta):

        self.timeNw = time.time()
        timeDiff = self.timeNw - self.startTime
        timeTxt = ""
        if (timeDiff / 3600) > 1:
            timeTxt += str(int(timeDiff / 3600)) + " : "
            timeDiff %= 3600
        if (timeDiff / 60) > 1:
            timeTxt += str(int(timeDiff / 60)) + " : "
            timeDiff %= 60
        timeTxt += str(int(timeDiff))

        self.thisVidCompletedText.config(text=str(round((recvd / 1024) / 1024, 2)) + " MB")
        self.thisVidSizeText.config(text=str(round(((total / 1024) / 1024), 2)) + " MB")
        self.totVidCompletedText.config(text=str(round((((self.completedSize + recvd) / 1024) / 1024), 2)) + " MB")
        self.totVidSizeText.config(text=str(round(((self.totDownloadSize / 1024) / 1024), 2)) + " MB")

        self.curSpeedText.config(text=str(round(rate / 1024, 2)) + " mbps")
        self.vidLengthText.config(text=self.vidDuration)
        self.etaText.config(text=str(round(eta, 1)) + " secs")
        self.timeTakenText.config(text=timeTxt)

        # statusText = "This video: " + str(round((recvd / 1024) / 1024, 2)) + " MB/" + str(
        #     round(((total / 1024) / 1024), 2)) + " MB\tTotal: " + str(
        #     round((((self.completedSize + recvd) / 1024) / 1024), 2)) + " MB/" + str(round(((self.totDownloadSize / 1024) / 1024), 2)) + " MB"
        # self.indiStat.config(text=statusText)
        # statusText = "Ratio: " + str(round(rate / 1024, 2)) + " mbps\t\tETA: " + str(round(eta, 1)) + " secs"
        # self.indiProgLabel.config(text=statusText)
        self.indiProg.config(value=ratio * 100)
        self.totProg.config(value=(
            (float(self.dwnldgVidNum) / len(self.selectedList)) * 100 + ((ratio * 100) / len(self.selectedList))))
        self.ipGui.update()

    def winStringFormat(self, name):
        return name.replace("|", " ").replace(":", " ").replace("/", " ").replace("\\", " ").replace("$", " ").replace(
            "#", " ").replace("@", " ").replace(";", " ").replace("\"", " ").replace("'", " ").replace("?", " ")

    def openDownloadFolder(self):
        safePlaylistTitle = self.winStringFormat(self.pafy['title'])
        os.system('explorer.exe "' + os.path.dirname(
            os.path.abspath(__file__)) + '\\downloads\\playlists\\' + safePlaylistTitle + '"')


if __name__ == '__main__':
    ys = YoutubeScript()
    ys.getUrlandStart()

