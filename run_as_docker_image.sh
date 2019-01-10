IMAGE_NAME="python-crawler-mat-orz"
URL="https://wiprodigital.com"
OUT_FILE="sitemap.json"

docker build -t $IMAGE_NAME .
docker run --mount type=bind,source="$(pwd)"/output,target=/output python-crawler $URL $OUT_FILE
docker rm $(docker ps -aq --no-trunc -f status=exited -f ancestor=$IMAGE_NAME)
