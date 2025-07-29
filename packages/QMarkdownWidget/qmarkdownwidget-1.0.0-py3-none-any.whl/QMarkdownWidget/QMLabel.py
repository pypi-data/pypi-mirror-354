import re
import markdown2
from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QTextDocument, QAbstractTextDocumentLayout, QMouseEvent


class QMLabel(QLabel):
    """
    支持Markdown渲染的标签控件
    继承自QLabel，具有QLabel的所有特性：
    - 无滚动条
    - 大小随内容缩放
    - 鼠标无法选中文字
    - 不可编辑
    - 支持QSS样式
    """
    
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self._markdown_text = ""
        self._enable_markdown = True
        
        # 设置基本属性，使其表现像QLabel
        self.setWordWrap(True)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        
        # 如果提供了初始文本，设置它
        if text:
            self.setText(text)
    
    def setText(self, text):
        """设置要显示的文本，支持Markdown语法"""
        self._markdown_text = text
        
        if self._enable_markdown and text:
            # 将Markdown转换为HTML
            html_content = self._markdown_to_html(text)
            # 使用父类的setText方法设置HTML内容
            super().setText(html_content)
        else:
            # 如果禁用Markdown或文本为空，直接设置纯文本
            super().setText(text)
        
        # 确保文本不可选中（特别是在设置HTML后）
        self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
    
    def text(self):
        """获取原始Markdown文本"""
        return self._markdown_text
    
    def setMarkdownEnabled(self, enabled):
        """启用或禁用Markdown渲染"""
        self._enable_markdown = enabled
        # 重新渲染文本
        self.setText(self._markdown_text)
    
    def isMarkdownEnabled(self):
        """检查是否启用了Markdown渲染"""
        return self._enable_markdown
        
    def _markdown_to_html(self, markdown_text):
        """将Markdown文本转换为HTML"""
        if not markdown_text:
            return ""
            
        # 预处理文本，处理一些特殊情况
        processed_text = self._preprocess_markdown(markdown_text)
        
        # 使用markdown2转换为HTML
        html_content = markdown2.markdown(
            processed_text, 
            extras=[
                'fenced-code-blocks',
                'tables',
                'break-on-newline',
                'cuddled-lists',
                'metadata',
                'nofollow',
                'pyshell',
                'spoiler',
                'strike',
                'target-blank-links',
                'task_list',
                'wiki-tables'
            ]
        )
        
        # 后处理HTML，添加样式和修复
        processed_html = self._postprocess_html(html_content)
        
        return processed_html
    
    def _preprocess_markdown(self, text):
        """预处理Markdown文本"""
        # 处理LaTeX公式，将其转换为适合在QLabel中显示的格式
        # 由于QLabel不支持MathJax，我们将LaTeX公式标记出来
        
        # 处理块级公式 $$...$$
        text = re.sub(r'\$\$(.*?)\$\$', r'<div class="latex-block">[数学公式: \1]</div>', text, flags=re.DOTALL)

        # 处理行内公式 $...$
        text = re.sub(r'\$(.*?)\$', r'<span class="latex-inline">[公式: \1]</span>', text)
        
        # 处理 \[...\] 和 \(...\) 格式
        text = re.sub(r'\\\[(.*?)\\\]', r'<div class="latex-block">[数学公式: \1]</div>', text, flags=re.DOTALL)
        text = re.sub(r'\\\((.*?)\\\)', r'<span class="latex-inline">[公式: \1]</span>', text)
        
        return text
    
    def _postprocess_html(self, html):
        """后处理HTML内容"""
        if not html:
            return ""
        
        # 添加内联样式，确保在QLabel中正确显示
        styled_html = f"""
        <div style="
            font-family: inherit;
            line-height: 1.6;
            color: inherit;
            margin: 0;
            padding: 0;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
            cursor: default;
        ">
            {html}
        </div>
        """
        
        # 修复一些HTML标签以确保在QLabel中正确显示
        styled_html = self._fix_html_for_qlabel(styled_html)
        
        return styled_html
    
    def _fix_html_for_qlabel(self, html):
        """修复HTML以确保在QLabel中正确显示"""
        # QLabel支持的HTML子集相对有限，我们需要简化一些标签
        
        # 添加LaTeX公式的样式
        html = html.replace('<span class="latex-inline">',
                          '<span style="color: #2e7d32; font-family: monospace; background-color: #f0f8ff; padding: 2px;">')
        html = html.replace('<div class="latex-block">',
                          '<div style="color: #2e7d32; font-family: monospace; background-color: #f0f8ff; padding: 8px; margin: 8px 0; border-left: 3px solid #2e7d32;">')
        
        # 为代码块添加样式
        html = re.sub(r'<pre><code>(.*?)</code></pre>',
                     r'<div style="background-color: #f8f8f8; padding: 10px; margin: 10px 0; border: 1px solid #e0e0e0; font-family: monospace;"><code>\1</code></div>',
                     html, flags=re.DOTALL)
        
        # 为行内代码添加样式
        html = re.sub(r'<code>(.*?)</code>',
                     r'<code style="background-color: #f0f0f0; padding: 2px 4px; font-family: monospace; font-size: 0.9em;">\1</code>',
                     html)
        
        # 为引用添加样式
        html = re.sub(r'<blockquote>(.*?)</blockquote>',
                     r'<div style="border-left: 4px solid #4CAF50; padding-left: 1em; margin: 1em 0; color: #555; background-color: #f9f9f9; padding: 8px 12px;">\1</div>',
                     html, flags=re.DOTALL)
        
        # 为表格添加基本样式（QLabel对表格支持有限）
        html = re.sub(r'<table>', r'<table style="border-collapse: collapse; margin: 10px 0;">', html)
        html = re.sub(r'<th>', r'<th style="border: 1px solid #ddd; padding: 6px; background-color: #f2f2f2; font-weight: bold;">', html)
        html = re.sub(r'<td>', r'<td style="border: 1px solid #ddd; padding: 6px;">', html)
        
        return html
    
    def sizeHint(self):
        """返回控件的推荐大小"""
        if not self.text():
            return QSize(0, 0)
        
        # 使用QLabel的默认sizeHint
        return super().sizeHint()
    
    def minimumSizeHint(self):
        """返回控件的最小大小"""
        if not self.text():
            return QSize(0, 0)
        
        return super().minimumSizeHint()
    
    def hasHeightForWidth(self):
        """支持高度随宽度变化"""
        return self.wordWrap()
    
    def heightForWidth(self, width):
        """根据给定宽度计算高度"""
        return super().heightForWidth(width)
    
    # 重载QLabel的一些方法以保持兼容性
    
    def setFont(self, font):
        """设置字体"""
        super().setFont(font)
        # 如果有Markdown内容，重新渲染
        if self._markdown_text:
            self.setText(self._markdown_text)
    
    def setAlignment(self, alignment):
        """设置对齐方式"""
        super().setAlignment(alignment)
    
    def setWordWrap(self, wrap):
        """设置自动换行"""
        super().setWordWrap(wrap)
    
    def setTextInteractionFlags(self, flags):
        """设置文本交互标志"""
        super().setTextInteractionFlags(flags)
    
    def setStyleSheet(self, styleSheet):
        """设置样式表（支持QSS）"""
        super().setStyleSheet(styleSheet)
        
    # 添加一些便利方法
    
    def setPlainText(self, text):
        """设置纯文本（不进行Markdown渲染）"""
        self._markdown_text = text
        super().setText(text)
    
    def toPlainText(self):
        """获取纯文本版本"""
        return self._markdown_text
    
    def toHtml(self):
        """获取HTML版本"""
        if self._enable_markdown and self._markdown_text:
            return self._markdown_to_html(self._markdown_text)
        else:
            return self._markdown_text
    
    # 重写鼠标事件以防止文本选择
    
    def mousePressEvent(self, event):
        """阻止鼠标按下事件的默认行为"""
        event.accept()
    
    def mouseMoveEvent(self, event):
        """阻止鼠标移动事件的默认行为"""
        event.accept()
    
    def mouseReleaseEvent(self, event):
        """阻止鼠标释放事件的默认行为"""
        event.accept()
        
    def mouseDoubleClickEvent(self, event):
        """阻止鼠标双击事件的默认行为"""
        event.accept()
        
    def contextMenuEvent(self, event):
        """阻止上下文菜单事件的默认行为"""
        event.accept() 