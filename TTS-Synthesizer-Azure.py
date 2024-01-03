from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QComboBox, QFileDialog, QMainWindow, QMessageBox
import os
import sys
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import azure.cognitiveservices.speech as speechsdk
import datetime as dt

os.environ['AZURE_CLIENT_ID'] = 'Redacted'
os.environ['AZURE_TENANT_ID'] = 'Redacted'
os.environ['AZURE_CLIENT_SECRET'] = 'Redacted'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = QWidget()
        self.window.setWindowTitle('Azure Text to Speech')
        self.window.setFixedSize(400, 400)

        self.layout = QVBoxLayout()

        self.text_to_synthesize = QTextEdit(parent = self.window)
        self.text_to_synthesize.setPlaceholderText('Text to synthesize here...')
        self.layout.addWidget(self.text_to_synthesize)

        self.credential = DefaultAzureCredential()
        self.secret_client = SecretClient(vault_url='https://tts-keys.vault.azure.net/', credential=self.credential)
        self.speech_service_key = self.secret_client.get_secret('<Redacted>KeyforTTS')


        self.VoiceNames = QComboBox(parent=self.window)
        self.layout.addWidget(self.VoiceNames)
        self.list_of_names = [
            'es-CU-ManuelNeural',
            'es-CU-BelkysNeural',
            'es-ES-ArnauNeural',
            'es-ES-EliasNeural',
            'es-ES-EstrellaNeural',
            'es-ES-IreneNeural',
            'en-US-ChristopherNeural',
            'en-US-CoraNeural',
            'en-US-ElizabethNeural',
            'en-US-JennyMultilingualV2Neural',
            'en-US-AvaMultilingualNeural',
            'de-DE-SeraphinaMultilingualNeural',
            'en-US-AvaNeural',
            'en-US-RogerNeural',
            'en-US-JennyNeural',
            'en-US-TonyNeural']

        for voice in self.list_of_names:
            self.VoiceNames.addItem(voice)

        self.save_button = QPushButton(parent=self.window, text='Save and Process')
        self.save_button.clicked.connect(self.synthesizer)
        self.layout.addWidget(self.save_button)

        self.window.setLayout(self.layout)
        self.window.show()
 
    def synthesizer(self):
        ChooseFile = QFileDialog.getSaveFileName(parent=None,caption='Save File',filter='WAV Files (*.wav);;MP3 Files (*.mp3);;All Files (*)')
        if ChooseFile:
            pass
        else:
            QMessageBox.warning(self, 'Error', "File was not named.")
        speech_config = speechsdk.SpeechConfig(subscription=self.speech_service_key.value, region='eastus')
        speech_config.speech_synthesis_voice_name = f'{self.VoiceNames.currentText()}'
        audio_config = speechsdk.AudioConfig(filename=f'{ChooseFile[0]}')
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        text = self.text_to_synthesize.toPlainText()
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

app = QApplication(sys.argv)
app.setStyle('Fusion')
window = MainWindow()
sys.exit(app.exec())
