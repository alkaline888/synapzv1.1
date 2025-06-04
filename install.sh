#!bin/bash
set -e

echo "Installing... This may take a few minutes"
pkg update && pkg upgrade && pkg install git zip clang python
git clone
