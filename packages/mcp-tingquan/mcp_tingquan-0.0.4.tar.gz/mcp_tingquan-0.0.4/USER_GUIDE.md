# MCP Feedback TingQuan Enhanced 用户指南

## 📖 简介

MCP Feedback TingQuan Enhanced 是一个强大的 MCP (Model Context Protocol) 服务器，为 AI 辅助开发工具提供人在回路的交互反馈功能。支持 Qt GUI 和 Web UI 双界面，具备图片上传、命令执行、多语言、主题切换等丰富功能。

## 🚀 快速开始

### 系统要求

- Python 3.11 或更高版本
- Windows、macOS 或 Linux 系统
- 支持 AI 编辑器（如 Cursor、Claude Desktop 等）

### 安装方法

#### 方法一：使用 uvx（推荐）

1. **安装 uv 包管理器**：
   ```bash
   # Windows (PowerShell)
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **运行工具**：
   ```bash
   uvx mcp-tingquan@latest
   ```

#### 方法二：使用 pip

```bash
pip install mcp-tingquan
python -m mcp_feedback_enhanced
```

## 🎯 配置 AI 编辑器

### Cursor 配置

1. 打开 Cursor 设置
2. 找到 MCP 服务器配置
3. 添加以下配置：

```json
{
  "mcpServers": {
    "mcp-tingquan": {
      "command": "uvx",
      "args": ["mcp-tingquan@latest"]
    }
  }
}
```

### Claude Desktop 配置

在 `claude_desktop_config.json` 文件中添加：

```json
{
  "mcpServers": {
    "mcp-tingquan": {
      "command": "uvx",
      "args": ["mcp-tingquan@latest"]
    }
  }
}
```

## 🎨 界面功能

### 主题选择

工具提供 5 种精美主题：

- 🌑 **经典深色**：原版深色主题，专业稳重
- 🌊 **海洋蓝**：清新淡雅的蓝色调
- 🌿 **森林绿**：自然护眼的绿色调
- 🌸 **樱花粉**：温馨柔和的粉色调
- 🔥 **炫酷红**：动感活力的红色调

**切换方法**：
1. 点击"设置"标签页
2. 在"界面主题"下拉框中选择喜欢的主题
3. 主题会立即生效并自动保存

### 界面模式

支持两种界面模式：

#### 分离模式
- AI 摘要和用户反馈分别显示在不同标签页
- 适合需要频繁查看摘要的场景

#### 合并模式
- AI 摘要和用户反馈在同一页面显示
- 支持垂直（上下）和水平（左右）布局
- 适合同时查看和编辑的场景

## 📝 使用功能

### 文本反馈
- 在"反馈"标签页输入文字反馈
- 支持多行文本和富文本格式
- 自动保存输入内容

### 图片上传
- 支持拖拽上传图片
- 支持剪贴板粘贴图片
- 自动压缩和格式转换
- 可设置图片大小限制

### 命令执行
- 在"命令"标签页执行系统命令
- 实时显示命令输出
- 支持命令历史记录

### 多语言支持
- 支持简体中文、繁体中文、英文
- 在设置页面切换语言
- 界面文字实时更新

## ⚙️ 高级设置

### 超时设置
- 可设置自动关闭时间
- 防止长时间占用系统资源
- 支持自定义超时时长

### 窗口设置
- 智能窗口定位
- 可选择总是在屏幕中心显示
- 自动保存窗口大小和位置

### 图片设置
- 可设置图片大小限制
- 支持 Base64 详细模式
- 自动优化图片质量

## 🔧 故障排除

### 常见问题

**Q: 无法启动 GUI 界面**
A: 确保已安装 PySide6：`pip install pyside6`

**Q: 图片上传失败**
A: 检查图片格式（支持 PNG、JPG、GIF）和大小限制

**Q: 命令执行没有输出**
A: 确保命令路径正确，检查系统权限

**Q: 主题切换不生效**
A: 重启应用程序，检查配置文件权限

### 获取帮助

- 🌐 **官方网站**：https://cursorpro.com.cn
- 💬 **技术支持**：通过官网联系我们
- 📧 **问题反馈**：在使用过程中遇到问题，欢迎反馈

## 📄 许可证

本项目采用开源许可证，详情请查看项目文档。

## 🙏 致谢

感谢所有用户的支持和反馈，让我们能够不断改进产品！

---

**祝您使用愉快！** 🎉 