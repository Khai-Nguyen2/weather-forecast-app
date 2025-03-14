from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QFrame, QSizePolicy)


class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dự báo thời tiết")
        self.setGeometry(100, 100, 1000, 750)
        self.setStyleSheet("background-color: #DCE6F1;")
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Thời gian và địa điểm
        self.label_time = QLabel("---", self)
        self.label_time.setStyleSheet(
            "font-size: 22px; font-weight: bold; color: black; background-color: rgba(255, 255, 255, 0.8);"
            "border-radius: 10px; padding: 12px; text-align: center;"
        )
        self.label_time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_location = QLabel("---", self)
        self.label_location.setStyleSheet(
            "font-size: 22px; font-weight: bold; color: black; background-color: rgba(255, 255, 255, 0.8);"
            "border-radius: 10px; padding: 12px; text-align: center;"
        )
        self.label_location.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.label_time)
        top_layout.addStretch()
        top_layout.addWidget(self.label_location)

        # Ô tìm kiếm (bo tròn đúng và giữ kích thước gọn)
        self.lineEdit_city_search = QLineEdit("Nhập tên thành phố...")
        self.lineEdit_city_search.setStyleSheet(
            "font-size: 14px; padding: 6px 10px; border: 2px solid #4A90E2; border-radius: 18px;"
            "background-color: white; color: black; font-weight: bold; min-width: 200px; max-width: 250px;"
        )
        self.lineEdit_city_search.setFixedHeight(36)
        self.lineEdit_city_search.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lineEdit_city_search.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Nút tìm kiếm (bo tròn hơn và sát với ô nhập)
        self.btn_search = QPushButton("🔍")
        self.btn_search.setStyleSheet(
            "background-color: #4A90E2; color: white; font-size: 16px; font-weight: bold;"
            "border-radius: 18px; padding: 0px; min-width: 36px; min-height: 36px; max-width: 36px; max-height: 36px;"
        )
        self.btn_search.setFixedSize(36, 36)

        # Layout chứa ô tìm kiếm và nút tìm kiếm
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.lineEdit_city_search)
        search_layout.addWidget(self.btn_search)
        search_layout.setSpacing(0)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout thời tiết hiện tại và biểu đồ đặt cạnh nhau
        weather_chart_layout = QHBoxLayout()

        # Khung thông tin thời tiết hiện tại
        self.frame_current_weather = QFrame()
        self.frame_current_weather.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_current_weather.setStyleSheet(
            "background-color: white; border: 2px solid #4A90E2; border-radius: 10px; padding: 10px;"
            "box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);"
        )
        weather_layout = QVBoxLayout(self.frame_current_weather)

        # Các nhãn thông tin thời tiết
        self.label_temperature = QLabel("Nhiệt độ: ---")
        self.label_humidity = QLabel("Độ ẩm: ---")
        self.label_pressure = QLabel("Áp suất: ---")
        self.label_wind_speed = QLabel("Tốc độ gió: ---")
        self.label_uv_index = QLabel("Chỉ số UV: ---")
        self.label_weather_description = QLabel("Trạng thái: ---")

        # Định dạng các nhãn
        for label in [self.label_temperature, self.label_humidity, self.label_pressure, self.label_wind_speed,
                      self.label_uv_index, self.label_weather_description]:
            label.setStyleSheet("color: black; font-weight: bold; font-size: 14px; padding: 5px;")
            weather_layout.addWidget(label)

        # Khung biểu đồ
        self.frame_chart = QFrame()
        self.frame_chart.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_chart.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.95); border: 2px solid #4A90E2; border-radius: 12px;"
        )

        weather_chart_layout.addWidget(self.frame_current_weather)
        weather_chart_layout.addWidget(self.frame_chart)

        # Dự báo thời tiết theo ngày
        self.forecast_container = QWidget()
        forecast_layout = QHBoxLayout(self.forecast_container)

        self.forecast_days = []
        for i in range(7):
            frame_day = QFrame()
            frame_day.setFrameShape(QFrame.Shape.StyledPanel)
            frame_day.setStyleSheet(
                "background: white; border: 2px solid #4A90E2; border-radius: 12px; padding: 10px;"
            )

            layout_day = QVBoxLayout(frame_day)
            label_day = QLabel("---")
            label_temp = QLabel("---")
            label_icon = QLabel("---")
            label_rain = QLabel("---")

            for label in [label_day, label_temp, label_icon, label_rain]:
                label.setStyleSheet("color: black; font-weight: bold;")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout_day.addWidget(label)

            self.forecast_days.append((label_day, label_temp, label_icon, label_rain))
            forecast_layout.addWidget(frame_day)

        # Cảnh báo thời tiết và Gợi ý trang phục đặt cạnh nhau
        alert_clothing_layout = QHBoxLayout()

        self.label_weather_alert = QLabel("⚠️ Cảnh báo: ---")
        self.label_weather_alert.setStyleSheet(
            "background-color: rgba(255, 102, 102, 0.9); padding: 12px; border-radius: 8px; font-weight: bold;"
            "font-size: 16px; color: white;"
        )

        self.frame_clothing_suggestion = QFrame()
        self.frame_clothing_suggestion.setFrameShape(QFrame.Shape.StyledPanel)
        clothing_layout = QVBoxLayout(self.frame_clothing_suggestion)

        self.label_clothing_title = QLabel("👕 Gợi ý trang phục hôm nay")
        self.label_clothing_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_clothing_title.setStyleSheet("color: black; font-weight: bold;")
        self.label_clothing_suggestion = QLabel("---")
        self.label_clothing_suggestion.setStyleSheet("color: black; font-weight: bold;")

        clothing_layout.addWidget(self.label_clothing_title)
        clothing_layout.addWidget(self.label_clothing_suggestion)

        alert_clothing_layout.addWidget(self.label_weather_alert)
        alert_clothing_layout.addWidget(self.frame_clothing_suggestion)

        # Sắp xếp các phần tử vào layout chính
        main_layout.addLayout(top_layout)
        main_layout.addLayout(search_layout)
        main_layout.addLayout(weather_chart_layout)
        main_layout.addWidget(self.forecast_container)
        main_layout.addLayout(alert_clothing_layout)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())
