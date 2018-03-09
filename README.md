Following are the steps to be followed in order accomplish the task of sorting on the virtual clusters using AWS cloud instances.

 NN
 ec2-54-152-0-85.compute-1.amazonaws.com
 DN1 
 ec2-34-201-116-73.compute-1.amazonaws.com
 DN2
 ec2-54-211-103-104.compute-1.amazonaws.com
 DN3
 ec2-52-23-195-185.compute-1.amazonaws.com
 
 scp ~/.ssh/my-hadoop-key.pem ~/.ssh/config datanode1:~/.ssh
 scp ~/.ssh/my-hadoop-key.pem ~/.ssh/config datanode2:~/.ssh
 scp ~/.ssh/my-hadoop-key.pem ~/.ssh/config datanode3:~/.ssh
 
 #generate key file on the namenode
 ssh-keygen -f ~/.ssh/ssh_rsa -t rsa -P ""	
 -f : file name which follows it
 -t : type of key which is rsa here
 -P : passphrase which is "" empty here
 
 #copy the content of the rsa.pub file into the authorised_key file
 cat ~/.ssh/ssh_rsa.pub >> ~/.ssh/authorized_keys
 
 #do the above for all the data nodes
 cat ~/.ssh/ssh_rsa.pub | ssh datanode1 'cat >> ~/.ssh/authorized_keys'
 
 
 
#launch all the four nodes
sudo apt-get update

#install java jdk. 7 doesn't work
sudo apt-get install openjdk-8-jdk

#confirm java version
java -version

#download hadoop from apache
wget http://apache.mirrors.tds.net/hadoop/common/hadoop-2.7.4/hadoop-2.7.4.tar.gz -P ~/Downloads

#decompress the hadoop tar file into the /usr/local folder
sudo tar zxvf ~/Downloads/hadoop-2.7.4.* -C /usr/local

#move files to hadoop form hadoop-2.7.4
sudo mv /usr/local/hadoop-* /usr/local/hadoop

#go to home/ubuntu/ edit .profile file

#set environment variables in all the nodes
export JAVA_HOME=/usr
export PATH=$PATH:$JAVA_HOME/bin
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin
export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop

#load variables
. ~/.profile

#hadoop configuration on all nodes
#$HADOOP_CONF_DIR/hadoop-env.sh change JAVA_HOMEexport 
JAVA_HOME=/usr

#NameNode configuration
#HADOOP_CONF_DIR/Core-site.xml change configuration element
#change the namenode_public_dns to your NameNode Public DNS
<congiuration>
	<property>
		<name>fs.defaultFS</name>
		<value>hdfs://namenode_public_dns:9000</value>
	</property>
</configuration>

#$HADOOP_CONF_DIR/yarn-site.xml change configuration element
#change the namenode_public_dns to your NameNode Public DNS 
<configuration>
	<property>
		<name>dfs.replication</name>
		<value>3</value>
	</property>
	<property>
		<name>dfs.namenode.name.dir</name>
		<value>file:///usr/local/hadoop/etc/hadoop_data/hdfs/namenode</value>
	</property>
</configuration>

#create a hadoop_data directory in the $HADOOP_HOME directory
sudo mkdir -p $HADOOP_HOME/hadoop_data/hdfs/namenode

#modify a file named masters in the $HADOOP_CONF_DIR directory
echo "namenode_hostname" | cat >> $HADOOP_CONF_DIR/masters

#add the host name to the file $HADOOP_CONF_DIR/masters
#for example ip-172.31.52.198
namenode_hostname

#remove any slaves file if exists
sudo rm $HADOOP_CONF_DIR/slaves

#modify the slaves file to add the slave file ips using their aliases
echo "datanode1" | cat >> $HADOOP_CONF_DIR/slaves
echo "datanode2" | cat >> $HADOOP_CONF_DIR/slaves
echo "datanode3" | cat >> $HADOOP_CONF_DIR/slaves

#datanode configuration

#modify each of the data node hdfs-site.xml file
<configuration>
	<property>
		<name>dfs.replication</name>
		<value>3</value>
	</property>
	<property>
		<name>dfs.datanode.name.dir</name>
		<value>file:///usr/local/hadoop/etc/hadoop_data/hdfs/datanode1</value>
	</property>
</configuration>

#copy this config file to the other datanodes
#execute these on the datanode which has the modified hdf-site.xml which is the datanode1 right now
scp $HADOOP_CONF_DIR/hdfs-site.xml datanode2:$HADOOP_CONF_DIR
scp $HADOOP_CONF_DIR/hdfs-site.xml datanode3:$HADOOP_CONF_DIR

#create data directory on each datanode
#run this command on all the three datanodes
sudo mkdir -p $HADOOP_HOME/hadoop_data/hdfs/datanode

#update the ownership of the $HADOOP_HOME directory to ubuntu in all the datanodes
sudo chown -R ubuntu $HADOOP_HOME

##Starting up the hadoop cluster
#format the HDFS
hdfs namenode -format

#start eh DFS service
$HADOOP_HOME/sbin/start-dfs.sh

##Browse the HDFS in your web browser
#change namenode_public_dns to your NameNode public DNS
namenode_public_dns:50070

##start YARN on NameNode
$HADOOP_HOME/sbin/start-yarn.sh
$HADOOP_HOME/sbin/mr-jobhistory-daemon.sh start historyserver

##Run JPS on NameNode
jps

##Run JPS on datanodes
jps

#Testing the HDFS
#create a file
echo "This will be first distributed and fault tolerant data set\!" | cat >> my_file.txt

#list the hdfs files
hdfs dfs -ls /

#make a directory name user
hdfs dfs -mkdir /user

#copy the created file a few times
hdfs dfs -copyFromLocal ~/my_file.txt /user
hdfs dfs -copyFromLocal ~/my_file.txt /user/my_file2.txt
hdfs dfs -copyFromLocal ~/my_file.txt /user/my_file3.txt

#list the files in the new directory
hdfs dfs -ls /user

#remove the files with a name starting wiht my_file
hdfs dfs -rm /user/my_file*

#remove the new directory
hdfs dfs -rmdir /user

to be written into the hosts file int he /etc/hosts directory
