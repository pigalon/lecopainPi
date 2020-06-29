rm /home/ubuntu/backup-*
export date_backup=$(date +%F_%T | tr ':' '-')
echo $date_backup
docker exec -it postgres-lecopain pg_dump -Fc -U postgres lecopain > /home/ubuntu/backup-$date_backup
s3cmd put /home/ubuntu/backup-$date_backup s3://lecopain