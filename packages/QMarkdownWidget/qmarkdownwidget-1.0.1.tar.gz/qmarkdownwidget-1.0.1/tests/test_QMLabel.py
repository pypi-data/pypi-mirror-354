import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                           QWidget, QScrollArea, QPushButton, QTextEdit, QLabel,
                           QFrame, QSizePolicy, QSpacerItem)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap, QPainter, QBrush, QColor
from QMarkdownWidget import QMLabel
import datetime


class ChatBubble(QFrame):
    """Chat bubble widget"""
    
    def __init__(self, message, is_self=False, username="", timestamp=None):
        super().__init__()
        self.is_self = is_self
        self.message = message
        self.username = username
        self.timestamp = timestamp or datetime.datetime.now()
        
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """Set up the UI"""
        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 5, 10, 5)
        
        if self.is_self:
            # Own message: right-aligned
            main_layout.addStretch()
            bubble_widget = self.create_bubble_widget()
            main_layout.addWidget(bubble_widget)
            main_layout.addWidget(self.create_avatar())
        else:
            # Other's message: left-aligned
            main_layout.addWidget(self.create_avatar())
            bubble_widget = self.create_bubble_widget()
            main_layout.addWidget(bubble_widget)
            main_layout.addStretch()
    
    def create_avatar(self):
        """Create avatar"""
        avatar = QLabel()
        avatar.setFixedSize(40, 40)
        avatar.setText("👤" if not self.is_self else "😊")
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border-radius: 20px;
                font-size: 20px;
                border: 2px solid #e0e0e0;
            }
        """)
        return avatar
    
    def create_bubble_widget(self):
        """Create message bubble"""
        bubble_widget = QWidget()
        bubble_layout = QVBoxLayout(bubble_widget)
        bubble_layout.setContentsMargins(0, 0, 0, 0)
        bubble_layout.setSpacing(2)
        
        # Username (displayed only for non-self messages)
        if not self.is_self and self.username:
            name_label = QLabel(self.username)
            name_label.setStyleSheet("""
                QLabel {
                    color: #888888;
                    font-size: 12px;
                    margin-bottom: 2px;
                }
            """)
            bubble_layout.addWidget(name_label)
        
        # Message content
        message_label = QMLabel()
        message_label.setText(self.message)
        message_label.setWordWrap(True)
        message_label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        
        # Set maximum width
        message_label.setMaximumWidth(400)
        message_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        
        bubble_layout.addWidget(message_label)
        
        # Timestamp
        time_label = QLabel(self.timestamp.strftime("%H:%M"))
        time_label.setAlignment(Qt.AlignmentFlag.AlignRight if self.is_self else Qt.AlignmentFlag.AlignLeft)
        time_label.setStyleSheet("""
            QLabel {
                color: #999999;
                font-size: 10px;
                margin-top: 2px;
            }
        """)
        bubble_layout.addWidget(time_label)
        
        # Set bubble style
        bubble_style = self.get_bubble_style()
        message_label.setStyleSheet(bubble_style)
        
        return bubble_widget
    
    def get_bubble_style(self):
        """Get bubble style"""
        if self.is_self:
            # Self message: green bubble
            return """
                QMLabel {
                    background-color: #95EC69;
                    border: none;
                    border-radius: 12px;
                    padding: 10px 15px;
                    color: #000000;
                    font-size: 14px;
                    line-height: 1.4;
                }
            """
        else:
            # Other's message: white bubble
            return """
                QMLabel {
                    background-color: #FFFFFF;
                    border: 1px solid #E5E5E5;
                    border-radius: 12px;
                    padding: 10px 15px;
                    color: #000000;
                    font-size: 14px;
                    line-height: 1.4;
                }
            """
    
    def setup_style(self):
        """Set overall style"""
        self.setStyleSheet("""
            ChatBubble {
                background-color: transparent;
                border: none;
            }
        """)


class ChatWindow(QMainWindow):
    """Chat window"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_style()
        self.add_demo_messages()
    
    def setup_ui(self):
        """Set up the UI"""
        self.setWindowTitle("QMLabel Chat Demo")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Title bar
        title_bar = self.create_title_bar()
        main_layout.addWidget(title_bar)
        
        # Chat area
        self.chat_area = self.create_chat_area()
        main_layout.addWidget(self.chat_area)
        
        # Input area
        input_area = self.create_input_area()
        main_layout.addWidget(input_area)
    
    def create_title_bar(self):
        """Create the title bar"""
        title_bar = QWidget()
        title_bar.setFixedHeight(60)
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # Title
        title_label = QLabel("QMLabel Chat Demo")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        # Function buttons
        demo_btn = QPushButton("Add Demo Messages")
        demo_btn.clicked.connect(self.add_demo_messages)
        layout.addWidget(demo_btn)
        
        clear_btn = QPushButton("Clear Chat")
        clear_btn.clicked.connect(self.clear_chat)
        layout.addWidget(clear_btn)
        
        title_bar.setStyleSheet("""
            QWidget {
                background-color: #F7F7F7;
                border-bottom: 1px solid #E5E5E5;
            }
            QLabel {
                color: #333333;
            }
            QPushButton {
                background-color: #07C160;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                margin-left: 5px;
            }
            QPushButton:hover {
                background-color: #06AD56;
            }
            QPushButton:pressed {
                background-color: #059748;
            }
        """)
        
        return title_bar
    
    def create_chat_area(self):
        """Create the chat area"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Chat content container
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(0, 10, 0, 10)
        self.chat_layout.setSpacing(5)
        self.chat_layout.addStretch()  # Add a stretch at the bottom
        
        scroll_area.setWidget(self.chat_container)
        
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #EDEDED;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #F0F0F0;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #C0C0C0;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #A0A0A0;
            }
        """)
        
        return scroll_area
    
    def create_input_area(self):
        """Create the input area"""
        input_widget = QWidget()
        input_widget.setFixedHeight(120)
        
        layout = QVBoxLayout(input_widget)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Input box
        self.input_text = QTextEdit()
        self.input_text.setFixedHeight(80)
        self.input_text.setPlaceholderText("Enter message... (Markdown supported)")
        layout.addWidget(self.input_text)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Send button
        send_btn = QPushButton("Send")
        send_btn.setFixedSize(80, 30)
        send_btn.clicked.connect(self.send_message)
        button_layout.addWidget(send_btn)
        
        layout.addLayout(button_layout)
        
        input_widget.setStyleSheet("""
            QWidget {
                background-color: #F7F7F7;
                border-top: 1px solid #E5E5E5;
            }
            QTextEdit {
                border: 1px solid #D1D1D1;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
                background-color: white;
            }
            QPushButton {
                background-color: #07C160;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #06AD56;
            }
            QPushButton:pressed {
                background-color: #059748;
            }
        """)
        
        return input_widget
    
    def add_chat_message(self, message, is_self=False, username=""):
        """Add chat message"""
        bubble = ChatBubble(message, is_self, username)
        
        # Insert before the last stretch
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)
        
        # Scroll to bottom
        QTimer.singleShot(100, self.scroll_to_bottom)
    
    def scroll_to_bottom(self):
        """Scroll to bottom"""
        scrollbar = self.chat_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def send_message(self):
        """Send message"""
        text = self.input_text.toPlainText().strip()
        if text:
            self.add_chat_message(text, is_self=True)
            self.input_text.clear()
            
            # Simulate auto-reply
            QTimer.singleShot(1000, lambda: self.auto_reply(text))
    
    def auto_reply(self, original_message):
        """Auto reply"""
        replies = [
            "Received your message: **{}** 👍".format(original_message[:20] + "..." if len(original_message) > 20 else original_message),
            "This is an auto-reply message demonstrating QMLabel features",
            """Looks good! QMLabel supports:
- **Bold text**
- *Italic text*
- `Code snippets`
- And more...""",
            """```python
# Code block demo
def greet(name):
    return f'Hello, {name}!'

print(greet('QMLabel'))
```""",
            """### Feature List
1. ✅ Markdown rendering
2. ✅ QSS style support  
3. ✅ Auto-wrap
4. ✅ Size adaptation

> This is really amazing!"""
        ]
        
        import random
        reply = random.choice(replies)
        self.add_chat_message(reply, is_self=False, username="QMLabel Assistant")
    
    def add_demo_messages(self):
        """Add demo messages"""
        demo_messages = [
            ("Hello! Welcome to the QMLabel chat demo.", False, "System"),
            ("This interface uses QMLabel to display messages.", False, "System"),
            ("That's great! The interface looks beautiful. 😊", True, ""),
            ("QMLabel supports **Markdown syntax**, such as *italics* and `code`.", False, "Assistant"),
            ("It can also display code blocks:\n```python\nprint('Hello QMLabel!')\n```", True, ""),
            ("### Supported Features\n- ✅ Text formatting\n- ✅ Code highlighting\n- ✅ Tables and lists\n- ✅ QSS styling", False, "Assistant"),
            ("| Feature | QLabel | QMLabel |\n|--- |--- |--- |\n| Basic Display | ✅ | ✅ |\n| Markdown | ❌ | ✅ |\n| QSS Styling | ✅ | ✅ |", True, ""),
            ("> This is a quote block.\n> \n> Showcasing the powerful features of QMLabel.", False, "Assistant")
        ]
        
        for message, is_self, username in demo_messages:
            self.add_chat_message(message, is_self, username)
    
    def clear_chat(self):
        """Clear chat history"""
        # Remove all widgets except the last stretch
        while self.chat_layout.count() > 1:
            child = self.chat_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def setup_style(self):
        """Set window style"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #EDEDED;
            }
        """)
    
    def keyPressEvent(self, event):
        """Handle keyboard events"""
        if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.send_message()
        else:
            super().keyPressEvent(event)


def main():
    app = QApplication(sys.argv)
    
    # Set global font
    font = QFont("Arial", 10)
    app.setFont(font)
    
    window = ChatWindow()
    window.show()
    
    return app.exec()


if __name__ == '__main__':
    sys.exit(main()) 