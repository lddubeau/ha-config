#!/bin/bash

set -e

BUILD_DIR=out
rm -rf prev
mv $BUILD_DIR prev || true
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR
# Copy the static files.
(cd static; tar -cpf - `find . -type f`) | tar -C out -xpf -
