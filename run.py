from proxypool.api import app
from proxypool.schedule import Schedule


def main():
    s = Schedule()
    s.run()   # 运行调度器
    app.run()  # 运行flask应用程序


if __name__ == '__main__':
    main()
