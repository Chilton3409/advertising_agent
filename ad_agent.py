#!/usr/bin/env python3
#New file created
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal
from meta_ai_api import MetaAI
import asyncio
import os
import logging

# Model
class AdvertisingAssistantModel:
    def __init__(self):
        self.meta_ai_api_key = os.environ.get("META_AI_TOKEN")
        self.api = MetaAI(self.meta_ai_api_key)

    async def generate_advertisement_async(self, prompt, filename):
        try:
            
            refactored_prompt = await self.refactor_prompt(prompt)
            advertisement = await self.get_meta_ai_insights(meta_ai_text=f"create a new advertisement based on: {refactored_prompt}")
            
            await self.append_file(filename, advertisement)
            
            
            return advertisement
        except Exception as e:
            logging.exception(msg=e)

    async def refactor_prompt(self, prompt: str) -> str:
        try:
            
            refactored_prompt = await self.get_meta_ai_insights(meta_ai_text=f"refactor this prompt from the user for advertisement generation: {prompt}")
            return refactored_prompt
        except Exception as e:
            logging.exception(msg=e)
            
    async def get_meta_ai_insights(self, meta_ai_text):
        try:
            
            response = self.api.prompt(message=meta_ai_text, new_conversation=False)
            return response['message']
        except Exception as e:
            logging.exception(msg=e)
            
    async def write_file(self, filename: str, text: str) -> str:
        try:
            
            with open(filename, 'w') as f:
                f.write(text)
        except Exception as e:
            logging.exception(msg=e)
            
    async def append_file(self, filename: str, text: str) -> str:
        try:
            
            with open(filename, 'a') as f:
                f.write(text)
        except Exception as e:
            logging.exception(msg=e)
            
# View
class AdvertisingAssistantView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Advertising Assistant')
        self.setStyleSheet("background-color: #2b2b2b;")

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)

        self.prompt_input = QTextEdit()
        self.prompt_input.setStyleSheet("background-color: #3b3b3b; color: #ffffff; border: 1px solid #4b4b4b; padding: 10px; font-size: 16px; border-radius: 5px;")
        self.prompt_input.setPlaceholderText("Enter your prompt here...")
        layout.addWidget(self.prompt_input)

        self.filename_input = QLineEdit()
        self.filename_input.setStyleSheet("background-color: #3b3b3b; color: #ffffff; border: 1px solid #4b4b4b; padding: 10px; font-size: 16px; border-radius: 5px;")
        self.filename_input.setPlaceholderText("Enter filename...")
        layout.addWidget(self.filename_input)

        self.button = QPushButton("Generate Advertisement")
        self.button.setStyleSheet("background-color: #4CAF50; color: #ffffff; padding: 10px 20px; border: none; border-radius: 5px; font-size: 16px;")
        layout.addWidget(self.button)

        self.result_label = QTextEdit()
        self.result_label.setStyleSheet("background-color: #3b3b3b; color: #ffffff; border: 1px solid #4b4b4b; padding: 10px; font-size: 16px; border-radius: 5px;")
        self.result_label.setReadOnly(True)
        layout.addWidget(self.result_label)

        self.setLayout(layout)
# Controller
class AdvertisingAssistantController:
    def __init__(self, app):
        self.model = AdvertisingAssistantModel()
        self.view = AdvertisingAssistantView()
        self.app = app
         # Enable the button by default
    def generate_advertisement(self):
        
        try:
            self.view.result_label.setText("be patient, generating advertisement.")
            prompt = self.view.prompt_input.toPlainText()
            filename = self.view.filename_input.text()
            self.thread = WorkerThread(self.model.generate_advertisement_async, prompt, filename)
            self.thread.finished.connect(self.advertisement_generated)
            self.thread.start()
        except Exception as e:
            self.view.result_label.setText(str(e))
            self.view.button.setEnabled(True)

    def advertisement_generated(self, result):
        """
        append the result to the result label and reenable button clicking
        this also the callback for the worker thread
        """
        try:
            
            self.view.result_label.setText(result)
            self.view.button.setEnabled(True)
        except Exception as e:
            logging.exception(msg=e)
    def run(self):
        try:
            
            self.view.button.clicked.connect(self.generate_advertisement)
            self.view.show()
            self.app.exec_()
        except Exception as e:
            logging.exception(msg=e)


class WorkerThread(QThread):
    finished = pyqtSignal(object)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    async def run_func(self):
        try:
            return await self.func(*self.args, **self.kwargs)
        except Exception as e:
            return str(e)

    def run(self):
        try:
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.run_func())
            self.finished.emit(result)
        except Exception as e:
            logging.exception(msg=e)
            
def main():
    app = QApplication(sys.argv)
    controller = AdvertisingAssistantController(app)
    controller.run()

if __name__ == "__main__":
    main()