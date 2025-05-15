```markdown
# 🌤️ Live Weather Dashboard – Day 25

Welcome to **Day 25 of the 100-Day Python + AI Challenge!**  
Today’s project is a **Live Weather Dashboard CLI App** – a clean, emoji-powered command-line tool that fetches and displays **real-time weather data** for any city using the OpenWeatherMap API. ☁️🌡️⚡

---

## 📌 Features

✅ Input any city name and fetch live weather info  
✅ Get temperature, humidity, wind speed, and condition  
✅ Display emoji-based mood for the weather ☀️❄️🌧️  
✅ Handles API errors and invalid city names gracefully  
✅ Easy to extend into GUI or web versions in the future  

---

## 🧱 Folder Structure

```

day\_25\_weather\_dashboard/
├── weather\_dashboard.py   # Main script to run the weather CLI
└── README.md              # You are here!

````

---

## 🚀 How to Run

1. Open your terminal  
2. Navigate to the project folder  
3. Install dependencies (if not already installed):  
   ```bash
   pip install requests
````

4. Replace the placeholder API key:

   * Sign up at [https://openweathermap.org/](https://openweathermap.org/)
   * Copy your API key
   * Paste it in `weather_dashboard.py`:

     ```python
     API_KEY = "OPENWEATHERMAP_API_KEY"
     ```

5. Run the app:

   ```bash
   python weather_dashboard.py
   ```

---

## 💡 Example Output

```
🌤️ Welcome to the Live Weather Dashboard! 🌤️
Enter a city name: New York

Weather in New York: 🌧️
🌡️ Temperature: 18°C
☁️ Condition: Rain
💧 Humidity: 72%
🌬️ Wind Speed: 5.5 m/s
```

---

## 🎯 Learning Highlights

* Consuming real-time REST APIs
* Parsing and validating JSON responses
* Writing modular Python functions
* Adding emoji for enhanced UX in terminal apps
* Graceful error handling and input validation

## 🙌 Author

Crafted by **Uday Kumar** with care and curiosity 💙
One step closer to Python mastery with every line of code 🚀
