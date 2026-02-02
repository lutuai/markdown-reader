#!/usr/bin/env python3
"""
批量替换markdown-reader.html中的emoji为Iconfont图标
并添加主题悬浮提示
"""

import re

# 读取文件
with open('E:/workspace/opencode_workspace/markdown-reader-project/ai_creator/markdown-reader.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 添加Iconfont CSS引用（如果还没有）
if 'iconfont/iconfont.css' not in content:
    content = content.replace(
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/highlight.js@11.8.0/styles/github-dark.min.css">',
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/highlight.js@11.8.0/styles/github-dark.min.css">\n    <!-- Iconfont CSS -->\n    <link rel="stylesheet" href="iconfont/iconfont.css">'
    )

# 2. 添加Iconfont基础样式（在第一个CSS规则后）
iconfont_styles = '''
        /* Iconfont基础样式 */
        .iconfont {
            font-family: "iconfont" !important;
            font-size: 16px;
            font-style: normal;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            display: inline-block;
            vertical-align: middle;
        }

        /* 图标尺寸 */
        .icon-xs { font-size: 12px; }
        .icon-sm { font-size: 14px; }
        .icon-md { font-size: 16px; }
        .icon-lg { font-size: 20px; }
        .icon-xl { font-size: 24px; }
'''

# 找到第一个CSS规则的位置插入
if '.iconfont' not in content:
    content = content.replace(
        'box-sizing: border-box;\n        }',
        'box-sizing: border-box;\n        }' + iconfont_styles
    )

# 3. 替换emoji为Iconfont图标
replacements = [
    # 侧边栏标题
    ('<span>📄</span>', '<i class="iconfont icon-file-text icon-lg"></i>'),
    
    # 按钮图标
    ('title="新建文件">+', 'title="新建文件">\n                        <i class="iconfont icon-plus"></i>\n                    '),
    ('title="导入文件">📁', 'title="导入文件">\n                        <i class="iconfont icon-folder"></i>\n                    '),
    ('title="导出">💾', 'title="导出">\n                        <i class="iconfont icon-save"></i>\n                    '),
    
    # 菜单按钮
    ('onclick="toggleSidebar()">☰', 'onclick="toggleSidebar()">\n                        <i class="iconfont icon-menu"></i>\n                    '),
    
    # 复制按钮
    ('title="一键复制" style="margin-right: 10px;">\n                        📋', 'title="一键复制" style="margin-right: 10px;">\n                        <i class="iconfont icon-copy"></i>\n                    '),
    
    # 模板栏
    ('<span>📋</span>', '<i class="iconfont icon-edit"></i>'),
    ('<span class="template-chip-icon">📝</span>', '<i class="iconfont icon-file-text template-chip-icon"></i>'),
    
    # 空状态
    ('<div class="empty-icon">📝</div>', '<div class="empty-icon">\n                            <i class="iconfont icon-edit" style="font-size: 64px;"></i>\n                        </div>'),
    
    # 模态框标题
    ('<div class="modal-title">📄 新建文件</div>', '<div class="modal-title">\n                <i class="iconfont icon-file-text"></i>\n                <span>新建文件</span>\n            </div>'),
    ('<div class="modal-title">✏️ 重命名文件</div>', '<div class="modal-title">\n                <i class="iconfont icon-edit"></i>\n                <span>重命名文件</span>\n            </div>'),
    
    # 文件列表图标
    ('<span class="file-icon">📄</span>', '<i class="iconfont icon-file-text file-icon"></i>'),
    
    # 文件操作按钮
    ('title="重命名">✏️</button>', 'title="重命名">\n                            <i class="iconfont icon-edit"></i>\n                        </button>'),
    ('title="删除">🗑️</button>', 'title="删除">\n                            <i class="iconfont icon-delete"></i>\n                        </button>'),
]

for old, new in replacements:
    content = content.replace(old, new)

# 4. 添加主题悬浮提示样式
tooltip_styles = '''
        /* 主题按钮悬浮提示 */
        .toolbar-theme-btn {
            position: relative;
        }

        .toolbar-theme-btn::before {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 35px;
            left: 50%;
            transform: translateX(-50%);
            background: #333;
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 12px;
            white-space: nowrap;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s;
            z-index: 1000;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }

        .toolbar-theme-btn::after {
            content: '';
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            border: 5px solid transparent;
            border-top-color: #333;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s;
        }

        .toolbar-theme-btn:hover::before,
        .toolbar-theme-btn:hover::after {
            opacity: 1;
            visibility: visible;
        }
'''

if 'toolbar-theme-btn::before' not in content:
    # 在.toolbar-theme-btn样式后添加
    content = content.replace(
        '.toolbar-theme-btn:hover {\n            transform: scale(1.2);\n        }',
        '.toolbar-theme-btn:hover {\n            transform: scale(1.2);\n        }' + tooltip_styles
    )

# 5. 为主题按钮添加data-tooltip属性
theme_buttons = [
    ('data-theme="simple"', 'data-tooltip="简约通用型 | 干净清爽，适合技术干货"'),
    ('data-theme="literary"', 'data-tooltip="文艺清新型 | 柔和色调，适合读书笔记"'),
    ('data-theme="business"', 'data-tooltip="商务大气型 | 专业规整，适合行业报告"'),
    ('data-theme="cartoon"', 'data-tooltip="活泼卡通风 | 色彩明亮，适合轻松内容"'),
]

for theme_attr, tooltip_attr in theme_buttons:
    if tooltip_attr.split('=')[0] not in content:
        content = content.replace(
            theme_attr + ' onclick',
            theme_attr + ' ' + tooltip_attr + ' onclick'
        )

# 保存文件
with open('E:/workspace/opencode_workspace/markdown-reader-project/ai_creator/markdown-reader.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 文件修改完成！")
print("\n已完成的修改：")
print("1. ✅ 添加Iconfont CSS引用")
print("2. ✅ 添加Iconfont基础样式")
print("3. ✅ 替换emoji为Iconfont图标")
print("4. ✅ 添加主题悬浮提示样式")
print("5. ✅ 为主题按钮添加data-tooltip属性")
print("\n修改的文件：markdown-reader.html")
print("新增的CSS：iconfont/iconfont.css")