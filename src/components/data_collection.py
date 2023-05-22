import os
import urllib.request


i2m = list(zip(range(1, 13), ['Gener', 'Febrer', 'Marc', 'Abril', 'Maig', 'Juny', 'Juliol', 'Agost', 'Setembre', 'Octubre', 'Novembre', 'Desembre']))
for year in [2022, 2021, 2020, 2019]:
    for month, month_name in i2m:
        
        file_url = f'https://opendata-ajuntament.barcelona.cat/resources/bcn/BicingBCN/{year}_{month:02d}_{month_name}_BicingNou_ESTACIONS.7z'
        file_name = f'data/raw/{year}_{month:02d}_{month_name}_BicingNou_ESTACIONS.7z'
        extraction_path = 'data/raw'
        
        # Download the file using urllib
        urllib.request.urlretrieve(file_url, file_name)
        
        # Extract the contents of the 7z archive using 7-Zip
        extract_cmd = f'7z x {file_name} -o{extraction_path}'
        os.system(extract_cmd)
        
        # Remove the downloaded 7z archive file using shutil
        os.remove(file_name)
