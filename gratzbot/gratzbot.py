import telebot
import cherrypy
import config
from misc import bot


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                'content-type' in cherrypy.request.headers and \
                cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            realip = cherrypy.request.headers.get('X-Real-Ip', '')
            if '91.108.6' in realip or '91.108.4' in realip or '149.154.160' in realip:
                update = telebot.types.Update.de_json(json_string)
                bot.process_new_updates([update])
                return ''
            else:
                raise cherrypy.HTTPError(403)
        else:
            return "What?"
            # raise cherrypy.HTTPError(403)


cherrypy.config.update(config.cherrypy_conf)
cherrypy.quickstart(WebhookServer(), config.WEBHOOK_URL_PATH, {'/': {}})
