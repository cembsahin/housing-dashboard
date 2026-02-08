# 🏠 Housing Market Dashboard

An interactive Python dashboard that visualizes US housing market trends using real data from Zillow and the FRED API.

Built with **Streamlit**, **Plotly**, and **Pandas**.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- 📈 Median home price trends over time
- 🗺️ State-by-state comparison
- 🔍 Filter by state, date range, and metric
- 📊 Interactive Plotly charts
- 🏗️ *More features coming soon: inventory levels, mortgage rates, map views*

## Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (comes with Python)

### Setup (Mac)

1. **Clone the repo**
   ```bash
   git clone https://github.com/YOUR_USERNAME/housing-dashboard.git
   cd housing-dashboard
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the data**
   ```bash
   python scripts/download_data.py
   ```

5. **Run the dashboard**
   ```bash
   streamlit run app.py
   ```
   The dashboard will open in your browser at `http://localhost:8501`

## Project Structure

```
housing-dashboard/
├── app.py                  # Main Streamlit dashboard
├── requirements.txt        # Python dependencies
├── README.md
├── .gitignore
├── data/                   # Downloaded datasets (not tracked by git)
│   └── .gitkeep
├── scripts/
│   └── download_data.py    # Script to fetch housing data
└── utils/
    ├── __init__.py
    └── data_loader.py      # Data loading and cleaning functions
```

## Data Sources

- [Zillow Research Data](https://www.zillow.com/research/data/) – Median home values by state/metro (ZHVI)
- [FRED API](https://fred.stlouisfed.org/) – Mortgage rates, housing starts *(future feature)*

## Roadmap

- [x] Basic price trend chart
- [x] State filter and date range selector
- [ ] Add inventory / days on market data
- [ ] Mortgage rate overlay (FRED API)
- [ ] Choropleth map view
- [ ] Year-over-year % change charts
- [ ] Deploy to Streamlit Community Cloud

## License

MIT
