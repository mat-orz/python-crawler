IMAGE_NAME="python-crawler-mat-orz"
URL="https://wiprodigital.com"
OUT_FILE="sitemap.json"
TEST_BEFORE="Y"

docker build -t $IMAGE_NAME .
docker run --mount type=bind,source="$(pwd)"/output,target=/python-crawler/output $IMAGE_NAME $URL $OUT_FILE $TEST_BEFORE
docker rm $(docker ps -aq --no-trunc -f status=exited -f ancestor=$IMAGE_NAME)
