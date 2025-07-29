import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                           QWidget, QPushButton, QTextEdit, QSplitter, QCheckBox,
                           QSpinBox, QLabel, QGroupBox, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from QMarkdownWidget import QMView


class QMViewTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMView Test - Markdown View with Scrolling and LaTeX Support")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left control area
        left_widget = self.create_control_panel()
        
        # Right display area
        right_widget = self.create_display_area()
        
        # Add to splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 800])
        
        # Set initial content
        self.set_initial_content()
        
        # Initialize widget states
        self.toggle_auto_height(self.auto_resize_checkbox.checkState().value)
    
    def create_control_panel(self):
        """Create left control panel"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Input text box
        input_group = QGroupBox("Markdown Input")
        input_layout = QVBoxLayout(input_group)
        
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter Markdown text here, supports LaTeX equations...")
        input_layout.addWidget(self.input_text)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        update_btn = QPushButton("Update Display")
        update_btn.clicked.connect(self.update_display)
        button_layout.addWidget(update_btn)
        
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_content)
        button_layout.addWidget(clear_btn)
        
        input_layout.addLayout(button_layout)
        layout.addWidget(input_group)
        
        # Display options
        options_group = QGroupBox("Display Options")
        options_layout = QVBoxLayout(options_group)
        
        # Markdown toggle
        self.markdown_checkbox = QCheckBox("Enable Markdown Rendering")
        self.markdown_checkbox.setChecked(True)
        self.markdown_checkbox.stateChanged.connect(self.toggle_markdown)
        options_layout.addWidget(self.markdown_checkbox)
        
        # Auto-resize toggle
        self.auto_resize_checkbox = QCheckBox("Auto-Adjust Height")
        self.auto_resize_checkbox.setChecked(False)
        self.auto_resize_checkbox.stateChanged.connect(self.toggle_auto_height)
        options_layout.addWidget(self.auto_resize_checkbox)
        
        # Max width setting
        max_width_layout = QHBoxLayout()
        max_width_layout.addWidget(QLabel("Max Width:"))
        self.max_width_spin = QSpinBox()
        self.max_width_spin.setRange(50, 1200)
        self.max_width_spin.setValue(600)
        self.max_width_spin.setSuffix(" px")
        self.max_width_spin.valueChanged.connect(self.update_max_width)
        self.max_width_spin.setEnabled(False)  # Disabled initially
        max_width_layout.addWidget(self.max_width_spin)
        options_layout.addLayout(max_width_layout)
        
        # Add info label
        info_label = QLabel("💡 Mode Explanation:\n"
                          "• Disable Auto-Height: QMView maintains fixed height, content scrolls internally\n"
                          "• Enable Auto-Height: QMView height fully adapts to content, width adjusts automatically")
        info_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 11px;
                padding: 8px;
                background-color: #f9f9f9;
                border-radius: 3px;
                border-left: 3px solid #007bff;
                line-height: 1.4;
            }
        """)
        info_label.setWordWrap(True)
        options_layout.addWidget(info_label)
        
        # Height settings
        height_layout = QVBoxLayout()
        
        # Fixed height setting (non-auto-resize mode)
        fixed_height_layout = QHBoxLayout()
        fixed_height_layout.addWidget(QLabel("Fixed Height:"))
        self.fixed_height_spin = QSpinBox()
        self.fixed_height_spin.setRange(100, 800)
        self.fixed_height_spin.setValue(300)
        self.fixed_height_spin.setSuffix(" px")
        self.fixed_height_spin.valueChanged.connect(self.update_fixed_height)
        fixed_height_layout.addWidget(self.fixed_height_spin)
        height_layout.addLayout(fixed_height_layout)
        
        # Removed max auto height setting as auto-resize mode no longer limits max height
        
        options_layout.addLayout(height_layout)
        
        layout.addWidget(options_group)
        
        # Preset examples
        examples_group = QGroupBox("Examples")
        examples_layout = QVBoxLayout(examples_group)
        
        basic_btn = QPushButton("Basic Markdown")
        basic_btn.clicked.connect(lambda: self.load_example("basic"))
        examples_layout.addWidget(basic_btn)
        
        math_btn = QPushButton("Math Equations")
        math_btn.clicked.connect(lambda: self.load_example("math"))
        examples_layout.addWidget(math_btn)
        
        complex_btn = QPushButton("Complex Document")
        complex_btn.clicked.connect(lambda: self.load_example("complex"))
        examples_layout.addWidget(complex_btn)
        
        table_btn = QPushButton("Tables and Code")
        table_btn.clicked.connect(lambda: self.load_example("table"))
        examples_layout.addWidget(table_btn)
        
        layout.addWidget(examples_group)
        
        layout.addStretch()
        
        return widget
    
    def create_display_area(self):
        """Create right display area"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Title
        title_label = QLabel("QMView Display Area")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create a container to wrap QMView, providing padding
        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)
        container_layout.setContentsMargins(15, 15, 15, 15)  # Set padding
        
        # Create a green-bordered frame to wrap QMView
        qmview_frame = QWidget()
        qmview_frame_layout = QVBoxLayout(qmview_frame)
        qmview_frame_layout.setContentsMargins(3, 3, 3, 3)  # Border width
        
        # QMView control
        self.qm_view = QMView()
        
        # Set QMView frame style (green border)
        qmview_frame.setStyleSheet("""
            QWidget {
                background-color: #4CAF50;
                border-radius: 8px;
            }
        """)
        
        # Set QMView style (white background, no border)
        self.qm_view.setStyleSheet("""
            QMView {
                background-color: white;
                border-radius: 5px;
            }
        """)
        
        # Set scroll area style
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 2px solid #2196F3;
                border-radius: 8px;
                background-color: #f8fafe;
            }
            
            /* Vertical scroll bar */
            QScrollBar:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f0f8ff, stop:1 #e3f2fd);
                width: 12px;
                border-radius: 6px;
                margin: 0px;
                border: 1px solid #bbdefb;
            }
            
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #42a5f5, stop:0.5 #2196f3, stop:1 #1e88e5);
                border-radius: 5px;
                min-height: 30px;
                margin: 1px;
                border: 1px solid #1976d2;
            }
            
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e88e5, stop:0.5 #1976d2, stop:1 #1565c0);
                border: 1px solid #0d47a1;
            }
            
            QScrollBar::handle:vertical:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1565c0, stop:0.5 #1565c0, stop:1 #0d47a1);
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                width: 0px;
            }
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: transparent;
            }
            
            /* Horizontal scroll bar */
            QScrollBar:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f0f8ff, stop:1 #e3f2fd);
                height: 12px;
                border-radius: 6px;
                margin: 0px;
                border: 1px solid #bbdefb;
            }
            
            QScrollBar::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #42a5f5, stop:0.5 #2196f3, stop:1 #1e88e5);
                border-radius: 5px;
                min-width: 30px;
                margin: 1px;
                border: 1px solid #1976d2;
            }
            
            QScrollBar::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e88e5, stop:0.5 #1976d2, stop:1 #1565c0);
                border: 1px solid #0d47a1;
            }
            
            QScrollBar::handle:horizontal:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1565c0, stop:0.5 #1565c0, stop:1 #0d47a1);
            }
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                height: 0px;
                width: 0px;
            }
            
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: transparent;
            }
            
            /* Scroll bar corners */
            QScrollBar::corner {
                background: #e3f2fd;
                border-radius: 2px;
            }
        """)
        
        # Set container style (transparent background, no visual impact)
        container_widget.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
        """)
        
        # Add QMView to green frame
        qmview_frame_layout.addWidget(self.qm_view)
        
        # Add green frame to container
        container_layout.addWidget(qmview_frame)
        
        # Add container to scroll area
        scroll_area.setWidget(container_widget)
        layout.addWidget(scroll_area)
        
        # Add legend
        legend_widget = QWidget()
        legend_layout = QHBoxLayout(legend_widget)
        legend_layout.setContentsMargins(5, 5, 5, 5)
        
        # Outer scroll area legend
        outer_legend = QLabel("�� Outer ScrollArea")
        outer_legend.setStyleSheet("""
            QLabel {
                padding: 3px 8px;
                background-color: #e3f2fd;
                border: 1px solid #2196F3;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
            }
        """)
        
        # Inner QMView legend
        inner_legend = QLabel("🟢 Inner QMView")
        inner_legend.setStyleSheet("""
            QLabel {
                padding: 3px 8px;
                background-color: #e8f5e8;
                border: 1px solid #4CAF50;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
            }
        """)
        
        legend_layout.addWidget(outer_legend)
        legend_layout.addWidget(inner_legend)
        legend_layout.addStretch()
        
        layout.addWidget(legend_widget)
        
        # Status info
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("""
            QLabel {
                padding: 5px;
                background-color: #f0f0f0;
                border-radius: 3px;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.status_label)
        
        # Connect signals
        self.qm_view.contentChanged.connect(self.on_content_changed)
        
        return widget
    
    def set_initial_content(self):
        """Set initial content"""
        initial_content = """# QMView Function Demo

This is a Markdown view control based on QWebEngineView, supporting:

## ✨ Main Features

- **Scrolling Support** - Can handle long documents
- **Text Selection** - Can select and copy text
- **LaTeX Rendering** - True mathematical formula display
- **Auto-Sizing** - Optional automatic height adjustment

## 🧮 Math Equation Demo

### Inline Equations
This is Einstein's mass-energy equation: $E = mc^2$

And Euler's formula: $e^{i\\pi} + 1 = 0$

### Block Equations
Quadratic equation:
$$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$

Integral equation:
$$\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}$$

Differential equation:
$$\\frac{d^2y}{dx^2} + \\frac{dy}{dx} + y = 0$$

### Matrices
$$
\\begin{pmatrix}
a & b \\\\
c & d
\\end{pmatrix}
\\begin{pmatrix}
x \\\\
y
\\end{pmatrix}
=
\\begin{pmatrix}
ax + by \\\\
cx + dy
\\end{pmatrix}
$$

## 📝 Text Formatting

**Bold text** and *italic text* and ~~strikethrough~~

`Inline code` and code blocks:

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Calculate the first 10 numbers
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
```

## 📊 Tables

| Feature | QMLabel | QMView |
|------|---------|--------|
| Markdown | ✓ | ✓ |
| LaTeX | ❌ | ✓ |
| Scrolling | ❌ | ✓ |
| Text Selection | ❌ | ✓ |
| Auto-Sizing | ✓ | ✓ |

## 💡 Tips

- Try selecting text above to copy
- Adjust settings on the left
- Click example buttons to view different content
- Observe scrolling effects:
  - 🔵 Outer ScrollArea (blue border): Auto-adjust mode provides scrolling
  - 🟢 Inner QMView (green border): Fixed height mode scrolls internally
  - Enable "Auto-Adjust Size" for full content expansion, scrolling via outer area
  - Disable "Auto-Adjust Size" to maintain fixed height, scrolling internally
"""
        
        self.input_text.setPlainText(initial_content)
        self.update_display()
    
    def update_display(self):
        """Update display content"""
        text = self.input_text.toPlainText()
        self.qm_view.setText(text)
        self.status_label.setText("Status: Content updated")
    
    def clear_content(self):
        """Clear content"""
        self.input_text.clear()
        self.qm_view.clear()
        self.status_label.setText("Status: Content cleared")
    
    def toggle_markdown(self, state):
        """Toggle Markdown rendering"""
        enabled = state == Qt.CheckState.Checked.value
        self.qm_view.setMarkdownEnabled(enabled)
        self.status_label.setText(f"Status: Markdown {'enabled' if enabled else 'disabled'}")
    
    def toggle_auto_height(self, state):
        """Toggle auto-height adjustment"""
        enabled = state == Qt.CheckState.Checked.value
        
        # Update control enable state
        self.fixed_height_spin.setEnabled(not enabled)
        self.max_width_spin.setEnabled(enabled)
        
        if enabled:
            # Enable auto-height mode
            max_width = self.max_width_spin.value()
            self.qm_view.setAutoHeight(max_width)
            self.status_label.setText(f"Status: Auto-height enabled - Max width {max_width}px, height adapts to content")
        else:
            # Use fixed height mode
            fixed_height = self.fixed_height_spin.value()
            
            # Use dedicated method to disable auto-height
            self.qm_view.disableAutoHeight()
            self.qm_view.setFixedViewHeight(fixed_height)
            
            self.status_label.setText(f"Status: Auto-height disabled - QMView fixed height({fixed_height}px), scrolls internally")
    
    def update_fixed_height(self, value):
        """Update fixed height"""
        self.qm_view.setFixedViewHeight(value)
        if not self.auto_resize_checkbox.isChecked():
            self.qm_view.setFixedHeight(value)
            self.status_label.setText(f"Status: Fixed height updated to {value}px")
    
    def update_max_width(self, value):
        """Update max width"""
        if self.auto_resize_checkbox.isChecked():
            self.qm_view.setAutoHeight(value)
            self.status_label.setText(f"Status: Max width updated to {value}px")
    
    def load_example(self, example_type):
        """Load example content"""
        examples = {
            "basic": """# Basic Markdown Example

## Text Formatting
This is **bold** text, this is *italic* text.

## Lists
- Item 1
- Item 2
  - Sub-item 2.1
  - Sub-item 2.2

## Quotes
> This is a quote block
> Can contain multiple lines of content
""",
            
            "math": """# Math Equation Collection

## Basic Equations
- Pythagorean theorem: $a^2 + b^2 = c^2$
- Area of a circle: $A = \\pi r^2$
- Volume of a sphere: $V = \\frac{4}{3}\\pi r^3$

## Calculus
Derivative definition:
$$f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}$$

Basic integral:
$$\\int x^n dx = \\frac{x^{n+1}}{n+1} + C$$

## Linear Algebra

### Matrix Multiplication
$$\\begin{pmatrix}
a & b \\\\
c & d
\\end{pmatrix}
\\begin{pmatrix}
x \\\\
y
\\end{pmatrix}
=
\\begin{pmatrix}
ax + by \\\\
cx + dy
\\end{pmatrix}$$

### Types of Matrices
Parentheses matrix:
$$\\begin{pmatrix}
1 & 2 & 3 \\\\
4 & 5 & 6 \\\\
7 & 8 & 9
\\end{pmatrix}$$

Bracket matrix:
$$\\begin{bmatrix}
1 & 0 \\\\
0 & 1
\\end{bmatrix}$$

### Determinants
$$\\begin{vmatrix}
a & b \\\\
c & d
\\end{vmatrix} = ad - bc$$

3x3 determinant:
$$\\begin{vmatrix}
a & b & c \\\\
d & e & f \\\\
g & h & i
\\end{vmatrix} = a(ei - fh) - b(di - fg) + c(dh - eg)$$

### Eigenvalue Equation
$$\\det(A - \\lambda I) = 0$$

## Probability and Statistics
Normal distribution:
$$f(x) = \\frac{1}{\\sqrt{2\\pi\\sigma^2}} e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}}$$
""",
            
            "complex": """# Complex Document Example

## 1. Project Introduction

This is a **complex document** that includes various Markdown elements and LaTeX equations.

### 1.1 Background
In modern scientific computing, we often need to handle complex mathematical expressions.

### 1.2 Objectives
- Provide clear mathematical representation
- Support multiple formats
- Easy to read and understand

## 2. Mathematical Theory

### 2.1 Basic Theory
Consider the function $f(x) = e^{-x^2}$, its integral is:

$$\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}$$

### 2.2 Application Examples

```python
import numpy as np
import matplotlib.pyplot as plt

def gaussian(x, mu=0, sigma=1):
    return (1/(sigma*np.sqrt(2*np.pi))) * np.exp(-0.5*((x-mu)/sigma)**2)

x = np.linspace(-5, 5, 1000)
y = gaussian(x)
plt.plot(x, y)
plt.title('Gaussian Distribution')
plt.show()
```

## 3. Experimental Results

| Parameter | Value | Unit |
|------|-----|------|
| μ | 0.0 | - |
| σ | 1.0 | - |
| Integral | 1.0 | - |

### 3.1 Error Analysis
Relative error defined as:
$$\\epsilon_{rel} = \\frac{|x_{true} - x_{approx}|}{|x_{true}|} \\times 100\\%$$

## 4. Conclusion

> Through this research, we have verified the consistency between theoretical predictions and experimental results.
> 
> This lays the foundation for further research.

---

**Note:** This is only a demonstration document, more detailed analysis is required for actual applications.
""",
            
            "table": """# Tables and Code Examples

## Data Tables

### Experimental Data
| Index | Input Value | Output Value | Error | Remarks |
|------|--------|--------|------|------|
| 1 | 1.0 | 1.05 | 0.05 | Normal |
| 2 | 2.0 | 2.02 | 0.02 | Normal |
| 3 | 3.0 | 2.98 | -0.02 | Normal |
| 4 | 4.0 | 4.10 | 0.10 | Abnormal |

### Statistical Results
| Statistic | Value | Formula |
|--------|-----|------|
| Mean | 2.5375 | $\\bar{x} = \\frac{1}{n}\\sum_{i=1}^n x_i$ |
| Standard Deviation | 0.0479 | $s = \\sqrt{\\frac{1}{n-1}\\sum_{i=1}^n (x_i - \\bar{x})^2}$ |
| Variance | 0.0023 | $s^2 = \\frac{1}{n-1}\\sum_{i=1}^n (x_i - \\bar{x})^2$ |

## Code Examples

### Python Data Processing
```python
import pandas as pd
import numpy as np

# Create data frame
data = {
    'input': [1.0, 2.0, 3.0, 4.0],
    'output': [1.05, 2.02, 2.98, 4.10],
    'error': [0.05, 0.02, -0.02, 0.10]
}
df = pd.DataFrame(data)

# Calculate statistics
mean_val = df['output'].mean()
std_val = df['output'].std()
var_val = df['output'].var()

print(f"Mean: {mean_val:.4f}")
print(f"Standard Deviation: {std_val:.4f}")
print(f"Variance: {var_val:.4f}")
```

### JavaScript Visualization
```javascript
// Create chart using Chart.js
const ctx = document.getElementById('myChart');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['1', '2', '3', '4'],
        datasets: [{
            label: 'Output Value',
            data: [1.05, 2.02, 2.98, 4.10],
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
```

## Mathematical Analysis

Linear fitting equation:
$$y = ax + b$$

Where parameters are solved by the method of least squares:
$$a = \\frac{n\\sum xy - \\sum x \\sum y}{n\\sum x^2 - (\\sum x)^2}$$
$$b = \\frac{\\sum y - a\\sum x}{n}$$

Correlation coefficient:
$$r = \\frac{n\\sum xy - \\sum x \\sum y}{\\sqrt{(n\\sum x^2 - (\\sum x)^2)(n\\sum y^2 - (\\sum y)^2)}}$$
"""
        }
        
        content = examples.get(example_type, "")
        self.input_text.setPlainText(content)
        self.update_display()
        self.status_label.setText(f"Status: Loaded {example_type} example")
    
    def on_content_changed(self):
        """Handle content change"""
        if self.auto_resize_checkbox.isChecked():
            self.status_label.setText("Status: Content updated, auto-adjusting height...")
        else:
            self.status_label.setText("Status: Content updated")


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QGroupBox {
            font-weight: bold;
            border: 2px solid #cccccc;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        QTextEdit {
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 5px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 12px;
        }
        QPushButton {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #0056b3;
        }
        QPushButton:pressed {
            background-color: #004085;
        }
        QCheckBox {
            spacing: 5px;
        }
        QSpinBox {
            padding: 4px;
            border: 1px solid #cccccc;
            border-radius: 3px;
        }
    """)
    
    window = QMViewTestWindow()
    window.show()
    
    return app.exec()


if __name__ == '__main__':
    sys.exit(main()) 