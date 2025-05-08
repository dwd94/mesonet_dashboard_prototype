# Mesonet Dashboard Prototype

A prototype dashboard for visualizing Mesonet data and provider information.

## Setup and Installation

### Option 1: Using Conda (Recommended)

1. Create and activate the conda environment:
```bash
conda env create -f ./environment.yml
conda activate meso_env
```

2. Install additional required packages:
```bash
pip install dash-bootstrap-components
```

### Option 2: Using Virtual Environment (venv)

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
pip install dash-bootstrap-components
```

## Running the Dashboard

1. Start the application:
```bash
python application.py
```

2. Access the dashboard:
- Open your web browser and go to: `http://localhost:8050`
- The dashboard will be available at this address

## Available Pages

The dashboard includes several pages that can be accessed via the following URLs:

- Home/Overview: `http://localhost:8050/`
- Providers: `http://localhost:8050/providers`
  - Shows provider locations on a map
  - Displays provider statistics and status
  - Includes interactive provider cards with progress bars and mini graphs

## Features

### Providers Page
- Interactive map showing provider locations
- Color-coded markers based on station count
- Provider cards showing:
  - Provider name
  - Progress bar indicating relative station count
  - Mini line graph
  - 24-hour average frequency
- Hover information on map markers
- Filterable provider list

## Data Sources

The dashboard uses data from:
- Mesonet Vendor Info Excel file
- Provider metadata
- Station information

## Development

To modify the dashboard:
1. Edit the Python files in the `pages` directory
2. Modify the layout in `application.py`
3. Update the data sources as needed

## Troubleshooting

If you encounter any issues:
1. Ensure all dependencies are installed
2. Check the console for error messages
3. Verify the data files are in the correct location
4. Make sure the environment (conda or venv) is activated
5. If using venv, ensure you're using Python 3.8 or higher