# Vista_BE
2024 캡스톤 디자인 백엔드 코드입니다.

코드 없이 데이터 분석 가능한 웹페이지입니다.

[BE](https://github.com/LlamaVista/LlamaVista/tree/BE)
[FE](https://github.com/LlamaVista/LlamaVista/tree/FE)
[ML](https://github.com/LlamaVista/LlamaVista/tree/ML)

[demo](https://youtu.be/Unw5NLc95Yw)


![demo (online-video-cutter (1)](https://github.com/user-attachments/assets/443706b4-d74b-4f77-a373-1b7dc2e9d321)


<img width="1281" alt="Screenshot 2024-06-10 at 11 59 57 AM" src="https://github.com/cshooon/Vista_BE/assets/113033780/e3993c2b-e3f9-4b8e-9e70-e6bb21b3f748">

### 데이터베이스

이 데이터베이스 스키마는 사용자와 채팅 기반 인터페이스를 통한 상호작용을 기록하고 관리하기 위한 구조를 나타냅니다. 주요 목적은 사용자의 요청에 따라 데이터 분석 및 시각화 서비스를 제공하는 것입니다.

- **사용자 데이터**
  - `name`: 사용자의 이름
  - `email`: 사용자의 이메일 주소
  - `hashed_password`: 사용자의 비밀번호 해시
  - `threads`: 채팅방 목록
    - `thread_id`: 스레드를 고유하게 식별하는 ID
    - `name`: 스레드에 연결된 파일의 이름
    - `file_name`: 파일 이름과 관련된 정보를 담고 있는 배열
    - `messages`: 스레드 내의 메시지 목록
      - `role`: 메시지를 보낸 주체 ('assistant' 또는 'user')
      - `text`: 메시지의 내용
      - `file_id`: 메시지와 관련된 파일의 ID 목록

### 데이터 분석 요청(Request) 처리

- **스레드(Thread) 기반 요청 관리**
  - 사용자가 데이터 분석을 요청할 때마다 해당 요청과 관련된 모든 대화가 개별 스레드로 구성되어 저장됩니다. 예를 들어, 사용자가 'cars.csv' 파일에 대한 분석을 요청할 경우, 'cars.csv'라는 이름의 스레드가 생성됩니다.
  - 이러한 스레드 기반 구조는 요청의 맥락을 유지하고, 분석 진행 상황을 명확하게 추적하기 위함입니다.

- **대화 기록 저장**
  - 사용자와의 모든 대화는 정의된 데이터베이스 스키마에 따라 저장됩니다.
  - 사용자는 언제든지 이전 대화를 확인할 수 있으며, 시스템은 지속적인 대화의 흐름을 유지하도록 설계되었습니다.

- **개인 정보 보안**
  - 사용자의 비밀번호는 해시된 형태로 저장되어 실제 비밀번호가 노출되지 않도록 설계됩니다.
  - 해싱 알고리즘을 통해 비밀번호를 일방향 암호화하여 저장하며, 데이터 유출 시에도 비밀번호를 안전하게 보호합니다.
  - 이메일을 통해 사용자는 비밀번호 재설정, 계정 확인 등의 주요 기능을 수행할 수 있습니다.

### FastAPI Endpoints

1. **회원가입 및 로그인**
   - `/user/register`: 사용자 등록
   - `/user/login`: 사용자 로그인
      <img width="819" alt="Screenshot 2024-06-10 at 11 54 37 AM" src="https://github.com/cshooon/Vista_BE/assets/113033780/2df44c96-aea1-4d57-aa4c-7786c52fd69a">

2. **채팅 및 데이터 분석**
   - `/create`: 파일과 채팅방 이름이 필요한 채팅방 생성
   - `/create_example`: 예시 파일로 채팅방 생성
   - `/chat`: 채팅방 아이디와 메시지가 필요한 채팅 수행
     <img width="807" alt="Screenshot 2024-06-10 at 11 54 42 AM" src="https://github.com/cshooon/Vista_BE/assets/113033780/0570a077-7363-480b-b815-cab375b544c8">
     
   - `/chat_list`: 모든 채팅 기록 반환 (메시지, 파일 ID 포함)
   - `/user_file`: 사용자가 제출한 파일 반환
   - `/file_list`: LLM이 생성한 파일(시각화 결과) 로컬에 저장
   - `/store`: LLM이 생성한 메시지를 데이터베이스에 업데이트
     <img width="807" alt="Screenshot 2024-06-10 at 11 54 47 AM" src="https://github.com/cshooon/Vista_BE/assets/113033780/187c7064-f6e9-4025-b9a0-0921e158d351">



### 소스코드 파일 구조


- `database`: 데이터베이스 관련 로직을 담은 모듈. `users.py`에

는 데이터베이스 스키마 구조가 정의되어 있습니다.
- `service`: 로그인 관련 로직을 처리하는 모듈. `fastapi_auth.py`는 일반 로그인, `google_auth.py`는 구글 로그인에 필요한 엔드포인트를 구현합니다.
- `settings`: 환경 변수(.env)를 로드하는 모듈.
- `vista`: 채팅 관련 로직을 처리하는 모듈. `chat.py`에서는 채팅방 생성 및 채팅 엔드포인트를 구현하고, `event_handler.py`에서는 스트리밍 방식으로 응답을 받는 로직을 구현합니다. `result.py`는 결과를 데이터베이스에 저장하는 로직을 구현합니다.
- `static`: 결과 파일(images) 또는 사용자가 제출한 파일을 보관하는 폴더입니다. `env`: API 키, 로그인 비밀키를 보관하며 `settings.py`를 통해 로드됩니다.

<img width="224" alt="Screenshot 2024-06-10 at 11 57 50 AM" src="https://github.com/cshooon/Vista_BE/assets/113033780/e62109c9-6b7e-4724-b9c0-2cf315a05869">
<img width="196" alt="Screenshot 2024-06-10 at 11 57 54 AM" src="https://github.com/cshooon/Vista_BE/assets/113033780/8b0b4dea-b01e-4636-b8b8-32e79911ae37">


#### 5.5 실행

- 기존 소스코드에서 "pip install -r requirements.txt"를 통해 가상환경에 의존 라이브러리를 설치한 후 "uvicorn main:app —reload —host 0.0.0.0 --port 8000"을 통해 실행합니다.
