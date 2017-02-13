![PCPBIM](https://github.com/reymond-group/pca/blob/master/logo.png?raw=true)
# The PCPBIM (Preparation - Cleanup - PCA - Binning - Info - Mapping) Toolchain

### File Integrity Check
The file can be checked on whether or not it is an ASCII file using the `checkascii.sh` script. Checks on the readability of the file can be run using the `check_file.py` script.

### Joining .smi files (if there are multiple)
```
cat smifile* > output.smi
```

### Preparation
If the files do not contain matching compounds (some might fail during fingerprint calculation), the differing files have to be removed in order to guarantee that the ids and smiles indices point to the correct value for each fingerprint. This is due to the fact, that smiles and ids are used per database and not per fingerprint (resulting in less memory usage).

Before running `doitall.sh`, make sure, that each field (including smiles and id) is separated by a whitespace character, the semicolon between the smiles and id fields can be replaced by this command:
```
sed -i 's/;/ /' output.smi
```

<!--
Decouple the ID from the smiles string by replacing the first occurance of `;` with a space:
```
sed -i 's/;/ /' output.smi
```
-->
If there are trailing semicolons, remove the last character from each line 
```
sed -i 's/.$//' <file>
```
First, sort the smi files by the ID:
```
sort --field-separator=' ' --key=2,2 --ignore-nonprinting output.smi -o output.smi
```
Then extract the ids from the .smi files:
```
cut -f2 -d' ' output.smi > output.ids
```
Finally, use the `comm` command to extract the shared lines among the files a, b, c, d by:
```
comm -12 a.ids b.ids | comm -12 - c.ids | comm -12 - d.ids > common.ids
```
Now join tile different `.smi` files on the file `common.ids`:
```
join -1 2 -2 2 common.ids output.smi -t $' ' > output.smi.fixed
```

### Cut the main file
```
cut -f1 -d' ' output.fixed.smi > output.ids
cut -f2 -d' ' output.fixed.smi > output.smiles
cut -f3 -d' ' output.fixed.smi > output.fp
cut -f4 -d' ' output.fixed.smi > output.prop
```

### PCA
Required packages: `scipy`, `numpy`, `pandas`, `colour` and `sklearn`
```
python3 incremental_pca.py output.fp output.fingerprint.xyz -d ';'
```

### Create the bins
```
python3 create_bins.py output.csv output.xyz -p output.prop -pd ';' -b 250
```

### Index files
Create indices for the different files:
```
python3 index_file.py output.ids
python3 index_file.py output.smiles
python3 index_file.py output.fingerprint.xyz
```
### Creating map files
Map files are created one by one using
```
python3 create_map.py output.means output.stds hac.map -i 1 
```
where `-i` is the index of the property starting from 1
