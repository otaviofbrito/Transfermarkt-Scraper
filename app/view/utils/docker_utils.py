from python_on_whales import DockerClient

docker = DockerClient(compose_files=["docker-compose.yaml"])


def start_mysql_container():
  docker.compose.up(detach=True, services="mysql_db")


def start_scrapy_container():
  container = docker.compose.run(service="scrapy", detach=True)
  return container.id

def stop_scrapy_container(container_id):
  docker.container.stop(containers=container_id)

def stop_all_containers():
  docker.compose.down()