import requests
import google.generativeai as genai
from test import Ui_WeatherApp
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QTimer, QDateTime

class WeatherAppEX(Ui_WeatherApp):
    def __init__(self):
        super().__init__()
        self.weather_api_key = "346c9af8645ff088a6a7ee92aed6f885"
        self.gemini_api_key = "AIzaSyC3FoPU_4kle0r-_PSKBvbGm7nRWxIcKjc"
        self.base_url = "http://api.openweathermap.org/data/2.5/"

        genai.configure(api_key=self.gemini_api_key)

    def setupUi(self, MainWindow):
        """Thiết lập giao diện và kết nối sự kiện"""
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()
        self.start_real_time_clock()

    def showWindow(self):
        """Hiển thị cửa sổ chính"""
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        """Kết nối sự kiện khi nhấn nút tìm kiếm"""
        self.btn_search.clicked.connect(self.search_weather)

    def start_real_time_clock(self):
        """Cập nhật thời gian thực trên label_time mỗi phút"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(60000)  # Cập nhật mỗi 60 giây
        self.update_time()

    def update_time(self):
        """Cập nhật thời gian hiện tại"""
        current_time = QDateTime.currentDateTime().toString("hh:mm AP - dd/MM/yyyy")
        self.label_time.setText(current_time)

    def search_weather(self):
        """Gửi yêu cầu đến API và cập nhật dữ liệu lên giao diện"""
        city = self.lineEdit_city_search.text().strip()
        if not city:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng nhập tên thành phố!")
            return

        weather_data = self.get_weather(city)
        if weather_data is None:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Không thể lấy dữ liệu thời tiết!")
            return

        self.update_current_weather(city, weather_data)

    def get_weather(self, city):
        """Lấy thông tin thời tiết từ OpenWeatherMap API"""
        url = (f"{self.base_url}"
               f"weather?q={city}&appid={self.weather_api_key}&units=metric&lang=vi")
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️ Lỗi khi lấy dữ liệu thời tiết: {response.status_code}")
            return None

    def update_current_weather(self, city, weather_data):
        """Cập nhật thông tin thời tiết hiện tại lên giao diện"""
        temp = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        pressure = weather_data["main"]["pressure"]
        description = weather_data["weather"][0]["description"]
        weather_main = weather_data["weather"][0]["main"]

        self.label_location.setText(f"{city.upper()}")
        self.label_temperature.setText(f"Nhiệt độ: {temp}°C")
        self.label_humidity.setText(f"Độ ẩm: {humidity}%")
        self.label_wind_speed.setText(f"Tốc độ gió: {wind_speed} m/s")
        self.label_pressure.setText(f"Áp suất: {pressure} hPa")
        self.label_weather_description.setText(f"Trạng thái: {description}")

        # Kiểm tra có mưa không để hiển thị cảnh báo
        if weather_main in ["Rain", "Thunderstorm", "Drizzle"]:
            self.label_weather_alert.setText("⚠️ Cảnh báo: Trời đang mưa, hãy mang theo ô!")
            self.label_weather_alert.show()
        else:
            self.label_weather_alert.hide()

        # Gửi dữ liệu thời tiết đến Gemini AI để nhận gợi ý trang phục
        clothing_suggestion = self.get_clothing_suggestion(temp, weather_main, description)
        self.label_clothing_suggestion.setText(clothing_suggestion)

    def get_clothing_suggestion(self, temp, weather_main, description):
        """Gửi thông tin thời tiết đến Gemini AI để nhận gợi ý trang phục"""
        prompt = f"""
        Tôi cần một đề xuất về trang phục dựa trên điều kiện thời tiết sau:
        - Nhiệt độ: {temp}°C
        - Điều kiện thời tiết: {weather_main} ({description})
        Hãy đề xuất loại trang phục phù hợp với điều kiện này.
        """

        try:
            model = genai.GenerativeModel("gemini-2.0-flash")  # Đổi sang gemini-1.5-pro
            response = model.generate_content(prompt)

            if response and response.text:
                print("AI:", response.text.strip())
                return response.text.strip()
            else:
                return "Không thể lấy gợi ý trang phục. Vui lòng thử lại sau!"
        except Exception as e:
            print(f"⚠️ Lỗi khi gọi Gemini AI: {e}")
            return "Không thể lấy gợi ý trang phục. Vui lòng thử lại sau!"
