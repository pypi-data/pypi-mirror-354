#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tab Auto-completion
===================

Tab untuk mengelola sistem auto-completion dan checkpoint.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, 
    QPushButton, QTextEdit, QSpinBox, QCheckBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QLineEdit,
    QComboBox, QSplitter, QTabWidget
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont
import json
import time

from ...utils.auto_completion import get_auto_completion_system
from ...utils.checkpoint_manager import get_checkpoint_integration
from ...models.completion_trigger import TriggerType
from ...models.checkpoint import CheckpointType


class AutoCompletionTab(QWidget):
    """Tab untuk mengelola auto-completion dan checkpoint"""
    
    # Signals
    status_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.auto_completion_system = get_auto_completion_system()
        self.checkpoint_integration = get_checkpoint_integration()
        
        self.setup_ui()
        self.setup_connections()
        self.refresh_status()
        
        # Timer untuk refresh otomatis
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_status)
        self.refresh_timer.start(5000)  # Refresh setiap 5 detik
    
    def setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        
        # Tab widget untuk memisahkan auto-completion dan checkpoint
        tab_widget = QTabWidget()
        
        # Tab Auto-completion
        auto_completion_tab = self.create_auto_completion_tab()
        tab_widget.addTab(auto_completion_tab, "🔔 Auto-completion")
        
        # Tab Checkpoint
        checkpoint_tab = self.create_checkpoint_tab()
        tab_widget.addTab(checkpoint_tab, "📋 Checkpoint")
        
        layout.addWidget(tab_widget)
    
    def create_auto_completion_tab(self) -> QWidget:
        """Membuat tab auto-completion"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Status Group
        status_group = QGroupBox("Status Auto-completion")
        status_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel("Status: Loading...")
        self.status_label.setFont(QFont("Consolas", 10))
        status_layout.addWidget(self.status_label)
        
        # Control buttons
        control_layout = QHBoxLayout()
        self.enable_btn = QPushButton("Enable Auto-completion")
        self.disable_btn = QPushButton("Disable Auto-completion")
        self.reset_session_btn = QPushButton("Reset Session")
        
        control_layout.addWidget(self.enable_btn)
        control_layout.addWidget(self.disable_btn)
        control_layout.addWidget(self.reset_session_btn)
        control_layout.addStretch()
        
        status_layout.addLayout(control_layout)
        layout.addWidget(status_group)
        
        # Configuration Group
        config_group = QGroupBox("Konfigurasi")
        config_layout = QVBoxLayout(config_group)
        
        # Auto trigger delay
        delay_layout = QHBoxLayout()
        delay_layout.addWidget(QLabel("Auto Trigger Delay (detik):"))
        self.delay_spinbox = QSpinBox()
        self.delay_spinbox.setRange(0, 60)
        self.delay_spinbox.setValue(2)
        delay_layout.addWidget(self.delay_spinbox)
        delay_layout.addStretch()
        config_layout.addLayout(delay_layout)
        
        # Max triggers per session
        max_triggers_layout = QHBoxLayout()
        max_triggers_layout.addWidget(QLabel("Max Triggers per Session:"))
        self.max_triggers_spinbox = QSpinBox()
        self.max_triggers_spinbox.setRange(1, 20)
        self.max_triggers_spinbox.setValue(5)
        max_triggers_layout.addWidget(self.max_triggers_spinbox)
        max_triggers_layout.addStretch()
        config_layout.addLayout(max_triggers_layout)
        
        # Cooldown period
        cooldown_layout = QHBoxLayout()
        cooldown_layout.addWidget(QLabel("Cooldown Period (detik):"))
        self.cooldown_spinbox = QSpinBox()
        self.cooldown_spinbox.setRange(10, 300)
        self.cooldown_spinbox.setValue(30)
        cooldown_layout.addWidget(self.cooldown_spinbox)
        cooldown_layout.addStretch()
        config_layout.addLayout(cooldown_layout)
        
        # Save config button
        self.save_config_btn = QPushButton("Simpan Konfigurasi")
        config_layout.addWidget(self.save_config_btn)
        
        layout.addWidget(config_group)
        
        # Test Group
        test_group = QGroupBox("Test Trigger")
        test_layout = QVBoxLayout(test_group)
        
        test_layout.addWidget(QLabel("Test text untuk trigger:"))
        self.test_text_edit = QLineEdit()
        self.test_text_edit.setPlaceholderText("Masukkan text untuk test trigger...")
        test_layout.addWidget(self.test_text_edit)
        
        test_btn_layout = QHBoxLayout()
        self.test_trigger_btn = QPushButton("Test Trigger")
        self.clear_test_btn = QPushButton("Clear")
        test_btn_layout.addWidget(self.test_trigger_btn)
        test_btn_layout.addWidget(self.clear_test_btn)
        test_btn_layout.addStretch()
        test_layout.addLayout(test_btn_layout)
        
        self.test_result_text = QTextEdit()
        self.test_result_text.setMaximumHeight(100)
        self.test_result_text.setReadOnly(True)
        test_layout.addWidget(self.test_result_text)
        
        layout.addWidget(test_group)
        
        # Trigger History Group
        history_group = QGroupBox("Trigger History")
        history_layout = QVBoxLayout(history_group)
        
        history_btn_layout = QHBoxLayout()
        self.refresh_history_btn = QPushButton("Refresh History")
        self.clear_history_btn = QPushButton("Clear History")
        history_btn_layout.addWidget(self.refresh_history_btn)
        history_btn_layout.addWidget(self.clear_history_btn)
        history_btn_layout.addStretch()
        history_layout.addLayout(history_btn_layout)
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Timestamp", "Triggers", "Text", "Context"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        history_layout.addWidget(self.history_table)
        
        layout.addWidget(history_group)
        
        return widget
    
    def create_checkpoint_tab(self) -> QWidget:
        """Membuat tab checkpoint"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Control Group
        control_group = QGroupBox("Kontrol Checkpoint")
        control_layout = QVBoxLayout(control_group)
        
        # Create checkpoint
        create_layout = QHBoxLayout()
        create_layout.addWidget(QLabel("Nama:"))
        self.checkpoint_name_edit = QLineEdit()
        self.checkpoint_name_edit.setPlaceholderText("Nama checkpoint...")
        create_layout.addWidget(self.checkpoint_name_edit)
        
        self.create_checkpoint_btn = QPushButton("Buat Checkpoint")
        create_layout.addWidget(self.create_checkpoint_btn)
        control_layout.addLayout(create_layout)
        
        # Description
        control_layout.addWidget(QLabel("Deskripsi:"))
        self.checkpoint_desc_edit = QLineEdit()
        self.checkpoint_desc_edit.setPlaceholderText("Deskripsi checkpoint...")
        control_layout.addWidget(self.checkpoint_desc_edit)
        
        # Auto checkpoint settings
        auto_checkpoint_layout = QHBoxLayout()
        self.auto_checkpoint_checkbox = QCheckBox("Enable Auto Checkpoint")
        auto_checkpoint_layout.addWidget(self.auto_checkpoint_checkbox)
        
        auto_checkpoint_layout.addWidget(QLabel("Interval (detik):"))
        self.auto_checkpoint_interval = QSpinBox()
        self.auto_checkpoint_interval.setRange(60, 3600)
        self.auto_checkpoint_interval.setValue(300)
        auto_checkpoint_layout.addWidget(self.auto_checkpoint_interval)
        auto_checkpoint_layout.addStretch()
        control_layout.addLayout(auto_checkpoint_layout)
        
        layout.addWidget(control_group)
        
        # Checkpoint List Group
        list_group = QGroupBox("Daftar Checkpoint")
        list_layout = QVBoxLayout(list_group)
        
        # Filter controls
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filter Type:"))
        self.checkpoint_type_combo = QComboBox()
        self.checkpoint_type_combo.addItem("All", "")
        for checkpoint_type in CheckpointType:
            self.checkpoint_type_combo.addItem(checkpoint_type.value.title(), checkpoint_type.value)
        filter_layout.addWidget(self.checkpoint_type_combo)
        
        self.refresh_checkpoints_btn = QPushButton("Refresh")
        filter_layout.addWidget(self.refresh_checkpoints_btn)
        filter_layout.addStretch()
        list_layout.addLayout(filter_layout)
        
        # Checkpoint table
        self.checkpoint_table = QTableWidget()
        self.checkpoint_table.setColumnCount(6)
        self.checkpoint_table.setHorizontalHeaderLabels([
            "Name", "Type", "Created", "Files", "Actions", "ID"
        ])
        self.checkpoint_table.horizontalHeader().setStretchLastSection(True)
        list_layout.addWidget(self.checkpoint_table)
        
        layout.addWidget(list_group)
        
        return widget
    
    def setup_connections(self):
        """Setup signal connections"""
        # Auto-completion controls
        self.enable_btn.clicked.connect(self.enable_auto_completion)
        self.disable_btn.clicked.connect(self.disable_auto_completion)
        self.reset_session_btn.clicked.connect(self.reset_session)
        self.save_config_btn.clicked.connect(self.save_config)
        
        # Test controls
        self.test_trigger_btn.clicked.connect(self.test_trigger)
        self.clear_test_btn.clicked.connect(self.clear_test)
        
        # History controls
        self.refresh_history_btn.clicked.connect(self.refresh_history)
        self.clear_history_btn.clicked.connect(self.clear_history)
        
        # Checkpoint controls
        self.create_checkpoint_btn.clicked.connect(self.create_checkpoint)
        self.refresh_checkpoints_btn.clicked.connect(self.refresh_checkpoints)
        self.auto_checkpoint_checkbox.toggled.connect(self.toggle_auto_checkpoint)
    
    def enable_auto_completion(self):
        """Enable auto-completion"""
        try:
            self.auto_completion_system.enable()
            self.status_changed.emit("Auto-completion enabled")
            self.refresh_status()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Gagal enable auto-completion: {str(e)}")
    
    def disable_auto_completion(self):
        """Disable auto-completion"""
        try:
            self.auto_completion_system.disable()
            self.status_changed.emit("Auto-completion disabled")
            self.refresh_status()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Gagal disable auto-completion: {str(e)}")
    
    def reset_session(self):
        """Reset session"""
        try:
            self.auto_completion_system.reset_session()
            self.status_changed.emit("Session reset")
            self.refresh_status()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Gagal reset session: {str(e)}")
    
    def save_config(self):
        """Save configuration"""
        try:
            self.auto_completion_system.update_config(
                auto_trigger_delay=self.delay_spinbox.value(),
                max_triggers_per_session=self.max_triggers_spinbox.value(),
                cooldown_period=self.cooldown_spinbox.value()
            )
            self.status_changed.emit("Configuration saved")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Gagal save config: {str(e)}")
    
    def test_trigger(self):
        """Test trigger"""
        try:
            text = self.test_text_edit.text()
            if not text:
                return
            
            triggered = self.auto_completion_system.trigger_manager.check_triggers(text)
            
            result = {
                "text": text,
                "triggered": len(triggered) > 0,
                "trigger_count": len(triggered),
                "triggers": [
                    {
                        "id": t.trigger_id,
                        "type": t.trigger_type.value,
                        "description": t.description
                    }
                    for t in triggered
                ]
            }
            
            self.test_result_text.setPlainText(json.dumps(result, ensure_ascii=False, indent=2))
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error testing trigger: {str(e)}")
    
    def clear_test(self):
        """Clear test"""
        self.test_text_edit.clear()
        self.test_result_text.clear()
    
    def refresh_status(self):
        """Refresh status display"""
        try:
            stats = self.auto_completion_system.get_statistics()
            
            status_text = f"""Status: {'Enabled' if stats['enabled'] else 'Disabled'}
Session Triggers: {stats['session_trigger_count']}
Total History: {stats['total_trigger_history']}
Last Trigger: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stats['last_trigger_time'])) if stats['last_trigger_time'] > 0 else 'Never'}
Registered Callbacks: {len(stats['registered_callbacks'])}

Config:
- Auto Trigger Delay: {stats['config']['auto_trigger_delay']}s
- Max Triggers/Session: {stats['config']['max_triggers_per_session']}
- Cooldown Period: {stats['config']['cooldown_period']}s"""
            
            self.status_label.setText(status_text)
            
            # Update config controls
            self.delay_spinbox.setValue(int(stats['config']['auto_trigger_delay']))
            self.max_triggers_spinbox.setValue(stats['config']['max_triggers_per_session'])
            self.cooldown_spinbox.setValue(int(stats['config']['cooldown_period']))
            
        except Exception as e:
            self.status_label.setText(f"Error loading status: {str(e)}")
    
    def refresh_history(self):
        """Refresh trigger history"""
        try:
            history = self.auto_completion_system.get_trigger_history(50)
            
            self.history_table.setRowCount(len(history))
            
            for i, record in enumerate(history):
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record['timestamp']))
                triggers = ', '.join(record['triggers'])
                text = record['text'][:50] + "..." if len(record['text']) > 50 else record['text']
                context = str(record.get('context', {}))[:30] + "..." if len(str(record.get('context', {}))) > 30 else str(record.get('context', {}))
                
                self.history_table.setItem(i, 0, QTableWidgetItem(timestamp))
                self.history_table.setItem(i, 1, QTableWidgetItem(triggers))
                self.history_table.setItem(i, 2, QTableWidgetItem(text))
                self.history_table.setItem(i, 3, QTableWidgetItem(context))
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error refreshing history: {str(e)}")
    
    def clear_history(self):
        """Clear trigger history"""
        try:
            self.auto_completion_system.clear_trigger_history()
            self.refresh_history()
            self.status_changed.emit("Trigger history cleared")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error clearing history: {str(e)}")
    
    def create_checkpoint(self):
        """Create checkpoint"""
        try:
            name = self.checkpoint_name_edit.text() or f"Manual Checkpoint {time.strftime('%Y-%m-%d %H:%M:%S')}"
            description = self.checkpoint_desc_edit.text()
            
            checkpoint_id = self.checkpoint_integration.create_checkpoint(
                name=name,
                description=description,
                checkpoint_type=CheckpointType.MANUAL,
                project_directory=".",  # Current directory
                tags=["manual", "gui"]
            )
            
            self.checkpoint_name_edit.clear()
            self.checkpoint_desc_edit.clear()
            self.refresh_checkpoints()
            self.status_changed.emit(f"Checkpoint created: {checkpoint_id}")
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error creating checkpoint: {str(e)}")
    
    def refresh_checkpoints(self):
        """Refresh checkpoint list"""
        try:
            filter_type = self.checkpoint_type_combo.currentData()
            checkpoints = self.checkpoint_integration.checkpoint_manager.list_checkpoints()
            
            # Filter by type if specified
            if filter_type:
                checkpoints = [c for c in checkpoints if c.checkpoint_type.value == filter_type]
            
            self.checkpoint_table.setRowCount(len(checkpoints))
            
            for i, checkpoint in enumerate(checkpoints):
                info = self.checkpoint_integration.checkpoint_manager.get_checkpoint_info(checkpoint.checkpoint_id)
                
                self.checkpoint_table.setItem(i, 0, QTableWidgetItem(info['name']))
                self.checkpoint_table.setItem(i, 1, QTableWidgetItem(info['type']))
                self.checkpoint_table.setItem(i, 2, QTableWidgetItem(info['created_at_str']))
                self.checkpoint_table.setItem(i, 3, QTableWidgetItem(str(info['file_count'])))
                
                # Actions button
                restore_btn = QPushButton("Restore")
                restore_btn.clicked.connect(lambda checked, cid=checkpoint.checkpoint_id: self.restore_checkpoint(cid))
                self.checkpoint_table.setCellWidget(i, 4, restore_btn)
                
                self.checkpoint_table.setItem(i, 5, QTableWidgetItem(checkpoint.checkpoint_id))
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error refreshing checkpoints: {str(e)}")
    
    def restore_checkpoint(self, checkpoint_id: str):
        """Restore checkpoint"""
        try:
            reply = QMessageBox.question(
                self, 
                "Confirm Restore", 
                f"Restore checkpoint {checkpoint_id}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                success = self.checkpoint_integration.restore_checkpoint(checkpoint_id)
                if success:
                    self.status_changed.emit(f"Checkpoint restored: {checkpoint_id}")
                    QMessageBox.information(self, "Success", "Checkpoint restored successfully!")
                else:
                    QMessageBox.warning(self, "Error", "Failed to restore checkpoint")
                    
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error restoring checkpoint: {str(e)}")
    
    def toggle_auto_checkpoint(self, enabled: bool):
        """Toggle auto checkpoint"""
        try:
            if enabled:
                interval = self.auto_checkpoint_interval.value()
                self.checkpoint_integration.set_auto_checkpoint_interval(interval)
                self.checkpoint_integration.enable_auto_checkpoint()
            else:
                self.checkpoint_integration.disable_auto_checkpoint()
            
            self.status_changed.emit(f"Auto checkpoint {'enabled' if enabled else 'disabled'}")
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error toggling auto checkpoint: {str(e)}")
