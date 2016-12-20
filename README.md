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

### PCA
```
python3 ~/Code/pca/incremental_pca.py output.fp output.csv -d ';'
```