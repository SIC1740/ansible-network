#!/bin/bash
set -euo pipefail

# --- CẤU HÌNH CƠ BẢN ---
REPO_DIR="/home/ubuntu/ansible-network"
LOG_DIR="$REPO_DIR"
INV="$REPO_DIR/inventories/lab/hosts.yml"
PLAY="$REPO_DIR/playbooks/backup.yml"

# Nếu bạn dùng venv trong dự án: kích hoạt (không lỗi nếu không có)
if [ -f "$REPO_DIR/.venv/bin/activate" ]; then
  source "$REPO_DIR/.venv/bin/activate"
fi

# Bảo đảm PATH đầy đủ khi chạy qua cron
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

cd "$REPO_DIR"

# 1) Chạy backup (playbook đã có ios_config backup: yes)
ansible-playbook -i "$INV" "$PLAY" -vv

# 2) Chỉ push khi có thay đổi (tránh spam commit rỗng)
NOW="$(date +"%Y-%m-%d %H:%M:%S")"
if [[ -n "$(git status --porcelain)" ]]; then
  git add .
  git commit -m "Auto backup at $NOW"
  git push origin main
  echo "[$NOW] Changes pushed to GitHub." >> "$LOG_DIR/auto_backup_push.log"
else
  echo "[$NOW] No changes to push." >> "$LOG_DIR/auto_backup_push.log"
fi
