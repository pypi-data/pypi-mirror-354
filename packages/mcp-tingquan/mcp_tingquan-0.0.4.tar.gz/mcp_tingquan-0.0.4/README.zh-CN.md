# MCP Feedback TingQuan Enhanced（交互反馈 MCP）

**🌐 语言切换 / Language:** [English](README.md) | [繁體中文](README.zh-TW.md) | **简体中文**

**原作者：** [Fábio Ferreira](https://x.com/fabiomlferreira) | [原始项目](https://github.com/noopstudios/interactive-feedback-mcp) ⭐
**增强版本：** [maticarmy](https://github.com/maticarmy)
**官方网站：** [https://cursorpro.com.cn](https://cursorpro.com.cn)

## 🎯 核心概念

这是一个 [MCP 服务器](https://modelcontextprotocol.io/)，建立**反馈导向的开发工作流程**，完美适配本地、**SSH 远程开发环境**与 **WSL (Windows Subsystem for Linux) 环境**。通过引导 AI 与用户确认而非进行推测性操作，可将多次工具调用合并为单次反馈导向请求，大幅节省平台成本并提升开发效率。

**支持平台：** [Cursor](https://www.cursor.com) | [Cline](https://cline.bot) | [Windsurf](https://windsurf.com) | [Augment](https://www.augmentcode.com) | [Trae](https://www.trae.ai)

### 🔄 工作流程
1. **AI 调用** → `mcp-tingquan`
2. **环境检测** → 自动选择合适界面
3. **用户交互** → 命令执行、文字反馈、图片上传
4. **反馈传递** → 信息返回 AI
5. **流程继续** → 根据反馈调整或结束

## 🌟 主要功能

### 🖥️ 双界面系统
- **Qt GUI**：本地环境原生体验，模块化重构设计
- **Web UI**：远程 SSH 环境与 WSL 环境现代化界面，全新架构
- **智能切换**：自动检测环境（本地/远程/WSL）并选择最适界面

### 🎨 全新界面设计
- **模块化架构**：GUI 和 Web UI 均采用模块化设计
- **集中管理**：文件夹结构重新组织，维护更容易
- **现代化主题**：改进的视觉设计和用户体验
- **响应式布局**：适应不同屏幕尺寸和窗口大小

### 🖼️ 图片支持
- **格式支持**：PNG、JPG、JPEG、GIF、BMP、WebP
- **上传方式**：拖拽文件 + 剪贴板粘贴（Ctrl+V）
- **自动处理**：智能压缩确保符合 1MB 限制

### 🌏 多语言
- **三语支持**：简体中文、英文、繁体中文
- **智能检测**：根据系统语言自动选择
- **即时切换**：界面内可直接切换语言

### ✨ WSL 环境支持
- **自动检测**：智能识别 WSL (Windows Subsystem for Linux) 环境
- **浏览器整合**：WSL 环境下自动启动 Windows 浏览器
- **多种启动方式**：支持 `cmd.exe`、`powershell.exe`、`wslview` 等多种浏览器启动方法
- **无缝体验**：WSL 用户可直接使用 Web UI，无需额外配置

## 🖥️ 界面预览

### Qt GUI 界面
<div align="center">
  <img src="docs/zh-CN/images/gui1.png" width="400" alt="Qt GUI 主界面" />
  <img src="docs/zh-CN/images/gui2.png" width="400" alt="Qt GUI 设置界面" />
</div>

*Qt GUI 界面 - 模块化重构，支持本地环境*

### Web UI 界面
<div align="center">
  <img src="docs/zh-CN/images/web1.png" width="400" alt="Web UI 主界面" />
  <img src="docs/zh-CN/images/web2.png" width="400" alt="Web UI 设置界面" />
</div>

*Web UI 界面 - 全新架构，适合 SSH Remote 环境*

**快捷键支持**
- `Ctrl+Enter`（Windows/Linux）/ `Cmd+Enter`（macOS）：提交反馈（主键盘与数字键盘皆支持）
- `Ctrl+V`（Windows/Linux）/ `Cmd+V`（macOS）：直接粘贴剪贴板图片

## 🚀 快速开始

### 1. 安装与测试
```bash
# 安装 uv（如果尚未安装）
pip install uv

# 快速测试
uvx mcp-tingquan@latest test
```

### 2. 配置 MCP
**基本配置**（适合大多数用户）：
```json
{
  "mcpServers": {
    "mcp-tingquan": {
      "command": "uvx",
      "args": ["mcp-tingquan@latest"],
      "timeout": 600,
      "autoApprove": ["interactive_feedback"]
    }
  }
}
```

**进阶配置**（需要自定义环境）：
```json
{
  "mcpServers": {
    "mcp-tingquan": {
      "command": "uvx",
      "args": ["mcp-tingquan@latest"],
      "timeout": 600,
      "env": {
        "FORCE_WEB": "true",
        "MCP_DEBUG": "false"
      },
      "autoApprove": ["interactive_feedback"]
    }
  }
}
```

### 3. 设定提示工程
为了获得最佳效果，请在 AI 助手中添加以下规则：

```
# MCP Interactive Feedback 规则

1. 在任何流程、任务、对话进行时，无论是询问、回复、或完成阶段性任务，皆必须调用 MCP mcp-tingquan。
2. 每当收到用户反馈，若反馈内容非空，必须再次调用 MCP mcp-tingquan，并根据反馈内容调整行为。
3. 仅当用户明确表示「结束」或「不再需要交互」时，才可停止调用 MCP mcp-tingquan，流程才算结束。
4. 除非收到结束指令，否则所有步骤都必须重复调用 MCP mcp-tingquan。
5. 完成任务前，必须使用 MCP mcp-tingquan 工具向用户询问反馈。
```

## ⚙️ 进阶设定

### 环境变量
| 变量 | 用途 | 值 | 默认 |
|------|------|-----|------|
| `FORCE_WEB` | 强制使用 Web UI | `true`/`false` | `false` |
| `MCP_DEBUG` | 调试模式 | `true`/`false` | `false` |

### 测试选项
```bash
# 版本查询
uvx mcp-tingquan@latest version       # 检查版本

# 指定界面测试
uvx mcp-tingquan@latest test --gui    # 快速测试 Qt GUI
uvx mcp-tingquan@latest test --web    # 测试 Web UI (自动持续运行)

# 调试模式
MCP_DEBUG=true uvx mcp-tingquan@latest test
```

### 开发者安装
```bash
git clone https://github.com/maticarmy/mcp-tingquan.git
cd mcp-tingquan
uv sync
```

**本地测试方式**
```bash
# 方式一：标准测试（推荐）
uv run python -m mcp_feedback_enhanced test

# 方式二：完整测试套件（macOS 和 Windows 通用开发环境）
uvx --with-editable . mcp-tingquan test

# 方式三：指定界面测试
uvx --with-editable . mcp-tingquan test --gui    # 快速测试 Qt GUI
uvx --with-editable . mcp-tingquan test --web    # 测试 Web UI (自动持续运行)
```

**测试说明**
- **标准测试**：执行完整的功能检查，适合日常开发验证
- **完整测试**：包含所有组件的深度测试，适合发布前验证
- **Qt GUI 测试**：快速启动并测试本地图形界面
- **Web UI 测试**：启动 Web 服务器并保持运行，便于完整测试 Web 功能

## 🆕 版本更新记录

### 最新版本亮点（v0.0.2）
- 🎨 **界面优化**: 优化关于页面文字信息和界面显示
- 🖥️ **双界面支持**: Qt GUI 和 Web UI 双界面系统
- 🌐 **智能环境检测**: 自动选择合适的界面类型
- 🖼️ **图片上传支持**: 支持多种图片格式上传和处理
- 🌏 **多语言支持**: 中英文界面切换
- ✨ **WSL 环境支持**: 完整支持 WSL 环境的 Web UI

## 🐛 常见问题

**Q: 出现 "Unexpected token 'D'" 错误**
A: 调试输出干扰。设置 `MCP_DEBUG=false` 或移除该环境变量。

**Q: 中文字符乱码**
A: 最新版本已优化编码处理。更新到最新版本：`uvx mcp-tingquan@latest`

**Q: 图片上传失败**
A: 检查文件大小（≤1MB）和格式（PNG/JPG/GIF/BMP/WebP）。

**Q: Web UI 无法启动**
A: 设置 `FORCE_WEB=true` 或检查防火墙设定。

**Q: WSL 环境下无法启动浏览器**
A: 确认 WSL 版本（建议使用 WSL 2）和 Windows 浏览器是否正常安装。

## 🙏 致谢

### 🌟 支持原作者
**Fábio Ferreira** - [X @fabiomlferreira](https://x.com/fabiomlferreira)
**原始项目：** [noopstudios/interactive-feedback-mcp](https://github.com/noopstudios/interactive-feedback-mcp)

如果您觉得有用，请：
- ⭐ [为原项目按星星](https://github.com/noopstudios/interactive-feedback-mcp)
- 📱 [关注原作者](https://x.com/fabiomlferreira)

### 技术支持
- **官方网站：** [https://cursorpro.com.cn](https://cursorpro.com.cn)
- **技术支持：** [https://cursorpro.com.cn](https://cursorpro.com.cn)

## 📄 授权

MIT 授权条款 - 详见 [LICENSE](LICENSE) 档案

---
**🌟 欢迎使用 MCP Feedback TingQuan Enhanced！**