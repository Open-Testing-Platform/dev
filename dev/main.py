import os
import json
import click
from . import template


@click.group()
def app():
    pass


@app.command()
@click.option(
    "-f",
    "--file",
    type=click.File("r"),
    required=True,
    help="JSON file for configuration",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    required=True,
    help="Output directory for generated repo",
)
def gw_gen(file, output):
    """
    Generate grpc gateway
    """
    if not os.path.isabs(output):
        output = os.path.join(os.getcwd(), output)
    if not os.path.exists(output):
        os.mkdir(output)

    config = json.load(file)
    for service_name in config:
        http_port = config[service_name]["http_port"]
        rpc_endpoint = config[service_name]["rpc_endpoint"]
        service_dir = os.path.join(output, service_name)
        os.mkdir(service_dir)

        dockerfile_path = os.path.join(service_dir, "Dockerfile")
        with open(dockerfile_path, "w") as fo:
            fo.write(template.dockerfile_go_gw.format(HTTP_PORT=http_port))

        main_path = os.path.join(service_dir, "main.go")
        with open(main_path, "w") as fo:
            fo.write(
                template.main_go_gw.format(
                    SERVICE_NAME=service_name,
                    HTTP_PORT=http_port,
                    RPC_ENDPOINT=rpc_endpoint,
                )
            )


if __name__ == "__main__":
    app()
