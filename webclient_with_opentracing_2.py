import requests
import sys
import time
from opentracing_instrumentation.request_context import get_current_span, span_in_context
from opentracing.ext import tags
from opentracing.propagation import Format
from opentracing_instrumentation.client_hooks import install_all_patches
from jaeger_client import Config


install_all_patches()

config = Config(config={'sampler':{'type': 'const','param': 1},'logging': True},service_name="jaeger_opentracing_example2")
tracer = config.initialize_tracer()

url = 'http://localhost:4999/log2'

span = tracer.start_span('TestSpan')

span.set_tag(tags.HTTP_METHOD, 'GET') 
span.set_tag(tags.HTTP_URL, url)
span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT) 
headers = {}
tracer.inject(span, Format.HTTP_HEADERS, headers)
print(headers)
r = requests.get(url)
