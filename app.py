from flask import Flask
from utils import register_app_blueprints, update_app_celery_config, initialize_celery, update_app_apispec_config,\
    initialize_apispec, register_apispec_methods, remove_options_from_apispec
from api import pc, get_cpu_history, get_ram_history, get_free_space, get_external_ip,\
    exchange, get_rates, node, get_logs, get_message_logs, get_uptime


app = Flask(__name__)
app = register_app_blueprints(
    app,
    [pc, exchange, node]
)

app = update_app_celery_config(app)
celery = initialize_celery(
    app
)

app = update_app_apispec_config(app)
apispec = initialize_apispec(app)
docs_methods = {
    'pc': [get_cpu_history, get_ram_history, get_free_space, get_external_ip],
    'exchange': [get_rates],
    'node': [get_logs, get_message_logs, get_uptime]
}
for blueprint, methods in docs_methods.items():
    apispec = register_apispec_methods(
        apispec,
        methods,
        blueprint
    )
apispec = remove_options_from_apispec(apispec)
