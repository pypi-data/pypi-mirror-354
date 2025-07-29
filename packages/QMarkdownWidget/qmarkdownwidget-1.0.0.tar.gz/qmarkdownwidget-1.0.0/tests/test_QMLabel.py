import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                           QWidget, QScrollArea, QPushButton, QTextEdit, QLabel,
                           QFrame, QSizePolicy, QSpacerItem)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap, QPainter, QBrush, QColor
from QMarkdownWidget import QMLabel
import datetime


class ChatBubble(QFrame):
    """聊天气泡控件"""
    
    def __init__(self, message, is_self=False, username="", timestamp=None):
        super().__init__()
        self.is_self = is_self
        self.message = message
        self.username = username
        self.timestamp = timestamp or datetime.datetime.now()
        
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """设置UI布局"""
        # 主布局
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 5, 10, 5)
        
        if self.is_self:
            # 自己的消息：右对齐
            main_layout.addStretch()
            bubble_widget = self.create_bubble_widget()
            main_layout.addWidget(bubble_widget)
            main_layout.addWidget(self.create_avatar())
        else:
            # 对方的消息：左对齐
            main_layout.addWidget(self.create_avatar())
            bubble_widget = self.create_bubble_widget()
            main_layout.addWidget(bubble_widget)
            main_layout.addStretch()
    
    def create_avatar(self):
        """创建头像"""
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
        """创建消息气泡"""
        bubble_widget = QWidget()
        bubble_layout = QVBoxLayout(bubble_widget)
        bubble_layout.setContentsMargins(0, 0, 0, 0)
        bubble_layout.setSpacing(2)
        
        # 用户名（非自己的消息才显示）
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
        
        # 消息内容
        message_label = QMLabel()
        message_label.setText(self.message)
        message_label.setWordWrap(True)
        message_label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        
        # 设置最大宽度
        message_label.setMaximumWidth(400)
        message_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        
        bubble_layout.addWidget(message_label)
        
        # 时间戳
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
        
        # 设置气泡样式
        bubble_style = self.get_bubble_style()
        message_label.setStyleSheet(bubble_style)
        
        return bubble_widget
    
    def get_bubble_style(self):
        """获取气泡样式"""
        if self.is_self:
            # 自己的消息：绿色气泡
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
            # 对方的消息：白色气泡
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
        """设置整体样式"""
        self.setStyleSheet("""
            ChatBubble {
                background-color: transparent;
                border: none;
            }
        """)


class ChatWindow(QMainWindow):
    """聊天窗口"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_style()
        self.add_demo_messages()
    
    def setup_ui(self):
        """设置UI"""
        self.setWindowTitle("QMLabel 聊天界面演示")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 标题栏
        title_bar = self.create_title_bar()
        main_layout.addWidget(title_bar)
        
        # 聊天区域
        self.chat_area = self.create_chat_area()
        main_layout.addWidget(self.chat_area)
        
        # 输入区域
        input_area = self.create_input_area()
        main_layout.addWidget(input_area)
    
    def create_title_bar(self):
        """创建标题栏"""
        title_bar = QWidget()
        title_bar.setFixedHeight(60)
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # 标题
        title_label = QLabel("QMLabel 聊天演示")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        # 功能按钮
        demo_btn = QPushButton("添加演示消息")
        demo_btn.clicked.connect(self.add_demo_messages)
        layout.addWidget(demo_btn)
        
        clear_btn = QPushButton("清空聊天")
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
        """创建聊天区域"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # 聊天内容容器
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(0, 10, 0, 10)
        self.chat_layout.setSpacing(5)
        self.chat_layout.addStretch()  # 在底部添加弹性空间
        
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
        """创建输入区域"""
        input_widget = QWidget()
        input_widget.setFixedHeight(120)
        
        layout = QVBoxLayout(input_widget)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # 输入框
        self.input_text = QTextEdit()
        self.input_text.setFixedHeight(80)
        self.input_text.setPlaceholderText("输入消息... (支持Markdown语法)")
        layout.addWidget(self.input_text)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 发送按钮
        send_btn = QPushButton("发送")
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
        """添加聊天消息"""
        bubble = ChatBubble(message, is_self, username)
        
        # 在最后一个stretch之前插入
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)
        
        # 滚动到底部
        QTimer.singleShot(100, self.scroll_to_bottom)
    
    def scroll_to_bottom(self):
        """滚动到底部"""
        scrollbar = self.chat_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def send_message(self):
        """发送消息"""
        text = self.input_text.toPlainText().strip()
        if text:
            self.add_chat_message(text, is_self=True)
            self.input_text.clear()
            
            # 模拟自动回复
            QTimer.singleShot(1000, lambda: self.auto_reply(text))
    
    def auto_reply(self, original_message):
        """自动回复"""
        replies = [
            "收到您的消息：**{}** 👍".format(original_message[:20] + "..." if len(original_message) > 20 else original_message),
            "这是一个自动回复消息，演示QMLabel的功能",
            """看起来不错！QMLabel支持：
- **粗体文本**
- *斜体文本*
- `代码片段`
- 还有更多...""",
            "```python\n# 代码块演示\ndef greet(name):\n    return f'Hello, {name}!'\n\nprint(greet('QMLabel'))\n```",
            """### 功能列表
1. ✅ Markdown渲染
2. ✅ QSS样式支持  
3. ✅ 自动换行
4. ✅ 大小自适应

> 这真是太棒了！"""
        ]
        
        import random
        reply = random.choice(replies)
        self.add_chat_message(reply, is_self=False, username="QMLabel助手")
    
    def add_demo_messages(self):
        """添加演示消息"""
        demo_messages = [
            ("Hello! 欢迎使用QMLabel聊天演示", False, "系统"),
            ("这个界面完全使用QMLabel控件来显示消息", False, "系统"),
            ("太棒了！界面很漂亮 😊", True, ""),
            ("QMLabel支持**Markdown语法**，比如*斜体*和`代码`", False, "助手"),
            ("还可以显示代码块：\n```python\nprint('Hello QMLabel!')\n```", True, ""),
            ("### 支持的功能\n- ✅ 文本格式化\n- ✅ 代码高亮\n- ✅ 表格和列表\n- ✅ QSS样式", False, "助手"),
            ("| 特性 | QLabel | QMLabel |\n|------|--------|----------|\n| 基础显示 | ✅ | ✅ |\n| Markdown | ❌ | ✅ |\n| QSS样式 | ✅ | ✅ |", True, ""),
            ("> 这是一个引用块\n> \n> 展示QMLabel的强大功能", False, "助手")
        ]
        
        for message, is_self, username in demo_messages:
            self.add_chat_message(message, is_self, username)
    
    def clear_chat(self):
        """清空聊天记录"""
        # 移除除了最后一个stretch之外的所有控件
        while self.chat_layout.count() > 1:
            child = self.chat_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def setup_style(self):
        """设置窗口样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #EDEDED;
            }
        """)
    
    def keyPressEvent(self, event):
        """处理键盘事件"""
        if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.send_message()
        else:
            super().keyPressEvent(event)


def main():
    app = QApplication(sys.argv)
    
    # 设置全局字体
    font = QFont("Arial", 10)
    app.setFont(font)
    
    window = ChatWindow()
    window.show()
    
    return app.exec()


if __name__ == '__main__':
    sys.exit(main()) 