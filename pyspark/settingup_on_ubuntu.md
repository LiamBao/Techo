### ***SETTING UP***

- install java8, python3.5, scala, pyspark, py4j, jupyter

```shell
sudo apt update

pip3 install pyspark py4j jupyter

```


add to .zshrc profile

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
# export SPARK_PATH=~/spark-1.6.0-bin-hadoop2.6 
# export PYSPARK_DRIVER_PYTHON="jupyter" 
# export PYSPARK_DRIVER_PYTHON_OPTS="notebook" 

# #For python 3, You have to add the line below or you will get an error
# # export PYSPARK_PYTHON=python3
# alias snotebook='$SPARK_PATH/bin/pyspark --master local[2]'
####<<<<<<<<<<<<<<<
```

> Notes: The PYSPARK_DRIVER_PYTHON parameter and the PYSPARK_DRIVER_PYTHON_OPTS parameter are used to launch the PySpark shell in Jupyter Notebook. The — master parameter is used for setting the master node address. Here we launch Spark locally on 2 cores for local testing.

then 

```shell
tar -zxvf hadoop-x.x.x.tar.gz
``` 

Now add export `HADOOP_HOME=~/hadoop-x.x.x` to your .zshrc. Open a new terminal and try again