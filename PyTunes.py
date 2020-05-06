import sys
from PyQt5.QtGui import QPalette, QColor
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl, QDirIterator, Qt
from PyQt5.QtWidgets import QApplication, QListWidget, QWidget, QMainWindow, QPushButton, QFileDialog, QAction, QHBoxLayout, QVBoxLayout, QSlider, QLineEdit ,QLabel, QListView, QFrame
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
import vlc
import pafy
from youtube_search import YoutubeSearch 
import json
from recognition import recognize
from text2speech import t2s

def select_by_speech():
    t2i_en = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine':9, 'ten':10 }
    t2i_vn = {'một': 1, 'hai': 2, 'ba': 3, 'bốn': 4, 'năm': 5, 'sáu': 6, 'bẩy': 7, 'tám': 8, 'chín':9, 'mười':10 }
    t2i_vn2 = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9':9, '10':10 }
    match = False
    while match != True:
        t2s('select song')
        text = recognize()
        if text in t2i_en.keys() or text in t2i_vn.keys() or t2i_vn2.keys():
            if text in t2i_en.keys():
                number = t2i_en[text]
                match = True
            elif text in t2i_vn.keys():
                number = t2i_vn[text]
                match = True
            elif text in t2i_vn2.keys():
                number = t2i_vn2[text]
                match = True
    return int(number) - 1

def listen_command():
    t2i_en = {'play':0, 'next':1, 'stop':2, 'search':3,'exit':8, 'up':4, 'down':5, 'yes':6, 'no':7}
    t2i_vn = {'phát':0, 'bài tiếp theo':1, 'dừng lại':2, 'tìm kiếm':3,'thoát':8, 'tăng âm lượng':4, 'giảm âm lượng':5 , 'có':6, 'không':7}
    match = False
    while match != True:
        t2s('speech command')
        text = recognize()
        if text in t2i_en or text in t2i_vn:
            if text in t2i_en:
                command = t2i_en[text]
                match = True
            else:
                command = t2i_vn[text]
                match = True
    return int(command)

def getVoiceKeyWord():
    #t2s('')
    match = False
    # key = ''
    while match!= True:
        key = recognize('keyword')
        t2s('you are want to find: {}'.format(key))
        cf = recognize('yes or no')
        if cf in ['yes','ok','oke','đúng','phải','đồng ý']:
            t2s('ok')
            match = True
        else:
            t2s('oh sorry! please speech keyword again')
    return key
        
def getLinkAudio(link):
    print('start get audio')
    video = pafy.new(link)
    best = video.getbestaudio()
    url = best.url
    print('done get audio')
    return url

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()
        #self.media = instance.media_new(playurl)
        #self.mediaplayer.set_media(self.media)
        
        self.title = 'Player'
        self.left = 500
        self.top = 200
        self.width = 600
        self.height = 400
        self.color = 0  # 0- toggle to dark 1- toggle to light
        self.initUI()

    def initUI(self):

        menubar = self.menuBar()
        windowmenu = menubar.addMenu('Theme')
        themeAct = QAction('Toggle light/dark theme', self)
        themeAct.setShortcut('Ctrl+T')
        windowmenu.addAction(themeAct)
        themeAct.triggered.connect(self.toggleColors)
        self.addControls()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.toggleColors()
        self.show()

    def addControls(self):
        wid = QWidget(self)
        self.setCentralWidget(wid)
        # Status
        self.status = QLabel()
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setText('Status')
        # Search
        self.searchInput = QLineEdit()
        self.searchBtn = QPushButton('Search')
        self.voicesearchBtn = QPushButton('Voice Search')
        self.searchBtn.clicked.connect(self.Search)
        self.voicesearchBtn.clicked.connect(self.VoiceSearch)
        #self.listSong = QListView()
        self.listAudio = QListWidget()
        
        self.volumeslider = QSlider(Qt.Horizontal, self)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.setToolTip("Volume")
        # self.volumeslabel = QLabel(alignment=QtCore.Qt.AlignCenter)
        
        self.playbutton = QPushButton('Play')  # play button
        self.stopbutton = QPushButton('Stop')  # Stop button
        self.nextbutton = QPushButton('Next')  # Next button
        self.command = QPushButton('Start Voice Command')  # Next button
        # Add button layouts
        mainLayout = QVBoxLayout()
        # search = QHBoxLayout()
        controls = QHBoxLayout()
        # Add search
        # search.addWidget(searchBtn)
        # search.addWidget(voicesearchBtn)
        # Add buttons to song controls layout
        controls.addWidget(self.playbutton)
        controls.addWidget(self.stopbutton)
        controls.addWidget(self.nextbutton)
        # Add to vertical layout
        mainLayout.addWidget(self.status)
        mainLayout.addWidget(self.searchInput)
        mainLayout.addWidget(self.searchBtn)
        mainLayout.addWidget(self.voicesearchBtn)
        mainLayout.addWidget(self.listAudio)
        mainLayout.addLayout(controls)
        #mainLayout.addLayout(self.volumeslabel)
        mainLayout.addWidget(self.command)
        mainLayout.addWidget(self.volumeslider)
        wid.setLayout(mainLayout)
        # Connect each signal to their appropriate function
        self.playbutton.clicked.connect(self.PlayPause)
        self.stopbutton.clicked.connect(self.Stop)
        self.nextbutton.clicked.connect(self.Next)
        self.command.clicked.connect(self.excCommand)
        self.volumeslider.valueChanged.connect(self.setVolume)
        # self.volumeslider.valueChanged.connect(self.volumeslabel.setNum)
        self.statusBar()

    def setVolume(self, Volume):
        self.mediaplayer.audio_set_volume(Volume)

    def PlayPause(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Play")
        else:
            self.mediaplayer.play()
            self.playbutton.setText("Pause")
            
    def Pause(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Play")

    def Stop(self):
        self.mediaplayer.stop()
        self.playbutton.setText("Play")
    
    def setMediaPlayerUrl(self, url):
        self.media = self.instance.media_new(url)
        self.mediaplayer.set_media(self.media)
        
    def Search(self):
        self.listAudio.clear()
        #del self.listAudio_text
        if self.searchInput.text() != '':
            print('keyword:', self.searchInput.text())
            print('searching...')
            #self.status.setText('search: {}'.format(self.searchInput.text()))
            #self.status.setText('Searching...')
            results = YoutubeSearch(self.searchInput.text(), max_results=10).to_json()
            results = json.loads(results)
            results = results["videos"]
            # self.idx_audio = 0
            self.listAudio_text = {}
            for i, item in enumerate(results):
                itemtitle = item['title']
                itemlink = 'https://www.youtube.com' + item['link']
                self.listAudio.insertItem(i+1, str(i+1) + ': ' + itemtitle + '#link#' + itemlink)
                self.listAudio_text[itemtitle] = itemlink
                self.status.setText('Result for: "{}"'.format(self.searchInput.text()))
            
            t2s('seach done, select song to play')
            self.idx_audio = select_by_speech()
            self.selectAndPlaySongByIndex()
        else:
            print('enter keyword to search!!!')
            self.status.setText('Enter keyword or voice search')
            t2s('enter keyword or voice search')
        #print(results)
    
    def VoiceSearch(self):
        print('start voice search')
        t2s('Start Voice Search')
        
        self.status.setText('Speech keyword')
        keyword = getVoiceKeyWord() # có xác nhận key
        #t2s('')
        # keyword = recognize('keyword')# không cần xác nhận
        t2s('search for {}'.format(keyword))
        self.status.setText('Keyword: "{}"'.format(keyword))
        self.searchInput.setText(keyword)
        self.Search()
        # self.selectAndPlaySongByIndex()
        
        
    def selectAndPlaySongByIndex(self):
        #print(self.idx_audio)
        title_audio = list(self.listAudio_text.keys())[self.idx_audio]
        link_audio = list(self.listAudio_text.values())[self.idx_audio]
        #self.cur_title = title_audio
        link_audio = getLinkAudio(link_audio)
        
        t2s('Start play: {}, {}'.format(self.idx_audio+1, title_audio))
        print('Start play: {}, {}'.format(self.idx_audio+1, title_audio))

        self.setMediaPlayerUrl(link_audio)
        self.PlayPause()
        self.status.setText('Playing: {}'.format(title_audio))
        
    def Next(self):
        self.Pause()
        if self.idx_audio == 9:
            self.idx_audio = 0
        else:
            self.idx_audio += 1
        self.selectAndPlaySongByIndex()
    
    def VoiceNext(self):
        print('Next song')
        t2s('Next song')
        self.Next()
        
    def excCommand(self):
        self.Pause()
        t2s('Speech command')
        print('Speech command')
        command = listen_command()
        if command == 0:
            self.PlayPause()
        elif command == 1:
            self.VoiceNext()
        elif command == 2:
            self.Stop()
        elif command == 3:
            self.VoiceSearch()
        elif command == 4:
            old_vl =  self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
            if old_vl == 100:
                self.volumeslider.setValue(old_vl)
            else:
                self.volumeslider.setValue(old_vl + 10)
            #self.setVolume()
        elif command == 5:
            old_vl =  self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
            if old_vl == 0:
                self.volumeslider.setValue(old_vl)
            else:
                self.volumeslider.setValue(old_vl - 10)
            #self.setVolume()
        elif command == 8:
            print('exited')
            t2s('you are sure exit')
            t2s('yes or no')
            cf_exit = recognize('yes or no')
            if cf_exit == 'yes':
                exit()
            
    def toggleColors(self):
        """ Fusion dark palette from https://gist.github.com/QuantumCD/6245215. Modified by me and J.J. """
        app.setStyle("Fusion")
        palette = QPalette()
        if self.color == 0:
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(235, 101, 54))
            palette.setColor(QPalette.Highlight, QColor(235, 101, 54))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(palette)
            self.color = 1
        elif self.color == 1:
            palette.setColor(QPalette.Window, Qt.white)
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, QColor(240, 240, 240))
            palette.setColor(QPalette.AlternateBase, Qt.white)
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, Qt.white)
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(66, 155, 248))
            palette.setColor(QPalette.Highlight, QColor(66, 155, 248))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(palette)
            self.color = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
