from mcp.server.fastmcp import FastMCP
import subprocess
import sys

# Create an MCP server
mcp = FastMCP("aiden-server")

# Add an get score tool
@mcp.tool()
def get_score_by_name(name: str) -> str:
    """根据员工的姓名获取该员工的绩效得分"""
    if name == "张三":
        return "name: 张三 绩效评分: 85.9"
    elif name == "李四":
        return "name: 李四 绩效评分: 92.7"
    else:
        return "未搜到该员工的绩效"
    
@mcp.tool()
def get_score_by_age(name: str) -> str:
    """根据员工的获取年龄"""
    if name == "张三":
        return "name: 张三 18岁"
    elif name == "李四":
        return "name: 李四 22岁"
    else:
        return "未搜到该员工的年龄"

@mcp.tool()
def add_network_printer() -> str:
    """添加网络打印机,安装打印机驱动"""
    printer_path = r"\\canonprinter.weoa.com\CanonPrinter"
    try:
        # 执行添加打印机命令
        cmd = f'rundll32 printui.dll,PrintUIEntry /in /u /z /q /n "{printer_path}"'
        result = subprocess.run(cmd, shell=True, check=True, text=True, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        cmd = f'rundll32 printui.dll,PrintUIEntry /y /n "{printer_path}"'
        result = subprocess.run(cmd, shell=True, check=True, text=True, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        return "打印机已添加成功"
    except subprocess.CalledProcessError as e:
        return "添加打印机失败"

def run():
    mcp.run(transport='stdio')


if __name__ == '__main__':
   run()