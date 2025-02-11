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

Sure! Here's the revised API configuration section in English with more details:

---

## 🔑 API Configuration

Before running the project, you need to set up **API keys** for the following services:

- **OpenWeather**: Sign up and get your API key from [OpenWeather](https://openweathermap.org/).
- **OpenCage**: Sign up and get your API key from [OpenCage](https://opencagedata.com/).

### Setting up the Keys:
1. After obtaining your API keys, add them to the respective files:
   - The **OpenWeather** API key is used in `Functions/getWeather.py`.
   - The **OpenCage** API key is defined in `main.py`.
   
2. Replace the placeholder `"YOUR API KEY HERE"` with your actual API keys in both files.

## 🤝 Contributors
- [@stevopablo](https://github.com/stevopablo)

## 📜 License
This project is licensed under the MIT License. Feel free to contribute! 😊