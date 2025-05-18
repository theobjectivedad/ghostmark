#!/bin/bash

NEW_VERSION=$1
hatch version $NEW_VERSION
git add .
git commit -m "Bump version to $NEW_VERSION"
git tag v$NEW_VERSION
git push origin v$NEW_VERSION