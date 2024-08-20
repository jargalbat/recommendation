# mbook-recommendation


## Env
Install Ananconda
create environment named ResSys
Python 3.11.8
brew install --cask docker
conda install -c conda-forge scikit-surprise
conda install apscheduler
conda install pytz
conda install -c conda-forge sqlalchemy
conda install -c conda-forge pymysql
conda install -c conda-forge python-dotenv
conda install -c conda-forge mysql-connector-python

pip install apscheduler


## Terminal commands
conda deactivate
conda activate RecSys
conda info

docker build -t mbook_recommendation .
docker run -it --rm docker build -t mbook_recommendation .
docker run -d --name mbook_recommendation_container mbook_recommendation

docker ps -a
docker rm 26322265eb7bef2ef9e9c9b5720700b1f2b62a7bc986f112e9ebfcf3aa6d9919
docker run -d --name mbook_recommendation_container mbook_recommendation
docker run -d --name mbook_recommendation_container_v2 mbook_recommendation

docker stop $(docker ps -q)
docker rm $(docker ps -a -q)
docker stop $(docker ps -q) && docker rm $(docker ps -a -q)

# new commands
docker stop mbook_recommendation && docker rm mbook_recommendation && \
docker build -t mbook_recommendation:latest . && \
docker run -d --name mbook_recommendation -p 8000:8000 mbook_recommendation:latest && \
sleep 5 && \
docker logs mbook_recommendation
