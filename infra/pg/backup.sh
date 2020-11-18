rm -f /home/ubuntu/backup-*
export date_backup=$(date +%F_%T | tr ':' '-')
echo $date_backup
docker exec -i postgres-lecopain bash <<EOF
rm -f dump.sql
pg_dump -Fc -U postgres lecopain > dump.sql
exit
EOF
docker cp postgres-lecopain:/dump.sql /home/ubuntu/backup-$date_backup
s3cmd put /home/ubuntu/backup-$date_backup s3://lecopain
