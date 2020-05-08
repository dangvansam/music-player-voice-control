# music-player-voice-control
search and control music player by speech

Cần cài đặt thư viện trước:
cài vlc:   
windows: https://www.videolan.org/vlc/download-windows.html  
ubuntu: sudo apt install vlc  
pip install python-vlc pafy SpeechRecognition youtube-search  


chạy chương trình:   
python PyTunes.py  
  
nhấn voice search sau khi nghe thấy "start" thì nói từ khóa pm sẽ báo "done" là kết thúc ghi âm bắt đầu nhận dạng
sau mỗi lệnh khi nào nó nói "start" mới bắt đầu đọc lệnh vì hơi delay một chút.
Khi đang play ấn phím "SPACE" (phím tắt của nút "Voice Speech Command") để ra lệnh: "play", "search", "tìm kiếm", "next", "tiếp theo", "stop", "dừng lại","đổi giao diện", "change skin", "thoát", "exit"
