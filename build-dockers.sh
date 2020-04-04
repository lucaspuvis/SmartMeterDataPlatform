docker build -t datahandler:latest -f components/data_handler/docker/Dockerfile .
docker tag datahandler:latest datahandler:staging