class ThemeManager:
    @staticmethod
    def get_dark_theme():
        return """
            QMainWindow, QWidget {
                background-color: #09090b; /* Zinc 950 */
                color: #fafafa;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
            
            /* Sidebar Styling */
            Sidebar {
                background-color: #18181b; /* Zinc 900 */
                border-right: 1px solid #27272a;
            }
            Sidebar QLabel {
                color: #3b82f6;
                font-weight: 800;
                margin-bottom: 20px;
            }
            Sidebar QPushButton {
                text-align: left;
                padding: 10px 16px;
                border: none;
                background: transparent;
                font-size: 13px;
                color: #a1a1aa;
                border-radius: 6px;
                margin: 2px 8px;
            }
            Sidebar QPushButton:hover {
                background-color: #27272a;
                color: #fff;
            }
            Sidebar QPushButton:checked {
                background-color: #27272a;
                color: #fff;
                font-weight: 600;
            }

            /* Buttons */
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
            QPushButton:disabled {
                background-color: #27272a;
                color: #52525b;
            }

            /* Inputs */
            QLineEdit, QTextEdit, QComboBox {
                background-color: #18181b;
                border: 1px solid #27272a;
                color: #fff;
                border-radius: 6px;
                padding: 8px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #3b82f6;
            }

            /* ScrollBars */
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 8px;
            }
            QScrollBar::handle:vertical {
                background: #3f3f46;
                border-radius: 4px;
            }
            
            /* Tabs */
            QTabWidget::pane {
                border: 1px solid #27272a;
                background-color: #09090b;
                border-radius: 6px;
            }
            QTabBar::tab {
                background: #18181b;
                color: #a1a1aa;
                padding: 8px 16px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #27272a;
                color: #fff;
            }
        """

    @staticmethod
    def get_light_theme():
        return """
            QMainWindow, QWidget {
                background-color: #ffffff;
                color: #09090b;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
            
            Sidebar {
                background-color: #f4f4f5;
                border-right: 1px solid #e4e4e7;
            }
            Sidebar QPushButton {
                text-align: left;
                padding: 10px 16px;
                border: none;
                background: transparent;
                font-size: 13px;
                color: #71717a;
                border-radius: 6px;
                margin: 2px 8px;
            }
            Sidebar QPushButton:hover {
                background-color: #e4e4e7;
                color: #09090b;
            }
            Sidebar QPushButton:checked {
                background-color: #e4e4e7;
                color: #09090b;
            }

            QPushButton {
                background-color: #09090b;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 600;
            }
        """
