# Golden Configuration Guideline

## Những phần bắt buộc
- hostname phải theo chuẩn: <Tên_Router>-LAB
- banner login, banner motd theo format **
- cấu hình NTP, SNMP location, AAA, logging buffered 16384
- line vty 0 4 login local transport input ssh
- service timestamps log datetime msec

## Những dòng *không* được giữ
- crypto key generate rsa
- ntp clock-period
- license udi
- uptime is ...
- *bất kỳ* timestamp hoặc giá trị thay đổi theo thời gian
