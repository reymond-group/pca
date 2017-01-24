# pca
### File Integrity Check
The file can be checked on whether or not it is an ASCII file using the `checkascii.sh` script. Checks on the readability of the file can be run using the `check_file.py` script.

### Preparation
If the files do not contain matching compounds (some might fail during fingerprint calculation), the differing files have to be removed in order to guarantee that the ids and smiles indices point to the correct value for each fingerprint. This is due to the fact, that smiles and ids are used per database and not per fingerprint (resulting in less memory usage).

First, extract the ids from the .smi files:
```
cut -f<columnindex> -d' ' output.smi > output.info
cut -f<columnindex> -d';' output.info > output.ids
```
Next, sort the ids:
```
sort output.ids -o output.ids
```
Finally, use the `comm` command to extract the shared lines among the files a, b, c, d by:
```
comm -12 a.ids b.ids | comm -12 - c.ids | comm -12 - d.ids > commond.ids
```
To join the files again, first, sort one of the `.info` files by the id:
```
sort --field-separator=';' --key=2 output.info -o output.info
join -1 2 -2 1 output.info commont.ids -t $';' > common.info
```
Reorder the columns and sort the file
```
awk -F";" '{print $2 ";" $1}' common.info > tmp && mv tmp common.info
sort common.info -o common.info
```
Then sort the file `output.smi` and join it with `common.info`
```
sort output.smi -o output.smi
join -1 1 -2 1 common.info output.smi -t $' ' > output.smi.fixed
```

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
sed -i 's/.$//' <file>
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
