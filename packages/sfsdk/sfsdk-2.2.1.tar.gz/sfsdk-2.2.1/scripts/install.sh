#!/bin/bash

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

# Check if pipx is installed
if ! command -v pipx &> /dev/null; then
    echo "pipx is not installed. Please install pipx and try again."
    exit 1
fi

# Navigate to the root of the repository
cd "$(dirname "$0")"/..

# Install the package using pipx if it is not already installed, or upgrade if a new version is available
package_name="sfsdk"

# Check if the package is installed via pipx
if pipx list | grep -q "$package_name"; then
    echo "$package_name is already installed. Checking for updates..."
    pipx upgrade "$package_name"
else
    echo "$package_name is not installed. Installing using pipx..."
    pipx install .
fi

echo "Installation/Upgrade completed successfully."
