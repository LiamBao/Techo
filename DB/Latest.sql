setup-ds.pl --silent\
 General.FullMachineName=`iok-oechestration.cisco.com`\
 General.SuiteSpotUserID=nobody\
 General.SuiteSpotGroup=nobody\
 slapd.ServerPort=389\
 slapd.ServerIdentifier=iok-orch\
 slapd.Suffix=dc=cisco,dc=com\
 slapd.RootDN="cn=Directory Manager"\
 slapd.RootDNPwd=cisco123
 
-- CONNECT TO MYSQL SERVER:
MYSQL -h host -u user -p;

-- CMD TO CLI TERMINAL
MYSQL;
QUIT;

-- INFO
SELECT VERSION(), CURRENT_DATE;

SELECT SIN(PI()/4), (1+1)*4;

SELECT VERSION(); SELECT NOW();

-- CREATE DATABASE AND TABLES
SHOW DATABASES;

