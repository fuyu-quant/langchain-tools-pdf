option=$1

if [ $option = up ]; then
    # Start container
    docker compose up -d
elif [ $option = force ]; then
    # Rebuild the docker image and start container
    docker compose up -d --force-recreate
elif [ $option = down ]; then
    # Stop container
    docker compose down -v
elif [ $option = rm ]; then
    # Stop the container and delete the image
    docker compose down -v --rmi all
else
    echo "Command is wrong"
fi