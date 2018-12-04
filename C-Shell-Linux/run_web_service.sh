#!/bin/sh 

#
# uwsgi     This script starts and stops the web server
#
# chkconfig: 345 99 01
# description: uwsgi is a network management system for the web server
# processname: uwsgi

# May be invoked directly by a system administrator. Do not allow the user's 
# environment to change the behavior of this script.

. /etc/rc.d/init.d/functions

# NOTE:
# when calling through service uwsgi (status|start|stop|restart)
# the uwsgi is expected to softlink to /etc/init.d/uwsgi
# so we need get the realpath before get the name for directory
ROOT_DIR=$(dirname $(readlink -e $0))


export HOME=$ROOT_DIR
export BASEDIR=$ROOT_DIR
export ORCHENV_DIR=$ROOT_DIR/../env
export ORCHBIN_DIR=$ORCHENV_DIR/bin

. $BASEDIR/../env/bin/activate

UWSGI=$ORCHBIN_DIR/uwsgi
UWSGI_CONFIG=$BASEDIR/uwsgi.ini
NGINX=/sbin/nginx
REDIS=/bin/redis-server
NODEJS=/bin/node

prepare_env() {
  echo "10152 65535" > /proc/sys/net/ipv4/ip_local_port_range
  sysctl -w fs.file-max=128000
  sysctl -w net.ipv4.tcp_keepalive_time=300
  sysctl -w net.ipv4.tcp_max_syn_backlog=2500
  sysctl -w net.core.netdev_max_backlog=2500
  sysctl -w net.core.somaxconn=65535

  ulimit -n 10240
}

start() {
  prepare_env >/dev/null

  ret=0
  RETVAL=0

  # start redis
  echo -n "Starting redis server: "
  result="$(systemctl status redis)"
  ret=$?
  if [ $ret -ne 0 ]; then
    result="$(systemctl start redis)"
    ret=$?

    if [ $ret -ne 0 ]; then
      failure
      RETVAL=$ret
    else
      success
    fi
  else
    success
  fi
  echo

  # start nodejs server
  # TODO: we need find some safe way to avoid nodejs failure
  echo -n "Starting websocket server: "
  daemon nohup $NODEJS $BASEDIR/socketio/server.js 2>/dev/null >$BASEDIR/socketio.log &
  success
  echo

  # start uwsgi
  echo -n "Starting uwsgi server: "
  daemon $UWSGI -i $UWSGI_CONFIG >/dev/null 2>&1 && success || failure
  ret=$?
  success
  if [ $ret != 0 ]; then
    RETVAL=$ret
  fi
  echo

  # start nginx
  echo -n "Starting nginx server: "
  result="$(systemctl status nginx)"
  ret=$?
  if [ $ret -ne 0 ]; then
    result="$(systemctl start nginx)"
    ret=$?
    if [ $ret -ne 0 ]; then
      failure
      RETVAL=$ret
    else
      success
    fi
  else
    success
  fi
  echo

  return $RETVAL
}

stop() {
  ret=0
  RETVAL=0

  echo -n "Stopping nginx server"
  result="$(systemctl status nginx)"
  ret=$?
  if [ $ret -eq 0 ]; then
    result="$(systemctl stop nginx)"
    ret=$?

    if [ $ret -ne 0 ]; then
        failure
        RETVAL=$ret
    else
      success
    fi
  else
    failure
  fi
  echo

  echo -n "Stopping uwsgi server"
  if [ -n "`pidofproc $UWSGI`" ]; then
    killproc $UWSGI -KILL && success || failure
    ret=$?

    for i in `seq 1 10`; do
      netstat -lnt | grep -q "127.0.0.1:8080\W"
      if [ $? = 0 ]; then
        sleep 1 
      else
        break
      fi
    done

    if [ $ret != 0 ]; then
        RETVAL=$ret
    fi
  else
    failure
  fi 
  echo

  echo -n "Stopping websocket server"
  if [ -n "`pidofproc $NODEJS`" ]; then
    killproc $NODEJS -KILL && success || failure
    ret=$?

    for i in `seq 1 10`; do
      netstat -lnt | grep -q "127.0.0.1:8080\W"
      if [ $? = 0 ]; then
        sleep 1
      else
        break
      fi
    done

    if [ $ret != 0 ]; then
      RETVAL=$ret
    fi
  else
    failure
  fi
  echo

  echo -n "Stopping redis server"
  result="$(systemctl status redis)"
  ret=$?
  if [ $ret -eq 0 ]; then
    result="$(systemctl stop redis)"
    ret=$?

    if [ $ret -eq 0 ]; then
      success
    else
      RETVAL=$ret
      failure
    fi 
  else
    failure
  fi
  echo

  return $RETVAL
}

case "$1" in
  start)
    start
    RETVAL=$?
    ;;
  stop)
    stop
    RETVAL=$?
    ;;
  restart)
    stop
    start
    RETVAL=$?
    ;;
  status)
    status $NGINX
    if [ $? -ne 0 ]; then
      RETVAL=1
    fi

    status $NODEJS
    if [ $? -ne 0 ]; then
      RETVAL=1
    fi

    status $UWSGI
    if [ $? -ne 0 ]; then
      RETVAL=1
    fi

    status $REDIS
    if [ $? -ne 0 ]; then
      RETVAL=1
    fi
    ;;
  *)
    echo $"Usage: $0 {start|stop|status|restart}"
    RETVAL=2
    ;;
esac

exit $RETVAL
