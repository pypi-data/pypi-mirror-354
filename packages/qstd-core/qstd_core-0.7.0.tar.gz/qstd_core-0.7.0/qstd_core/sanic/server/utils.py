from qstd_async_tools import trace
from sanic import Request
from sanic.response import BaseHTTPResponse


def request_add_trace_id(_: Request):
    trace.add_trace_id()


def response_x_trace_header(request: Request, response: BaseHTTPResponse):
    response.headers['X-TRACE'] = ','.join(trace.get_trace_ids() or [])
