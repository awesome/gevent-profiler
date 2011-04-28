import gevent_profiler


class GeventProfilerMiddleware(object):

	def __init__(self, app):
		self.app = app

	def __call__(self, environ, start_response):
		response_body = []

		def catching_start_response(status, headers):
			start_response(status, headers)
			return response_body.append

		def runapp():
			appiter = self.app(environ, catching_start_response)
			response_body.extend(appiter)
			if hasattr(appiter, 'close'):
				appiter.close()

		gevent_profiler.profile(runapp)
		body = ''.join(response_body)
		return [body]


