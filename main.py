import sys
import pandas as pd

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget, QLabel,
    QComboBox, QPushButton, QMessageBox,
    QDialog, QHBoxLayout, QProgressBar, QLineEdit,
    QGroupBox, QFormLayout, QHeaderView, QTabWidget
)

from scrapper import ScraperWorker

from sorting_algorithms import (
    bubble_sort,
    insertion_sort,
    selection_sort,
    merge_sort,
    hybrid_merge_sort,
    quick_sort,
    heap_sort
)


class BookExplorer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Book Data Explorer")
        self.resize(1400, 850)
        self.setMinimumSize(950, 600)

        self.df = pd.read_csv("books_data.csv")
        self.filtered_df = self.df.copy()
        self.worker = None

        # Header

        self.label = QLabel(
            "BOOK DATA EXPLORER     |     Total Books: "
            + str(len(self.df))
        )
        self.label.setObjectName("summaryLabel")

        # Sorting controls

        self.algorithm_box = QComboBox()
        self.algorithm_box.addItems([
            "Bubble Sort",
            "Insertion Sort",
            "Selection Sort",
            "Merge Sort",
            "Hybrid Merge Sort",
            "Quick Sort",
            "Heap Sort"
        ])

        self.column_box = QComboBox()
        self.column_box.addItems(self.df.columns.tolist())

        self.second_sort_column_box = QComboBox()
        self.second_sort_column_box.addItems(
            ["None"] + self.df.columns.tolist()
        )

        self.third_sort_column_box = QComboBox()
        self.third_sort_column_box.addItems(
            ["None"] + self.df.columns.tolist()
        )

        self.sort_order_box = QComboBox()
        self.sort_order_box.addItems([
            "Ascending",
            "Descending"
        ])

        self.sort_scope_box = QComboBox()
        self.sort_scope_box.addItems([
            "Full Dataset",
            "Filtered Results"
        ])

        self.sort_button = QPushButton("Sort Books")
        self.sort_button.clicked.connect(self.sort_books)

        self.benchmark_button = QPushButton("Benchmark")
        self.benchmark_button.clicked.connect(
            self.benchmark_sorts
        )

        # First search condition

        self.search_column_box = QComboBox()
        self.search_column_box.addItems(
            self.df.columns.tolist()
        )

        self.filter_box = QComboBox()
        self.filter_box.addItems([
            "Contains",
            "Starts With",
            "Ends With",
            "Equals",
            "Does Not Contain"
        ])

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Enter first search text"
        )

        # Second search condition

        self.second_search_column_box = QComboBox()
        self.second_search_column_box.addItems(
            self.df.columns.tolist()
        )

        self.second_filter_box = QComboBox()
        self.second_filter_box.addItems([
            "Contains",
            "Starts With",
            "Ends With",
            "Equals",
            "Does Not Contain"
        ])

        self.second_search_input = QLineEdit()
        self.second_search_input.setPlaceholderText(
            "Optional second search text"
        )

        self.logic_box = QComboBox()
        self.logic_box.addItems(["AND", "OR", "NOT"])

        self.search_button = QPushButton("Search Books")
        self.search_button.clicked.connect(
            self.search_books_table
        )

        self.show_all_button = QPushButton("Show All Books")
        self.show_all_button.clicked.connect(
            self.show_all_books
        )

        # Scraping controls

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText(
            "Optional Open Library Search API URL"
        )

        self.start_button = QPushButton("Start Scraping")
        self.start_button.clicked.connect(
            self.start_scraping
        )

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(
            self.pause_scraping
        )
        self.pause_button.setEnabled(False)

        self.resume_button = QPushButton("Resume")
        self.resume_button.clicked.connect(
            self.resume_scraping
        )
        self.resume_button.setEnabled(False)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(
            self.stop_scraping
        )
        self.stop_button.setEnabled(False)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 15000)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%v / %m books")

        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setWordWrap(True)

        # Search tab

        search_tab = QWidget()
        search_layout = QVBoxLayout(search_tab)

        search_group = QGroupBox("Search and Combined Filters")
        search_form = QFormLayout(search_group)

        search_form.addRow(
            "First column:", self.search_column_box
        )
        search_form.addRow(
            "First filter:", self.filter_box
        )
        search_form.addRow(
            "First text:", self.search_input
        )
        search_form.addRow(
            "Logic:", self.logic_box
        )
        search_form.addRow(
            "Second column:", self.second_search_column_box
        )
        search_form.addRow(
            "Second filter:", self.second_filter_box
        )
        search_form.addRow(
            "Second text:", self.second_search_input
        )

        search_buttons = QHBoxLayout()
        search_buttons.addWidget(self.search_button)
        search_buttons.addWidget(self.show_all_button)
        search_form.addRow(search_buttons)

        search_layout.addWidget(search_group)
        search_layout.addStretch()

        # Sorting tab

        sort_tab = QWidget()
        sort_layout = QVBoxLayout(sort_tab)

        sort_group = QGroupBox("Sorting and Benchmark")
        sort_form = QFormLayout(sort_group)

        sort_form.addRow(
            "Algorithm:", self.algorithm_box
        )
        sort_form.addRow(
            "Primary column:", self.column_box
        )
        sort_form.addRow(
            "Second-level column:",
            self.second_sort_column_box
        )
        sort_form.addRow(
            "Third-level column:",
            self.third_sort_column_box
        )
        sort_form.addRow(
            "Order:", self.sort_order_box
        )
        sort_form.addRow(
            "Sort scope:", self.sort_scope_box
        )

        sort_buttons = QHBoxLayout()
        sort_buttons.addWidget(self.sort_button)
        sort_buttons.addWidget(self.benchmark_button)
        sort_form.addRow(sort_buttons)

        sort_layout.addWidget(sort_group)
        sort_layout.addStretch()

        # Scraping tab

        scrape_tab = QWidget()
        scrape_layout = QVBoxLayout(scrape_tab)

        scrape_group = QGroupBox("Data Collection")
        scrape_group_layout = QVBoxLayout(scrape_group)

        scrape_group_layout.addWidget(QLabel(
            "Use an Open Library Search API URL, or leave blank "
            "to use the default search queries."
        ))
        scrape_group_layout.addWidget(self.url_input)

        scrape_buttons = QHBoxLayout()
        scrape_buttons.addWidget(self.start_button)
        scrape_buttons.addWidget(self.pause_button)
        scrape_buttons.addWidget(self.resume_button)
        scrape_buttons.addWidget(self.stop_button)

        scrape_group_layout.addLayout(scrape_buttons)
        scrape_group_layout.addWidget(self.progress_bar)
        scrape_group_layout.addWidget(self.status_label)

        scrape_layout.addWidget(scrape_group)
        scrape_layout.addStretch()

        # Tabs keep the controls compact

        self.tabs = QTabWidget()
        self.tabs.addTab(search_tab, "Search")
        self.tabs.addTab(sort_tab, "Sorting")
        self.tabs.addTab(scrape_tab, "Data Collection")

        # Books table

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(False)
        self.table.setWordWrap(False)
        self.table.setShowGrid(True)
        self.table.setHorizontalScrollMode(
            QTableWidget.ScrollPerPixel
        )
        self.table.setVerticalScrollMode(
            QTableWidget.ScrollPerPixel
        )
        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )
        self.table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Interactive
        )
        self.table.verticalHeader().setDefaultSectionSize(26)

        self.fill_table()

        # Main layout: table gets most of the space

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        layout.addWidget(self.label)
        layout.addWidget(self.tabs)
        layout.addWidget(self.table, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.apply_style()

    def apply_style(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #FFF5F8;
                color: #34443F;
                font-family: Segoe UI, Arial;
                font-size: 10pt;
            }

            QLabel#summaryLabel {
                background-color: #BFE8DA;
                color: #254E43;
                font-size: 16pt;
                font-weight: bold;
                padding: 12px;
                border: 1px solid #A2D7C5;
                border-radius: 9px;
            }

            QLabel#statusLabel {
                color: #28735E;
                font-weight: bold;
                padding: 5px;
            }

            QTabWidget::pane {
                border: 1px solid #E8C9D5;
                border-radius: 7px;
                background-color: #FFF9FB;
            }

            QTabBar::tab {
                background-color: #F6DDE7;
                color: #654451;
                padding: 8px 22px;
                margin-right: 3px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }

            QTabBar::tab:selected {
                background-color: #BFE8DA;
                color: #254E43;
                font-weight: bold;
            }

            QGroupBox {
                background-color: #FFF9FB;
                border: 1px solid #E8C9D5;
                border-radius: 8px;
                margin-top: 10px;
                padding: 10px;
                font-weight: bold;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 5px;
                color: #28735E;
            }

            QComboBox, QLineEdit {
                background-color: white;
                border: 1px solid #D9C1CC;
                border-radius: 5px;
                padding: 6px;
                min-height: 18px;
            }

            QComboBox:focus, QLineEdit:focus {
                border: 2px solid #79BDA8;
            }

            QPushButton {
                background-color: #BFE8DA;
                color: #254E43;
                border: 1px solid #A2D7C5;
                border-radius: 6px;
                padding: 8px 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #A6DCCB;
            }

            QPushButton:pressed {
                background-color: #8FCBB7;
            }

            QPushButton:disabled {
                background-color: #E9E4E6;
                color: #999094;
                border: 1px solid #DDD5D9;
            }

            QTableWidget {
                background-color: white;
                alternate-background-color: #FFF0F5;
                border: 1px solid #E4C9D5;
                gridline-color: #E9DDE2;
                selection-background-color: #BFE8DA;
                selection-color: #254E43;
            }

            QTableWidget::item {
                padding: 3px;
            }

            QHeaderView::section {
                background-color: #BFE8DA;
                color: #254E43;
                padding: 7px;
                border: 1px solid #A2D7C5;
                font-weight: bold;
            }

            QProgressBar {
                background-color: #F9E8EE;
                border: 1px solid #E4C9D5;
                border-radius: 6px;
                text-align: center;
                min-height: 20px;
            }

            QProgressBar::chunk {
                background-color: #79BDA8;
                border-radius: 5px;
            }

            QScrollBar:horizontal {
                background-color: #F9E8EE;
                height: 14px;
                margin: 0;
            }

            QScrollBar::handle:horizontal {
                background-color: #A6DCCB;
                min-width: 30px;
                border-radius: 5px;
            }

            QScrollBar:vertical {
                background-color: #F9E8EE;
                width: 14px;
                margin: 0;
            }

            QScrollBar::handle:vertical {
                background-color: #A6DCCB;
                min-height: 30px;
                border-radius: 5px;
            }
        """)

    # Display functions

    def fill_table(self):
        self.display_dataframe(self.df)

    def display_dataframe(self, data):
        self.table.setUpdatesEnabled(False)

        try:
            self.table.clearContents()
            self.table.setRowCount(len(data))
            self.table.setColumnCount(len(data.columns))

            self.table.setHorizontalHeaderLabels(
                data.columns.tolist()
            )

            for i in range(len(data)):
                for j in range(len(data.columns)):
                    value = data.iloc[i, j]

                    if pd.isna(value):
                        value = ""
                    else:
                        value = str(value)

                    item = QTableWidgetItem(value)
                    item.setToolTip(value)

                    self.table.setItem(i, j, item)

            # Practical widths for a laptop screen

            widths = [
                105, 180, 135, 70, 125,
                135, 170, 75, 100, 75
            ]

            for column, width in enumerate(widths):
                if column < self.table.columnCount():
                    self.table.setColumnWidth(column, width)

            self.table.verticalHeader().setDefaultSectionSize(26)

        finally:
            self.table.setUpdatesEnabled(True)

    # Searching functions

    def condition_mask(
        self, data, column, filter_type, search_text
    ):
        if search_text.strip() == "":
            return pd.Series(
                True, index=data.index, dtype=bool
            )

        values = (
            data[column]
            .fillna("")
            .astype(str)
            .str.casefold()
        )

        search_text = search_text.strip().casefold()

        if filter_type == "Contains":
            return values.str.contains(
                search_text, regex=False
            )

        elif filter_type == "Starts With":
            return values.str.startswith(search_text)

        elif filter_type == "Ends With":
            return values.str.endswith(search_text)

        elif filter_type == "Equals":
            return values == search_text

        elif filter_type == "Does Not Contain":
            return ~values.str.contains(
                search_text, regex=False
            )

        return pd.Series(
            True, index=data.index, dtype=bool
        )

    def search_books_table(self):
        first_text = self.search_input.text().strip()
        second_text = self.second_search_input.text().strip()

        if not first_text and not second_text:
            QMessageBox.information(
                self,
                "Search",
                "Enter text in at least one search field."
            )
            return

        first_mask = self.condition_mask(
            self.df,
            self.search_column_box.currentText(),
            self.filter_box.currentText(),
            first_text
        )

        second_mask = self.condition_mask(
            self.df,
            self.second_search_column_box.currentText(),
            self.second_filter_box.currentText(),
            second_text
        )

        if not first_text:
            combined_mask = second_mask

        elif not second_text:
            combined_mask = first_mask

        else:
            logic = self.logic_box.currentText()

            if logic == "AND":
                combined_mask = first_mask & second_mask

            elif logic == "OR":
                combined_mask = first_mask | second_mask

            else:
                combined_mask = first_mask & ~second_mask

        self.filtered_df = self.df[combined_mask].copy()
        self.display_dataframe(self.filtered_df)

        self.label.setText(
            "Matching Books: "
            + str(len(self.filtered_df))
            + " / "
            + str(len(self.df))
        )

        self.status_label.setText(
            "Search complete. Matching records: "
            + str(len(self.filtered_df))
        )

        self.tabs.setCurrentIndex(0)

    def show_all_books(self):
        self.filtered_df = self.df.copy()
        self.display_dataframe(self.df)

        self.label.setText(
            "BOOK DATA EXPLORER     |     Total Books: "
            + str(len(self.df))
        )

        self.status_label.setText("Showing all books.")

        self.search_input.clear()
        self.second_search_input.clear()

    # Sorting helper functions

    def make_sort_values(self, data, columns):
        values = []

        numeric_flags = [
            pd.api.types.is_numeric_dtype(data[col])
            for col in columns
        ]

        for index, row in data.iterrows():
            item = []

            for position, column in enumerate(columns):
                value = row[column]
                numeric = numeric_flags[position]

                if pd.isna(value) or str(value).strip() == "":
                    item.extend([
                        1,
                        0 if numeric else ""
                    ])

                elif numeric:
                    try:
                        item.extend([0, float(value)])
                    except (ValueError, TypeError):
                        item.extend([1, 0])

                else:
                    item.extend([
                        0,
                        str(value).casefold()
                    ])

            item.append(index)
            values.append(tuple(item))

        return values

    def selected_sort_data(self):
        if self.sort_scope_box.currentText() == "Filtered Results":
            return self.filtered_df.copy()

        return self.df.copy()

    def sort_books(self):
        column = self.column_box.currentText()
        algorithm = self.algorithm_box.currentText()

        source_df = self.selected_sort_data()

        if source_df.empty:
            QMessageBox.information(
                self, "Sorting", "There are no books to sort."
            )
            return

        columns = [column]

        for box in [
            self.second_sort_column_box,
            self.third_sort_column_box
        ]:
            extra_column = box.currentText()

            if (
                extra_column != "None"
                and extra_column not in columns
            ):
                columns.append(extra_column)

        algorithms = {
            "Bubble Sort": bubble_sort,
            "Insertion Sort": insertion_sort,
            "Selection Sort": selection_sort,
            "Merge Sort": merge_sort,
            "Hybrid Merge Sort": hybrid_merge_sort,
            "Quick Sort": quick_sort,
            "Heap Sort": heap_sort
        }

        try:
            values = self.make_sort_values(
                source_df, columns
            )

            result = algorithms[algorithm](values)

            sorted_indices = [
                item[-1] for item in result["sorted_data"]
            ]

            if self.sort_order_box.currentText() == "Descending":
                valid_indices = []
                missing_indices = []

                for index in sorted_indices:
                    value = source_df.loc[index, column]

                    if (
                        pd.isna(value)
                        or str(value).strip() == ""
                    ):
                        missing_indices.append(index)
                    else:
                        valid_indices.append(index)

                sorted_indices = (
                    list(reversed(valid_indices))
                    + missing_indices
                )

            sorted_df = source_df.loc[sorted_indices]
            self.display_dataframe(sorted_df)

            self.label.setText(
                "Displayed: " + str(len(sorted_df))
                + " | Sorted by: " + ", ".join(columns)
            )

            self.tabs.setCurrentIndex(1)

            QMessageBox.information(
                self,
                "Sorting Results",
                "Algorithm: " + algorithm
                + "\nColumns: " + ", ".join(columns)
                + "\nOrder: " + self.sort_order_box.currentText()
                + "\nScope: " + self.sort_scope_box.currentText()
                + "\nTime: "
                + str(round(result["time_ms"], 3)) + " ms"
                + "\nComparisons: "
                + str(result["comparisons"])
                + "\nSwaps: " + str(result["swaps"])
                + "\nComplexity: " + result["complexity"]
                + "\nStable: " + result["stable"]
            )

        except Exception as error:
            QMessageBox.warning(
                self, "Sorting Error", str(error)
            )

    # Benchmark function

    def benchmark_sorts(self):
        column = self.column_box.currentText()
        source_df = self.selected_sort_data()

        if source_df.empty:
            QMessageBox.information(
                self, "Benchmark", "There are no books to benchmark."
            )
            return

        if len(source_df) > 5000:
            answer = QMessageBox.question(
                self,
                "Large Benchmark",
                "Benchmarking all algorithms on "
                + str(len(source_df))
                + " records may take a long time because "
                "some algorithms are O(n^2).\n\nContinue?",
                QMessageBox.Yes | QMessageBox.No
            )

            if answer != QMessageBox.Yes:
                return

        algorithms = {
            "Bubble Sort": bubble_sort,
            "Insertion Sort": insertion_sort,
            "Selection Sort": selection_sort,
            "Merge Sort": merge_sort,
            "Hybrid Merge Sort": hybrid_merge_sort,
            "Quick Sort": quick_sort,
            "Heap Sort": heap_sort
        }

        try:
            values = self.make_sort_values(
                source_df, [column]
            )

            results = []

            for name, function in algorithms.items():
                result = function(values)

                results.append([
                    name,
                    round(result["time_ms"], 3),
                    result["comparisons"],
                    result["swaps"],
                    result["complexity"],
                    result["stable"]
                ])

        except Exception as error:
            QMessageBox.warning(
                self, "Benchmark Error", str(error)
            )
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Sorting Benchmark Results")
        dialog.resize(900, 420)

        layout = QVBoxLayout()

        layout.addWidget(QLabel(
            "Column: " + column
            + " | Records: " + str(len(source_df))
        ))

        table = QTableWidget()
        table.setAlternatingRowColors(True)
        table.setRowCount(len(results))
        table.setColumnCount(6)

        table.setHorizontalHeaderLabels([
            "Algorithm",
            "Time (ms)",
            "Comparisons",
            "Swaps",
            "Complexity",
            "Stable"
        ])

        for i, row in enumerate(results):
            for j, value in enumerate(row):
                table.setItem(
                    i, j, QTableWidgetItem(str(value))
                )

        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        layout.addWidget(table)
        dialog.setLayout(layout)
        dialog.exec_()

    # Scraping functions

    def start_scraping(self):
        if (
            self.worker is not None
            and self.worker.isRunning()
        ):
            return

        custom_url = self.url_input.text().strip()

        self.worker = ScraperWorker(
            custom_url if custom_url else None
        )

        self.worker.progress_changed.connect(
            self.update_progress
        )

        self.worker.scraping_done.connect(
            self.scraping_finished
        )

        self.progress_bar.setValue(0)
        self.status_label.setText("Starting scraping...")

        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.resume_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.sort_button.setEnabled(False)
        self.benchmark_button.setEnabled(False)
        self.search_button.setEnabled(False)
        self.show_all_button.setEnabled(False)
        self.url_input.setEnabled(False)

        self.tabs.setCurrentIndex(2)
        self.worker.start()

    def update_progress(self, count, query):
        self.progress_bar.setValue(min(count, 15000))

        self.status_label.setText(
            "Query: " + query
            + " | New books: " + str(count)
        )

    def pause_scraping(self):
        if self.worker and self.worker.isRunning():
            self.worker.pause()

            self.status_label.setText("Scraping paused.")

            self.pause_button.setEnabled(False)
            self.resume_button.setEnabled(True)

    def resume_scraping(self):
        if self.worker and self.worker.isRunning():
            self.worker.resume()

            self.status_label.setText("Scraping resumed.")

            self.pause_button.setEnabled(True)
            self.resume_button.setEnabled(False)

    def stop_scraping(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()

            self.status_label.setText(
                "Stopping and saving collected books..."
            )

            self.pause_button.setEnabled(False)
            self.resume_button.setEnabled(False)
            self.stop_button.setEnabled(False)

    def scraping_finished(self, message, total):
        if total >= 0:
            try:
                self.df = pd.read_csv("books_data.csv")
                self.filtered_df = self.df.copy()

                self.fill_table()

                self.label.setText(
                    "BOOK DATA EXPLORER     |     Total Books: "
                    + str(len(self.df))
                )

            except Exception as error:
                QMessageBox.warning(
                    self, "File Error", str(error)
                )

        self.status_label.setText(message)

        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.resume_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.sort_button.setEnabled(True)
        self.benchmark_button.setEnabled(True)
        self.search_button.setEnabled(True)
        self.show_all_button.setEnabled(True)
        self.url_input.setEnabled(True)

        QMessageBox.information(
            self, "Scraping Status", message
        )


app = QApplication(sys.argv)
window = BookExplorer()
window.show()
sys.exit(app.exec_())