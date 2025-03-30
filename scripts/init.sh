#!/bin/bash
# Create the data directory and load package
echo "===== Downloading Haskell Base Package ====="
rm -rf data/repos data/source data/filtered
mkdir -p data/repos
wget -P data/repos https://hackage.haskell.org/package/base-4.20.0.0/base-4.20.0.0.tar.gz
tar xvf data/repos/base-4.20.0.0.tar.gz -C data/repos

echo "===== Downloading Haskell GHC-Internal Package ====="
wget -P data/repos https://hackage.haskell.org/package/ghc-internal-9.1001.0/ghc-internal-9.1001.0.tar.gz
tar xvf data/repos/ghc-internal-9.1001.0.tar.gz -C data/repos
