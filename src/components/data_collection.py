import os
import urllib.request
from src.logger import logging


i2m = list(zip(range(1, 13), ['Gener', 'Febrer', 'Marc', 'Abril', 'Maig', 'Juny', 'Juliol', 'Agost', 'Setembre', 'Octubre', 'Novembre', 'Desembre']))

for year in [2022, 2021, 2020, 2019]:
    if not os.path.exists(f'data/raw/bicing_stations_status/{year}'):
        os.makedirs(f'data/raw/bicing_stations_status/{year}', exist_ok=True)
        
        for month, month_name in i2m:
        
            file_url = f'https://opendata-ajuntament.barcelona.cat/resources/bcn/BicingBCN/{year}_{month:02d}_{month_name}_BicingNou_ESTACIONS.7z'
            file_name = f'data/raw/bicing_stations_status/{year}/{year}_{month:02d}_{month_name}_BicingNou_ESTACIONS.7z'
            extraction_path = f'data/raw/bicing_stations_status/{year}/'
        
            try:
                # Download the file using urllib
                urllib.request.urlretrieve(file_url, file_name)
        
            except urllib.error.HTTPError as e:
            
                if e.code == 404:
                    logging.info(f'File not found: {year}_{month:02d}_{month_name}_BicingNou_ESTACIONS.7z')
                    continue
            
            # Extract the contents of the 7z archive using 7-Zip
            extract_cmd = f'7z x {file_name} -o{extraction_path}'
            os.system(extract_cmd)
        
            # Remove the downloaded 7z archive file
            os.remove(file_name)
        
            logging.info(f'File successfully downloaded!: {year}_{month:02d}_{month_name}_BicingNou_ESTACIONS.7z')
