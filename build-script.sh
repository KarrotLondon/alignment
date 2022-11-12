docker build --tag registry.heroku.com/align-ment/web .
docker push registry.heroku.com/align-ment/web
heroku container:release web