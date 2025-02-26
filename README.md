# LlamaVista

**데이터 분석 자동화 서비스!**

<img width="800" alt="스크린샷 2025-01-03 오전 12 50 42" src="https://github.com/user-attachments/assets/cc8d23a2-07aa-46d6-92fb-7f520e2866b5" />


## 📖 Description

VISTA는 대규모 언어 모델(LLM)을 기반으로 한 데이터 분석 자동화 서비스입니다.

사용자가 제출한 파일을 인공지능이 분석하고 대화를 통해 인공지능과 상호작용하며 데이터 분석을 고도화해 나갈 수 있습니다.

노코드 형식의 프롬프트를 통해 코드작성 없이도 전문적인 데이터 분석이 가능합니다!

## ⭐ Main Feature
### 데이터 분석 기능
- csv, json, txt 파일의 데이터 분석 지원
- 분석 방향 제시
- 대화 전송시, 추가적인 자료 제출 가능
- 데이터 시각화 이미지 제공(그래프, 산점도 등)
- 스트리밍을 통한 실시간 응답 지원

### 회원가입 및 로그인 
- 회원가입
- 로그인
- google 로그인 (**DNS 사용 기간이 종료되어 현재 이용 불가능합니다**)

### 기타 기능
- 채팅 기록 저장
- 반응형 지원
- 분석 샘플 파일 제공
- 제출 파일 다운로드
- 로그아웃

## 💻 Getting Started

배포된 링크 🔗 로 접속!

### 회원가입 후 로그인 진행
- 구글 로그인은 DNS 서비스가 만료되어 현재 이용 불가능합니다
- 회원가입 시 중복체크 후 회원가입이 완료됩니다
<img width="800" alt="로그인" src="https://github.com/user-attachments/assets/c7668091-c8cf-4f8d-977d-7f10ceafca27">

### 분석할 파일 제출
- 분석을 원하시는 파일을 제출하여 채팅방을 생성하는 곳입니다
- 분석 파일은 json, csv, txt 파일만 가능합니다
- london_house, shopping_trends, iris 와 관련된 샘플 데이터로 분석을 진행해 볼 수 있습니다
<img width="800" alt="스크린샷 2025-01-03 오전 12 53 07" src="https://github.com/user-attachments/assets/a846a69f-8cee-418e-a808-1460db7829d7" />


### 데이터 분석 진행
- 대화 입력창을 통해 인공지능과 대화하며 다양한 형식으로 데이터 분석을 진행할 수 있습니다
- 데이터 분석을 통해 알게된 인사이트로 추가적인 파일을 채팅방에 제출하며 분석을 고도화해 나갈 수 있습니다
- 시각화 된 자료가 필요한 경우 생성할 수 있습니다
  
<img width="1510" alt="스크린샷 2025-01-03 오전 12 56 05" src="https://github.com/user-attachments/assets/922db4f4-0532-47b6-ad97-76b695236b08" />


## 🔧 Stack

### FE 
- **Language**: TypeScript
- **Library & Framework** : React, React-rocoil, React-Query, styled-components

### BE 
- **Language**: Python
- **Library & Framework** : Fastapi, Pymongo
- **Deploy**: AWS EC2

### ML 
- **Hardware & OS env**: DGX-Station(A100*8), Ubuntu 20.04, CUDA 11.8
- **Language**: Python
- **Library & Framework** : torch, transformers, accelerate, sentencepiece, langchain


## 👨‍💻 Role & Contribution

**Frontend** (👨🏻‍💻 [seoungJun](https://github.com/seo-seoungjun))

- 사용자 페이지 디자인(Figma) 및 프론트개발(React.js)
- 데이터베이스 스키마 설계
- API 설계

**BackEnd** (👨🏻‍💻 [cshoon](https://github.com/cshooon)) [code](https://github.com/LlamaVista/LlamaVista/tree/BE)

- 데이터베이스 스키마 설계
- API 설계
- REST API 개발
- 서버 배포 및 관리

**ML** (👨🏻‍💻 [sabin](https://github.com/sabin5105))

- 인공지능 설계 및 개발
- MLOps
- RESTApi 개발

