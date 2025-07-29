import click

from . import Foundry


@click.command()
@click.option('-m', '--machine', help='machine id')
@click.option('-a', '--app', help='app name')
@click.option('-f', '--features', help='feature list')
@click.option('-l', '--license', help='license key')
@click.option('-e', '--encrypt', help='encrypt key')
@click.option('-l', '--lifespan', default=86400, help='left span')
def main(machine: str, app: str, features: str, license: str, encrypt: str, lifespan: int):
    foundry = Foundry(app_name=app, license_key=license, encrypt_key=encrypt)
    if license is None:
        with open('license_key.pem', 'wb') as f:
            f.write(foundry.license_key)
    features = features.split(',')
    license_data = foundry.generate(machine_id=machine, features=features, expire_secs=lifespan)
    print(license_data)
