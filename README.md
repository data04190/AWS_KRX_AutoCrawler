# Capston_Design_Project

<br>

- AWS CLI 설치

```shell
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
$ unzip awscliv2.zip
$ sudo ./aws/install
```

- AWS EC2 인스턴스 내 파일을 S3 파일 업로드
```shell
$ aws s3 cp [source파일명] s3://[destination버킷명]/[destination파일명] 
```

- AWS EC2 인스턴스 내 파일을 S3 파일 다운로드
```
$ aws s3 cp s3://[source버킷명]/[source파일명] [destination파일명] 
```
