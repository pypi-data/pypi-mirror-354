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
        self.setWindowTitle("QMView 测试 - 支持滚动和LaTeX的Markdown视图")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左侧控制区域
        left_widget = self.create_control_panel()
        
        # 右侧显示区域
        right_widget = self.create_display_area()
        
        # 添加到分割器
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 800])
        
        # 设置初始内容
        self.set_initial_content()
        
        # 初始化控件状态
        self.toggle_auto_height(self.auto_resize_checkbox.checkState().value)
    
    def create_control_panel(self):
        """创建左侧控制面板"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 输入文本框
        input_group = QGroupBox("Markdown输入")
        input_layout = QVBoxLayout(input_group)
        
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("在这里输入Markdown文本，支持LaTeX公式...")
        input_layout.addWidget(self.input_text)
        
        # 控制按钮
        button_layout = QHBoxLayout()
        
        update_btn = QPushButton("更新显示")
        update_btn.clicked.connect(self.update_display)
        button_layout.addWidget(update_btn)
        
        clear_btn = QPushButton("清空")
        clear_btn.clicked.connect(self.clear_content)
        button_layout.addWidget(clear_btn)
        
        input_layout.addLayout(button_layout)
        layout.addWidget(input_group)
        
        # 设置选项
        options_group = QGroupBox("显示选项")
        options_layout = QVBoxLayout(options_group)
        
        # Markdown开关
        self.markdown_checkbox = QCheckBox("启用Markdown渲染")
        self.markdown_checkbox.setChecked(True)
        self.markdown_checkbox.stateChanged.connect(self.toggle_markdown)
        options_layout.addWidget(self.markdown_checkbox)
        
        # 自动调整大小开关
        self.auto_resize_checkbox = QCheckBox("自动调整高度")
        self.auto_resize_checkbox.setChecked(False)
        self.auto_resize_checkbox.stateChanged.connect(self.toggle_auto_height)
        options_layout.addWidget(self.auto_resize_checkbox)
        
        # 最大宽度设置
        max_width_layout = QHBoxLayout()
        max_width_layout.addWidget(QLabel("最大宽度:"))
        self.max_width_spin = QSpinBox()
        self.max_width_spin.setRange(50, 1200)
        self.max_width_spin.setValue(600)
        self.max_width_spin.setSuffix(" px")
        self.max_width_spin.valueChanged.connect(self.update_max_width)
        self.max_width_spin.setEnabled(False)  # 初始时禁用
        max_width_layout.addWidget(self.max_width_spin)
        options_layout.addLayout(max_width_layout)
        
        # 添加说明标签
        info_label = QLabel("💡 模式说明：\n"
                          "• 禁用自动高度：QMView保持固定高度，内容在内部滚动\n"
                          "• 启用自动高度：QMView高度完全适应内容，宽度可根据内容自动调整")
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
        
        # 高度设置
        height_layout = QVBoxLayout()
        
        # 固定高度设置（非自动调整模式）
        fixed_height_layout = QHBoxLayout()
        fixed_height_layout.addWidget(QLabel("固定高度:"))
        self.fixed_height_spin = QSpinBox()
        self.fixed_height_spin.setRange(100, 800)
        self.fixed_height_spin.setValue(300)
        self.fixed_height_spin.setSuffix(" px")
        self.fixed_height_spin.valueChanged.connect(self.update_fixed_height)
        fixed_height_layout.addWidget(self.fixed_height_spin)
        height_layout.addLayout(fixed_height_layout)
        
        # 移除最大自动高度设置，因为自动调整模式不再限制最大高度
        
        options_layout.addLayout(height_layout)
        
        layout.addWidget(options_group)
        
        # 预设示例
        examples_group = QGroupBox("示例")
        examples_layout = QVBoxLayout(examples_group)
        
        basic_btn = QPushButton("基础Markdown")
        basic_btn.clicked.connect(lambda: self.load_example("basic"))
        examples_layout.addWidget(basic_btn)
        
        math_btn = QPushButton("数学公式")
        math_btn.clicked.connect(lambda: self.load_example("math"))
        examples_layout.addWidget(math_btn)
        
        complex_btn = QPushButton("复杂文档")
        complex_btn.clicked.connect(lambda: self.load_example("complex"))
        examples_layout.addWidget(complex_btn)
        
        table_btn = QPushButton("表格和代码")
        table_btn.clicked.connect(lambda: self.load_example("table"))
        examples_layout.addWidget(table_btn)
        
        layout.addWidget(examples_group)
        
        layout.addStretch()
        
        return widget
    
    def create_display_area(self):
        """创建右侧显示区域"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 标题
        title_label = QLabel("QMView 显示区域")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # 创建一个容器来包装QMView，提供间距
        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)
        container_layout.setContentsMargins(15, 15, 15, 15)  # 设置间距
        
        # 创建一个带绿色边框的框架来包装QMView
        qmview_frame = QWidget()
        qmview_frame_layout = QVBoxLayout(qmview_frame)
        qmview_frame_layout.setContentsMargins(3, 3, 3, 3)  # 边框宽度
        
        # QMView控件
        self.qm_view = QMView()
        
        # 设置QMView框架的样式（绿色边框）
        qmview_frame.setStyleSheet("""
            QWidget {
                background-color: #4CAF50;
                border-radius: 8px;
            }
        """)
        
        # 设置QMView的样式（白色背景，无边框）
        self.qm_view.setStyleSheet("""
            QMView {
                background-color: white;
                border-radius: 5px;
            }
        """)
        
        # 设置滚动区域样式
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 2px solid #2196F3;
                border-radius: 8px;
                background-color: #f8fafe;
            }
            
            /* 垂直滚动条 */
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
            
            /* 水平滚动条 */
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
            
            /* 滚动条角落 */
            QScrollBar::corner {
                background: #e3f2fd;
                border-radius: 2px;
            }
        """)
        
        # 设置容器样式（透明背景，不影响视觉）
        container_widget.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
        """)
        
        # 将QMView添加到绿色框架
        qmview_frame_layout.addWidget(self.qm_view)
        
        # 将绿色框架添加到容器
        container_layout.addWidget(qmview_frame)
        
        # 将容器添加到滚动区域
        scroll_area.setWidget(container_widget)
        layout.addWidget(scroll_area)
        
        # 添加图例说明
        legend_widget = QWidget()
        legend_layout = QHBoxLayout(legend_widget)
        legend_layout.setContentsMargins(5, 5, 5, 5)
        
        # 外层滚动区域图例
        outer_legend = QLabel("🔵 外层ScrollArea")
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
        
        # 内层QMView图例
        inner_legend = QLabel("🟢 内层QMView")
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
        
        # 状态信息
        self.status_label = QLabel("状态: 就绪")
        self.status_label.setStyleSheet("""
            QLabel {
                padding: 5px;
                background-color: #f0f0f0;
                border-radius: 3px;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.status_label)
        
        # 连接信号
        self.qm_view.contentChanged.connect(self.on_content_changed)
        
        return widget
    
    def set_initial_content(self):
        """设置初始内容"""
        initial_content = """# QMView 功能演示

这是一个基于QWebEngineView的Markdown视图控件，支持：

## ✨ 主要特性

- **滚动支持** - 可以处理长文档
- **文本选择** - 可以选中和复制文本
- **LaTeX渲染** - 真正的数学公式显示
- **自适应大小** - 可选的自动调整高度

## 🧮 数学公式演示

### 行内公式
这是爱因斯坦的质能方程：$E = mc^2$

还有欧拉公式：$e^{i\\pi} + 1 = 0$

### 块级公式
二次公式：
$$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$

积分公式：
$$\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}$$

微分方程：
$$\\frac{d^2y}{dx^2} + \\frac{dy}{dx} + y = 0$$

### 矩阵
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

## 📝 文本格式

**粗体文本** 和 *斜体文本* 以及 ~~删除线~~

`行内代码` 和代码块：

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 计算前10个数
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
```

## 📊 表格

| 功能 | QMLabel | QMView |
|------|---------|--------|
| Markdown | ✓ | ✓ |
| LaTeX | ❌ | ✓ |
| 滚动 | ❌ | ✓ |
| 文本选择 | ❌ | ✓ |
| 自适应 | ✓ | ✓ |

## 💡 提示

- 尝试选择上面的文本进行复制
- 调整左侧的设置选项
- 点击示例按钮查看不同内容
- 观察滚动效果：
  - 🔵 外层ScrollArea（蓝色边框）：自动调整模式下提供滚动
  - 🟢 内层QMView（绿色边框）：固定高度模式下内部滚动
  - 启用"自动调整大小"时，内容完全展开，通过外层滚动
  - 禁用"自动调整大小"时，保持固定高度，内部滚动
"""
        
        self.input_text.setPlainText(initial_content)
        self.update_display()
    
    def update_display(self):
        """更新显示内容"""
        text = self.input_text.toPlainText()
        self.qm_view.setText(text)
        self.status_label.setText("状态: 内容已更新")
    
    def clear_content(self):
        """清空内容"""
        self.input_text.clear()
        self.qm_view.clear()
        self.status_label.setText("状态: 内容已清空")
    
    def toggle_markdown(self, state):
        """切换Markdown渲染"""
        enabled = state == Qt.CheckState.Checked.value
        self.qm_view.setMarkdownEnabled(enabled)
        self.status_label.setText(f"状态: Markdown {'启用' if enabled else '禁用'}")
    
    def toggle_auto_height(self, state):
        """切换自动高度调整"""
        enabled = state == Qt.CheckState.Checked.value
        
        # 更新控件启用状态
        self.fixed_height_spin.setEnabled(not enabled)
        self.max_width_spin.setEnabled(enabled)
        
        if enabled:
            # 启用自动高度模式
            max_width = self.max_width_spin.value()
            self.qm_view.setAutoHeight(max_width)
            self.status_label.setText(f"状态: 自动高度已启用 - 最大宽度 {max_width}px，高度自适应内容")
        else:
            # 使用固定高度模式
            fixed_height = self.fixed_height_spin.value()
            
            # 使用专门的方法禁用自动高度
            self.qm_view.disableAutoHeight()
            self.qm_view.setFixedViewHeight(fixed_height)
            
            self.status_label.setText(f"状态: 自动高度已禁用 - QMView固定高度({fixed_height}px)，内部可滚动")
    
    def update_fixed_height(self, value):
        """更新固定高度"""
        self.qm_view.setFixedViewHeight(value)
        if not self.auto_resize_checkbox.isChecked():
            self.qm_view.setFixedHeight(value)
            self.status_label.setText(f"状态: 固定高度已更新为 {value}px")
    
    def update_max_width(self, value):
        """更新最大宽度"""
        if self.auto_resize_checkbox.isChecked():
            self.qm_view.setAutoHeight(value)
            self.status_label.setText(f"状态: 最大宽度已更新为 {value}px")
    
    def load_example(self, example_type):
        """加载示例内容"""
        examples = {
            "basic": """# 基础Markdown示例

## 文本格式
这是**粗体**文本，这是*斜体*文本。

## 列表
- 项目1
- 项目2
  - 子项目2.1
  - 子项目2.2

## 引用
> 这是一个引用块
> 可以包含多行内容
""",
            
            "math": """# 数学公式集合

## 基础公式
- 勾股定理：$a^2 + b^2 = c^2$
- 圆的面积：$A = \\pi r^2$
- 球的体积：$V = \\frac{4}{3}\\pi r^3$

## 微积分
导数定义：
$$f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}$$

基本积分：
$$\\int x^n dx = \\frac{x^{n+1}}{n+1} + C$$

## 线性代数

### 矩阵乘法
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

### 不同类型的矩阵
圆括号矩阵：
$$\\begin{pmatrix}
1 & 2 & 3 \\\\
4 & 5 & 6 \\\\
7 & 8 & 9
\\end{pmatrix}$$

方括号矩阵：
$$\\begin{bmatrix}
1 & 0 \\\\
0 & 1
\\end{bmatrix}$$

### 行列式
$$\\begin{vmatrix}
a & b \\\\
c & d
\\end{vmatrix} = ad - bc$$

3阶行列式：
$$\\begin{vmatrix}
a & b & c \\\\
d & e & f \\\\
g & h & i
\\end{vmatrix} = a(ei - fh) - b(di - fg) + c(dh - eg)$$

### 特征值方程
$$\\det(A - \\lambda I) = 0$$

## 概率统计
正态分布：
$$f(x) = \\frac{1}{\\sqrt{2\\pi\\sigma^2}} e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}}$$
""",
            
            "complex": """# 复杂文档示例

## 1. 项目介绍

这是一个**复杂的文档**，包含了多种Markdown元素和LaTeX公式。

### 1.1 背景
在现代科学计算中，我们经常需要处理复杂的数学表达式。

### 1.2 目标
- 提供清晰的数学表示
- 支持多种格式
- 易于阅读和理解

## 2. 数学理论

### 2.1 基础理论
考虑函数 $f(x) = e^{-x^2}$，其积分为：

$$\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}$$

### 2.2 应用示例

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

## 3. 实验结果

| 参数 | 值 | 单位 |
|------|-----|------|
| μ | 0.0 | - |
| σ | 1.0 | - |
| 积分 | 1.0 | - |

### 3.1 误差分析
相对误差定义为：
$$\\epsilon_{rel} = \\frac{|x_{true} - x_{approx}|}{|x_{true}|} \\times 100\\%$$

## 4. 结论

> 通过本研究，我们验证了理论预测与实验结果的一致性。
> 
> 这为进一步的研究奠定了基础。

---

**注意：** 这只是一个演示文档，实际应用中需要更详细的分析。
""",
            
            "table": """# 表格和代码示例

## 数据表格

### 实验数据
| 序号 | 输入值 | 输出值 | 误差 | 备注 |
|------|--------|--------|------|------|
| 1 | 1.0 | 1.05 | 0.05 | 正常 |
| 2 | 2.0 | 2.02 | 0.02 | 正常 |
| 3 | 3.0 | 2.98 | -0.02 | 正常 |
| 4 | 4.0 | 4.10 | 0.10 | 异常 |

### 统计结果
| 统计量 | 值 | 公式 |
|--------|-----|------|
| 平均值 | 2.5375 | $\\bar{x} = \\frac{1}{n}\\sum_{i=1}^n x_i$ |
| 标准差 | 0.0479 | $s = \\sqrt{\\frac{1}{n-1}\\sum_{i=1}^n (x_i - \\bar{x})^2}$ |
| 方差 | 0.0023 | $s^2 = \\frac{1}{n-1}\\sum_{i=1}^n (x_i - \\bar{x})^2$ |

## 代码示例

### Python数据处理
```python
import pandas as pd
import numpy as np

# 创建数据框
data = {
    'input': [1.0, 2.0, 3.0, 4.0],
    'output': [1.05, 2.02, 2.98, 4.10],
    'error': [0.05, 0.02, -0.02, 0.10]
}
df = pd.DataFrame(data)

# 计算统计量
mean_val = df['output'].mean()
std_val = df['output'].std()
var_val = df['output'].var()

print(f"平均值: {mean_val:.4f}")
print(f"标准差: {std_val:.4f}")
print(f"方差: {var_val:.4f}")
```

### JavaScript可视化
```javascript
// 使用Chart.js创建图表
const ctx = document.getElementById('myChart');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['1', '2', '3', '4'],
        datasets: [{
            label: '输出值',
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

## 数学分析

线性拟合方程：
$$y = ax + b$$

其中参数通过最小二乘法求解：
$$a = \\frac{n\\sum xy - \\sum x \\sum y}{n\\sum x^2 - (\\sum x)^2}$$
$$b = \\frac{\\sum y - a\\sum x}{n}$$

相关系数：
$$r = \\frac{n\\sum xy - \\sum x \\sum y}{\\sqrt{(n\\sum x^2 - (\\sum x)^2)(n\\sum y^2 - (\\sum y)^2)}}$$
"""
        }
        
        content = examples.get(example_type, "")
        self.input_text.setPlainText(content)
        self.update_display()
        self.status_label.setText(f"状态: 已加载{example_type}示例")
    
    def on_content_changed(self):
        """内容改变时的处理"""
        if self.auto_resize_checkbox.isChecked():
            self.status_label.setText("状态: 内容已更新，自动调整高度中...")
        else:
            self.status_label.setText("状态: 内容已更新")


def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
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