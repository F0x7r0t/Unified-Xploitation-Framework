#!/bin/sh
echo "Test"
#apt-get install posrgresql
mkdir -p ../Database/data
chown -R postgres:postgres ../Database/data
sudo -i -u postgres
initdb -D ../Database/data
createuser postgreuser1
createdb uxf -U postgreuser1
exit
service start postgresql

