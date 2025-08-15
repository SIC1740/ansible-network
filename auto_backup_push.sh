#!/bin/bash
set -euo pipefail

# ===== CONFIG =====
REPO_DIR="/home/ubuntu/ansible-network"
INV="$REPO_DIR/inventories/lab/hosts.yml"
PLAY="$REPO_DIR/playbooks/backup.yml"
LOG_MAIN="$REPO_DIR/auto_backup_push.log"

# Bổ sung PATH cho cron
export PATH="/home/ubuntu/ansible-network/venv/bin:/home/ubuntu/ansible-network/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH"

# Kích hoạt venv nếu có (ưu tiên venv -> .venv)
if [ -f "$REPO_DIR/venv/bin/activate" ]; then
  source "$REPO_DIR/venv/bin/activate"
elif [ -f "$REPO_DIR/.venv/bin/activate" ]; then
  source "$REPO_DIR/.venv/bin/activate"
fi

cd "$REPO_DIR"

NOW="$(date +"%Y-%m-%d %H:%M:%S")"

{
  echo "[$NOW] ==== RUN START ===="
  echo "which ansible-playbook: $(command -v ansible-playbook || echo 'not found')"

  # 1) Backup running-config (module ios_config backup: yes trong backup.yml)
  ansible-playbook -i "$INV" "$PLAY" -vv

  # 2) Chỉ push khi có thay đổi
  if [[ -n "$(git status --porcelain)" ]]; then
    git add .
    git commit -m "Auto backup at $NOW"
    git push origin main
    echo "[$NOW] Pushed changes to GitHub."
  else
    echo "[$NOW] No changes to push."
  fi

  echo "[$NOW] ==== RUN END ===="
  echo
} >> "$LOG_MAIN" 2>&1
