# pca

### Joining .smi files (if there are multiple)
```
cat smifile* > output.smi
```

### Export fingerprint values and map values
```
cut -f<columnindex> -d' ' output.smi > output.fp
cut -f<columnindex> -d' ' output.smi > output.prop
```

If there are trailing semicolons, remove the last character from each line 
```
sed 's/.$//'
```

### PCA
Required packages: `scipy`, `numpy`, `pandas`, `colour` and `sklearn`
```
python3 incremental_pca.py output.fp output.csv -d ';'
```

### Create the bins
```
python3 create_bins.py output.csv output.xyz -p output.prop -pd ';'
```

### Export SMILES and IDs
```
cut -f<columnindex> -d' ' output.smi > output.info
cut -f<columnindex> -d';' output.info > output.smiles
cut -f<columnindex> -d';' output.info > output.ids
```

### Pad smiles and coordinates files
Create a padded coordinate file (for each point, not for the bins)
```
python3 pad_coord_file.py output.csv output.pad.full.xyz
```
Important, the script `pad_coord_file.py` returns a value which is the offset of the padded file. This value is NOT stored anywhere.

Next, pad the smiles file
```
python3 pad_file.py output.smiles output.pad.smiles
```
Important, the script `pad_file.py` returns a value which is the offset of the padded file. This value is NOT stored anywhere.

### Creating map files
Map files are created one by one using
```
python3 create_map.py output.means output.stds hac.map -i 0
```
where `-i` is the index of the property
