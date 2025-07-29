import alpha_init_test # 用于修正路径到项目根目录，请勿删除

from teamwork_mcp.rfft_tools.get_downloaded_files import GetDownloadedFiles as Tool

fn = Tool().__call__
args = Tool(file_path="what is the close price of Alibaba Group Holding Limited (BABA) on 2025-5-12?")
result = fn(args)
print(result)

