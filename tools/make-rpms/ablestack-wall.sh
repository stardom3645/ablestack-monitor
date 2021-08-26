# Copyright (c) 2021 ABLECLOUD Co. Ltd
# 이 파일은 rpmbuild 이후 실행되는 스크립트 파일입니다.
# 최초 작성일 : 2021. 08. 26


#!/bin/sh

# 함수명 : conf
# PATH 정의
conf(){
ABLESTACK_PATH="/usr/share/ablestack"
RPM_PATH="$ABLESTACK_PATH/ablestack-wall/tools/makerpm/rpmbuild"
return
}

# 함수명 : settingFile
# 파일 삭제 및 권한 설정 함수
settingFile() {
echo "====================Start of All process"
echo "1. setting Files"
rm -rf $RPM_PATH
chmod 644 $ABLESTACK_PATH/ablestack-wall/*
return
}


# 함수명 : default
# 프로세스 종료
default(){
settingFile
startCockpit
echo "====================End of All process"
pkill -9 -f /usr/share/ablestack/ablestack-wall/tools/make-rpm/ablestack-wall.sh
}

# 스크립트 실행
productName=$1
echo $productName
if [ $productName="default" ]; then
 conf
 default
fi