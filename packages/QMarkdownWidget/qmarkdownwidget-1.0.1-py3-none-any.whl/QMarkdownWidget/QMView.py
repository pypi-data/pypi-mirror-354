import re
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
import markdown2


class QMView(QWidget):
    """
    A view control supporting Markdown and LaTeX rendering
    Based on QWebEngineView, with the following features:
    - Supports scrolling
    - Can select and copy text
    - Non-editable
    - Supports LaTeX mathematical equation rendering
    - Can be set to resize with content or maintain fixed size
    """
    
    # Signals
    contentChanged = pyqtSignal()  # Signal for content change
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._markdown_text = ""
        self._enable_markdown = True
        self._auto_resize = False  # We keep this variable, but no longer modify it through functions
        self._fixed_height = 300  # Fixed height when not auto-resizing
        self._max_auto_height = 800  # Maximum height limit for auto-resizing
        self._max_width = 0  # Store the maximum width value
        
        self.init_ui()
        self.setup_web_settings()
        
        # Create a delayed rendering timer
        self.render_timer = QTimer()
        self.render_timer.setSingleShot(True)
        self.render_timer.timeout.connect(self._render_content)
    
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)  # Set padding to show QMView border
        
        # Create QWebEngineView as a renderer
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
        # Set size policy
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Connect the page load finished signal
        self.web_view.loadFinished.connect(self._on_load_finished)
    
    def setup_web_settings(self):
        """Set up WebEngine configuration"""
        settings = self.web_view.settings()
        
        # Disable editing features
        settings.setAttribute(QWebEngineSettings.WebAttribute.FocusOnNavigationEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        
        # Allow text selection
        settings.setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, True)
        
        # Disable some unnecessary features
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
    
    def setText(self, text):
        """Set the text to display, supports Markdown syntax"""
        self._markdown_text = text
        
        # If auto height is set, use adaptive height rendering
        if hasattr(self, '_max_width') and self._max_width > 0:
            self._render_content_with_auto_height()
        else:
            # Use the original rendering method, ensuring scrolling is enabled
            self.render_timer.stop()
            self.render_timer.start(100)  # 100ms delay
    
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
    
    def setFixedViewHeight(self, height):
        """Set the fixed height in non-auto-resize mode"""
        self._fixed_height = max(50, height)
        
        # If not in auto-height mode, apply fixed height and enable scrolling
        if not hasattr(self, '_max_width') or self._max_width <= 0:
            self.setFixedHeight(self._fixed_height)
            
            # Enable internal scrolling
            if hasattr(self, 'web_view') and self.web_view.page():
                self.web_view.page().runJavaScript("""
                    document.body.style.overflow = 'auto';
                    document.documentElement.style.overflow = 'auto';
                """)
    
    def getFixedViewHeight(self):
        """Get the fixed height setting"""
        return self._fixed_height
    
    def setMaxAutoHeight(self, max_height):
        """Set the maximum height limit in auto-resize mode"""
        self._max_auto_height = max(100, max_height)
        if self._auto_resize:
            self._render_content()
    
    def getMaxAutoHeight(self):
        """Get the maximum height limit in auto-resize mode"""
        return self._max_auto_height
    
    def _render_content(self):
        """Render content to QWebEngineView"""
        if not self._markdown_text:
            self.web_view.setHtml("")
            return
        
        if self._enable_markdown:
            # Process LaTeX formulas
            processed_text, latex_blocks = self._process_latex(self._markdown_text)
            
            # Convert Markdown to HTML
            html_content = markdown2.markdown(
                processed_text, 
                extras=[
                    'fenced-code-blocks', 
                    'tables', 
                    'break-on-newline',
                    'cuddled-lists',
                    'strike',
                    'task_list',
                    'target-blank-links',
                ]
            )
            
            # Restore LaTeX placeholders
            for placeholder, latex_content in latex_blocks.items():
                # Since placeholders are included in the HTML, they need to be found and restored
                # Also need to unescape HTML entities
                html_content = html_content.replace(placeholder, latex_content)
            
            # Fix the impact of markdown2 on LaTeX content
            html_content = self._fix_latex_in_html(html_content)
            
        else:
            # Plain text mode
            html_content = f"<pre>{self._markdown_text}</pre>"
        
        # Generate the complete HTML document
        full_html = self._generate_html_template(html_content)
        
        # Set to WebView
        self.web_view.setHtml(full_html)
        
        # Enable internal scrolling in fixed height mode
        if not hasattr(self, '_max_width') or self._max_width <= 0:
            self.web_view.page().runJavaScript("""
                document.body.style.overflow = 'auto';
                document.documentElement.style.overflow = 'auto';
            """)
        
        # Emit content changed signal
        self.contentChanged.emit()
    
    def _process_latex(self, text):
        """
        Process LaTeX equations, ensuring MathJax can correctly parse
        Returns: (processed text, LaTeX placeholder dictionary)
        """
        # Core fix: remove special protection for tables.
        # The correct process is to protect all LaTeX first, and then let markdown2 handle all content including tables.
        
        latex_blocks = {}
        
        # Protect $$...$$ block formulas
        def protect_block_formula(match):
            content = match.group(1)
            placeholder = f"LATEXBLOCK{len(latex_blocks):04d}"
            latex_blocks[placeholder] = f"$${content}$$"
            return placeholder
        
        # Protect $...$ inline formulas  
        def protect_inline_formula(match):
            content = match.group(1)
            placeholder = f"LATEXINLINE{len(latex_blocks):04d}"
            latex_blocks[placeholder] = f"${content}$"
            return placeholder
        
        # Protect \[...\] block formulas
        def protect_bracket_formula(match):
            content = match.group(1)
            placeholder = f"LATEXBRACKET{len(latex_blocks):04d}"
            latex_blocks[placeholder] = f"$$\\[{content}\\]$$"  # Keep original format
            return placeholder
            
        # Protect \(...\) inline formulas
        def protect_paren_formula(match):
            content = match.group(1)
            placeholder = f"LATEXPAREN{len(latex_blocks):04d}"
            latex_blocks[placeholder] = f"\\({content}\\)"  # Keep original format
            return placeholder
        
        # Protect various LaTeX syntaxes in order, starting with the longest/most specific patterns
        text = re.sub(r'\$\$(.*?)\$\$', protect_block_formula, text, flags=re.DOTALL)
        text = re.sub(r'\\\[(.*?)\\\]', protect_bracket_formula, text, flags=re.DOTALL)
        text = re.sub(r'\\\((.*?)\\\)', protect_paren_formula, text, flags=re.DOTALL)
        text = re.sub(r'\$([^\$]+?)\$', protect_inline_formula, text) # Use non-greedy matching to avoid incorrect matches like $a$b$c$
        
        # Process other LaTeX environments
        def protect_env(match):
            env_name = match.group(1)
            content = match.group(2)
            placeholder = f"LATEXENV{len(latex_blocks):04d}"
            latex_blocks[placeholder] = f"\\begin{{{env_name}}}{content}\\end{{{env_name}}}"
            return placeholder
            
        # Protect common LaTeX environments
        envs = ['equation', 'align', 'matrix', 'pmatrix', 'bmatrix', 'vmatrix', 'Vmatrix']
        for env in envs:
            pattern = f'\\\\begin{{{env}}}(.*?)\\\\end{{{env}}}'
            text = re.sub(pattern, protect_env, text, flags=re.DOTALL)

        return text, latex_blocks
    
    def _fix_latex_in_html(self, html):
        """Fix LaTeX content in HTML, reverse HTML entity escaping"""
        def fix_latex_content(match):
            content = match.group(0)
            # Restore HTML entities inside LaTeX equations, e.g., &amp; -> &
            content = content.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            return content
        
        # Fix all types of formulas
        # Note: The regular expression needs to match the original format returned by the placeholder
        html = re.sub(r'\$\$(.*?)\$\$', fix_latex_content, html, flags=re.DOTALL)
        html = re.sub(r'\$([^\$]+?)\$', fix_latex_content, html)
        html = re.sub(r'\\\[(.*?)\\\]', fix_latex_content, html, flags=re.DOTALL)
        html = re.sub(r'\\\((.*?)\\\)', fix_latex_content, html, flags=re.DOTALL)
        html = re.sub(r'\\begin\{(.*?)\}(.*?)\\end\{(.*?)\}', fix_latex_content, html, flags=re.DOTALL)
        
        return html
    
    def _generate_html_template(self, html_content):
        """Generate complete HTML template"""
        # Set body style based on whether auto-resizing is enabled
        body_style = "margin: 10px; line-height: 1.6; color: #333; font-size: 14px; font-family: 'Arial', 'Helvetica Neue', sans-serif;"
        
        if self._auto_resize:
            # Auto-resize mode: disable internal scrolling, fully expand height
            body_style += " overflow: hidden;"
        else:
            # Fixed-height mode: enable internal scrolling
            body_style += " overflow: auto;"
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <script>
            window.MathJax = {{
              tex: {{
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true,
                tags: 'ams'
              }},
              svg: {{
                fontCache: 'global'
              }},
              startup: {{
                ready: () => {{
                  MathJax.startup.defaultReady();
                  MathJax.startup.promise.then(() => {{
                    // After math formulas are rendered, adjust height if auto-resizing is enabled
                    if (window.autoResize) {{
                      setTimeout(updateHeight, 100);
                    }}
                  }});
                }}
              }}
            }};
            
            window.autoResize = {str(self._auto_resize).lower()};
            
            function updateHeight() {{
              if (window.autoResize) {{
                const body = document.body;
                const html = document.documentElement;
                const height = Math.max(
                  body.scrollHeight,
                  body.offsetHeight,
                  html.clientHeight,
                  html.scrollHeight,
                  html.offsetHeight
                );
                
                // In auto-resize mode, only limit the maximum height
                const maxHeight = {self._max_auto_height};
                const finalHeight = Math.min(height, maxHeight);
                
                // Resize via Qt's interface
                if (window.qt && window.qt.webChannelTransport) {{
                  // Communicate with Qt via webChannel here
                }}
              }}
            }}
            </script>
            <script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js' async></script>
            <style>
                body {{ 
                    {body_style}
                    background-color: transparent;
                }}
                h1, h2, h3, h4, h5, h6 {{
                    color: #2c3e50;
                    margin-top: 1.2em;
                    margin-bottom: 0.6em;
                    font-weight: 600;
                }}
                h1 {{ font-size: 1.8em; }}
                h2 {{ font-size: 1.5em; }}
                h3 {{ font-size: 1.3em; }}
                h4 {{ font-size: 1.1em; }}
                p {{ 
                    margin: 0.6em 0;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }}
                pre {{ 
                    background: #f8f8f8; 
                    padding: 10px; 
                    border-radius: 5px; 
                    overflow-x: auto; 
                    border: 1px solid #e0e0e0;
                    margin: 1em 0;
                }}
                code {{ 
                    font-family: Consolas, Monaco, "Andale Mono", monospace;
                    font-size: 0.9em;
                    background-color: #f0f0f0;
                    padding: 2px 4px;
                    border-radius: 3px;
                }}
                pre code {{
                    background-color: transparent;
                    padding: 0;
                    border-radius: 0;
                }}
                .math {{ 
                    color: #2e7d32; 
                }}
                ul, ol {{
                    padding-left: 1.5em;
                    margin: 0.6em 0;
                }}
                li {{
                    margin: 0.3em 0;
                }}
                blockquote {{
                    border-left: 4px solid #4CAF50;
                    padding-left: 1em;
                    margin: 1em 0;
                    color: #555;
                    background-color: #f9f9f9;
                    padding: 8px 12px;
                    border-radius: 0 3px 3px 0;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 1em 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 6px 10px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                    font-weight: bold;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                strong {{ font-weight: bold; }}
                em {{ font-style: italic; }}
                
                /* Ensure text can be selected */
                * {{
                    -webkit-user-select: text;
                    -moz-user-select: text;
                    -ms-user-select: text;
                    user-select: text;
                }}
            </style>
        </head>
        <body>
            {html_content}
            <script>
                document.addEventListener("DOMContentLoaded", function() {{
                    if (window.MathJax) {{
                        window.MathJax.typeset && window.MathJax.typeset();
                    }}
                    
                    // Initialize height adjustment
                    if (window.autoResize) {{
                        setTimeout(updateHeight, 500);
                    }}
                }});
                
                // Listen for window size changes
                window.addEventListener('resize', function() {{
                    if (window.autoResize) {{
                        setTimeout(updateHeight, 100);
                    }}
                }});
            </script>
        </body>
        </html>
        """ 
    
    def _on_load_finished(self, success):
        """Handle post-page load"""
        if success and self._auto_resize:
            # Delay resizing to wait for MathJax rendering to complete
            QTimer.singleShot(1000, self._adjust_height)
    
    def _adjust_height(self):
        """Adjust widget height to fit content"""
        if not self._auto_resize:
            return
            
        # Get the actual page height via JavaScript
        self.web_view.page().runJavaScript(
            """
            Math.max(
                document.body.scrollHeight,
                document.body.offsetHeight,
                document.documentElement.clientHeight,
                document.documentElement.scrollHeight,
                document.documentElement.offsetHeight
            );
            """,
            self._set_content_height
        )
    
    def _set_content_height(self, height):
        """Set content height"""
        if height and self._auto_resize:
            # In auto-resize mode, the height fully adapts to the content, with no maximum height limit
            content_height = height + 20  # Add some margin
            
            # Fully display content, no height limit
            self.setMinimumHeight(int(content_height))
            self.setMaximumHeight(int(content_height))
            
            # In auto-resize mode, always disable internal scrolling
            self.web_view.page().runJavaScript("""
                document.body.style.overflow = 'hidden';
                document.documentElement.style.overflow = 'hidden';
            """)
            
            self.updateGeometry()
    
    # Convenience methods
    
    def setPlainText(self, text):
        """Set plain text (no Markdown rendering)"""
        self._enable_markdown = False
        self.setText(text)
    
    def toPlainText(self):
        """Get plain text version"""
        return self._markdown_text
    
    def toHtml(self):
        """Get HTML version"""
        if self._enable_markdown and self._markdown_text:
            processed_text, latex_blocks = self._process_latex(self._markdown_text)
            html = markdown2.markdown(processed_text, extras=['fenced-code-blocks', 'tables', 'break-on-newline'])
            # Restore LaTeX
            for placeholder, latex_content in latex_blocks.items():
                html = html.replace(placeholder, latex_content)
            # Fix the impact of markdown2 on LaTeX content
            html = self._fix_latex_in_html(html)
            return html
        else:
            return self._markdown_text
    
    def clear(self):
        """Clear content"""
        self.setText("")
    
    def sizeHint(self):
        """Return the recommended size of the widget"""
        if self._auto_resize:
            return QSize(400, 100)  # Initial size in auto-resize mode
        else:
            return QSize(400, self._fixed_height)
    
    def minimumSizeHint(self):
        """Return the minimum size of the widget"""
        if self._auto_resize:
            return QSize(200, 50)  # Minimum size in auto-resize mode
        else:
            return QSize(200, self._fixed_height)
    
    def setAutoHeight(self, max_width):
        """
        Set automatic height adjustment, and limit maximum width
        
        Rules:
        1. If all text lines are less than max_width, set the widget width to the actual width of the longest line
        2. If any line exceeds max_width, the width is fixed to max_width, and the excess is automatically wrapped
        3. After setting the width, the height is automatically adjusted to just wrap all content
        
        Parameters:
            max_width: Maximum width of the widget (pixels)
        """
        # Ensure minimum width is at least 50px
        max_width = max(max_width, 50)
        
        # Store maximum width value
        self._max_width = max_width
        
        # Enable automatic height adjustment
        self._auto_resize = True
        
        # Disconnect previous connection (if any)
        try:
            self.web_view.loadFinished.disconnect(self._on_content_loaded)
        except:
            pass
        
        # Set initial width and height
        self.setFixedWidth(max_width)
        self.setFixedHeight(50)  # Set a small initial height first
        
        # Connect load completion signal
        self.web_view.loadFinished.connect(self._on_content_loaded)
        
        # Render content
        self._render_content_with_auto_height()
    
    def disableAutoHeight(self):
        """
        Disable automatic height adjustment, reset to fixed height mode
        """
        # Reset automatic height flag
        self._max_width = 0
        self._auto_resize = False
        
        # Set to fixed height
        self.setFixedHeight(self._fixed_height)
        
        # Ensure internal scrolling is enabled
        if hasattr(self, 'web_view') and self.web_view.page():
            self.web_view.page().runJavaScript("""
                document.body.style.overflow = 'auto';
                document.documentElement.style.overflow = 'auto';
            """)
        
        # Re-render content to apply new settings
        if self._markdown_text:
            self._render_content()
    
    def _render_content_with_auto_height(self):
        """Render content with adaptive height"""
        # Core fix: Reset widget width to maximum width before rendering and measuring
        # This ensures that measurements are always taken in the same environment, breaking the feedback loop of shrinking width
        self.setFixedWidth(self._max_width)

        if not self._markdown_text:
            self.web_view.setHtml("")
            return
        
        if self._enable_markdown:
            # Process LaTeX formulas
            processed_text, latex_blocks = self._process_latex(self._markdown_text)
            
            # Convert Markdown to HTML
            html_content = markdown2.markdown(
                processed_text, 
                extras=[
                    'fenced-code-blocks', 
                    'tables', 
                    'break-on-newline',
                    'cuddled-lists',
                    'strike',
                    'task_list',
                    'target-blank-links',
                ]
            )
            
            # Restore LaTeX placeholders
            for placeholder, latex_content in latex_blocks.items():
                html_content = html_content.replace(placeholder, latex_content)
            
            # Fix markdown2's impact on LaTeX content
            html_content = self._fix_latex_in_html(html_content)
            
        else:
            # Plain text mode
            html_content = f"<pre>{self._markdown_text}</pre>"
        
        # HTML template
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    font-family: Arial, sans-serif;
                    font-size: 14px;
                    line-height: 1.6;
                    color: #333;
                    overflow: hidden;
                    display: inline-block; /* Force body contraction to fit content */
                }}
                
                #wrapper {{
                    max-width: {self._max_width}px;
                    padding: 2px 5px;
                    box-sizing: border-box;
                }}
                
                /* Eliminate bottom margin of the last element to reduce bottom white space */
                #wrapper > *:last-child {{
                    margin-bottom: 0 !important;
                }}

                p {{
                    margin: 0.2em 0;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }}
                
                pre {{
                    margin: 0.5em 0;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                    background-color: #f8f8f8;
                    padding: 5px;
                    border-radius: 4px;
                    overflow-x: hidden;
                }}
            </style>
            <script>
                // MathJax configuration, adding support for \(...\) and \[...\]
                window.MathJax = {{
                  tex: {{
                    inlineMath: [['$', '$'], ['\\(', '\\)']],
                    displayMath: [['$$', '$$'], ['\\[', '\\]']],
                    processEscapes: true
                  }},
                  svg: {{
                    fontCache: 'global'
                  }}
                }};
                
                function measureContent() {{
                    // Measure body's dimensions directly, as it's inline-block
                    const width = document.body.offsetWidth;
                    const height = document.body.offsetHeight;
                    
                    return {{
                        width: width,
                        height: height
                    }};
                }}
                
                // Measure immediately after DOM loads
                document.addEventListener('DOMContentLoaded', function() {{
                    // Measure once immediately
                    measureContent();
                    // Brief delay before measuring again, to ensure all content is rendered
                    setTimeout(measureContent, 10);
                }});
                
                // Measure immediately when window size changes
                window.addEventListener('resize', measureContent);
            </script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js" async></script>
        </head>
        <body>
            <div id="wrapper">{html_content}</div>
            <script>
                // Ensure MathJax rendering completes
                if (window.MathJax) {{
                    window.MathJax.startup = {{
                        ready: () => {{
                            MathJax.startup.defaultReady();
                            MathJax.startup.promise.then(() => {{
                                // Measure after MathJax rendering completes
                                setTimeout(measureContent, 100);
                            }});
                        }}
                    }};
                }}
            </script>
        </body>
        </html>
        """
        
        # Set to WebView
        self.web_view.setHtml(html)
    
    def _on_content_loaded(self, success):
        """Measure after content is loaded"""
        if success:
            # Reduce delay for faster measurement
            QTimer.singleShot(50, self._measure_content)
    
    def _measure_content(self):
        """Measure content dimensions"""
        # Run JavaScript measurement function
        self.web_view.page().runJavaScript("measureContent();", self._adjust_size)
    
    def _adjust_size(self, size):
        """Adjust widget size based on measurement"""
        if not size:
            return
        
        width = size.get('width', 0)
        
        if width:
            # Based on user feedback, if content width is less than max width, add 10px extra margin
            if width < self._max_width:
                final_width = min(width + 10, self._max_width)
            else:
                final_width = width
            
            # Ensure final width is not less than the 10px hard limit
            final_width = max(final_width, 10)
            
            self.setFixedWidth(int(final_width))
            
            # Update layout, need to re-measure to get the correct height
            self.updateGeometry()
            QTimer.singleShot(50, self._final_check)
    
    def _final_check(self):
        """Final check if dimensions are correct"""
        self.web_view.page().runJavaScript("measureContent();", self._final_adjust)
    
    def _final_adjust(self, size):
        """Final size adjustment"""
        if not size:
            return
        
        height = size.get('height', 0)
        
        if height:
            # Use the directly measured height without adding extra margin
            self.setFixedHeight(int(height))
            self.updateGeometry() 