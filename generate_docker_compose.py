import argparse

def set_server_service(config_file):
    config_file.write("  server:\n    container_name: server\n")
    config_file.write("    image: server:latest\n    entrypoint: python3 /main.py\n")
    config_file.write("    environment:\n      - PYTHONUNBUFFERED=1\n      - LOGGING_LEVEL=DEBUG\n")
    config_file.write("    networks:\n      - testing_net\n\n")

def set_client_service(config_file, id):
    config_file.write("  client" + str(id) + ":\n    container_name: client" + str(id) + "\n")
    config_file.write("    image: client:latest\n    entrypoint: /client\n")
    config_file.write("    environment:\n      - CLI_ID=" + str(id) + "\n")
    config_file.write("      - CLI_LOG_LEVEL=DEBUG\n    networks:\n")
    config_file.write("      - testing_net\n    depends_on:\n      - server\n\n")

# Leemos la cantidad de clientes a crear.
parser = argparse.ArgumentParser()
parser.add_argument("--clients", type=int, default=1)
args = parser.parse_args()
clients_quantity = args.clients

# Generamos el DockerCompose con la cantidad de clientes especificada.
docker_file = open("docker-compose-dev.yaml", "w")
docker_file.write("version: '3.9'\nname: tp0\nservices:\n")
set_server_service(docker_file)
for i in range(1, clients_quantity + 1):
    set_client_service(docker_file, i)
docker_file.write("networks:\n  testing_net:\n    ipam:\n")
docker_file.write("      driver: default\n      config:\n        - subnet: 172.25.125.0/24\n")
docker_file.close()