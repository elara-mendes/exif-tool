# 📸 Image Metadata Explorer

This project allows you to analyze image metadata, extracting information such as GPS location, capture date and time, and displaying maps and weather forecasts for the location where the photo was taken.

## 🚀 Features
- Upload images and automatically extract EXIF metadata
- Retrieve GPS coordinates from the image (if available)
- Display location on an interactive map
- Query address based on coordinates
- Show weather forecast for the image location

## 🛠 Technologies Used
- **Python**
- **Streamlit** (interactive interface)
- **Folium** (map display)
- **Geopy** (address lookup)
- **OpenWeather API** (weather forecast)
- **OpenCage API** (coordinate to address conversion)
- **Pillow (Exif)** (reading image metadata)

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/elara-mendes/exif-tool.git
cd exif-tool
```

2. Set up a virtual environment:

### Using venv (Optional)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Using Conda (Recommended)
```bash
conda create --name my_environment python=3.11
conda activate my_environment
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

## ▶️ How to Use

1. Run the app:
```bash
streamlit run main.py
```
2. Upload an image and view the extracted information!

## 🔑 API Configuration
Before running the project, configure your **API keys**:
- **OpenWeather**: Get a key from [https://openweathermap.org/](https://openweathermap.org/)
- **OpenCage**: Get a key from [https://opencagedata.com/](https://opencagedata.com/)

Add these keys where necessary in the code.

## 🤝 Contributors
- [@stevopablo](https://github.com/stevopablo)

## 📜 License
This project is licensed under the MIT License. Feel free to contribute! 😊