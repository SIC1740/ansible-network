# Ansible Network Automation – Backup & Compliance

## 📌 1. Giới thiệu
Dự án này sử dụng **Ansible** để tự động hóa việc quản lý, backup cấu hình và kiểm tra compliance cho các thiết bị mạng Cisco IOS.  
Mục tiêu:
- Quản lý nhiều router từ một máy chủ Ansible.
- Tự động backup cấu hình thiết bị vào thư mục `/backups/`.
- So sánh cấu hình thực tế với “golden config” chuẩn và xuất kết quả diff.
- Đề xuất áp dụng vào hệ thống mạng lớn (ví dụ Viettel).

---

## 📦 2. Yêu cầu hệ thống
| Thành phần            | Phiên bản tối thiểu |
|-----------------------|----------------------|
| Python                | 3.10+               |
| Ansible Core          | 2.15.9              |
| Ansible Navigator     | 25.5.0              |
| Cisco IOS Collection  | 10.1.1              |
| Netcommon Collection  | 8.0.1               |
| PNETLab VM            | 0.12+               |
| Hệ điều hành máy chủ  | Ubuntu 20.04+        |

---

## 🚀 3. Cách cài đặt

### 3.1 Clone dự án
```bash
git clone git@github.com:SIC1740/ansible-network.git
cd ansible-network

