#!/bin/bash
set -euo pipefail

# ===== CONFIG =====
REPO_DIR="/home/ubuntu/ansible-network"
INV="$REPO_DIR/inventories/hosts.yml"         # inventory file (đường dẫn tuyệt đối)
PLAY="$REPO_DIR/playbooks/backup.yml"         # playbook file (đường dẫn tuyệt đối)
LOG_MAIN="$REPO_DIR/auto_backup_push.log"

# ===== Chuẩn bị môi trường =====
# PATH đầy đủ để cron tìm thấy ansible & git
export PATH="$REPO_DIR/venv/bin:$REPO_DIR/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH"

# Vào thư mục dự án
cd "$REPO_DIR" || exit

# Kích hoạt venv nếu có
if [ -f "$REPO_DIR/venv/bin/activate" ]; then
  source "$REPO_DIR/venv/bin/activate"
elif [ -f "$REPO_DIR/.venv/bin/activate" ]; then
  source "$REPO_DIR/.venv/bin/activate"
fi

NOW="$(date +"%Y-%m-%d %H:%M:%S")"

{
  echo "[$NOW] ==== RUN START ===="
  echo "whoami=$(whoami)"
  echo "pwd=$(pwd)"
  echo "which ansible-playbook: $(command -v ansible-playbook || echo 'not found')"
  echo "branch=$(git rev-parse --abbrev-ref HEAD)"
  echo "remote=$(git remote -v | head -n1)"

  # Kiểm tra inventory
  if ! ansible-inventory -i "$INV" --graph >/dev/null 2>&1; then
    echo "ERROR: Inventory file $INV không hợp lệ hoặc không load được!"
    echo "==== RUN END ===="
    exit 1
  fi

  # 1) Chạy backup
  ansible-playbook -i "$INV" "$PLAY" -vv

  # 2) Push nếu có thay đổi
  if [[ -n "$(git status --porcelain)" ]]; then
    git add .
    git commit -m "Auto backup at $NOW"
    if git push origin main; then
      echo "[$NOW] Pushed changes to GitHub."
    else
      echo "[$NOW] ERROR: git push failed."
    fi
  else
    echo "[$NOW] No changes to push."
  fi

  echo "[$NOW] ==== RUN END ===="
  echo
} >> "$LOG_MAIN" 2>&1
