import gevent
from gevent import socket
import Tkinter as tk

class SockLoop(object):
    def __init__(self, callback):
        self.callback = callback

    def __call__(self, sock, client):
        while 1:
            mes = sock.recv(256)
            ret = self.callback(client, mes)
            if ret is not None:
                sock.send(ret)

def socket_server(port, callback):
    ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    ssock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssock.bind(('', port))
    ssock.listen(5)

    while 1:
        sock, client = ssock.accept()
        gevent.spawn(callback, sock, client)

class App(object):
    def __init__(self, root):
        self.greenlet = None
        self.root = root
        self._build_window(root)
        self.root.after(100, self._connect)

    def add_text(self, text):
        cleaned_string = text.replace('\r', '')
        self.text.insert(tk.END, cleaned_string)

    def quit(self):
        self.root.quit()

    def _build_window(self, root):
        self.frame = tk.Frame(root)
        self.text = tk.Text(self.frame)
        self.quit_button = tk.Button(self.frame, text="Quit", command=self.quit)
        self.text.pack()
        self.quit_button.pack()
        self.frame.pack()

    def _connect(self):
        self.greenlet = gevent.spawn(
                socket_server,
                8080,
                SockLoop(lambda cl, txt: self.add_text("%s: %s" % (cl, txt))))
        self.gevent_loop_step()

    def gevent_loop_step(self):
        gevent.sleep()
        self.root.after_idle(self.gevent_loop_step)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()



