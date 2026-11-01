-- 예시 테이블 생성 코드이고, 추후 변경
-- 컨테이너 생성 후 아래 명령어 실행
-- docker compose exec -T db psql -U postgres -d novel_db < db/init.sql
-- "실행 중인 db 컨테이너의 novel_db 데이터베이스에 postgres 계정으로 접속해서, 내 컴퓨터에 있는 db/init.sql 파일의 SQL 문들을 싹 실행해라"


CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS chunks (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1024)   -- bge-m3는 1024차원
);