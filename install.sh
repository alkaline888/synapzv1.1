#!bin/bash
set -e

clear
echo "Installing... This may take a few minutes"
pkg update && pkg upgrade && pkg install git zip clang python
wget https://raw.githubusercontent.com/alkaline888/synapzv1.1/refs/heads/main/synapz.py
wget https://github.com/alkaline888/synapzv1.1/releases/download/lib/syn_utils.so
mkdir synapz
mv synapz.py synapz/
mv syn_utils.so synapz/
cd synapz && python synapz.py
echo "running synapzV1.1 global"
echo "https://t.me/synapzzz join for purry forn!"
