# Data Sources Documentation

## AtlasIQ Macro Economic Indicators

**Version**: 1.0  
**Last Updated**: January 2025  
**Data Period**: 2015-2023  
**Coverage**: Benelux + Germany (NLD, BEL, LUX, DEU)

---

## Overview

AtlasIQ uses a **hybrid data approach** for macro economic indicators:
- **Phase 1 (MVP)**: Historical data (2015-2023) from official statistics
- **Phase 2 (Post-Launch)**: Real-time APIs integrated for live updates

This approach provides:
✅ Stable, validated data for MVP launch  
✅ No external API dependencies blocking features  
✅ Consistent user experience  
✅ Clear upgrade path to real-time data

---

## Current Data Sources (Historical)

### 1. GDP Growth Rate
**Indicator**: Real GDP growth (annual % change)  
**Source**: OECD Statistics  
**Period**: 2015-2023  
**Countries**: Netherlands (NLD), Belgium (BEL), Luxembourg (LUX), Germany (DEU)  
**Update Frequency**: Static (historical baseline)

**Sample Data**:
```json
{
  "country": "NLD",
  "year": 2023,
  "value": 0.1,
  "unit": "percent"
}
```

**Validation**:
- Cross-referenced with World Bank, Eurostat
- Includes COVID-19 impact (2020: -3.9% Netherlands)
- Post-pandemic recovery (2021: 5.0% Netherlands)

### 2. Inflation Rate (HICP)
**Indicator**: Harmonized Index of Consumer Prices (annual % change)  
**Source**: Eurostat / OECD  
**Period**: 2015-2023  
**Countries**: NLD, BEL, LUX, DEU  
**Update Frequency**: Static (historical baseline)

**Sample Data**:
```json
{
  "country": "DEU",
  "year": 2022,
  "value": 8.7,
  "unit": "percent"
}
```

**Validation**:
- Official Eurostat HICP data
- Reflects 2022 inflation spike (energy crisis)
- Normalization in 2023 (5.9% Germany)

### 3. Unemployment Rate
**Indicator**: Total unemployment (% of labor force)  
**Source**: Eurostat / National Statistics  
**Period**: 2015-2023  
**Countries**: NLD, BEL, LUX, DEU  
**Update Frequency**: Static (historical baseline)

**Sample Data**:
```json
{
  "country": "NLD",
  "year": 2023,
  "value": 3.6,
  "unit": "percent"
}
```

**Validation**:
- ILO definition methodology
- Seasonally adjusted annual averages
- Low Netherlands rate reflects tight labor market

### 4. Interest Rates (ECB Policy Rates)
**Indicators**: 
- DFR: Deposit Facility Rate
- MRO: Main Refinancing Operations Rate  
**Source**: European Central Bank  
**Period**: 2015-present  
**Currency**: EUR  
**Update Frequency**: Static (historical baseline)

**Sample Data**:
```json
{
  "rate_type": "DFR",
  "year": 2023,
  "value": 4.0,
  "currency": "EUR",
  "unit": "percent"
}
```

**Validation**:
- Official ECB monetary policy decisions
- Reflects negative rates era (2015-2022)
- Tightening cycle 2022-2023 (inflation response)

---

## API Endpoints

### Base URL
```
http://localhost:8000/api/v1/macro
```

### 1. GET `/gdp`
**Description**: Retrieve GDP growth rates

**Query Parameters**:
- `countries` (array): Country codes (e.g., ["NLD", "BEL"])
- `start_year` (int): Start year (2015-2023)
- `end_year` (int): End year (2015-2023)

**Example Request**:
```bash
GET /api/v1/macro/gdp?countries=NLD&countries=BEL&start_year=2020
```

**Example Response**:
```json
{
  "data": [
    {
      "country": "NLD",
      "date": "2020-12-31",
      "year": 2020,
      "value": -3.9,
      "indicator": "gdp_growth",
      "unit": "percent"
    }
  ],
  "meta": {
    "countries": ["NLD", "BEL"],
    "start_year": 2020,
    "end_year": 2023,
    "total_records": 8,
    "data_source": "OECD Statistics",
    "data_type": "historical"
  }
}
```

### 2. GET `/inflation`
**Description**: Retrieve inflation rates (HICP)

**Query Parameters**: Same as GDP endpoint

**Example Request**:
```bash
GET /api/v1/macro/inflation?countries=DEU&start_year=2018
```

### 3. GET `/unemployment`
**Description**: Retrieve unemployment rates

**Query Parameters**: Same as GDP endpoint

**Example Request**:
```bash
GET /api/v1/macro/unemployment?countries=NLD&countries=LUX
```

### 4. GET `/interest-rates`
**Description**: Retrieve ECB policy interest rates

**Query Parameters**:
- `start_year` (int): Start year
- `end_year` (int): End year

**Example Request**:
```bash
GET /api/v1/macro/interest-rates?start_year=2020
```

**Example Response**:
```json
{
  "data": [
    {
      "rate_type": "DFR",
      "rate_name": "Deposit Facility Rate",
      "date": "2023-12-31",
      "year": 2023,
      "value": 4.0,
      "currency": "EUR",
      "unit": "percent"
    }
  ]
}
```

---

## Data Quality & Validation

### Quality Assurance
✅ **Source Verification**: All data from official statistical agencies  
✅ **Cross-Validation**: Compared across multiple authoritative sources  
✅ **Temporal Consistency**: Checked for anomalies and outliers  
✅ **Unit Consistency**: All percentages, properly formatted  
✅ **Completeness**: 9 years coverage (2015-2023) for all indicators

### Known Limitations
⚠️ **Static Data**: No real-time updates until Phase 2  
⚠️ **Annual Frequency**: GDP, inflation, unemployment are annual averages  
⚠️ **Historical Only**: Ends at 2023, no forecasts included  
⚠️ **Country Coverage**: Limited to NLD, BEL, LUX, DEU (Benelux + Germany)

### Future Enhancements (Phase 2)
- Monthly/quarterly frequency for recent data
- Forecasts and projections
- Extended country coverage (EU27, USA, others)
- Real-time API integration
- Automated daily updates

---

## Phase 2: Real-Time Data Integration

### Planned Data Sources

#### 1. FRED API (Federal Reserve Economic Data)
**Status**: Evaluation  
**Coverage**: Global indicators, excellent US data  
**Cost**: Free (API key required)  
**Reliability**: ★★★★★ Excellent  
**Documentation**: ★★★★★ Outstanding  
**Integration Effort**: Low (Python library available)

**Benefits**:
- 818,000+ economic time series
- Free, unlimited access
- Official Fed data
- Easy-to-use REST API

**Implementation**:
```python
from fredapi import Fred
fred = Fred(api_key='YOUR_KEY')
gdp = fred.get_series('GDPC1')  # Real GDP
```

#### 2. ECB Data Portal API
**Status**: Evaluation  
**Coverage**: Eurozone monetary data  
**Cost**: Free  
**Reliability**: ★★★★☆ Good  
**Documentation**: ★★★☆☆ Moderate  
**Integration Effort**: Medium (JSON API, but complex structure)

**Benefits**:
- Authoritative ECB data
- Real-time interest rates
- Free access
- Official eurozone statistics

#### 3. World Bank API v2
**Status**: Evaluation  
**Coverage**: Global development indicators  
**Cost**: Free  
**Reliability**: ★★★★☆ Good  
**Documentation**: ★★★★☆ Good  
**Integration Effort**: Low (Python library available)

**Benefits**:
- 16,000+ development indicators
- Historical data back to 1960
- Country coverage: 200+
- Python library: `wbgapi`

#### 4. Alpha Vantage
**Status**: Alternative option  
**Coverage**: Financial markets + economics  
**Cost**: Free tier (25 requests/day), Paid ($50/month unlimited)  
**Reliability**: ★★★☆☆ Moderate  
**Documentation**: ★★★★☆ Good  
**Integration Effort**: Low (simple REST API)

**Benefits**:
- Economic indicators API
- Stock market data
- Forex rates
- Time series data

---

## Automation Strategy (Phase 2)

### Daily Refresh Architecture

```
┌─────────────────┐
│  External APIs  │
│ (FRED, ECB, WB) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Celery Worker   │ ← Scheduled daily at 6 AM UTC
│ (Background)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PostgreSQL DB  │ ← Cached data
│ (macro_         │
│  indicators)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI        │ ← Same API contract
│  /api/v1/macro  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  React Frontend │ ← No changes needed!
│  Charts & UI    │
└─────────────────┘
```

### Update Schedule
- **GDP**: Quarterly (OECD releases)
- **Inflation**: Monthly (Eurostat releases)
- **Unemployment**: Monthly (Eurostat releases)
- **Interest Rates**: Real-time (ECB announcements)

### Error Handling
- Retry logic: 3 attempts with exponential backoff
- Fallback to cached data if API fails
- Email alerts on persistent failures
- DataRefreshLog table tracks all operations

---

## Migration Path

### Transition to Live Data

**Step 1: Parallel Operation** (Week 1)
- Run historical and live data side-by-side
- Compare results for accuracy
- Identify any discrepancies

**Step 2: Gradual Rollout** (Week 2)
- Add "Live Data" badge in UI
- Show timestamp of last update
- Allow users to toggle historical vs. live

**Step 3: Full Migration** (Week 3)
- Switch default to live data
- Maintain historical data for backtesting
- Deprecate old static service

**Step 4: Enhancements** (Week 4+)
- Add forecasts
- Expand country coverage
- Increase frequency (monthly/quarterly)
- Add data visualizations

---

## Usage Examples

### Frontend Integration (React)

```typescript
// Fetch GDP growth data
const fetchGDPData = async () => {
  const response = await fetch(
    '/api/v1/macro/gdp?countries=NLD&countries=BEL&start_year=2015'
  );
  const data = await response.json();
  
  // Format for chart
  const chartData = data.data.map(item => ({
    x: item.year,
    y: item.value,
    country: item.country
  }));
  
  return chartData;
};
```

### Backend Analysis (Python)

```python
import requests
import pandas as pd

# Fetch all indicators for Netherlands
def get_macro_dashboard(country='NLD'):
    base_url = 'http://localhost:8000/api/v1/macro'
    
    # GDP
    gdp = requests.get(f'{base_url}/gdp', params={'countries': [country]})
    
    # Inflation
    inflation = requests.get(f'{base_url}/inflation', params={'countries': [country]})
    
    # Unemployment
    unemployment = requests.get(f'{base_url}/unemployment', params={'countries': [country]})
    
    # Combine into DataFrame
    df = pd.DataFrame({
        'gdp_growth': [x['value'] for x in gdp.json()['data']],
        'inflation': [x['value'] for x in inflation.json()['data']],
        'unemployment': [x['value'] for x in unemployment.json()['data']]
    })
    
    return df
```

---

## Support & Contact

**Questions about data sources?**  
Email: data@atlasiq.com

**Report data quality issues?**  
GitHub: https://github.com/Icemclovin/atlasiq-web/issues

**Request new indicators?**  
Feature requests: Use GitHub Discussions

---

## Version History

**v1.0** (January 2025)
- Initial release with historical data (2015-2023)
- Coverage: NLD, BEL, LUX, DEU
- Indicators: GDP growth, inflation, unemployment, interest rates
- API endpoints: 4 endpoints operational

**Planned v2.0** (Q2 2025)
- Real-time data integration (FRED, ECB)
- Monthly/quarterly frequency
- Extended country coverage
- Automated daily updates
- Forecasting capabilities

---

## License & Attribution

**Data Sources**:
- OECD Statistics (CC BY 4.0)
- Eurostat (Free access, attribution required)
- European Central Bank (Public data)
- World Bank (CC BY 4.0)

**Attribution Required**:
When using this data in publications or presentations, please cite:
```
AtlasIQ (2025). Macro Economic Indicators. 
Data sources: OECD, Eurostat, ECB. 
Retrieved from https://atlasiq.com
```

---

**Document Status**: ✅ Complete  
**Last Review**: January 2025  
**Next Review**: Q2 2025 (before Phase 2 integration)
