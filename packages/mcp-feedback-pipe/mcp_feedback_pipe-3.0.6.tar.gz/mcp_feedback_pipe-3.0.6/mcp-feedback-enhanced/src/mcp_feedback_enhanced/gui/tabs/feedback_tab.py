#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
回饋分頁組件
============

專門處理用戶回饋輸入的分頁組件。
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSplitter, QSizePolicy
from PySide6.QtCore import Qt, Signal

from ..widgets import SmartTextEdit, ImageUploadWidget
from ...i18n import t
from ..window.config_manager import ConfigManager


class FeedbackTab(QWidget):
    """回饋分頁組件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = ConfigManager()
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """設置用戶介面"""
        # 主布局
        tab_layout = QVBoxLayout(self)
        tab_layout.setSpacing(12)
        tab_layout.setContentsMargins(0, 0, 0, 0)  # 設置邊距為0，與合併分頁保持一致
        
        # 說明文字容器
        description_wrapper = QWidget()
        description_layout = QVBoxLayout(description_wrapper)
        description_layout.setContentsMargins(16, 16, 16, 10)  # 只對說明文字設置邊距
        description_layout.setSpacing(0)
        
        # 說明文字
        self.feedback_description = QLabel(t('feedback.description'))
        self.feedback_description.setStyleSheet("color: #9e9e9e; font-size: 12px;")
        self.feedback_description.setWordWrap(True)
        description_layout.addWidget(self.feedback_description)
        
        tab_layout.addWidget(description_wrapper)
        
        # 使用分割器來管理回饋輸入和圖片區域
        splitter_wrapper = QWidget()  # 創建包裝容器
        splitter_wrapper_layout = QVBoxLayout(splitter_wrapper)
        splitter_wrapper_layout.setContentsMargins(16, 0, 16, 16)  # 設置左右邊距
        splitter_wrapper_layout.setSpacing(0)
        
        feedback_splitter = QSplitter(Qt.Vertical)
        feedback_splitter.setChildrenCollapsible(False)
        feedback_splitter.setHandleWidth(6)
        feedback_splitter.setContentsMargins(0, 0, 0, 0)  # 設置分割器邊距為0
        feedback_splitter.setStyleSheet("""
            QSplitter {
                border: none;
                background: transparent;
            }
            QSplitter::handle:vertical {
                height: 8px;
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 4px;
                margin-left: 0px;
                margin-right: 0px;
                margin-top: 2px;
                margin-bottom: 2px;
            }
            QSplitter::handle:vertical:hover {
                background-color: #606060;
                border-color: #808080;
            }
            QSplitter::handle:vertical:pressed {
                background-color: #007acc;
                border-color: #005a9e;
            }
        """)
        
        # 創建圖片上傳區域（需要先創建以便連接信號）
        image_upload_widget = QWidget()
        image_upload_widget.setMinimumHeight(200)  # 進一步增加最小高度
        image_upload_widget.setMaximumHeight(320)  # 增加最大高度
        image_upload_layout = QVBoxLayout(image_upload_widget)
        image_upload_layout.setSpacing(8)
        image_upload_layout.setContentsMargins(0, 8, 0, 0)  # 與回饋輸入區域保持一致的邊距
        
        self.image_upload = ImageUploadWidget(config_manager=self.config_manager)
        image_upload_layout.addWidget(self.image_upload, 1)
        
        # 回饋輸入區域
        self.feedback_input = SmartTextEdit()
        placeholder_text = t('feedback.placeholder').replace("Ctrl+Enter", "Ctrl+Enter/Cmd+Enter").replace("Ctrl+V", "Ctrl+V/Cmd+V")
        self.feedback_input.setPlaceholderText(placeholder_text)
        self.feedback_input.setMinimumHeight(120)
        self.feedback_input.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d30;
                border: 1px solid #464647;
                border-radius: 4px;
                padding: 10px;
                color: #ffffff;
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        # 直接連接文字輸入框的圖片貼上信號到圖片上傳組件
        self.feedback_input.image_paste_requested.connect(self.image_upload.paste_from_clipboard)
        
        # 添加到分割器
        feedback_splitter.addWidget(self.feedback_input)
        feedback_splitter.addWidget(image_upload_widget)
        
        # 調整分割器比例和設置（確保圖片區域始終可見）
        feedback_splitter.setStretchFactor(0, 2)  # 回饋輸入區域
        feedback_splitter.setStretchFactor(1, 1)  # 圖片上傳區域
        
        # 從配置載入分割器位置，如果沒有則使用預設值
        saved_sizes = self.config_manager.get_splitter_sizes('feedback_splitter')
        if saved_sizes and len(saved_sizes) == 2:
            feedback_splitter.setSizes(saved_sizes)
        else:
            feedback_splitter.setSizes([220, 200])    # 預設大小
        
        # 連接分割器位置變化信號，自動保存位置
        feedback_splitter.splitterMoved.connect(
            lambda pos, index: self._save_feedback_splitter_position(feedback_splitter)
        )
        
        # 設置分割器的最小尺寸和處理策略
        feedback_splitter.setMinimumHeight(200)   # 降低分割器最小高度，支持小窗口
        feedback_splitter.setMaximumHeight(2000)  # 允許更大的高度以觸發滾動
        
        # 確保子控件的最小尺寸（防止過度壓縮）
        self.feedback_input.setMinimumHeight(80)   # 降低文字輸入最小高度
        image_upload_widget.setMinimumHeight(100)  # 降低圖片區域最小高度
        
        splitter_wrapper_layout.addWidget(feedback_splitter)
        
        tab_layout.addWidget(splitter_wrapper, 1)
        
        # 設置分頁的大小策略，確保能夠觸發父容器的滾動條
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.setMinimumHeight(200)  # 降低回饋分頁最小高度  # 設置最小高度
    
    def get_feedback_text(self) -> str:
        """獲取回饋文字"""
        return self.feedback_input.toPlainText().strip()
    
    def get_images_data(self) -> list:
        """獲取圖片數據"""
        return self.image_upload.get_images_data()
    
    def update_texts(self) -> None:
        """更新界面文字（用於語言切換）"""
        self.feedback_description.setText(t('feedback.description'))
        placeholder_text = t('feedback.placeholder').replace("Ctrl+Enter", "Ctrl+Enter/Cmd+Enter").replace("Ctrl+V", "Ctrl+V/Cmd+V")
        self.feedback_input.setPlaceholderText(placeholder_text)
        
        if hasattr(self, 'image_upload'):
            self.image_upload.update_texts()

    def _save_feedback_splitter_position(self, splitter: QSplitter) -> None:
        """保存分割器的位置"""
        sizes = splitter.sizes()
        self.config_manager.set_splitter_sizes('feedback_splitter', sizes) 