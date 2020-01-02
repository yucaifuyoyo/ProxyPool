from proxypool.api import app
from proxypool.schedule import Schedule


def main():
    s = Schedule()
    s.run()  # 运行调度器
    app.run(debug=True, host='0.0.0.0', port=9090)  # 运行flask应用程序


if __name__ == '__main__':
    main()
