![PCPBIM](https://github.com/reymond-group/pca/blob/master/logo.png?raw=true)
# The PCPBIM (Preparation - Cleanup - PCA - Binning - Info - Mapping) Toolchain
This collection of utility scripts creates files which can be served by the [Underdark Go](https://github.com/reymond-group/underdarkgo) web service which is part of the FUn Framework.
## Dependencies
- Python 3
    - numpy
    - pandas
    - scipy
    - sklearn
## Getting Started
It is important to have all input files in a correct file format which is a plain-text file containing information on one molecule per line, structured as follows
```
c1ccccc1 Benzene 1;0;0;1;0;1;1;1;1;1;0 1.25;6
C1CCCC1 Cyclopentan 1;0;0;1;1;1;1;1;1;0;1 0.75;5
```
Where each line contains the SMILES, an arbitrary label, a fingerprint vector, and any number of numerical properties for which the colour maps will be generated. The default delimiters are `whitespace` and `;`, both can be changed by modifying the script `doitall.sh`.

To generate the files for Underdark Go, make sure the files are in the correct format and all dependencies are met and clone this repository
```bash
git clone https://github.com/reymond-group/pca.git
```
Next, make sure the bash script is executable
```bash
chmod +x doitall.sh
```
Finally, run the bash script which will in turn run the necessary python scripts
```bash
./doitall.sh inputFile databaseName fingerprintName n
```
where `inputFile` is a plain-text file formatted according to the information provided above, `databaseName` and `fingerprintName` are arbitrary names chosen for the database and the fingerprint respectively. `n` is an integer setting the resolution of the final cubic map. It is good practice to provide low (n <= 250) and high (n >= 500) resolution versions of each map. While most maps are probably sparse and do not approach the maximum number of rendered bins n<sup>3</sup>, these numbers might have to be lowered for densly populated maps.

Example
```bash
./doitall.sh my-awesome-data.txt ACMEbase Xfp 250
```