#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
關於分頁組件
============

顯示應用程式資訊和聯繫方式的分頁組件。
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QPushButton, QTextEdit, QScrollArea
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont, QDesktopServices

from ...i18n import t
from ... import __version__


class AboutTab(QWidget):
    """關於分頁組件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """設置用戶介面"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 創建滾動區域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background-color: #2d2d30;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #464647;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #555555;
            }
        """)
        
        # 創建內容容器
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(16)
        content_layout.setContentsMargins(16, 16, 16, 16)
        
        # === 主要資訊區域（合併應用程式資訊、專案連結、聯繫與支援） ===
        self.main_info_group = QGroupBox("应用程序信息")
        self.main_info_group.setObjectName('main_info_group')
        main_info_layout = QVBoxLayout(self.main_info_group)
        main_info_layout.setSpacing(16)
        main_info_layout.setContentsMargins(20, 20, 20, 20)
        
        # 應用程式標題和版本
        title_layout = QHBoxLayout()
        self.app_title_label = QLabel("MCP Feedback TingQuan Enhanced")
        self.app_title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #e0e0e0;")
        title_layout.addWidget(self.app_title_label)
        
        title_layout.addStretch()
        
        self.version_label = QLabel(f"v{__version__}")
        self.version_label.setStyleSheet("font-size: 16px; color: #007acc; font-weight: bold;")
        title_layout.addWidget(self.version_label)
        
        main_info_layout.addLayout(title_layout)
        
        # 應用程式描述
        self.app_description = QLabel("一个强大的 MCP 服务器，为 AI 辅助的开发工具提供人在回路的交互反馈功能。支持 Qt GUI 和 Web UI 双界面，并具备图片上传、命令执行、多语言等丰富功能。")
        self.app_description.setStyleSheet("color: #9e9e9e; font-size: 13px; line-height: 1.4; margin-bottom: 16px;")
        self.app_description.setWordWrap(True)
        main_info_layout.addWidget(self.app_description)
        
        # 分隔線
        separator1 = QLabel()
        separator1.setFixedHeight(1)
        separator1.setStyleSheet("background-color: #464647; margin: 8px 0;")
        main_info_layout.addWidget(separator1)
        
        # 官网区域
        website_layout = QHBoxLayout()
        self.website_label = QLabel("🌐 官方网站")
        self.website_label.setStyleSheet("font-weight: bold; color: #e0e0e0; font-size: 14px;")
        website_layout.addWidget(self.website_label)
        
        website_layout.addStretch()
        
        self.website_button = QPushButton("访问官网")
        self.website_button.setFixedSize(120, 32)
        self.website_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                border: none;
                border-radius: 4px;
                color: white;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        self.website_button.clicked.connect(self._open_website)
        website_layout.addWidget(self.website_button)
        
        main_info_layout.addLayout(website_layout)
        
        # 官网 URL
        self.website_url_label = QLabel("https://cursorpro.com.cn")
        self.website_url_label.setStyleSheet("color: #9e9e9e; font-size: 11px; margin-left: 24px; margin-bottom: 12px;")
        main_info_layout.addWidget(self.website_url_label)
        
        # 分隔線
        separator2 = QLabel()
        separator2.setFixedHeight(1)
        separator2.setStyleSheet("background-color: #464647; margin: 8px 0;")
        main_info_layout.addWidget(separator2)
        
        # 技术支持区域
        support_layout = QHBoxLayout()
        self.support_label = QLabel("💬 技术支持")
        self.support_label.setStyleSheet("font-weight: bold; color: #e0e0e0; font-size: 14px;")
        support_layout.addWidget(self.support_label)
        
        support_layout.addStretch()
        
        self.support_button = QPushButton("联系我们")
        self.support_button.setFixedSize(120, 32)
        self.support_button.setStyleSheet("""
            QPushButton {
                background-color: #5865F2;
                border: none;
                border-radius: 4px;
                color: white;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4752C4;
            }
            QPushButton:pressed {
                background-color: #3C45A5;
            }
        """)
        self.support_button.clicked.connect(self._open_support)
        support_layout.addWidget(self.support_button)
        
        main_info_layout.addLayout(support_layout)
        
        # 支持说明
        self.support_url_label = QLabel("如需技术支持，请通过官网联系我们")
        self.support_url_label.setStyleSheet("color: #9e9e9e; font-size: 11px; margin-left: 24px;")
        main_info_layout.addWidget(self.support_url_label)
        
        self.contact_description = QLabel("我们提供专业的技术支持服务，帮助您解决使用过程中遇到的问题。")
        self.contact_description.setStyleSheet("color: #9e9e9e; font-size: 12px; margin-left: 24px; margin-top: 8px;")
        self.contact_description.setWordWrap(True)
        main_info_layout.addWidget(self.contact_description)
        
        content_layout.addWidget(self.main_info_group)
        
        # === 致謝區域 ===
        self.thanks_group = QGroupBox("致谢与贡献")
        self.thanks_group.setObjectName('thanks_group')
        thanks_layout = QVBoxLayout(self.thanks_group)
        thanks_layout.setSpacing(12)
        thanks_layout.setContentsMargins(20, 20, 20, 20)
        
        # 致謝文字
        self.thanks_text = QTextEdit()
        self.thanks_text.setReadOnly(True)
        self.thanks_text.setMinimumHeight(160)
        self.thanks_text.setMaximumHeight(220)
        self.thanks_text.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d30;
                border: 1px solid #464647;
                border-radius: 4px;
                padding: 12px;
                color: #e0e0e0;
                font-size: 12px;
                line-height: 1.4;
            }
            QScrollBar:vertical {
                background-color: #2d2d30;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #464647;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #555555;
            }
        """)
        self.thanks_text.setPlainText("感谢您使用 MCP Feedback TingQuan Enhanced！\n\n本项目致力于为 AI 辅助开发提供更好的交互体验。\n\n如果您在使用过程中有任何建议或问题，欢迎通过官网联系我们。\n\n祝您使用愉快！")
        thanks_layout.addWidget(self.thanks_text)
        
        content_layout.addWidget(self.thanks_group)
        
        # 添加彈性空間
        content_layout.addStretch()
        
        # 設置滾動區域的內容
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
    
    def _open_website(self) -> None:
        """開啟 官方网站"""
        QDesktopServices.openUrl(QUrl("https://cursorpro.com.cn"))
    
    def _open_support(self) -> None:
        """開啟 技术支持"""
        QDesktopServices.openUrl(QUrl("https://cursorpro.com.cn"))
    
    def update_texts(self) -> None:
        """更新界面文字（用於語言切換）"""
        # 更新GroupBox標題
        self.main_info_group.setTitle("应用程序信息")
        self.thanks_group.setTitle("致谢与贡献")
        
        # 更新版本資訊
        self.version_label.setText(f"v{__version__}")
        
        # 更新描述文字
        self.app_description.setText("一个强大的 MCP 服务器，为 AI 辅助的开发工具提供人在回路的交互反馈功能。支持 Qt GUI 和 Web UI 双界面，并具备图片上传、命令执行、多语言等丰富功能。")
        self.contact_description.setText("我们提供专业的技术支持服务，帮助您解决使用过程中遇到的问题。")
        
        # 更新標籤文字
        self.website_label.setText("🌐 官方网站")
        self.support_label.setText("💬 技术支持")
        
        # 更新按鈕文字
        self.website_button.setText("访问官网")
        self.support_button.setText("联系我们")
        
        # 更新致謝文字
        self.thanks_text.setPlainText("感谢您使用 MCP Feedback TingQuan Enhanced！\n\n本项目致力于为 AI 辅助开发提供更好的交互体验。\n\n如果您在使用过程中有任何建议或问题，欢迎通过官网联系我们。\n\n祝您使用愉快！") 