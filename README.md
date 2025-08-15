Dưới đây là bản **README.md** đầy đủ cho toàn bộ dự án của bạn, bao gồm cả tự động backup, push Git và chạy AWX/Execution Environment.
Mình đã tổng hợp từ cả hai file bạn gửi và bổ sung thêm cấu trúc, hướng dẫn cài đặt và vận hành.

---

# Ansible Network Automation Project

## 1. Giới thiệu

Dự án này triển khai giải pháp **tự động quản lý, backup, kiểm tra compliance và triển khai cấu hình** cho hệ thống router Cisco (và có thể mở rộng cho multi-vendor như Arista, Juniper) thông qua **Ansible**.
Hệ thống được xây dựng và thử nghiệm trong môi trường **Pnetlab** mô phỏng mạng Viettel, kèm các chức năng:

* **Backup định kỳ** cấu hình router, lưu trữ có timestamp.
* **Push tự động** các file backup lên GitHub/GitLab.
* **Kiểm tra compliance** giữa cấu hình thực tế và cấu hình chuẩn (golden config).
* **Tự động khôi phục** cấu hình khi phát hiện sai lệch.
* **Chạy Ansible trong Execution Environment** (EE) với ansible-navigator hoặc AWX.
* **Pipeline CI/CD** để đảm bảo cấu hình chuẩn trước khi merge.

---

## 2. Mục tiêu

* Khẳng định tính khả thi khi ứng dụng Ansible trong môi trường mạng lớn như Viettel.
* Mô phỏng thực tế trên Pnetlab với nhiều router đóng vai trò khác nhau.
* Giảm lỗi thủ công, chuẩn hóa cấu hình, rút ngắn thời gian vận hành.
* Xây dựng quy trình chuẩn: **Backup → Compliance → Rollout**.

---

## 3. Kiến trúc & Quy trình

```plaintext
Pnetlab (Router Cisco/Arista/Juniper)
      ↓ SSH / NETCONF
Ubuntu Server (Ansible Control Node)
      ↓
Ansible Playbooks + Roles
      ↓
Backup / Compliance / Deploy
      ↓
Push GitHub/GitLab → CI/CD Pipeline
      ↓
Execution Environment / AWX
```

---

## 4. Cấu trúc thư mục dự án

```plaintext
ansible-network/
├── ansible.cfg
├── inventories/
│   └── lab/
│       ├── hosts.yml
│       ├── group_vars/
│       │   └── routers.yml
│       └── host_vars/
│           └── R3.yml
├── playbooks/
│   ├── backup.yml
│   ├── compliance.yml
│   ├── compliance_and_fix.yml
│   ├── init-golden.yml
│   └── restore-golden.yml
├── roles/
│   └── backup_config/
│       ├── tasks/
│       ├── defaults/
│       ├── handlers/
│       └── meta/
├── backups/
│   └── R1/
│       └── *.cfg
├── golden/
│   └── R1/
│       └── base.cfg
├── secrets/
│   ├── ios_creds.yml
│   └── vault_ios_pw.yml
├── collections/
│   └── requirements.yml
├── .ansible-lint
├── requirements.txt
└── Dockerfile.ee
```

---

## 5. Cài đặt & Chuẩn bị môi trường

### 5.1. Cài đặt Python & Virtualenv

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 5.2. Cài đặt dependencies

```bash
pip install -r requirements.txt
ansible-galaxy collection install -r collections/requirements.yml
```

### 5.3. Cấu hình SSH & NAT

* Tạo user `netadmin` trên router với privilege 15.
* NAT port SSH nếu truy cập qua router trung gian.
* Bổ sung `ansible_port` trong `hosts.yml` khi cần.

---

## 6. Các Playbook chính

| Playbook                 | Chức năng                                              |
| ------------------------ | ------------------------------------------------------ |
| `backup.yml`             | Backup cấu hình hiện tại, lưu theo timestamp.          |
| `init-golden.yml`        | Lấy cấu hình hiện tại và lưu làm golden config.        |
| `compliance.yml`         | So sánh running-config với golden config.              |
| `compliance_and_fix.yml` | Kiểm tra compliance và tự động khôi phục khi sai lệch. |
| `restore-golden.yml`     | Khôi phục cấu hình từ golden.                          |

---

## 7. Tự động backup & push Git

### 7.1. Cron job

Thêm vào `crontab -e`:

```bash
0 2 * * * cd /path/to/ansible-network && ansible-playbook playbooks/backup.yml && ./scripts/git_auto_push.sh
```

### 7.2. Script `git_auto_push.sh`

```bash
#!/bin/bash
git add backups/
git commit -m "Auto backup at $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
```

---

## 8. Chạy trong Execution Environment / AWX

### 8.1. Build EE image

```Dockerfile
FROM quay.io/ansible/creator-ee:latest
COPY offline_collections/ /usr/share/ansible/collections/
```

```bash
docker build -t my-ee:latest -f Dockerfile.ee .
```

### 8.2. Run với ansible-navigator

```bash
ansible-navigator run playbooks/backup.yml --eei my-ee:latest --pull-policy never
```

### 8.3. AWX Job Template

* Inventory: `inventories/lab/hosts.yml`
* Project: Git repo của bạn.
* Playbook: Chọn `backup.yml` hoặc `compliance.yml`.

---

## 9. Kiểm tra & Lint code

```bash
ansible-lint playbooks/backup.yml
```

Đảm bảo **Lint = 0** trước khi commit.

---

## 10. Kế hoạch mở rộng

* Hỗ trợ multi-vendor (Arista, Juniper).
* Tích hợp với hệ thống giám sát (Zabbix, Prometheus).
* Tự động tạo báo cáo PDF sau mỗi lần backup/compliance.

---

## 11. Tài liệu tham khảo

* [Ansible Documentation](https://docs.ansible.com/)
* [Cisco IOS Collection](https://galaxy.ansible.com/cisco/ios)
* [AWX Project](https://github.com/ansible/awx)

---

Nếu bạn muốn mình có thể viết thêm **phần hướng dẫn chạy test toàn bộ pipeline** để README của bạn vừa là tài liệu hướng dẫn triển khai vừa là hướng dẫn kiểm thử.
Bạn có muốn mình bổ sung phần đó không?
