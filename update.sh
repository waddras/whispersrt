#!/bin/bash
cd /opt/whispersrt
git fetch origin main
git reset --hard origin/main
echo "Updated to latest."
