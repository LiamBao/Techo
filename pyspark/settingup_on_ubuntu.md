### ***SETTING UP***

- install java8, python3.5, scala, pyspark, py4j, jupyter 

```shell
#java
sudo apt-get update
sudo apt-get install default-jre
java -version
sudo apt-get install scala
scala -version

# python packages
pip3 install pyspark py4j jupyter

```

download spark zip,then 

```shell

sudo tar -zxvf hadoop-x.x.x.tar.gz
export SPARK_HOME='~/spark-2.1.0-bin-hadoop2.7'
export PATH=$SPARK_HOME:$PATH
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
export PYSPARK_DRIVER_PYTHON='jupyter'
export PYSPARK_DRIVER_PYTHON_OPTS="notebook"
export PYSPARK_PYTHON=python3

sudo chmod 777 '~/spark-2.1.0-bin-hadoop2.7' 
sudo chmod 777 '~/spark-2.1.0-bin-hadoop2.7/python'
sudo chmod 777 '~/spark-2.1.0-bin-hadoop2.7/python/pyspark'
```
cd to '~/spark-2.1.0-bin-hadoop2.7/python' ,cmd :
`jupyter notebook`

OR add to .zshrc profile

```shell

####>>>>>>>>>>>>>for ubuntu16.0.4
function snotebook () 
{
#Spark path (based on your computer)
SPARK_PATH=~/spark-2.0.0-bin-hadoop2.7

export PYSPARK_DRIVER_PYTHON="jupyter"
export PYSPARK_DRIVER_PYTHON_OPTS="notebook"

# For python 3 users, you have to add the line below or you will get an error 
#export PYSPARK_PYTHON=python3

$SPARK_PATH/bin/pyspark --master local[2]
}
####<<<<<<<<<<<<<<<

####>>>>>>>>>>>>>>>for MAC
export SPARK_PATH=~/spark-1.6.0-bin-hadoop2.6 
export PYSPARK_DRIVER_PYTHON="jupyter" 
export PYSPARK_DRIVER_PYTHON_OPTS="notebook" 

#For python 3, You have to add the line below or you will get an error
# export PYSPARK_PYTHON=python3
alias snotebook='$SPARK_PATH/bin/pyspark --master local[2]'
####<<<<<<<<<<<<<<<
```


> Notes: The PYSPARK_DRIVER_PYTHON parameter and the PYSPARK_DRIVER_PYTHON_OPTS parameter are used to launch the PySpark shell in Jupyter Notebook. The — master parameter is used for setting the master node address. Here we launch Spark locally on 2 cores for local testing.


Now add export `HADOOP_HOME=~/hadoop-x.x.x` to your .zshrc. Open a new terminal and try again


### Databricks: 
https://accounts.cloud.databricks.com/registration.html