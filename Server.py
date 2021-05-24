import json
import tornado.web
import itertools

class LogHandler(tornado.web.RequestHandler):

    def post(self):
        message =[]
        request = tornado.escape.json_decode(self.request.body)
        total_size = 0
        offset = int(request['offset'])
        next_offset = offset + 10
        code = str(self._status_code)
        try:
            with open('log.jsonl', 'r') as f:
                for size in f:
                    total_size += 1
                f.seek(0)
                if next_offset >= total_size:
                    next_offset = total_size

                for line in itertools.islice(f, offset, next_offset):
                    message.append(json.loads(line))

                response = json.dumps([{'ok': True, 'next_offset': next_offset,
                                   "total_size": total_size,
                                   "messages": message}], sort_keys = True,
                                    indent=4)
                self.finish(response)
        except IOError:
            message = 'file was not found'
            response = json.dumps({'ok': False,'reason': message},
                                  sort_keys = True, indent=4)
            self.set_status(200)
            self.finish(response)
        except:
            message = 'oops something went wrong'
            response = json.dumps({'ok': False, 'reason': message},
                                   sort_keys = True, indent=4)
            self.set_status(200)
            self.finish(response)
        print (response)


def make_app():
    return tornado.web.Application([
        (r"/read_log", LogHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
