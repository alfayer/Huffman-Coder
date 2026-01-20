from init import create_app
from prometheus.test import run_metrics_server
from threading import Thread

app = create_app()

if __name__ == "__main__":
    monitor_Thread = Thread(target=run_metrics_server)
    monitor_Thread.daemon = True
    monitor_Thread.start()

    app.run(host="localhost", port=9000)



