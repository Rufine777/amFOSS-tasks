import sys
import csv
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QGridLayout,
    QTextEdit, QSizePolicy, QLineEdit, QFileDialog
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from connector import MySQLConnector

class Dashboard2(QWidget):
    def __init__(self):
        super().__init__()
        self.db = MySQLConnector()
        if not self.db.connect():
            raise Exception("Failed to connect to database")

        self.search_mode = None
        self.selected_columns = set(["title", "year", "genre", "rating", "director", "stars"])

        self.setWindowTitle("CineScope – Dashboard")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet("background-color: #121212; color: white; padding: 20px;")
        self.init_ui()
        self.load_movies_data()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Header
        header = QLabel("🎬 CineScope Dashboard")
        header.setFont(QFont("Arial", 24, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setFixedHeight(80)
        main_layout.addWidget(header)

        split_layout = QHBoxLayout()

        # Left Panel
        left_container = QVBoxLayout()
        left_container.setSpacing(10)
        left_container.setAlignment(Qt.AlignTop)

        # Search By Section
        search_heading = QLabel("Search By")
        search_heading.setFont(QFont("Arial", 18, QFont.Bold))
        left_container.addWidget(search_heading)

        search_buttons = [
            ("Genre", "genre"),
            ("Year", "year"),
            ("Rating", "rating"),
            ("Director", "director"),
            ("Actor", "actor"),
        ]

        search_grid = QGridLayout()
        for index, (label, mode) in enumerate(search_buttons):
            btn = QPushButton(label)
            btn.setStyleSheet(self.get_button_style(False))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(lambda _, m=mode: self.set_search_mode(m))
            row, col = divmod(index, 2)
            search_grid.addWidget(btn, row, col)
        left_container.addLayout(search_grid)

        # Select Columns Section
        column_heading = QLabel("Select Columns")
        column_heading.setFont(QFont("Arial", 18, QFont.Bold))
        left_container.addWidget(column_heading)

        column_buttons = [
            ("Title", "title"),
            ("Year", "year"),
            ("Genre", "genre"),
            ("Rating", "rating"),
            ("Director", "director"),
            ("Stars", "stars"),
        ]

        column_grid = QGridLayout()
        for index, (label, col) in enumerate(column_buttons):
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setChecked(True)
            btn.setStyleSheet(self.get_button_style(True))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(lambda _, c=col, b=btn: self.toggle_column(c, b))
            row, col = divmod(index, 2)
            column_grid.addWidget(btn, row, col)
        left_container.addLayout(column_grid)

        # Search Input
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Enter search term")
        self.query_input.setStyleSheet("background-color: #1e1e1e; color: white; padding: 5px; border: 1px solid #444;")
        left_container.addWidget(self.query_input)

        # Action Buttons
        action_layout = QHBoxLayout()
        search_btn = QPushButton("Search")
        search_btn.setStyleSheet("background-color: #e50914; color: white; padding: 6px; border-radius: 5px;")
        search_btn.clicked.connect(self.execute_search)
        action_layout.addWidget(search_btn)

        export_btn = QPushButton("Export CSV")
        export_btn.setStyleSheet("background-color: #1f1f1f; color: white; padding: 6px; border-radius: 5px;")
        export_btn.clicked.connect(self.export_csv)
        action_layout.addWidget(export_btn)

        left_container.addLayout(action_layout)

        # Right Panel
        right_side_layout = QVBoxLayout()
        right_side_layout.setSpacing(10)

        # Table Widget
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                color: white;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: white;
                color: black;
                padding: 4px;
            }
        """)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Output Console
        self.output_console = QTextEdit()
        self.output_console.setPlaceholderText("Results will appear here...")
        self.output_console.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #444;
                padding: 5px;
            }
        """)
        self.output_console.setFixedHeight(100)

        right_side_layout.addWidget(self.table)
        right_side_layout.addWidget(self.output_console)

        split_layout.addLayout(left_container, 2)
        split_layout.addLayout(right_side_layout, 8)

        main_layout.addLayout(split_layout)
        self.setLayout(main_layout)

    def get_button_style(self, is_selected):
        if is_selected:
            return """
                QPushButton {
                    background-color: #ffcc00;
                    border: 1px solid #ff9900;
                    border-radius: 3px;
                    padding: 6px;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: #1f1f1f;
                    border: 1px solid #333;
                    border-radius: 3px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: #333;
                }
            """

    def set_search_mode(self, mode):
        self.search_mode = mode
        self.output_console.append(f"Search mode set to: {mode}")

    def toggle_column(self, column, button):
        if column in self.selected_columns:
            self.selected_columns.remove(column)
            button.setStyleSheet(self.get_button_style(False))
        else:
            self.selected_columns.add(column)
            button.setStyleSheet(self.get_button_style(True))
        self.output_console.append(f"Column toggled: {column}")

    def execute_search(self):
        if not self.search_mode:
            self.output_console.append("Please select a Search By mode.")
            return
        term = self.query_input.text().strip()
        if not term:
            self.output_console.append("Please enter a search term.")
            return

        mode_map = {
            "genre": "genre",
            "year": "released_year",
            "rating": "imdb_rating",
            "director": "director",
            "actor": ["star1", "star2", "star3"],
        }

        columns_map = {
            "title": "series_title",
            "year": "released_year",
            "genre": "genre",
            "rating": "imdb_rating",
            "director": "director",
            "stars": ["star1", "star2", "star3"],
        }

        columns_to_fetch = []
        for col in self.selected_columns:
            db_col = columns_map[col]
            if isinstance(db_col, list):
                columns_to_fetch.extend(db_col)
            else:
                columns_to_fetch.append(db_col)

        search_cols = mode_map[self.search_mode]

        results = []
        if isinstance(search_cols, list):
            for c in search_cols:
                rows = self.db.fetch_movies(columns=columns_to_fetch, search_column=c, search_value=term)
                if rows:
                    results.extend(rows)
            # Remove duplicates
            results = list({tuple(r): r for r in results}.values())
        else:
            results = self.db.fetch_movies(columns=columns_to_fetch, search_column=search_cols, search_value=term)

        self.display_results(results, columns_to_fetch)
        self.output_console.append(f"Search for '{term}' by {self.search_mode} returned {len(results) if results else 0} records.")

    def display_results(self, results, columns):
        if not results:
            self.output_console.append("No results found.")
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return

        headers_map_rev = {
            "series_title": "Title",
            "released_year": "Year",
            "genre": "Genre",
            "imdb_rating": "Rating",
            "director": "Director",
            "star1": "Star 1",
            "star2": "Star 2",
            "star3": "Star 3",
        }

        self.table.setRowCount(len(results))
        self.table.setColumnCount(len(columns))
        header_labels = [headers_map_rev.get(col, col) for col in columns]
        self.table.setHorizontalHeaderLabels(header_labels)

        for row_idx, row_data in enumerate(results):
            for col_idx, cell in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell)))

    def load_movies_data(self):
        columns = ["series_title", "released_year", "genre", "imdb_rating", "director", "star1", "star2", "star3"]
        results = self.db.fetch_movies(columns=columns)
        self.display_results(results, columns)
        self.output_console.append(f"Loaded {len(results) if results else 0} records from database.")

    def export_csv(self):
        if self.table.rowCount() == 0 or self.table.columnCount() == 0:
            self.output_console.append("No data to export.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if not path:
            return

        headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]

        with open(path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for row_idx in range(self.table.rowCount()):
                row = []
                for col_idx in range(self.table.columnCount()):
                    item = self.table.item(row_idx, col_idx)
                    row.append(item.text() if item else "")
                writer.writerow(row)

        self.output_console.append(f"Exported data to {path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard2()
    dashboard.show()
    sys.exit(app.exec())
