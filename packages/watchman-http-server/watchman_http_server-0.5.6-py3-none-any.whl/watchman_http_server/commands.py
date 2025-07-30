import os
import sys
import click
import subprocess
import logging
import uvicorn
import psutil
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import set_key, load_dotenv

from watchman_http_server.main import create_env_file


class WatchmanCLI(click.Group):
    def resolve_command(self, ctx, args):
        if not args and not ctx.protected_args:
            args = ['default']
        return super(WatchmanCLI, self).resolve_command(ctx, args)


@click.command(cls=WatchmanCLI)
def cli():
    pass


@cli.command(name='runserver')
@click.option('--port', default=8001, help="Port sur lequel démarrer le serveur (par défaut : 8001)", type=int,
              required=True)
@click.option('--api-key', help="Clé API pour accéder au serveur.", type=str, required=True)
@click.option('--ip', help="Adresse(s) IP autorisée(s) à accéder au serveur.", type=str, required=False)
@click.option('-d', '--detach', is_flag=True, help="Exécuter en arrière-plan.")
def runserver(port, api_key, ip, detach):
    # Chemin du fichier .env
    config_dir = os.path.join(os.getcwd(), 'watchman_http_server', 'config')
    os.makedirs(config_dir, exist_ok=True)
    dotenv_path = os.path.join(config_dir, '.env')

    # Assurer que la clé API est définie
    if api_key:
        create_env_file(api_key)
    else:
        click.echo("Erreur : la clé API doit être fournie.")
        sys.exit(1)

    # Étape 1 : Lire les IPs existantes avant mise à jour
    existing_ips = [ip.strip() for ip in os.getenv("ALLOWED_IPS", "").split(",") if ip.strip()]

    # Étape 2 : Mise à jour des IPs autorisées
    if ip:
        ip_list = [addr.strip() for addr in ip.split(",") if addr.strip()]
        for new_ip in ip_list:
            if new_ip not in existing_ips:
                existing_ips.append(new_ip)

        set_key(dotenv_path, "ENABLE_IP_FILTERING", "true")
        set_key(dotenv_path, "ALLOWED_IPS", ",".join(existing_ips))
    else:
        set_key(dotenv_path, "ENABLE_IP_FILTERING", "false")
        print("🔓 Filtrage IP désactivé. 💡 Vous pouvez spécifier des IPs avec l'option --ip pour plus de sécurité.")

    # ✅ Étape 3 : RECHARGER les variables .env après mise à jour
    load_dotenv(dotenv_path, override=True)

    # Configuration des logs
    # file_path = "watchman_http_server/logs/logs.log"
    # directory = os.path.dirname(file_path)
    # os.makedirs(directory, exist_ok=True)
    # log_file = file_path
    # logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    if detach:
        log_file = os.path.expanduser("~/watchman_http_server.log")
        with open(log_file, "w") as f:
            subprocess.Popen(
                ["python", "-m", "uvicorn", "watchman_http_server.main:app", "--host", "0.0.0.0", "--port", str(port)],
                stdout=f, stderr=f, close_fds=True
            )
        print(f"✅ Serveur lancé en arrière-plan (logs: {log_file})")
    else:
        logging.info(f"Starting Watchman HTTP Server on port {port}...")
        uvicorn.run("watchman_http_server.main:app", host="0.0.0.0", port=port, log_level="info")


@cli.command(name="stopserver")
def stopserver():
    """Arrêter le serveur Watchman HTTP tournant en arrière-plan."""
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        if proc.info['cmdline'] and "uvicorn" in " ".join(proc.info['cmdline']):
            print(f"🔴 Arrêt du serveur (PID: {proc.info['pid']})")
            os.kill(proc.info['pid'], 9)  # Signal 9 = kill immédiat
            break
    else:
        print("⚠️ Aucun serveur Watchman HTTP trouvé en cours d'exécution.")


# Assurez-vous que vous avez une configuration de logging correcte
logging.basicConfig(level=logging.INFO)


# @cli.command(name='schedule')
# @click.option('--hour', type=str, required=True, help="L'heure à laquelle démarrer le serveur (0-23).")
# @click.option('--minute', type=str, required=True, help="La minute à laquelle démarrer le serveur (0-59).")
# @click.option('--day', type=str, required=False, default="*", help="Jour du mois (1-31), * pour chaque jour.")
# @click.option('--month', type=str, required=False, default="*", help="Mois (1-12), * pour chaque mois.")
# @click.option('--port', type=str, default=8001, help="Port sur lequel démarrer le serveur (par défaut : 8001)")
# @click.option('--api-key', type=str, required=True, help="Clé API pour accéder au serveur.")
# @click.option('-d', 'detach', is_flag=True, help="Exécuter en arrière-plan.")
# def schedule_task(hour, minute, day, month, port, api_key, detach):
#     """Planifier une tâche pour démarrer le serveur à un moment précis"""
#
#     # Configurer l'environnement
#     create_env_file(api_key)
#
#     # Configurer le planificateur
#     scheduler = BackgroundScheduler()
#     trigger = CronTrigger(hour=hour, minute=minute, day=day, month=month)
#
#     # Configuration des logs
#     file_path = "watchman_http_server/logs/logs.log"
#     directory = os.path.dirname(file_path)
#     os.makedirs(directory, exist_ok=True)
#     log_file = file_path
#     logging.basicConfig(
#         filename=log_file,
#         level=logging.INFO,
#         format="%(asctime)s - %(levelname)s - %(message)s",
#         encoding="utf-8"
#     )
#
#     def runserver_on_schedule():
#         # log_file = os.path.expanduser("watchman_http_server/logs/logs.log")
#         logging.info(f"🔄 Tâche exécutée à {hour}:{minute} (journée: {day}, mois: {month})")
#
#         try:
#             with open(log_file, "w") as f:
#                 subprocess.Popen(
#                     ["python", "-m", "uvicorn", "watchman_http_server.commands:app", "--host", "0.0.0.0", "--port",
#                      str(port)],
#                     stdout=f, stderr=f, close_fds=True
#                 )
#             logging.info(f"✅ Serveur démarré (logs: {log_file})")
#         except Exception as e:
#             logging.error(f"❌ Erreur lors du démarrage du serveur: {e}")
#
#     scheduler.add_job(runserver_on_schedule, trigger=trigger, name="runserver_on_schedule")
#
#     if detach:
#         # log_file = os.path.expanduser("~/watchman_http_server.log")
#         logging.info("🛠 Démarrage du planificateur en arrière-plan...")
#
#         subprocess.Popen(
#             ["watchman-http-server", "schedule",
#              "--hour", hour, "--minute", minute,
#              "--day", day, "--month", month,
#              "--port", port, "--api-key", api_key],
#             stdout=open(log_file, "w"),
#             stderr=subprocess.STDOUT,
#             close_fds=True
#         )
#
#         logging.info(f"✅ Serveur planifié en arrière-plan (logs: {log_file})")
#     else:
#         logging.info("🟢 Planificateur en cours d'exécution...")
#         scheduler.start()
#         logging.info(f"✅ Tâche planifiée pour {hour}:{minute} (Journée: {day}, Mois: {month})")
#
#         try:
#             while True:
#                 time.sleep(1)
#         except (KeyboardInterrupt, SystemExit):
#             scheduler.shutdown()
#             logging.info("🛑 Planificateur arrêté.")


def validate_cron_field(ctx, param, value):
    if value != "*" and not value.isdigit():
        raise click.BadParameter(f"{param.name} doit être '*' ou un entier.")
    return value


@cli.command(name='schedule')
@click.option('--hour', type=str, callback=validate_cron_field, required=True, help="Heure (0-23) ou '*'.")
@click.option('--minute', type=str, callback=validate_cron_field, required=True, help="Minute (0-59) ou '*'.")
@click.option('--day', type=str, callback=validate_cron_field, required=False, default="*", help="Jour du mois (1-31) "
                                                                                                 "ou '*'.")
@click.option('--month', type=str, callback=validate_cron_field, required=False, default="*", help="Mois (1-12) ou '*'.")
@click.option('--port', type=str, default="8001", help="Port sur lequel démarrer le serveur (par défaut : 8001)")
@click.option('--api-key', type=str, required=True, help="Clé API pour accéder au serveur.")
@click.option('-d', 'detach', is_flag=True, help="Exécuter en arrière-plan.")
def schedule_task(hour, minute, day, month, port, api_key, detach):
    """Planifier une tâche pour démarrer le serveur à un moment précis"""

    # Configurer l'environnement
    create_env_file(api_key)

    # Configuration des logs
    log_dir = "watchman_http_server/logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "logs.log")

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"
    )

    # Protection contre récursion
    if detach and os.getenv("WATCHMAN_DETACHED") != "1":
        logging.info("🛠 Lancement du planificateur en arrière-plan...")
        new_env = os.environ.copy()
        new_env["WATCHMAN_DETACHED"] = "1"

        subprocess.Popen(
            ["watchman-http-server",
             "schedule",
             "--hour", hour, "--minute", minute,
             "--day", day, "--month", month,
             "--port", port, "--api-key", api_key],
            stdout=open(log_file, "w"),
            stderr=subprocess.STDOUT,
            env=new_env,
            close_fds=True
        )

        logging.info(f"✅ Planificateur détaché (logs: {log_file})")
        return

    # Démarrage du planificateur
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(hour=hour, minute=minute, day=day, month=month)

    def runserver_on_schedule():
        logging.info(f"🔄 Tâche exécutée à {hour}:{minute} (jour: {day}, mois: {month})")
        try:
            with open(log_file, "a") as f:
                subprocess.Popen(
                    [sys.executable, "-m", "uvicorn",
                     "watchman_http_server.commands:app",
                     "--host", "0.0.0.0", "--port", str(port)],
                    stdout=f, stderr=f, close_fds=True
                )
            logging.info(f"✅ Serveur démarré (port {port})")
        except Exception as e:
            logging.error(f"❌ Erreur lors du démarrage du serveur: {e}")

    scheduler.add_job(runserver_on_schedule, trigger=trigger, name="runserver_on_schedule")

    # PID file (optionnel)
    # with open(os.path.join(log_dir, "scheduler.pid"), "w") as f:
    #     f.write(str(os.getpid()))

    click.echo("🟢 Planificateur en cours d'exécution...")
    logging.info(f"✅ Tâche planifiée pour {hour}:{minute} (jour: {day}, mois: {month})")

    scheduler.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logging.info("🛑 Planificateur arrêté.")
