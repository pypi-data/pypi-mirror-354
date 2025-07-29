import re
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
import markdown2


class QMView(QWidget):
    """
    支持Markdown和LaTeX渲染的视图控件
    基于QWebEngineView实现，具有以下特性：
    - 支持滚动
    - 可以选中和复制文本
    - 不可编辑
    - 支持LaTeX数学公式渲染
    - 可设置为随内容缩放或固定大小
    """
    
    # 信号
    contentChanged = pyqtSignal()  # 内容改变信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._markdown_text = ""
        self._enable_markdown = True
        self._auto_resize = False  # 这个变量我们保留，但不再通过函数修改它
        self._fixed_height = 300  # 非自动调整时的固定高度
        self._max_auto_height = 800  # 自动调整时的最大高度限制
        self._max_width = 0  # 存储最大宽度值
        
        self.init_ui()
        self.setup_web_settings()
        
        # 创建延迟渲染定时器
        self.render_timer = QTimer()
        self.render_timer.setSingleShot(True)
        self.render_timer.timeout.connect(self._render_content)
    
    def init_ui(self):
        """初始化UI组件"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)  # 设置内边距以显示QMView的边框
        
        # 创建QWebEngineView作为渲染器
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
        # 设置大小策略
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # 连接页面加载完成信号
        self.web_view.loadFinished.connect(self._on_load_finished)
    
    def setup_web_settings(self):
        """设置WebEngine配置"""
        settings = self.web_view.settings()
        
        # 禁用编辑功能
        settings.setAttribute(QWebEngineSettings.WebAttribute.FocusOnNavigationEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        
        # 允许文本选择
        settings.setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, True)
        
        # 禁用某些不需要的功能
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
    
    def setText(self, text):
        """设置要显示的文本，支持Markdown语法"""
        self._markdown_text = text
        
        # 如果设置了自动高度，使用自适应高度渲染
        if hasattr(self, '_max_width') and self._max_width > 0:
            self._render_content_with_auto_height()
        else:
            # 使用原始渲染方法，确保启用滚动
            self.render_timer.stop()
            self.render_timer.start(100)  # 100ms延迟
    
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
    
    def setFixedViewHeight(self, height):
        """设置非自动调整模式下的固定高度"""
        self._fixed_height = max(50, height)
        
        # 如果不是自动高度模式，应用固定高度并启用滚动
        if not hasattr(self, '_max_width') or self._max_width <= 0:
            self.setFixedHeight(self._fixed_height)
            
            # 启用内部滚动
            if hasattr(self, 'web_view') and self.web_view.page():
                self.web_view.page().runJavaScript("""
                    document.body.style.overflow = 'auto';
                    document.documentElement.style.overflow = 'auto';
                """)
    
    def getFixedViewHeight(self):
        """获取固定高度设置"""
        return self._fixed_height
    
    def setMaxAutoHeight(self, max_height):
        """设置自动调整模式下的最大高度限制"""
        self._max_auto_height = max(100, max_height)
        if self._auto_resize:
            self._render_content()
    
    def getMaxAutoHeight(self):
        """获取自动调整模式下的最大高度限制"""
        return self._max_auto_height
    
    def _render_content(self):
        """渲染内容到QWebEngineView"""
        if not self._markdown_text:
            self.web_view.setHtml("")
            return
        
        if self._enable_markdown:
            # 处理LaTeX公式
            processed_text, latex_blocks = self._process_latex(self._markdown_text)
            
            # 转换Markdown为HTML
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
            
            # 恢复LaTeX占位符
            for placeholder, latex_content in latex_blocks.items():
                # 由于placeholder被包含在HTML中，需要先找到它们并恢复
                # 同时需要反转义HTML实体
                html_content = html_content.replace(placeholder, latex_content)
            
            # 修复markdown2对LaTeX内容的影响
            html_content = self._fix_latex_in_html(html_content)
            
        else:
            # 纯文本模式
            html_content = f"<pre>{self._markdown_text}</pre>"
        
        # 生成完整的HTML文档
        full_html = self._generate_html_template(html_content)
        
        # 设置到WebView
        self.web_view.setHtml(full_html)
        
        # 在固定高度模式下启用内部滚动
        if not hasattr(self, '_max_width') or self._max_width <= 0:
            self.web_view.page().runJavaScript("""
                document.body.style.overflow = 'auto';
                document.documentElement.style.overflow = 'auto';
            """)
        
        # 发出内容改变信号
        self.contentChanged.emit()
    
    def _process_latex(self, text):
        """
        处理LaTeX公式，确保MathJax可以正确解析
        返回: (处理后的文本, LaTeX占位符字典)
        """
        # 核心修复：移除对表格的特殊保护。
        # 正确的流程是先保护所有LaTeX，然后再让markdown2处理包括表格在内的所有内容。
        
        latex_blocks = {}
        
        # 保护 $$...$$ 块级公式
        def protect_block_formula(match):
            content = match.group(1)
            placeholder = f"LATEXBLOCK{len(latex_blocks):04d}"
            latex_blocks[placeholder] = f"$${content}$$"
            return placeholder
        
        # 保护 $...$ 行内公式  
        def protect_inline_formula(match):
            content = match.group(1)
            placeholder = f"LATEXINLINE{len(latex_blocks):04d}"
            latex_blocks[placeholder] = f"${content}$"
            return placeholder
        
        # 保护 \[...\] 块级公式
        def protect_bracket_formula(match):
            content = match.group(1)
            placeholder = f"LATEXBRACKET{len(latex_blocks):04d}"
            latex_blocks[placeholder] = f"$$\\[{content}\\]$$"  # 保持原始格式
            return placeholder
            
        # 保护 \(...\) 行内公式
        def protect_paren_formula(match):
            content = match.group(1)
            placeholder = f"LATEXPAREN{len(latex_blocks):04d}"
            latex_blocks[placeholder] = f"\\({content}\\)"  # 保持原始格式
            return placeholder
        
        # 依次保护各种LaTeX语法，注意保护顺序，从最长的/最明确的模式开始
        text = re.sub(r'\$\$(.*?)\$\$', protect_block_formula, text, flags=re.DOTALL)
        text = re.sub(r'\\\[(.*?)\\\]', protect_bracket_formula, text, flags=re.DOTALL)
        text = re.sub(r'\\\((.*?)\\\)', protect_paren_formula, text, flags=re.DOTALL)
        text = re.sub(r'\$([^\$]+?)\$', protect_inline_formula, text) # 使用非贪婪匹配，避免$a$b$c$这样的错误匹配
        
        # 处理其他LaTeX环境
        def protect_env(match):
            env_name = match.group(1)
            content = match.group(2)
            placeholder = f"LATEXENV{len(latex_blocks):04d}"
            latex_blocks[placeholder] = f"\\begin{{{env_name}}}{content}\\end{{{env_name}}}"
            return placeholder
            
        # 保护常见的LaTeX环境
        envs = ['equation', 'align', 'matrix', 'pmatrix', 'bmatrix', 'vmatrix', 'Vmatrix']
        for env in envs:
            pattern = f'\\\\begin{{{env}}}(.*?)\\\\end{{{env}}}'
            text = re.sub(pattern, protect_env, text, flags=re.DOTALL)

        return text, latex_blocks
    
    def _fix_latex_in_html(self, html):
        """修复HTML中的LaTeX内容，反转义HTML实体"""
        def fix_latex_content(match):
            content = match.group(0)
            # 在LaTeX公式内部还原HTML实体，例如 &amp; -> &
            content = content.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            return content
        
        # 修复所有类型的公式
        # 注意: 正则表达式需要匹配占位符返回的原始格式
        html = re.sub(r'\$\$(.*?)\$\$', fix_latex_content, html, flags=re.DOTALL)
        html = re.sub(r'\$([^\$]+?)\$', fix_latex_content, html)
        html = re.sub(r'\\\[(.*?)\\\]', fix_latex_content, html, flags=re.DOTALL)
        html = re.sub(r'\\\((.*?)\\\)', fix_latex_content, html, flags=re.DOTALL)
        html = re.sub(r'\\begin\{(.*?)\}(.*?)\\end\{(.*?)\}', fix_latex_content, html, flags=re.DOTALL)
        
        return html
    
    def _generate_html_template(self, html_content):
        """生成完整的HTML模板"""
        # 根据是否自动调整大小来设置body样式
        body_style = "margin: 10px; line-height: 1.6; color: #333; font-size: 14px; font-family: 'Arial', 'Helvetica Neue', sans-serif;"
        
        if self._auto_resize:
            # 自动调整模式：禁用内部滚动，高度完全展开
            body_style += " overflow: hidden;"
        else:
            # 固定高度模式：启用内部滚动
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
                    // 数学公式渲染完成后，如果启用了自动调整大小，则调整高度
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
                
                // 在自动调整模式下，只限制最大高度
                const maxHeight = {self._max_auto_height};
                const finalHeight = Math.min(height, maxHeight);
                
                // 通过Qt的接口调整大小
                if (window.qt && window.qt.webChannelTransport) {{
                  // 这里可以通过webChannel与Qt通信
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
                
                /* 确保可以选择文本 */
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
                    
                    // 初始化高度调整
                    if (window.autoResize) {{
                        setTimeout(updateHeight, 500);
                    }}
                }});
                
                // 监听窗口大小变化
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
        """页面加载完成后的处理"""
        if success and self._auto_resize:
            # 延迟一段时间后调整大小，等待MathJax渲染完成
            QTimer.singleShot(1000, self._adjust_height)
    
    def _adjust_height(self):
        """调整控件高度以适应内容"""
        if not self._auto_resize:
            return
            
        # 通过JavaScript获取页面实际高度
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
        """设置内容高度"""
        if height and self._auto_resize:
            # 在自动调整模式下，高度完全适应内容，无最大高度限制
            content_height = height + 20  # 添加一些边距
            
            # 完全显示内容，不进行高度限制
            self.setMinimumHeight(int(content_height))
            self.setMaximumHeight(int(content_height))
            
            # 自动调整模式下，始终禁用内部滚动
            self.web_view.page().runJavaScript("""
                document.body.style.overflow = 'hidden';
                document.documentElement.style.overflow = 'hidden';
            """)
            
            self.updateGeometry()
    
    # 便利方法
    
    def setPlainText(self, text):
        """设置纯文本（不进行Markdown渲染）"""
        self._enable_markdown = False
        self.setText(text)
    
    def toPlainText(self):
        """获取纯文本版本"""
        return self._markdown_text
    
    def toHtml(self):
        """获取HTML版本"""
        if self._enable_markdown and self._markdown_text:
            processed_text, latex_blocks = self._process_latex(self._markdown_text)
            html = markdown2.markdown(processed_text, extras=['fenced-code-blocks', 'tables', 'break-on-newline'])
            # 恢复LaTeX
            for placeholder, latex_content in latex_blocks.items():
                html = html.replace(placeholder, latex_content)
            # 修复markdown2对LaTeX内容的影响
            html = self._fix_latex_in_html(html)
            return html
        else:
            return self._markdown_text
    
    def clear(self):
        """清空内容"""
        self.setText("")
    
    def sizeHint(self):
        """返回控件的推荐大小"""
        if self._auto_resize:
            return QSize(400, 100)  # 自动调整模式下的初始大小
        else:
            return QSize(400, self._fixed_height)
    
    def minimumSizeHint(self):
        """返回控件的最小大小"""
        if self._auto_resize:
            return QSize(200, 50)  # 自动调整模式下的最小大小
        else:
            return QSize(200, self._fixed_height)
    
    def setAutoHeight(self, max_width):
        """
        设置自动高度调整，并限制最大宽度
        
        规则:
        1. 如果所有文本行宽度都小于max_width，则控件宽度设为最长行的实际宽度
        2. 如果任一行超过max_width，则宽度固定为max_width，超出部分自动换行
        3. 设置完宽度后，高度自动调整为刚好包裹所有内容
        
        参数:
            max_width: 控件的最大宽度（像素）
        """
        # 确保最小宽度至少为50px
        max_width = max(max_width, 50)
        
        # 存储最大宽度值
        self._max_width = max_width
        
        # 启用自动调整高度
        self._auto_resize = True
        
        # 断开之前的连接（如果有）
        try:
            self.web_view.loadFinished.disconnect(self._on_content_loaded)
        except:
            pass
        
        # 设置初始宽度和高度
        self.setFixedWidth(max_width)
        self.setFixedHeight(50)  # 先设置一个小的初始高度
        
        # 连接加载完成信号
        self.web_view.loadFinished.connect(self._on_content_loaded)
        
        # 渲染内容
        self._render_content_with_auto_height()
    
    def disableAutoHeight(self):
        """
        禁用自动高度调整，重置为固定高度模式
        """
        # 重置自动高度标志
        self._max_width = 0
        self._auto_resize = False
        
        # 设置为固定高度
        self.setFixedHeight(self._fixed_height)
        
        # 确保启用内部滚动
        if hasattr(self, 'web_view') and self.web_view.page():
            self.web_view.page().runJavaScript("""
                document.body.style.overflow = 'auto';
                document.documentElement.style.overflow = 'auto';
            """)
        
        # 重新渲染内容以应用新设置
        if self._markdown_text:
            self._render_content()
    
    def _render_content_with_auto_height(self):
        """使用自适应高度渲染内容"""
        # 核心修复：在渲染和测量前，先将控件宽度重置为最大宽度。
        # 这能确保每次测量都在同样的环境下进行，从而打破宽度不断缩小的反馈循环。
        self.setFixedWidth(self._max_width)

        if not self._markdown_text:
            self.web_view.setHtml("")
            return
        
        if self._enable_markdown:
            # 处理LaTeX公式
            processed_text, latex_blocks = self._process_latex(self._markdown_text)
            
            # 转换Markdown为HTML
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
            
            # 恢复LaTeX占位符
            for placeholder, latex_content in latex_blocks.items():
                html_content = html_content.replace(placeholder, latex_content)
            
            # 修复markdown2对LaTeX内容的影响
            html_content = self._fix_latex_in_html(html_content)
            
        else:
            # 纯文本模式
            html_content = f"<pre>{self._markdown_text}</pre>"
        
        # HTML模板
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
                    display: inline-block; /* 强制body收缩以适应内容 */
                }}
                
                #wrapper {{
                    max-width: {self._max_width}px;
                    padding: 2px 5px;
                    box-sizing: border-box;
                }}
                
                /* 消除最后一个元素的下边距，减少底部留白 */
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
                // MathJax配置，增加对\(...\)和\[...\]的支持
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
                    // 直接测量body的尺寸，因为它是inline-block
                    const width = document.body.offsetWidth;
                    const height = document.body.offsetHeight;
                    
                    return {{
                        width: width,
                        height: height
                    }};
                }}
                
                // 在DOM加载完成后立即执行测量
                document.addEventListener('DOMContentLoaded', function() {{
                    // 立即测量一次
                    measureContent();
                    // 短暂延迟后再测量一次，确保所有内容已渲染
                    setTimeout(measureContent, 10);
                }});
                
                // 在窗口大小改变时立即重新测量
                window.addEventListener('resize', measureContent);
            </script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js" async></script>
        </head>
        <body>
            <div id="wrapper">{html_content}</div>
            <script>
                // 确保MathJax渲染完成
                if (window.MathJax) {{
                    window.MathJax.startup = {{
                        ready: () => {{
                            MathJax.startup.defaultReady();
                            MathJax.startup.promise.then(() => {{
                                // MathJax渲染完成后重新测量
                                setTimeout(measureContent, 100);
                            }});
                        }}
                    }};
                }}
            </script>
        </body>
        </html>
        """
        
        # 设置到WebView
        self.web_view.setHtml(html)
    
    def _on_content_loaded(self, success):
        """页面加载完成后进行测量"""
        if success:
            # 减少延迟时间，加快测量
            QTimer.singleShot(50, self._measure_content)
    
    def _measure_content(self):
        """测量内容尺寸"""
        # 运行JavaScript测量函数
        self.web_view.page().runJavaScript("measureContent();", self._adjust_size)
    
    def _adjust_size(self, size):
        """根据测量结果调整控件尺寸"""
        if not size:
            return
        
        width = size.get('width', 0)
        
        if width:
            # 根据用户反馈，如果内容宽度小于最大宽度，则增加10px的额外边距
            if width < self._max_width:
                final_width = min(width + 10, self._max_width)
            else:
                final_width = width
            
            # 确保最终宽度不小于10px的硬性限制
            final_width = max(final_width, 10)
            
            self.setFixedWidth(int(final_width))
            
            # 更新布局后，需要重新测量以获得正确的高度
            self.updateGeometry()
            QTimer.singleShot(50, self._final_check)
    
    def _final_check(self):
        """最终检查尺寸是否正确"""
        self.web_view.page().runJavaScript("measureContent();", self._final_adjust)
    
    def _final_adjust(self, size):
        """最终调整尺寸"""
        if not size:
            return
        
        height = size.get('height', 0)
        
        if height:
            # 直接使用测量到的高度，不再添加额外边距
            self.setFixedHeight(int(height))
            self.updateGeometry() 