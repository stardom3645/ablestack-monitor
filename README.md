# Wall 모니터링 개발 및 구성 가이드
Wall 모니터링 개발 준비 및 ablestack-template ( scvm, ccvm 템플릿 ) 에 적용하는 방법을 제공합니다.

## 1. 개발환경 세팅
Wall을 개발하기 위한 os 및 소프트웨어 버전은 아래 표와 같습니다.

|구분|버전|
|--------------|--------------|
|운영체제|Centos 8.4|
|grafana|8.1.2|
|golang|1.16.6 (16 이상)|
|nodejs|16.6.1 (14 이상)|
|yarn|1.22.11|


### MacOS에 개발환경 구성 방법
~~~
1.	brew install git
2.	brew install go
3.	brew install nodejs ( 14 버전 이상 ) 
4.	node -v ( 버전 확인 )
5.	npm install -g yarn ( yarn 설치 )
6.	yarn -v ( 버전 확인 )
7.	git clonehttps://github.com/ablecloud-team/ablestack-wall.git ( 그라파나 소스다운로드 )
8.	cd ablestack-wall( 폴더로 이동 )
9.	git checkout ablestack-bronto ( branch 변경 )
10.	구성 완료
~~~

### Centos 8.4 VN에 개발환경 구성 방법
~~~
1.	dnf -y install git make gcc
2.	wget https://golang.org/dl/go1.16.6.linux-amd64.tar.gz
3.	tar -C /usr/local -xvf go1.16.6.linux-amd64.tar.gz
4.	vi ~/.bash_profile
5.	export GOPATH=$HOME/go
6.	export PATH=$PATH:$GOPATH/bin
7.	export PATH=$PATH:/usr/local/go/bin
8.	source ~/.bash_profile
9.	curl -sL https://rpm.nodesource.com/setup_16.x | sudo bash - (nodejs 최신버전 다운, 14이상)
10.	dnf -y install nodejs
11.	node -v ( 버전 확인 16.11 이상)
12.	npm install -g yarn
13.	yarn -v ( 버전 확인 1.22.17 이상)
14.	git clone https://github.com/ablecloud-team/ablestack-wall.git ( 그라파나 소스다운로드 )
15.	cd ablestack-wall( 폴더로 이동 )
16.	git checkout ablestack-bronto ( branch 변경 )
17.	구성 완료
~~~

## 2. 소스 빌드
Wall을 개발된 내용을 빌드 하는 방법은 아래와 같습니다. 

~~~
1. cd grafana (개발 폴더)
2. yarn install --pure-lockfile
3. yarn start
4. make build
5. make run ("too many open files 에러 발생하면 url을 참조하여 해결 https://github.com/grafana/grafana/blob/main/contribute/developer-guide.md#troubleshooting")
~~~

소스 수정 후 빌드하면 수정된 소스로 반영됨

## 3. Wall 소스 system vm (scvm, ccvm template)에 반영하기
Wall 개발 및 소스 빌드가 완료 되었다면 ablestack-template.qcow2에 반영해야 합니다. 
ablestack-template 가상머신을 구동 후 필요한 소스만 적용
Wall 개발 환경에서 개발 및 빌드가 완료된 소스를 ablestack-template에 복사 하기

### 아래 표는 ablestack-template 가상머신에 적용해야 할 폴더 및 파일 입니다.
|구분|1 뎁스|2 뎁스|
|---|---|---|
|/usr/share/ablestack/ablestack-wall/grafana|bin|grafana-cli|
|||grafana-server|
||conf||
||data||
||plugins-bundled||
||public||
||scripts||

### 빌드된 소스를 파일 grafana ablestack-template 가상머신에 붙여 넣기
~~~
1. scp -r /<개발 소스 경로>/bin root@< ablestack-template-vm-ip>:/usr/share/ablecloud/ablecloud-wall/grafana
2. scp -r /<개발 소스 경로>/bin/grafana-cli root@< ablestack-template-vm-ip>:/
3. scp -r /<개발 소스 경로>/conf root@< ablestack-template-vm-ip>:/usr/share/ablecloud/ablecloud-wall/grafana
4. scp -r /<개발 소스 경로>/data root@< ablestack-template-vm-ip>:/usr/share/ablecloud/ablecloud-wall/grafana
5. scp -r /<개발 소스 경로>/ plugins-bundled root@< ablestack-template-vm-ip>:/usr/share/ablecloud/ablecloud-wall/grafana
6. scp -r /<개발 소스 경로>/public root@< ablestack-template-vm-ip>:/usr/share/ablecloud/ablecloud-wall/grafana
7. scp -r /<개발 소스 경로>/scripts root@< ablestack-template-vm-ip>:/usr/share/ablecloud/ablecloud-wall/grafana
~~~

### ablestack-template 가상머신에 접속하여 실행파일 복사
~~~
1. cp /usr/share/ablestack/ablestack-wall/grafana/bin/grafana-cli /usr/sbin/
2. cp /usr/share/ablestack/ablestack-wall/grafana/bin/grafana-server /usr/sbin/
~~~

### ablestack-template 가상머신에 접속하여 필요한 플러그인 패널 추가
ablestack-template 가상머신의 /var/lib/grafana/plugins 경로에 grafana-clock-panel 및 grafana-image-renderer 폴더가 없을 경우 grafana-cli 명령어로 플러그인 패널 추가
~~~
1. grafana-cli plugins install grafana-clock-pane
2. grafana-cli plugins install grafana-image-renderer
~~~

## 4. wall 용 grafana.db 만드는 법
wall은 sqlite3 기반의 grafana.db를 사용하며 make build 명령을 통해 소스 빌드할 때 생성 됩니다. 개발 된 Wall 대시보드 템플릿 적용하고 ccvm 배포 시 곧 바로 사용 가능하도록 초기 상태의 grafana.db 파일을 생성하여 ablestack-template 가상머신에 반영해야 합니다. 

~~~
1. 기존 grafana.db 삭제 작업
2. rm -f <개발 폴더 경로>/gragana/data/grafana.db (db를 지워야 make build 할떄 새로 초기화 상태로 생성됨)
3. 초기상태 grafana.db 생성
4. make build
5. wall 웹 포탈에 접속후 로그인
6. 환경설정 > 데이터 소스 Wall, Glue, Mold 순서로 추가 (순서 중요함)
7. 템플릿 repository : https://github.com/ablecloud-team/ablestack-monitor.git 다운로드
8. wall-template 안의 admin 폴더의 7개 대시보드 임포트 적용
9. “Alert” 폴더 생성
10. wall-template 안의 alert 폴더의 4개 대시보드 임포트 적용
11. “1.종합대시보드” 즐겨찾기 후 환경설정 > 기본 설정 > 홈 대시보드 에서 기본페이지로 설정
12. 플레이리스트 “Default Playlist” 이름으로 인터벌은 30s로 “1.종합 대시보드”, “2. 호스트 종합 현황”, “6. 사용자 가상머신 종합현황” 등록
13. 조직 변경 Main Org.를 adminOrg로 변경
14. 조직 추가 viewerOrg 추가
15. 조직을 viewerOrg 변경하고 환경설정 > 데이터 소스에서 Wall 등록
16. wall-template 안의 user폴더의 1개 대시보드 임포트 적용
17. “가상머신 상세 현황” 즐겨찾기 후 환경설정 > 기본 설정 > 홈 대시보드 에서 기본페이지로 설정
18. Sqlite3 로 grafana.db 에 접근
19. grafana.db 불필요 데이터 수동 삭제 ( ex : login 정보 등 )
20. UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'user_auth_token';  (개발을 하기 위해 로그인 했던 정보 삭제)
21. select * FROM SQLITE_SEQUENCE where name = 'user_auth_token';
22. 작업 완료된 grafana.db 파일 gablestack-template 가상머신에 grafana.db, grafana_org.db 파일로 생성 복사
23. scp <개발 폴더 경로>/gragana/data/grafana.db /usr/share/ablestack/ablestack-wall/grafana/data/grafana_org.db 
~~~