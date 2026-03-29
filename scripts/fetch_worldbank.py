import urllib.request
import json
import os

print("Fetching latest data from World Bank Free API for Saudi Arabia (SAU)...")

# World Bank API indicators
indicators = {
    "population_total": "SP.POP.TOTL",
    "gdp_usd": "NY.GDP.MKTP.CD",
    "labor_force_participation_rate": "SL.TLF.CACT.ZS",
    "gdp_growth_annual_percent": "NY.GDP.MKTP.KD.ZG"
}

macro_data = {
    "metadata": {
        "source": "World Bank Free API (api.worldbank.org)",
        "description": "Baseline macroeconomic parameters for the Saudi Arabian Economy Simulator."
    },
    "saudi_arabia": {
        # Defaults to be overwritten by API
        "population_total": {"value": 32200000, "year": 2022, "source": "Fallback"},
        "gdp_usd": {"value": 1108000000000, "year": 2022, "source": "Fallback"},
        "gdp_growth_annual_percent": {"value": 2.0, "year": 2022, "source": "Fallback"},
        "labor_force_participation_rate": {"value": 61.5, "year": 2022, "source": "Fallback"},
        
        # Values that are fixed/structural and not in World Bank API
        "pif_aum_billion_usd": {"value": 925.0, "source": "Fixed: Public Investment Fund"},
        "vat_rate": {"value": 15.0, "source": "Fixed: ZATCA"},
        "corporate_zakat_rate": {"value": 2.5, "source": "Fixed: ZATCA"},
        "citizens_account_monthly_usd_equiv": {"value": 930.0, "source": "Fixed: CA Average"}
    }
}

for key, indicator in indicators.items():
    url = f"http://api.worldbank.org/v2/country/SAU/indicator/{indicator}?format=json&per_page=1"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read())
            if len(res) > 1 and len(res[1]) > 0:
                val = res[1][0]['value']
                year = res[1][0]['date']
                if val is not None:
                    macro_data["saudi_arabia"][key] = {"value": val, "year": year, "source": "World Bank API"}
                    print(f"Successfully fetched {key}: {val} ({year})")
    except Exception as e:
        print(f"Warning: Failed to fetch {key} from World Bank. Error: {e}")

# Save to root macro_data.json
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "macro_data.json")
with open(out_path, "w") as f:
    json.dump(macro_data, f, indent=4)

print(f"macro_data.json successfully written to {os.path.abspath(out_path)}!")
