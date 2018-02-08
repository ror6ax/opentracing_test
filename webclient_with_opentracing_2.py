import requests
import time
from opentracing_instrumentation.client_hooks import install_all_patches
from jaeger_client import Config

config = Config(config={'sampler':{'type': 'const','param': 1},'logging': True},service_name="jaeger_opentracing_example2")
tracer = config.initialize_tracer()

install_all_patches()

url = 'http://localhost:4999/log2'

r = requests.get(url)

time.sleep(2)
tracer.close()