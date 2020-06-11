import sys
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl, QDirIterator, Qt
from PyQt5.QtWidgets import QApplication, QListWidget, QWidget, QMainWindow, QPushButton, QFileDialog, QAction, QHBoxLayout, QVBoxLayout, QSlider, QLineEdit ,QLabel, QListView, QFrame, QShortcut
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
import vlc
import pafy
from youtube_search import YoutubeSearch 
import json
from recognition import recognize
from text2speech import t2s
from time import sleep
from next_keyword import next_keyword

def select_by_speech():
    t2i_en = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine':9, 'ten':10 }
    t2i_en2 = {'number one': 1, 'number two': 2, 'number three': 3, 'number four': 4, 'number five': 5, 'number six': 6, 'number seven': 7, 'number eight': 8, 'number nine':9, 'number ten':10 }
    t2i_vn = {'một': 1, 'hai': 2, 'ba': 3, 'bốn': 4, 'năm': 5, 'sáu': 6, 'bẩy': 7, 'tám': 8, 'chín':9, 'mười':10 }
    t2i_vn2 = {'số 1': 1, 'số 2': 2, 'số 3': 3, 'số 4': 4, 'số 5': 5, 'số 6': 6, 'số 7': 7, 'số 8': 8, 'số 9':9, 'số 10':10 }
    t2i = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9':9, '10':10 }
    match = False
    while match != True:
        t2s('select song')
        text = recognize()
        if text in t2i_en.keys() or text in t2i_en2.keys() or text in t2i_vn.keys() or t2i_vn2.keys() or text in t2i.keys():
            if text in t2i_en.keys():
                number = t2i_en[text]
                match = True
            elif text in t2i_en2.keys():
                number = t2i_en2[text]
                match = True
            elif text in t2i_vn.keys():
                number = t2i_vn[text]
                match = True
            elif text in t2i_vn2.keys():
                number = t2i_vn2[text]
                match = True
            elif text in t2i.keys():
                number = t2i[text]
                match = True
    return int(number) - 1

def waitForSpeech():
    t2s('I am listing')
    #print('I am listing')


def listen_command():
    t2i_en = {'play':0, 'next':1, 'stop':2, 'search':3, 'select song':4, 'exit':5}
    t2i_vn = {'phát':0, 'tiếp tục':0, 'tiếp theo':1, 'kế tiếp':1, 'dừng lại':2, 'tìm kiếm':3, 'chọn bài hát':4, 'chọn bài':4, 'thoát':5, 'thoát chương trình':5}
    match = False
    while match != True:
        t2s('speech command')
        text = recognize()
        if text in t2i_en.keys() or text in t2i_vn.keys():
            if text in t2i_en.keys():
                command = t2i_en[text]
                match = True
            elif text in t2i_vn.keys():
                command = t2i_vn[text]
                match = True
    return int(command)

def getVoiceKeyWord():
    match = False
    while match!= True:
        key = recognize('keyword')
        t2s('you are want to find: {}'.format(key))
        cf = recognize('YES or OK to confirm and NO to try again')
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
        
        self.title = 'Player'
        self.left = 500
        self.top = 200
        self.width = 600
        self.height = 400
        self.color = 0  # 0- toggle to dark 1- toggle to light
        self.initUI()

    def initUI(self):

        #menubar = self.menuBar()
        #windowmenu = menubar.addMenu('Theme')
        #themeAct = QAction('Toggle light/dark theme', self)
        #themeAct.setShortcut('Ctrl+T')
        #windowmenu.addAction(themeAct)
        #themeAct.triggered.connect(self.toggleColors)
        self.addControls()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.toggleColors()
        self.show()
        #self.Wellcome()

    def addControls(self):
        wid = QWidget(self)
        self.setCentralWidget(wid)
        # Status
        self.status = QLabel()
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setStyleSheet('color: #1DB954')
        self.status.setText('Xin chào')
        # Search
        self.searchInput = QLineEdit()
        self.searchInput.setFixedHeight(30)
        self.searchBtn = QPushButton('Tìm kiếm')
        self.searchBtn.setFixedHeight(30)
        self.searchBtn.clicked.connect(self.Search)

        self.voicesearchBtn = QPushButton('Tìm bằng giọng nói')
        self.voicesearchBtn.setFixedHeight(30)
        self.voicesearchBtn.clicked.connect(self.VoiceSearch)
        #self.listSong = QListView()
        self.listAudio = QListWidget()
        
        self.volumeslider = QSlider(Qt.Horizontal, self)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.setToolTip("Âm lượng")
        # self.volumeslabel = QLabel(alignment=QtCore.Qt.AlignCenter)
        
        self.playbutton = QPushButton('Phát/Tạm dừng')  # play button
        self.playbutton.setFixedHeight(30)
        self.stopbutton = QPushButton('Dừng')  # Stop button
        self.stopbutton.setFixedHeight(30)
        self.nextbutton = QPushButton('Tiếp theo')  # Next button
        self.nextbutton.setFixedHeight(30)
        self.nextbutton2 = QPushButton('Tiếp theo(random)')  # Next button
        self.nextbutton2.setFixedHeight(30)
        self.command = QPushButton('Ra lệnh bằng giọng nói')  # Next button
        self.command.setFixedHeight(30)

        self.shortcut = QShortcut(QKeySequence("Space"), self)
        self.shortcut.activated.connect(self.excCommand)
        # Add button layouts
        mainLayout = QVBoxLayout()
        # search = QHBoxLayout()
        controls = QHBoxLayout()
        # Add search
        # search.addWidget(searchBtn)
        # search.addWidget(voicesearchBtn)
        # Add buttons to song controls layout
        controls.addWidget(self.playbutton)
        controls.addWidget(self.nextbutton)
        controls.addWidget(self.stopbutton)
        controls.addWidget(self.nextbutton2)
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
        self.nextbutton2.clicked.connect(self.nextRecommend)
        self.command.clicked.connect(self.excCommand)
        self.volumeslider.valueChanged.connect(self.setVolume)
        # self.volumeslider.valueChanged.connect(self.volumeslabel.setNum)
        self.statusBar()

    def setVolume(self, Volume):
        self.mediaplayer.audio_set_volume(Volume)

    def PlayPause(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Phát")
        else:
            self.mediaplayer.play()
            self.playbutton.setText("Tạm dừng")
            
    def Pause(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Phát")

    def Stop(self):
        self.mediaplayer.stop()
        self.playbutton.setText("Phát")
    
    def setMediaPlayerUrl(self, url):
        self.media = self.instance.media_new(url)
        self.mediaplayer.set_media(self.media)

    def generateRandomList(self):
        list_title = ["nhạc hay", "nhạc mới", "nhạc trẻ hot", "nhac viet", "top hit", "best song"]
        next_key = next_keyword(list_title)
        self.status.setText('Tìm kiếm cho: "{}"'.format(next_key))
        self.searchInput.setText(next_key)
        self.Search(get_idx_by_user=False)

    def Search(self, get_idx_by_user=False):
        self.Pause()
        self.listAudio.clear()
        if self.searchInput.text() != '':
            print('keyword:', self.searchInput.text())
            print('searching...')
            results = YoutubeSearch(self.searchInput.text(), max_results=10).to_json()
            results = json.loads(results)
            results = results["videos"]
            
            if len(results) == 0:
                self.status.setText('Không có kết quả hoặc lỗi')
                t2s('try again')
                #self.searchInput.setText('')
            else:
                self.listAudio_text = {}
                self.list_title = [e["title"] for e in results]
                print(results)
                for i, item in enumerate(results):
                    itemtitle = item['title']
                    itemlink = 'https://www.youtube.com' + item['link']
                    self.listAudio.insertItem(i+1, str(i+1) + ': ' + itemtitle + '#link#' + itemlink)
                    self.listAudio_text[itemtitle] = itemlink
                    self.status.setText('Kết quả cho: "{}"'.format(self.searchInput.text()))
                
                #self.searchInput.setText('')
                t2s('seach done')
                if get_idx_by_user:
                    #sau khi search, cho người dùng chọn bài hát bằng voice
                    self.idx_audio = select_by_speech()
                else:
                    #cho chế độ tự động phát ramdom. phát bài đầu tiên trong list. không cần chọn bằng voice
                    self.idx_audio = 0
                sleep(1)
                self.selectAndPlaySongByIndex()
        else:
            self.status.setText('Nhập từ khóa hoặc tìm bằng giọng nói')
            t2s('enter keyword or voice search')

    def Wellcome(self):
        #sleep(1)
        t2s('Hello! Wellcome to music player')
        t2s('Let search a song!')
        self.VoiceSearch()

    def VoiceSearch(self):
        self.Pause()
        t2s('Start Voice Search')
        
        self.status.setText('Nói từ khóa')
        keyword = getVoiceKeyWord() # có xác nhận key
        #t2s('')
        # keyword = recognize('keyword')# không cần xác nhận
        t2s('search for {}'.format(keyword))
        self.status.setText('Tìm kiếm cho: "{}"'.format(keyword))
        self.searchInput.setText(keyword)
        self.Search()
        # self.selectAndPlaySongByIndex()
        
    def selectAndPlaySongByIndex(self):
        title_audio = list(self.listAudio_text.keys())[self.idx_audio]
        link_audio = list(self.listAudio_text.values())[self.idx_audio]
        link_audio = getLinkAudio(link_audio)
        
        t2s('Start play: {}'.format(self.idx_audio+1))

        self.setMediaPlayerUrl(link_audio)
        self.PlayPause()
        self.status.setText('Đang phát: {}'.format(title_audio))
        
    def Next(self):
        self.Pause()
        if self.idx_audio == 9:
            self.idx_audio = 0
        else:
            self.idx_audio += 1
        self.selectAndPlaySongByIndex()
    
    def nextRecommend(self):
        self.Pause()
        next_key = next_keyword(self.list_title)
        self.status.setText('Tìm kiếm cho: "{}"'.format(next_key))
        self.searchInput.setText(next_key)
        self.Search(get_idx_by_user=False)
    
    def voiceNext(self):
        print('Next song')
        self.Next()

    def voiceSelect(self):
        self.idx_audio = select_by_speech()
        self.selectAndPlaySongByIndex()

    def excCommand(self):
        self.Pause()
        t2s('OK. Im here')
        t2s('Please speech a command')
        command = listen_command()
        if command == 0:
            self.PlayPause()
        elif command == 1:
            self.voiceNext()
        elif command == 2:
            self.Stop()
        elif command == 3:
            self.VoiceSearch()
        elif command == 4:
            self.voiceSelect()
        elif command == 5:
            t2s('You are sure to exit!')
            t2s('Speech Yes or OK to comfirm!')
            cf_exit = recognize('')
            if cf_exit == 'yes' or cf_exit == 'ok' or cf_exit =='oke':
                exit()
            else:
                print('no exit')
            
    def toggleColors(self):
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(41, 41, 41))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(41, 41, 41))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(29, 185, 84))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(235, 101, 54))
        palette.setColor(QPalette.Highlight, Qt.white)
        palette.setColor(QPalette.HighlightedText,  QColor(29, 185, 84))
        app.setPalette(palette)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # load and set stylesheet
    with open('style.css', "r") as fh:
        app.setStyleSheet(fh.read())
    ex = App()
    sys.exit(app.exec_())
