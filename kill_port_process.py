import psutil
import sys

def find_and_kill_process(port: int) -> None:
    """
    查找并杀死占用指定端口的进程。

    Args:
        port (int): 需要检查的端口号。
    """
    found = False
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            connections = proc.connections(kind='inet')
            for conn in connections:
                if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
                    print(f"找到进程: {proc.info['name']} (PID: {proc.info['pid']}) 占用端口 {port}")
                    proc.kill()
                    print(f"已杀死进程 PID: {proc.info['pid']}")
                    found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    if not found:
        print(f"没有找到占用端口 {port} 的进程")

def main():
    """
    主函数，解析命令行参数并执行查找与杀死进程的操作。
    """
    if len(sys.argv) != 2:
        print("使用方法: python kill_port_process.py <端口号>")
        sys.exit(1)
    
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("请提供一个有效的端口号。")
        sys.exit(1)
    
    find_and_kill_process(port)

if __name__ == "__main__":
    main() 