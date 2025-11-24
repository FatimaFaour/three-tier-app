FROM postgres:16-alpine

ENV POSTGRES_DB=three_tier_db
ENV POSTGRES_USER=three_tier_user
ENV POSTGRES_PASSWORD=three_tier_password

COPY init.sql /docker-entrypoint-initdb.d/
