# Market Data Refresh Architecture

## Overview

The AlphaPulse system uses automated market data updates to ensure risk metrics remain accurate.

## Components

### Data Source

* Yahoo Finance

### Data Collection Layer

* scraper.py downloads historical market data.

### Data Processing Layer

* cleaner.py validates and cleans downloaded data.

### Storage Layer

* Cleaned datasets are stored in data/clean/.

### Analytics Layer

* Portfolio risk calculations use cleaned return data.

### Visualization Layer

* Dashboard displays risk metrics and portfolio performance.

## Architecture Flow

Yahoo Finance → Scraper → Data Cleaning → Data Storage → Risk Analysis → Dashboard
