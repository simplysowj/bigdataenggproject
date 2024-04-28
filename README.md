# bigdataenggproject
![Alt text](view.jpeg?raw=true "Title")



## Clean up
stop all containers
###### docker stop $(docker ps -a -q)
remove all containers
###### docker rm $(docker ps -a -q)
delete producer image
###### docker rmi <id>
delete web image
###### docker rmi <id>

## download code, data and run the containers
###### download spark 2.4.8 from https://archive.apache.org/dist/spark/
###### update the location of spark in compose file "/Users/mubarak/Documents/Demos/spark248"
###### download data
###### update the location of data in compose file "/Users/mubarak/Documents/Demos/data"
###### download code
###### cd FraudAnalytics
###### docker-compose up



## run producer (on port 9000)
###### curl --header "Content-Type: application/json" --request POST --data "{\\"Timestamp\\":\\"01-01-2023 08:00\\",\\"TransactionID\\":\\"TXN1127\\", \\"AccountID\\":\\"ACC4\\", \\"Amount\\":95071.92, \\"Merchant\\":\\"MerchantH\\", \\"TransactionType\\":\\"Purchase\\",\\"Location\\":\\"Tokyo\\"}" http://localhost:9000/add



## see messages in kafka
###### docker images ps
###### docker exec -it 1c31511ce206 bash
###### /* list all topics */
###### kafka-topics.sh --bootstrap-server localhost:9092 --list
###### /* read */
###### kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic my-topic -from-beginning
###### /* if you want to write directly */
###### kafka-console-producer.sh --broker-list localhost:9092 --topic my-topic
###### > {"transaction":"234"}
###### > {"transaction":"456"}
###### > ^c


## open zeppelin editor (on port 8080)
###### http://localhost:8080/

## Train the model
###### copy MLModelTrain.py code to the editor
###### train the model

## configure Spark interpeter
###### org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.8 

## in zeppelin editor install mysql connector 
###### %sh
###### pip install mysql-connector-python

## run Spark job
###### copy MLStreamJob.py code to the editor
###### run code

## check data in SQL
###### docker exec -it id /bin/bash
###### mysql -u[username] -p[password]
###### mysql -uroot -pabc
###### mysql> use FRAUDSDB;
###### mysql> select * from fraudtrans;

## see output in web App (on port 8000)
###### http://localhost:8000
###### configure llm key
###### run query "show all frauds"
