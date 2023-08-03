# Retrieving BIOGRID data for VERIT

VERSION="4.4.222"

curl -L https://downloads.thebiogrid.org/Download/BioGRID/Release-Archive/BIOGRID-$VERSION/BIOGRID-ALL-$VERSION.tab3.zip --output BIOGRID-ALL-$VERSION.tab3.zip

unzip BIOGRID-ALL-$VERSION.tab3.zip

mv ./BIOGRID-ALL-$VERSION.tab3.txt ./BIOGRID-ALL-$VERSION.tsv

cut -f 8-11,24,27,36,37,12-15 ./BIOGRID-ALL-$VERSION.tsv > ./BIOGRID-ALL-$VERSION.trunc.tsv