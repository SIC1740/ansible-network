#!/bin/bash
cd /home/ubuntu/ansible-network || exit

NOW=$(date +"%Y-%m-%d %H:%M:%S")

git add .
git commit -m "Auto backup at $NOW"
git push origin main
