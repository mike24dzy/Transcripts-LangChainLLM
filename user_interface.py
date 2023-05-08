import os
import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QWidget, QMessageBox
from PyQt5.QtCore import Qt
from getpass import getpass
from chain_io import file_load_split, init_embeddings, qa_docs, summarization

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DocGPT: Ask Anything About Your Document")
        self.setGeometry(100, 100, 800, 600)

        self.db = None

        widget = QWidget()
        layout = QVBoxLayout()

        # Drag and drop
        self.drop_zone = DropZone(self)
        layout.addWidget(self.drop_zone)

        # OpenAI API key input
        self.api_key_button = QPushButton("Enter OpenAI API Key")
        self.api_key_button.clicked.connect(self.enter_api_key)
        layout.addWidget(self.api_key_button)

        # Ask anything in the doc
        layout.addWidget(QLabel("Ask anything in the doc"))
        self.question_input = QLineEdit()
        layout.addWidget(self.question_input)
        self.ask_button = QPushButton("Ask")
        self.ask_button.clicked.connect(self.ask_question)
        layout.addWidget(self.ask_button)
        self.answer_output = QTextEdit()
        layout.addWidget(self.answer_output)

        # Summarize the whole doc
        layout.addWidget(QLabel("Summarize the whole doc"))
        self.summarize_input = QLineEdit()
        layout.addWidget(self.summarize_input)
        self.summarize_button = QPushButton("Summarize")
        self.summarize_button.clicked.connect(self.summarize_doc)
        layout.addWidget(self.summarize_button)
        self.summarize_output = QTextEdit()
        layout.addWidget(self.summarize_output)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def enter_api_key(self):
        api_key = getpass("Enter your OpenAI API key: ")
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key
            self.api_key_button.setEnabled(False)

    def load_file_and_init_db(self, file_path):
        if not file_path:
            return
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return
        
        texts, data = file_load_split(file_path)
        self.db = init_embeddings(api_key, texts)
        return data

    # def load_file(self, file_path):
    #     self.file_path = file_path

    def ask_question(self):
        if not self.drop_zone.file_path:
            return

        query = self.question_input.text()
        if not query:
            return

        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return
        
        if not self.db:
            _ = self.load_file_and_init_db(self.drop_zone.file_path)

        result = qa_docs(self.db, api_key, query)
        self.answer_output.setPlainText(json.dumps(result, indent=2))

    def summarize_doc(self):
        if not self.drop_zone.file_path:
            return

        query = self.summarize_input.text()
        if not query:
            return

        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return

        texts, data = file_load_split(self.drop_zone.file_path)
        result = summarization(api_key, data, query)
        self.summarize_output.setPlainText(result)


class DropZone(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("Drop a document here")
        self.file_path = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1:
                new_file_path = urls[0].toLocalFile()
                if new_file_path != self.file_path:
                    self.file_path = new_file_path
                    self.setText(f"Loaded file: {self.file_path}")
                    self.parentWidget().db = None  # Reset the previous db before initializing a new one
                    event.acceptProposedAction()
            else:
                QMessageBox.warning(self, "Warning", "Please drop only one file at a time.")
        else:
            QMessageBox.warning(self, "Warning", "Invalid file type. Please drop a valid document file.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

