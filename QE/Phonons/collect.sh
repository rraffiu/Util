#!/bin/bash


#Change the prefix below

PREFIX='w'
TMP_DIR='./tmp'


#ph-collect.sh should be in the work directory of PHonon calculation
echo `date`
echo `pwd`
echo 'PREFIX: ' $PREFIX
echo "Creating a save dir..."
mkdir -p save/${PREFIX}.phsave
echo "Copying dyn files..."
cp ./${PREFIX}.dyn* save/
for q in `seq 1 29 ` ; do
PH0_DIR="./tmp/$q/_ph0"
echo "Copying the dynamt files ..."
cp ${PH0_DIR}/${PREFIX}.phsave/dynmat.* save/${PREFIX}.phsave/
if [ "$q" -eq 1 ]; then
        echo "Copying the dvscf file for the first q-point..."
        cp ${PH0_DIR}/${PREFIX}.dvscf1 save/${PREFIX}.dvscf_q1
        cp ${PH0_DIR}/${PREFIX}.phsave/pattern* save/${PREFIX}.phsave/
else
        echo "Copying the dvscf for q = $q ..."
        cp ${PH0_DIR}/${PREFIX}.q_$q/${PREFIX}.dvscf1 save/${PREFIX}.dvscf_q${q}        
fi
done
echo "Done!"
echo `date`
