import sys
from PyQt6 import QtWidgets
from ui_ex import WeatherAppEX  # Import WeatherAppEX thay vì Ui_WeatherApp

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Tạo cửa sổ chính
    WeatherApp = QtWidgets.QMainWindow()

    # Tạo đối tượng WeatherAppEX thay vì Ui_WeatherApp
    ui = WeatherAppEX()

    # Gọi phương thức setupUi của WeatherAppEX
    ui.setupUi(WeatherApp)

    # Hiển thị cửa sổ chính
    WeatherApp.show()

    sys.exit(app.exec())
