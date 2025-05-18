#!/bin/bash

set -e

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "Error: There are uncommitted changes in the repository"
    echo "Please commit or stash your changes before releasing"
    exit 1
fi

# Check if version parameter is provided
if [ -z "$1" ]; then
    echo "Error: Version number is required"
    echo "Usage: $0 <version>"
    exit 1
fi

NEW_VERSION=$1

# Validate semver format (MAJOR.MINOR.PATCH)
if ! [[ $NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Version must follow semantic versioning format: MAJOR.MINOR.PATCH"
    echo "Example: 1.2.3"
    exit 1
fi

echo "Updating to version $NEW_VERSION"
hatch version $NEW_VERSION || { echo "Failed to update version with hatch"; exit 1; }

git add . || { echo "Failed to stage changes"; exit 1; }
git commit -m "Bump version to $NEW_VERSION" || { echo "Failed to commit changes"; exit 1; }
git tag v$NEW_VERSION || { echo "Failed to create tag"; exit 1; }
git push origin v$NEW_VERSION || { echo "Failed to push tag"; exit 1; }

echo "Successfully released version $NEW_VERSION"