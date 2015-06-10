export ORIGPASSWD=$(cat /etc/passwd | grep synda)
export ORIG_UID=$(echo $ORIGPASSWD | cut -f3 -d:)
export ORIG_GID=$(echo $ORIGPASSWD | cut -f4 -d:)

export UID=${UID:=$ORIG_UID}
export GID=${GID:=$ORIG_GID}

ORIG_HOME=$(echo $ORIGPASSWD | cut -f6 -d:)

sed -i -e "s/:$ORIG_UID:$ORIG_GID:/:$UID:$GID:/" /etc/passwd
sed -i -e "s/synda:x:$ORIG_GID:/synda:x:$GID:/" /etc/group

chown -R ${UID}:${GID} ${ORIG_HOME}

exec su - synda

