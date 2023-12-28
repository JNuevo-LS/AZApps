from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QComboBox, QFileDialog, QMainWindow
import os
import sys
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import azure.cognitiveservices.speech as speechsdk
import datetime as dt

os.environ['AZURE_CLIENT_ID'] = 'x'
os.environ['AZURE_TENANT_ID'] = 'x'
os.environ['AZURE_CLIENT_SECRET'] = 'x'

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
        self.secret_client = SecretClient(vault_url='x', credential=self.credential)
        self.speech_service_key = self.secret_client.get_secret('x')


        self.VoiceNames = QComboBox(parent=self.window)
        self.layout.addWidget(self.VoiceNames)
        self.list_of_names = [
            'es-CU-ManuelNeural',
            'es-CU-BelkysNeural',
            'es-ES-ElviraNeural',
            'es-ES-AlvaroNeural',
            'es-ES-AbrilNeural',
            'es-ES-ArnauNeural',
            'es-ES-DarioNeural',
            'es-ES-EliasNeural',
            'es-ES-EstrellaNeural',
            'es-ES-IreneNeural',
            'es-ES-LaiaNeural',
            'es-ES-LiaNeural',
            'es-ES-NilNeural',
            'es-ES-SaulNeural',
            'es-ES-TeoNeural',
            'es-ES-TrianaNeural',
            'es-ES-VeraNeural',
            'es-ES-XimenaNeural']

        for voice in self.list_of_names:
            self.VoiceNames.addItem(voice)

        self.save_button = QPushButton(parent=self.window, text='Save and Process')
        self.save_button.clicked.connect(self.synthesizer)
        self.layout.addWidget(self.save_button)

        self.window.setLayout(self.layout)
        self.window.show()
 
    def synthesizer(self):
        ChooseFile = QFileDialog.getExistingDirectory(parent=None, caption='Select Directory' )
        timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        speech_config = speechsdk.SpeechConfig(subscription=self.speech_service_key.value, region='eastus')
        speech_config.speech_synthesis_voice_name = f'{self.VoiceNames.currentText()}'
        audio_config = speechsdk.AudioConfig(filename=f'{ChooseFile}\output_{timestamp}.wav')
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        text = self.text_to_synthesize.toPlainText()
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

app = QApplication(sys.argv)
app.setStyle('Fusion')
window = MainWindow()
sys.exit(app.exec())
