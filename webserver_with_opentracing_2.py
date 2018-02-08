import opentracing
import logging
import time
from jaeger_client import Config
from flask import Flask
from flask_opentracing import FlaskTracer
from opentracing_instrumentation.client_hooks import install_all_patches
import requests
from opentracing.propagation import Format
from flask import Flask, request
from opentracing.ext import tags
  

if __name__ == '__main__':
        app = Flask(__name__)
        
        #tracer = init_tracer('formatter') import from lib.tracer ???

        log_level = logging.DEBUG
        logging.getLogger('').handlers = []
        logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)
        config = Config(config={'sampler':{'type': 'const','param': 1},'logging': True},service_name="jaeger_opentracing_example2")
        ls_tracer = config.initialize_tracer()
        tracer = FlaskTracer(ls_tracer)
        
        @app.route('/log2')
        @tracer.trace()
        def log_something2():

                span_ctx = ls_tracer.extract(Format.HTTP_HEADERS, request.headers)
                print(request.headers)
                span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}
                print(span_tags)
                child_span = ls_tracer.start_span("python webserver internal span of log2", child_of=span_ctx, tags=span_tags)
                child_span.finish()
                return "log2"

		
		
        app.run(debug=True, port=4999)
		