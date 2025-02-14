docker stop $(docker ps -a --filter "name=lba" -q) && docker rm $(docker ps -a --filter "name=lba" -q) && docker rmi $(docker images --filter=reference="*lba*" -q)
) && docker volume rm $(docker volume ls -q --filter name=lba)
