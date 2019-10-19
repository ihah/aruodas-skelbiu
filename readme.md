# Info

- Scripts are made only for learning purpose.
- Scripts originally made only for collecting sample data.
- Scripts requires manually change the total of list pages exists in the website.

## Aruodas.lt filters

- Only apartments
- Only full established apartments

## Skelbiu.lt filters

- Only apartments
- Do not show Aruodas.lt ads


# How it works

1. Script starts in list page (1);
2. It will collect all links to the ads. (in aruodas.py it will collect url from the title plus city)
3. Next links are passed to collect data about the AD, get_data(item).
4. get_data() - collect the data and returns it, if no error occurred the data will be recorded into csv file, if error occurred script will skip the ad.
5. After script runs out of the links it will change the page to next one and repeat the process.


# CSV rows

- 'city' - city where apartment is
- 'years' - year of construction
- 'area' - area of the apartment
- 'price' - price of the apartment 
- 'avg_heat_per_m' - average cost of heating per month in the apartment
- 'url' - url to the AD