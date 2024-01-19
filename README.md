## 실행

```commandline
docker compose up
```

## 테스트

```sh
# 도커 컴포즈 실행 후
docker exec -it backend /bin/bash
python manage.py test app.tests.test_auth app.tests.test_product
```

## API Endpoint

### 유저

- 회원가입 : /user/signup(POST)
- 로그인 : /user/login(POST)
- 로그아웃 : /user/logout(POST)

### 상품

- 상품 생성 : /products - POST
- 상품 상세 조회 : /products/pk - GET
- 상품 삭제 : /products/pk - DELETE
- 상품 리스트 조회 : /products - GET
  - param : `search`
- 상품 수정 : /products/pk - PATCH
