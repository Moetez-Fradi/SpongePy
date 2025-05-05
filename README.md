# SpongePy - Data Processing Toolkit 🧽

A versatile Python CLI tool for cleaning, analyzing, and transforming structured data. Designed for data professionals who need quick data wrangling capabilities without spreadsheet software.
Download here: https://pypi.org/project/spongepy/
 
       _____                              _____        
      / ____|                            |  __ \       
     | (___  _ __   ___  _ __   __ _  ___| |__) |   _  
      \___ \| '_ \ / _ \| '_ \ / _` |/ _ \  ___/ | | | 
      ____) | |_) | (_) | | | | (_| |  __/ |   | |_| | 
     |_____/| .__/ \___/|_| |_|\__, |\___|_|    \__, | 
            | |                 __/ |            __/ | 
            |_|                |___/            |___/   

## Features 🌟

### 🔄 Data Cleaning
- Auto-clean phone numbers, IDs, and names
- Handle missing data with smart strategies:
  - Delete columns with >55% missing values
  - Fill numeric columns with mean/median
  - Multiple threshold configurations
- Text normalization (case conversion, special characters)

### 📊 Data Analysis
- Generate comprehensive reports:
  - Missing value analysis
  - Statistical summaries
  - Column type detection
  - Character distribution in text columns

### 📁 Multi-Format Support
- **Input:** CSV, Excel, JSON, Parquet, SQLite, Stata, Feather, Pickle
- **Output:** All input formats + HTML, XML (with consistent schema)

## Installation 💻
```bash
pip install spongepy
```
## Usage 🛠️
Basic Command Structure
```bash
spongepy --file <input> [OPTIONS]
```
### Key Options:
| Option          | Description                                  |
|-----------------|----------------------------------------------|
| `-f/--file`     | Input file (required)                        |
| `--clean`       | Enable auto-cleaning                         |
| `-c/--config`   | Use custom cleaning config (JSON)            |
| `-s/--stats`    | Show summary statistics                      |
| `-d/--details`  | Show detailed column analysis                |
| `-e/--export`   | Export cleaned data (specify filename)       |

## Configuration Example 🧠
### Generate config template:
```bash
spongepy -f data.csv --details  # Creates config.json
Sample config actions:
```
```json
exemple config.json : 
{
  "missing-data": [
    ["Age", "4.2%", "mean"],
    ["CreditScore", "12.1%", "median"]
  ],
  "phone-number": "Contact",
  "name": ["FirstName", "LastName"],
  "text-columns": [
    {
      "column": "Notes",
      "special": "!?,.-",
      "numbers": ""  // Remove all digits if exists
    }
  ]
}
```
## Common Workflows 🔄
#### Quick Clean & Export

```bash
spongepy -f dirty_data.xlsx --clean --export clean_data.parquet
```
#### Generate Data Health Report

```bash
spongepy -f customer_db.sqlite --details > report.txt
```

### Custom Pipeline { }
#### Generate config:

```bash
spongepy -f raw.csv --details
```

#### Edit config.json
rules are specified in config.json under 'Guide'

#### Run targeted clean:

```bash
spongepy -f raw.csv --clean -c config.json -e cleaned.csv
```

## Technical Specs ⚙️
Data Cleaning Logic
Missing Data %	Action
5%<	Drop rows
5%-55%	Mean/median imputation
80%<	Column removal

### Supported Text Operations
Case normalization

Special character whitelisting

Digit removal

Custom regex patterns

## Support & Contribution 🤝
Found a bug? Want a new feature?

Open an Issue

Contribution Guidelines

License: MIT
Version: 1.1.0
Compatibility: Python 3.8+
