import re
import markdown2
from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QTextDocument, QAbstractTextDocumentLayout, QMouseEvent


class QMLabel(QLabel):
    """
    A label control supporting Markdown rendering
    Inherits from QLabel, with all QLabel features:
    - No scrollbar
    - Size adjusts with content
    - Text cannot be selected with mouse
    - Non-editable
    - Supports QSS styling
    """
    
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self._markdown_text = ""
        self._enable_markdown = True
        
        # Set basic properties to make it behave like a QLabel
        self.setWordWrap(True)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        
        # If initial text is provided, set it
        if text:
            self.setText(text)
    
    def setText(self, text):
        """Set the text to display, supports Markdown syntax"""
        self._markdown_text = text
        
        if self._enable_markdown and text:
            # Convert Markdown to HTML
            html_content = self._markdown_to_html(text)
            # Use the parent's setText method to set the HTML content
            super().setText(html_content)
        else:
            # If Markdown is disabled or the text is empty, set plain text directly
            super().setText(text)
        
        # Ensure text is not selectable (especially after setting HTML)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
    
    def text(self):
        """Get the original Markdown text"""
        return self._markdown_text
    
    def setMarkdownEnabled(self, enabled):
        """Enable or disable Markdown rendering"""
        self._enable_markdown = enabled
        # Re-render text
        self.setText(self._markdown_text)
    
    def isMarkdownEnabled(self):
        """Check if Markdown rendering is enabled"""
        return self._enable_markdown
        
    def _markdown_to_html(self, markdown_text):
        """Convert Markdown text to HTML"""
        if not markdown_text:
            return ""
            
        # Preprocess the text to handle some special cases
        processed_text = self._preprocess_markdown(markdown_text)
        
        # Convert to HTML using markdown2
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
        
        # Post-process HTML, add styles and fixes
        processed_html = self._postprocess_html(html_content)
        
        return processed_html
    
    def _preprocess_markdown(self, text):
        """Preprocess Markdown text"""
        # Process LaTeX equations, converting them to a format suitable for display in QLabel
        # Since QLabel does not support MathJax, we mark LaTeX equations
        
        # Process block-level formulas $$...$$
        text = re.sub(r'\$\$(.*?)\$\$', r'<div class="latex-block">[Math Formula: \1]</div>', text, flags=re.DOTALL)

        # Process inline formulas $...$
        text = re.sub(r'\$(.*?)\$', r'<span class="latex-inline">[Formula: \1]</span>', text)
        
        # Process \[...\] and \(...\) formats
        text = re.sub(r'\\\[(.*?)\\\]', r'<div class="latex-block">[Math Formula: \1]</div>', text, flags=re.DOTALL)
        text = re.sub(r'\\\((.*?)\\\)', r'<span class="latex-inline">[Formula: \1]</span>', text)
        
        return text
    
    def _postprocess_html(self, html):
        """Post-process HTML, add styles and fixes"""
        # Add basic styles for Markdown elements
        html = f"""
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                font-size: 14px;
                line-height: 1.6;
                color: #333;
            }}
            p {{
                margin: 0.5em 0;
            }}
            h1, h2, h3, h4, h5, h6 {{
                margin: 0.8em 0 0.5em;
                font-weight: bold;
            }}
            h1 {{
                font-size: 1.8em;
            }}
            h2 {{
                font-size: 1.5em;
            }}
            h3 {{
                font-size: 1.3em;
            }}
            ul, ol {{
                margin: 0.5em 0;
                padding-left: 2em;
            }}
            li {{
                margin: 0.3em 0;
            }}
            code {{
                font-family: monospace;
                background-color: #f0f0f0;
                padding: 0.2em 0.4em;
                border-radius: 3px;
            }}
            pre {{
                background-color: #f0f0f0;
                padding: 1em;
                border-radius: 4px;
                overflow-x: auto;
                margin: 0.5em 0;
            }}
            pre code {{
                background-color: transparent;
                padding: 0;
            }}
            blockquote {{
                border-left: 4px solid #4CAF50;
                padding-left: 1em;
                margin: 1em 0;
                color: #555;
                background-color: #f9f9f9;
                padding: 8px 12px;
            }}
            table {{
                border-collapse: collapse;
                margin: 10px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 6px;
            }}
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            a {{
                color: #0066cc;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .latex-block {{
                color: #0066cc;
                font-style: italic;
                background-color: #f0f8ff;
                padding: 5px;
                border-radius: 3px;
                margin: 5px 0;
                display: block;
            }}
            .latex-inline {{
                color: #0066cc;
                font-style: italic;
                background-color: #f0f8ff;
                padding: 2px 4px;
                border-radius: 3px;
            }}
        </style>
        {html}
        """
        
        # Fix some HTML tags to ensure correct display in QLabel
        styled_html = self._fix_html_for_qlabel(html)
        
        return styled_html
    
    def _fix_html_for_qlabel(self, html):
        """Fix HTML for QLabel display"""
        # Fix for code blocks (QLabel does not handle <pre> well, so we use div with style)
        html = re.sub(r'<pre><code>(.*?)</code></pre>', r'<div style="background-color: #f0f0f0; padding: 10px; border-radius: 4px; font-family: monospace; white-space: pre-wrap; overflow-x: hidden; margin: 10px 0;">\1</div>', html, flags=re.DOTALL)
        html = re.sub(r'<pre>(.*?)</pre>', r'<div style="background-color: #f0f0f0; padding: 10px; border-radius: 4px; font-family: monospace; white-space: pre-wrap; overflow-x: hidden; margin: 10px 0;">\1</div>', html, flags=re.DOTALL)
        
        # Add styles for LaTeX formulas
        html = html.replace('<span class="latex-inline">',
                          '<span style="color: #2e7d32; font-family: monospace; background-color: #f0f8ff; padding: 2px;">')
        html = html.replace('<div class="latex-block">',
                          '<div style="color: #2e7d32; font-family: monospace; background-color: #f0f8ff; padding: 8px; margin: 8px 0; border-left: 3px solid #2e7d32;">')
        
        # Add basic styles for tables (QLabel has limited support for tables)
        html = re.sub(r'<table>', r'<table style="border-collapse: collapse; margin: 10px 0;">', html)
        html = re.sub(r'<th>', r'<th style="border: 1px solid #ddd; padding: 6px; background-color: #f2f2f2; font-weight: bold;">', html)
        html = re.sub(r'<td>', r'<td style="border: 1px solid #ddd; padding: 6px;">', html)
        
        return html
    
    def sizeHint(self):
        """Return recommended size for the widget"""
        if not self.text():
            return QSize(0, 0)
        
        # Use QLabel's default sizeHint
        return super().sizeHint()
    
    def minimumSizeHint(self):
        """Return minimum size for the widget"""
        if not self.text():
            return QSize(0, 0)
        
        return super().minimumSizeHint()
    
    def hasHeightForWidth(self):
        """Support height dependent on width"""
        return self.wordWrap()
    
    def heightForWidth(self, width):
        """Calculate height based on given width"""
        return super().heightForWidth(width)
    
    # Override some QLabel methods for compatibility
    
    def setFont(self, font):
        """Set font"""
        super().setFont(font)
        # If there is Markdown content, re-render
        if self._markdown_text:
            self.setText(self._markdown_text)
    
    def setAlignment(self, alignment):
        """Set alignment"""
        super().setAlignment(alignment)
    
    def setWordWrap(self, wrap):
        """Set word wrap"""
        super().setWordWrap(wrap)
    
    def setTextInteractionFlags(self, flags):
        """Set text interaction flags"""
        super().setTextInteractionFlags(flags)
    
    def setStyleSheet(self, styleSheet):
        """Set stylesheet (supports QSS)"""
        super().setStyleSheet(styleSheet)
        
    # Add some convenience methods
    
    def setPlainText(self, text):
        """Set plain text (no Markdown rendering)"""
        self._markdown_text = text
        super().setText(text)
    
    def toPlainText(self):
        """Get plain text version"""
        return self._markdown_text
    
    def toHtml(self):
        """Get HTML version"""
        if self._enable_markdown and self._markdown_text:
            return self._markdown_to_html(self._markdown_text)
        else:
            return self._markdown_text
    
    # Override mouse events to prevent text selection
    
    def mousePressEvent(self, event):
        """Prevent default behavior of mouse press event"""
        event.accept()
    
    def mouseMoveEvent(self, event):
        """Prevent default behavior of mouse move event"""
        event.accept()
    
    def mouseReleaseEvent(self, event):
        """Prevent default behavior of mouse release event"""
        event.accept()
        
    def mouseDoubleClickEvent(self, event):
        """Prevent default behavior of mouse double-click event"""
        event.accept()
        
    def contextMenuEvent(self, event):
        """Prevent default behavior of context menu event"""
        event.accept() 