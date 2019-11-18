#!/bin/bash
set -e
mkdir ispell
echo -e "\e[33mExtracting ispell source...\e[39m"
tar xvjf sjp-ispell-pl-*-src.tar.bz2 --transform 's/sjp-ispell-pl-[0-9]*/ispell/'
cd ispell
sort -u -t/ +0f -1 +0 -T /usr/tmp -o polish.med polish.all
for a in polish.aff polish.med; do cat $a | iconv -f iso8859-2 -t utf-8 > $a.utf8; done
echo -e "\e[33mAdding ispell files to postgres share directory...\e[39m"
sudo cp polish.aff.utf8 `pg_config --sharedir`/tsearch_data/polish.affix
sudo cp polish.med.utf8 `pg_config --sharedir`/tsearch_data/polish.dict
sudo touch `pg_config --sharedir`/tsearch_data/polish.stop
cd ..

echo -e "\e[33mCreating locus_db database...\e[39m"
sudo -u postgres psql -f postgresql_db_setup.sql
echo -e "\e[33mAdding ispell to locus_db...\e[39m"
sudo -u postgres psql -f postgresql_ispell_setup.sql locus_db

rm -r ispell
