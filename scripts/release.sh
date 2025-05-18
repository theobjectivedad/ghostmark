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

# Make sure we pull the up


# Validate semver format (MAJOR.MINOR.PATCH) or version increment keywords
if [[ $1 =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    # Valid semver format
    echo "Setting version to $1"
    elif [[ $1 =~ ^(major|minor|patch)$ ]]; then
    echo "Incrementing $1 version"
else
    echo "Error: Version must be either:"
    echo "  - Semantic version format: MAJOR.MINOR.PATCH (e.g., 1.2.3)"
    echo "  - Version increment: major, minor, or patch"
    exit 1
fi

hatch version $1 || { echo "Failed to update version with hatch"; exit 1; }

NEW_VERSION=$(hatch version)
echo "Updating to version $NEW_VERSION"

git add . || { echo "Failed to stage changes"; exit 1; }
git commit -m "Bump version to $NEW_VERSION" || { echo "Failed to commit changes"; exit 1; }
git push
git tag v$NEW_VERSION || { echo "Failed to create tag"; exit 1; }
git push origin v$NEW_VERSION || { echo "Failed to push tag"; exit 1; }

echo "Successfully released version $NEW_VERSION"