"""
QMarkdownWidget - 支持 Markdown 和 LaTeX 的 Qt 组件库

基于不同技术实现的Markdown渲染控件：
- QMLabel: 基于QLabel的轻量级Markdown控件（不支持LaTeX渲染）
- QMView: 基于QWebEngineView的完整Markdown+LaTeX控件（支持滚动和文本选择）
"""

from .QMLabel import QMLabel
from .QMView import QMView

__version__ = '1.0.0'

__all__ = [
    'QMLabel',
    'QMView'
] 