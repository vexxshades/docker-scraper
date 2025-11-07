#!/bin/bash
# Build script for docker-scraper Debian package

set -e

PACKAGE_NAME="docker-scraper"
VERSION="1.0.0"
BUILD_DIR="debian-package"
TEMP_BUILD_DIR="/tmp/${PACKAGE_NAME}-build"

echo "Building ${PACKAGE_NAME} v${VERSION} Debian package..."

# Clean previous build
rm -f ${PACKAGE_NAME}_${VERSION}_all.deb
rm -rf ${TEMP_BUILD_DIR}

# Copy package structure to Linux filesystem (WSL workaround for permissions)
echo "Copying to temporary build directory..."
cp -r ${BUILD_DIR} ${TEMP_BUILD_DIR}

# Set correct permissions for DEBIAN scripts
echo "Setting permissions..."
chmod 755 ${TEMP_BUILD_DIR}/DEBIAN
chmod 755 ${TEMP_BUILD_DIR}/DEBIAN/postinst
chmod 755 ${TEMP_BUILD_DIR}/DEBIAN/prerm
chmod 644 ${TEMP_BUILD_DIR}/DEBIAN/control
chmod 644 ${TEMP_BUILD_DIR}/etc/systemd/system/docker-scraper.service

# Fix line endings (WSL/Windows compatibility)
echo "Fixing line endings..."
sed -i 's/\r$//' ${TEMP_BUILD_DIR}/DEBIAN/postinst
sed -i 's/\r$//' ${TEMP_BUILD_DIR}/DEBIAN/prerm
sed -i 's/\r$//' ${TEMP_BUILD_DIR}/DEBIAN/control

# Build the package
echo "Building package..."
dpkg-deb --build ${TEMP_BUILD_DIR} ${PACKAGE_NAME}_${VERSION}_all.deb

# Clean up temp directory
rm -rf ${TEMP_BUILD_DIR}

# Verify the package
echo ""
echo "Package built successfully!"
echo "Package info:"
dpkg-deb --info ${PACKAGE_NAME}_${VERSION}_all.deb

echo ""
echo "Package contents:"
dpkg-deb --contents ${PACKAGE_NAME}_${VERSION}_all.deb

echo ""
echo "To install: sudo dpkg -i ${PACKAGE_NAME}_${VERSION}_all.deb"
echo "To remove:  sudo dpkg -r ${PACKAGE_NAME}"
