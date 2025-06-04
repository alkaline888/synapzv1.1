#!bin/bash
set -e

echo "Installing... This may take a few minutes"
pkg update && pkg upgrade && pkg install git zip clang python
git clone https://github.com/alkaline888/synapzv1.1/blob/main/build.zip
mkdir synapz
unzip build.zip
mv synapz.py synapz/
mv syn_utils.so synapz/
mv compileV1.sh synapz/
cd synapz && python synapz.py
echo "running synapzV1.1 global"
echo "https://t.me/synapzzz join for purry forn!"
