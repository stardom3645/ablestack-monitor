# mold db 비밀번호 생성방법
libvirt-exporter에서 mold db 비밀번호를 암호화 하는 방법을 설명합니다.

실행방법 예시
```
1. dnf -y install go
2. go run pw_encryption.go <비밀번호>
```

출력결과 예시
```
xd6L0cRe05Tg7ClcwealQ_pjkFnF9wEebux5
```
암호화된 비밀번호가 출력됨

적용방법
conf.json 설정 파일에 password 값을 변경하고 libvirt-exporter 서비스를 재시작하여 반영합니다.
```
vi conf.json

{
    "mold_db": {
        "serverhost":"ccvm",
        "port":"3306",
        "database": "cloud",
        "username": "cloud",
        "password": "xd6L0cRe05Tg7ClcwealQ_pjkFnF9wEebux5"
    }
}

변경 후

systemctl restart libvirt-exporter.service
```