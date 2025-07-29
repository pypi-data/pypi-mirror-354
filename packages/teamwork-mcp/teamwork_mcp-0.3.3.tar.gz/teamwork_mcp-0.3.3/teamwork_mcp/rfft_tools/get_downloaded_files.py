import os
from pydantic import BaseModel, Field
from teamwork_mcp.base_tool import BaseTool, cache_to_file

class GetDownloadedFiles(BaseTool):
    # 工具名称和介绍
    tool_name: str = Field("GetDownloadedFiles", description="获取下载完的文件。")
    
    # 参数
    file_path: str = Field("", description="文件的路径。")

    # 调用
    @staticmethod
    def __call__(tool_name_and_param: "GetDownloadedFiles") -> str:
        file_path = tool_name_and_param.file_path
        if not os.path.exists(file_path):
            return f"文件不存在：{file_path}"
        else:
            from beyond.doc_fns.boyin_textloader import extract_text
            from pathlib import Path
            file_name = Path(file_path)
            file_content = extract_text(str(file_name)).strip()
            file_path = file_name
            if not file_path.exists():
                raise RuntimeError(f"Skipping task because file not found: {file_path}")
            if file_path.suffix in ['.pdf', '.docx', '.doc', '.txt']:
                return f"\n=== {file_path.name} begins ===\n{file_content}\n=== {file_path.name} ends ==="
            elif file_path.suffix in ['.jpg', '.jpeg', '.png']:
                return f"\n=== {file_path.name} begins ===\n{file_content}\n=== {file_path.name} ends ==="
            elif file_path.suffix in ['.xlsx', 'xls', '.csv']:
                return f"\n=== {file_path.name} begins ===\n{file_content}\n=== {file_path.name} ends ==="
            elif file_path.suffix in ['.py']:
                return f"\n=== {file_path.name} begins ===\n{file_content}\n=== {file_path.name} ends ==="
            else:
                return f"\n=== {file_path.name} begins ===\n{file_content}\n=== {file_path.name} ends ==="

