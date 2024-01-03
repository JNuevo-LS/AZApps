from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import azure.cognitiveservices.speech as speechsdk
import os
import moviepy.editor as editor
import wave, contextlib
import praw
from PyQt6 import QtCore
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QComboBox, QFileDialog, QMainWindow, QListWidget, QLineEdit, QCheckBox, QMessageBox
from PyQt6.QtGui import QIntValidator
import sys

os.environ['AZURE_CLIENT_ID'] = '<Redacted>'
os.environ['AZURE_TENANT_ID'] = '<Redacted>'
os.environ['AZURE_CLIENT_SECRET'] = '<Redacted>'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = QWidget()
        self.window.setWindowTitle('Azure Video Creator')
        self.window.setFixedSize(400,500)

        credential = DefaultAzureCredential()
        secret_client = SecretClient(vault_url='<Redacted>', credential=credential)
        speech_service_key = secret_client.get_secret('<Redacted>')
        self.speech_config = speechsdk.SpeechConfig(subscription=speech_service_key.value, region='eastus')

        self.layout = QVBoxLayout()

        self.subreddit_add_line = QLineEdit(self)
        self.subreddit_add_line.setPlaceholderText('Subreddit...')
        self.layout.addWidget(self.subreddit_add_line)

        self.add_button = QPushButton(self, text='Add Subreddit to List')
        self.add_button.clicked.connect(self.add_to_list)
        self.layout.addWidget(self.add_button)

        self.subreddits = QListWidget(self)
        self.layout.addWidget(self.subreddits)

        self.empty_button = QPushButton(self, text='EMPTIES LIST')
        self.empty_button.clicked.connect(self.empty_list)
        self.layout.addWidget(self.empty_button)

        self.postcount = QLineEdit(self)
        self.postcount.setPlaceholderText('# of posts to get (from each subreddit, not total)')
        self.postcount.setValidator(QIntValidator())
        self.layout.addWidget(self.postcount)

        self.voices = ['en-GB-ThomasNeural', 'en-GB-SoniaNeural', 'en-GB-NoahNeural', 'en-US-JennyNeural', 'en-US-EricNeural', 'en-US-TonyNeural', 
                    'en-CA-LiamNeural', 'en-CA-ClaraNeural', 'en-US-AndrewNeural', 'en-US-EmmaNeural', 'en-US-JacobNeural',
                    'en-US-GuyNeural', 'en-US-AriaNeural','en-US-DavisNeural', 'en-US-AmberNeural',
                    'en-US-AnaNeural', 'en-US-AshleyNeural','en-US-BrandonNeural','en-US-BrianNeural',
                    'en-US-ChristopherNeural','en-US-CoraNeural','en-US-ElizabethNeural','en-US-JaneNeural','en-US-JasonNeural',
                    'en-US-MichelleNeural','en-US-MonicaNeural','en-US-NancyNeural','en-US-RogerNeural','en-US-SaraNeural',
                    'en-US-SteffanNeural','en-US-AvaNeural']
        
        self.VoiceNames = QComboBox(self)
        self.VoiceNames.addItems(self.voices)
        self.layout.addWidget(self.VoiceNames)

        self.ChooseVideo = QPushButton(self, text='Select Video')
        self.ChooseVideo.clicked.connect(self.choose_video)
        self.layout.addWidget(self.ChooseVideo)

        self.ChooseSaveLocation = QPushButton(self, text='Select where to save output')
        self.ChooseSaveLocation.clicked.connect(self.choose_save_location)
        self.layout.addWidget(self.ChooseSaveLocation)

        self.ChosenVideo = QLineEdit(self)
        self.ChosenVideo.setPlaceholderText('Chosen video file path goes here...')
        self.ChosenVideo.setReadOnly(True)
        self.layout.addWidget(self.ChosenVideo)

        self.ChosenSaveLocation = QLineEdit(self)
        self.ChosenSaveLocation.setPlaceholderText('Chosen output folder file path goes here...')
        self.ChosenSaveLocation.setReadOnly(True)
        self.layout.addWidget(self.ChosenSaveLocation)

        self.time_marker = 0
        self.FinalButton = QPushButton(self, text='Create Videos')
        self.FinalButton.clicked.connect(self.FinalRun)
        self.layout.addWidget(self.FinalButton)

        self.window.setLayout(self.layout)
        self.window.show()

    def choose_video(self):
        ChooseFile = QFileDialog.getOpenFileUrl(parent=None, caption='Select Video File', filter="Video Files (*.mp4 *.avi *.mkv *.webm)")
        ChooseFile = ChooseFile[0].toString()
        self.ChosenVideo.setText(ChooseFile[8:])

    def choose_save_location(self):
        ChooseFolder = QFileDialog.getExistingDirectory(parent=None, caption='Select Folder')
        self.ChosenSaveLocation.setText(ChooseFolder)


    def add_to_list(self):
        text = self.subreddit_add_line.text()
        self.subreddits.addItem(text)

    def empty_list(self):
        caution = QMessageBox.question(self, 'Confirmation', 'Are you sure you want to empty the list?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if caution == QMessageBox.StandardButton.Yes:
            self.subreddits.clear()
        else: 
            pass


    def prowl_reddit(self):
        client_id = '<Redacted>'
        client_secret='<Redacted>'
        user_agent='<Redacted>'
        username = '<Redacted>'
        password = '<Redacted>'

        reddit = praw.Reddit(client_id = client_id, client_secret = client_secret,
                            user_agent = user_agent, password = password, username = username)

        subreddits = []
        for index in range(self.subreddits.count()):
            item = self.subreddits.item(index)
            subreddits.append(item.text())

        self.Title_n_Text = []

        for subr in subreddits:
            obj = reddit.subreddit(subr)
            postcount = (int(self.postcount.text()))
            fetched_posts = 0

            for post in obj.hot(limit=None):
                if fetched_posts >= postcount:
                    break
                if not post.stickied:
                    self.Title_n_Text.append(self.combine_title_and_text(post=post))
                    fetched_posts += 1
                else: pass                    

    def combine_title_and_text(self, post):
        title = post.title
        text = post.selftext
        combined = title + '\n' + text
        return combined

    def calculate_audio_length(self, audio):
        with contextlib.closing(wave.open(audio, 'r')) as data:
            frames = data.getnframes()
            framerate = float(data.getframerate())
            total_seconds = frames/framerate
            return total_seconds

    def video_tts_synthesizer(self):
        video = editor.VideoFileClip(f'{self.ChosenVideo.text()}')

        for index, post in enumerate(self.Title_n_Text):
            audio = f'{self.ChosenSaveLocation.text()}\\Audio{index+1}.wav'
            print(audio)
            audio_config = speechsdk.audio.AudioConfig(filename=audio)
            speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=audio_config)

            ssml_string = f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'><voice name='{self.VoiceNames.currentText()}'><prosody rate='1.25'>{post}</prosody></voice></speak>"
            speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml_string).get()

            moviepy_audio = editor.AudioFileClip(audio)
            length = self.calculate_audio_length(audio)
            subclip = video.subclip(t_start=self.time_marker, t_end = (self.time_marker + length))
            mixed_a_v = subclip.set_audio(moviepy_audio)
            self.saved_to = f'{self.ChosenSaveLocation.text()}\\SynthesizedVideo{index+1}.mp4'
            mixed_a_v.write_videofile(self.saved_to)

            self.time_marker += length
        
    def FinalRun(self):
        if self.postcount.text().strip() == '':
            QMessageBox.critical(self, 'Error', '# of Posts cannot be empty')
            return
        if self.subreddits.count() == 0:
            QMessageBox.critical(self, 'Error', 'Subreddit List Cannot be Empty')
            return
        if self.ChosenSaveLocation.text().strip() == '' or self.ChosenVideo.text().strip() == '':
            QMessageBox.critical(self, 'Error', 'No Video or Save Location Selected')
            return    
        self.prowl_reddit()
        self.video_tts_synthesizer()
        QMessageBox.information(self, 'Completion', 'Task completed successfully!')



app = QApplication(sys.argv)
window = MainWindow()
app.setStyle('Fusion')
sys.exit(app.exec())
