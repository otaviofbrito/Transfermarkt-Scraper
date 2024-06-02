from python_on_whales import DockerClient

docker = DockerClient(compose_files=["../../../docker-compose.yaml"])


def start_mysql_container():
  docker.compose.up(detach=True, services="mysql_db")


def stop_all_containers():
  docker.compose.down()