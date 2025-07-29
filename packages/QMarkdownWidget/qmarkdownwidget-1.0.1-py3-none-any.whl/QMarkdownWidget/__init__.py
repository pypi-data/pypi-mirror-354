"""
QMarkdownWidget - A Qt component library for Markdown and LaTeX

Markdown rendering widgets implemented with different technologies:
- QMLabel: A lightweight Markdown widget based on QLabel (does not support LaTeX rendering)
- QMView: A complete Markdown+LaTeX widget based on QWebEngineView (supports scrolling and text selection)
"""

from .QMLabel import QMLabel
from .QMView import QMView

__version__ = '1.0.0'

__all__ = [
    'QMLabel',
    'QMView'
] 