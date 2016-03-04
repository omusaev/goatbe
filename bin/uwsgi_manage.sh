#!/bin/bash

# These variables may be overwritten from environment using
# `VIRTUALENV=<my_venv> UWSGI_CONFIG=<my_config> <...> uwsgi_manage.sh start`
# http://stackoverflow.com/a/4609718/410556


: ${PATH_TO_THE_ROOT:=/home/goat}
: ${VIRTUALENV:=${PATH_TO_THE_ROOT}/goat/venv}
: ${PYTHON:=${VIRTUALENV}/bin/python}

: ${APP_PATH:=${PATH_TO_THE_ROOT}/goat/app/}
: ${APP_PY:=${APP_PATH}app.py}

: ${UWSGI:=${VIRTUALENV}/bin/uwsgi}
: ${UWSGI_CONFIG:=${PATH_TO_THE_ROOT}/goat/wsgi/uwsgi.conf}
: ${UWSGI_PIDFILE:=${PATH_TO_THE_ROOT}/run/uwsgi.pid}

PID=`cat ${UWSGI_PIDFILE}`
#if [[ $(echo 'import constants'|$PYTHON $APP_PY shell > /dev/null 2>&1)$? != 0 ]]; then
#    echo "ALERT"
#    echo "constants.py seems to be broken, check it using"
#    echo "now exiting..."
#    exit
#fi

function start {
    if [ ! -f /proc/`cat $UWSGI_PIDFILE 2>/dev/null`/exe ]; then
        echo 'Starting uWSGI'
        $UWSGI --ini $UWSGI_CONFIG
        for i in `seq 30`;
        do
          sleep 1
          if [ ! -f /proc/`cat $UWSGI_PIDFILE 2>/dev/null`/status ]; then
            echo -n '.'
          else
            echo 'Started'
            break
          fi
        done
        if [ ! -f /proc/`cat $UWSGI_PIDFILE 2>/dev/null`/status ]; then                                                                                                                                          
            echo 'Can`t start uWSGI.'
            exit 1
        fi
      echo ''
      echo 'uWSGI started'
    else
        echo 'uWSGI ALREADY RUNNING'
    fi

}

function stop {
    if [ ! -f /proc/$PID/exe ]; then
        echo 'uWSGI ALREADY STOPPED'
    else
        echo 'Stopping uWSGI'
        $UWSGI --stop $UWSGI_PIDFILE
        for i in `seq 30`;
        do
          sleep 1
          if [ -f /proc/$PID/status ]; then
            echo -n '.'
          else
            echo 'Exited'
            break
          fi
        done
        if [ -f /proc/$PID/status ]; then                                                                                                                                          
            echo 'Can`t stop. Killing.'
            kill -9 $PID
        fi
        echo 'uWSGI STOPPED'
    fi

}
case "$1" in
        status)
            if [ ! -f /proc/$PID/exe ]; then
                echo 'uWSGI IS NOT RUNNING'
            else
                echo 'uWSGI IS RUNNING'
            fi

            ;;
        reload)
            if [ ! -f /proc/$PID/exe ]; then
                $UWSGI --ini $UWSGI_CONFIG
                echo 'uWSGI WAS NOT RUNNING'
            fi
            $UWSGI --reload $UWSGI_PIDFILE
            echo 'uWSGI RELOADED'
            ;;
        restart)
            echo 'Restarting uWSGI'
            stop
            start
            ;;
        stop)
            stop            
            ;;
        start)
            start
            ;;
         
        *)
            echo $"Usage: $0 {start|stop|reload|status}"
            exit 1
 
esac
