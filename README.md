# music-player-voice-control
search and control music player by speech

Cần cài đặt thư viện trước:
cài vlc:   
windows: https://www.videolan.org/vlc/download-windows.html  
ubuntu: sudo apt install vlc  
pip install python-vlc pafy SpeechRecognition youtube-search  


chạy chương trình:   
python PyTunes.py  
  
nhấn voice search sau khi nghe thấy "start speech" thì nói từ khóa pm sẽ báo "done" là kết thúc ghi âm bắt đầu nhận dạng
sau mỗi lệnh khi nào nó nói "start speech" mới bắt đầu đọc lệnh vì hơi delay một chút.
ấn nút "Speech Command" để ra một lệnh: "play", "seach", "tìm", "next", "tiếp", "stop". Phần mềm chỉ nhận đúng từ khóa nếu nhận dạng đúng, nếu nói sai thì phải nói lại cho đến khi đúng với lệnh
