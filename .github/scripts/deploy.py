import requests
import logging
import sys
import os
from dataclasses import dataclass

# config for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



USERNAME = os.environ.get("PYTHON_ANYWHERE_USERNAME")
TOKEN = os.environ.get("PYTHON_ANYWHERE_TOKEN")
HOST = os.environ.get("PYTHON_ANYWHERE_HOST")
DOMAIN_NAME = os.environ.get("PYTHON_ANYWHERE_DOMAIN_NAME")


@dataclass
class Console:
    console_url: str
    user: str
    id: int
    name: str


def check_envs() -> None:
    """check if environment variables are set correctly"""
    if not USERNAME or not TOKEN or not HOST or not DOMAIN_NAME:
        logging.error("missing environment variable(s)")
        sys.exit(1)


def send_input(cmd: str, console_id: int) -> None:
    """send input to the console"""
    response = requests.post(
        f"https://{HOST}/api/v0/user/{USERNAME}/consoles/{console_id}/send_input/",
        headers={"Authorization": f"Token {TOKEN}"},
        json={"input": cmd}
    )

    if response.status_code != 200:
        logging.error(f"error sending input, status code: {response.status_code}")
        sys.exit(1)



def get_deployment_console(console_name: str = "deploy") -> Console:
    """get deployment console"""
    response = requests.get(
        f"https://{HOST}/api/v0/user/{USERNAME}/consoles/",
        headers={"Authorization": f"Token {TOKEN}"},
    )

    if response.status_code == 200:
        for console in response.json():
            if console["name"] == console_name:
                return Console(
                    console_url=console["console_url"],
                    user=console["user"],
                    id=console["id"],
                    name=console["name"],
                )
        logging.error(f"'{console_name}' console not found, you must create one first")
        sys.exit(1)
    else:
        logging.error(f"error fetching list of consoles, status code: {response.status_code}")
        sys.exit(1)


def reload() -> None:
    """reload app"""
    logging.info("reloading app...")
    response = requests.post(
        f"https://{HOST}/api/v0/user/{USERNAME}/webapps/{DOMAIN_NAME}/reload/",
        headers={"Authorization": f"Token {TOKEN}"},
    )

    if response.status_code != 200:
        logging.error(f"error reloading website, try reloading it manually, status code: {response.status_code}")
    else:
        logging.info("app reloaded!")


def deploy() -> None:
    logging.info("starting the deployment")
    console = get_deployment_console()
    steps = [
        "cd ~/2025.djangocon.africa",
        "git pull",
        "pip install -r requirements.txt",
        "npm install",
        "python manage.py migrate",
        "npm run tailwind",
        "python manage.py collectstatic --no-input",

        # return home
        "cd",
    ]

    for step in steps:
        logging.info(f"cmd: {step}")
        send_input(cmd=f"{step}\n", console_id=console.id)



def main() -> None:
    check_envs()
    deploy()
    # reload()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(e)


