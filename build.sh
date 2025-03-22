docker_build() {
    docker run -d -p 80:80 fastapi-app
}

docker_run() {
    docker run -d -p 8000:8000 fastapi-app
}

run() {
    uvicorn main:app --host 0.0.0.0 --port 8000
}

# Extract the command (first argument)
# Shift arguments to remove the command, leaving only the arguments for the command
# Execute the command with the remaining arguments
COMMAND=$1
shift
$COMMAND "$@"