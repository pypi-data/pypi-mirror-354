#!/bin/bash

declare -A base_images=(
    ["debian-testing"]="debian:testing"
    ["debian-latest"]="debian:latest" # Passes
    ["debian-trixie"]="debian:bookworm" # Passes
    ["debian-bookworm"]="debian:bookworm" # Passes

    ["ubuntu-devel"]="ubuntu:devel" # Passes
    ["ubuntu-latest"]="ubuntu:latest" # Passes
    ["ubuntu-plucky"]="ubuntu:plucky" # Passes
    ["ubuntu-oracular"]="ubuntu:oracular" # Passes
    ["ubuntu-noble"]="ubuntu:noble" # Passes
    ["ubuntu-jammy"]="ubuntu:jammy" # Passes

    ["manjaro-latest"]="manjarolinux/base:latest" # Passes

    ["fedora-rawhide"]="fedora:rawhide" # Passes
    ["fedora-latest"]="fedora:latest" # Passes
    ["fedora-42"]="fedora:42" # Passes
    ["fedora-41"]="fedora:41" # Passes
    ["fedora-40"]="fedora:40" # Passes
    ["fedora-39"]="fedora:39" # Passes
    ["fedora-38"]="fedora:38" # Passes
    ["fedora-37"]="fedora:37" # Passes
)

# Function to build a Docker image for multiple architectures, log its output, and check for expected output
build_and_log_multiarch() {
    local tag=$1
    local base_image=$2
    local architectures=$3
    local expected_output_partial="usage: sfsdk [-h] [--verbose]"

    # Loop through specified architectures and build images
    for arch in "${architectures[@]}"; do
        local logfile="/tmp/build_$tag_$arch.log"
        
        echo "Building $tag-$arch..."
        docker buildx build --platform "linux/$arch" -f $dockerfile \
            --build-arg BASE_IMAGE="$base_image" \
            -t "sfsdk:$tag-$arch" --load . > "$logfile" 2>&1

        output=$(docker run --platform "linux/$arch" --rm sfsdk:$tag-$arch bash -lc 'sfsdk')

        # Check if the actual output contains the expected partial output
        if [[ "$output" == *"$expected_output_partial"* ]]; then
            echo "sfsdk installed successfully on: $tag-$arch"
        else
            echo "-----------------------------------"
            echo "Contents of Logfile ($logfile):"
            echo "-----------------------------------"
            cat $logfile

            echo "-----------------------------------"
            echo "Output Variable:"
            echo "-----------------------------------"
            echo $output

            echo "-----------------------------------"
            echo "Error: Output does not contain expected partial output for $tag-$arch."
            echo "-----------------------------------"
            exit 1
        fi
    done
}

# Directory where the Dockerfile is located
dockerfile_dir="$(dirname "$0")"

# Path to the Dockerfile
dockerfile="$dockerfile_dir/Dockerfile"

# Create and use a new Buildx builder
if docker buildx inspect sfsdk > /dev/null 2>&1; then
  echo "Builder sfsdk already exists, setting it as current builder."
  docker buildx use sfsdk
else
  echo "Creating new builder sfsdk and setting it as current builder."
  docker buildx create --name sfsdk --use
fi

# Determine architectures to build based on the input argument
architectures=("amd64")
if [ "$1" == "arm64" ]; then
    architectures=("arm64")
elif [ "$1" == "both" ]; then
    architectures=("amd64" "arm64")
fi

# Must have installed: sudo apt-get install qemu binfmt-support qemu-user-static
# To enable arm64 emulation on an x86 PC
if [ "$1" == "arm64" ] || [ "$1" == "both" ]; then
    docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
fi

# Build images
for image_tag in "${!base_images[@]}"; do
    build_and_log_multiarch "$image_tag" "${base_images[$image_tag]}" "${architectures[@]}"
done

echo "sfsdk installed on all distros successfully!"