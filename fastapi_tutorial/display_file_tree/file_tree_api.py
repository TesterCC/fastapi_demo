# file_tree_api.py 优化建议
import os
import sys
import json
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from datetime import datetime

# 获取文件大小的格式化函数
def format_size(size_bytes: int) -> str:
    """将字节大小转换为人类可读的格式"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

# 递归构建文件树结构函数
def build_tree(base_path: str, current_path: str, max_depth: int = 3, include_files: bool = True, current_depth: int = 0) -> Dict[str, Any]:
    """
    递归构建文件树结构
    
    参数:
        base_path: 基础路径，用于计算相对路径
        current_path: 当前处理的路径
        max_depth: 最大递归深度
        include_files: 是否包含文件
        current_depth: 当前递归深度
    
    返回:
        包含文件树结构的字典
    """
    # 获取路径的最后一部分作为名称
    try:
        name = os.path.basename(current_path) or os.path.basename(os.path.abspath(current_path))
    except:
        name = os.path.basename(str(current_path))
    
    # 计算相对路径
    try:
        relative_path = os.path.relpath(current_path, base_path)
    except (ValueError, OSError):
        # 处理不同驱动器的情况
        relative_path = str(current_path)
    
    # 如果已达到最大深度
    if current_depth > max_depth:
        return {
            "name": name, 
            "type": "directory", 
            "path": relative_path.replace("\\", "/"),
            "max_depth_reached": True,
            "children": []
        }
    
    # 如果是目录
    if os.path.isdir(current_path):
        try:
            children = []
            items = sorted(os.listdir(current_path))
            
            # 分离目录和文件，并按名称排序
            dirs = []
            files = []
            for item in items:
                item_path = os.path.join(current_path, item)
                if os.path.isdir(item_path):
                    dirs.append(item)
                elif os.path.isfile(item_path) and include_files:
                    files.append(item)
            
            # 先处理目录
            for item in dirs:
                item_path = os.path.join(current_path, item)
                children.append(build_tree(base_path, item_path, max_depth, include_files, current_depth + 1))
            
            # 再处理文件
            if include_files:
                for item in files:
                    item_path = os.path.join(current_path, item)
                    try:
                        size_bytes = os.path.getsize(item_path)
                        children.append({
                            "name": item,
                            "type": "file",
                            "path": os.path.relpath(item_path, base_path).replace("\\", "/"),
                            "size": format_size(size_bytes),
                            "size_bytes": size_bytes
                        })
                    except (PermissionError, OSError) as e:
                        children.append({
                            "name": item,
                            "type": "file",
                            "path": os.path.relpath(item_path, base_path).replace("\\", "/"),
                            "error": "无法访问: " + str(e)
                        })
            
            return {
                "name": name,
                "type": "directory",
                "path": relative_path.replace("\\", "/"),
                "children": children
            }
        except PermissionError:
            return {
                "name": name,
                "type": "directory",
                "path": relative_path.replace("\\", "/"),
                "error": "权限不足",
                "children": []
            }
    # 如果是文件
    elif os.path.isfile(current_path):
        try:
            size_bytes = os.path.getsize(current_path)
            return {
                "name": name,
                "type": "file",
                "path": relative_path.replace("\\", "/"),
                "size": format_size(size_bytes),
                "size_bytes": size_bytes
            }
        except (PermissionError, OSError) as e:
            return {
                "name": name,
                "type": "file",
                "path": relative_path.replace("\\", "/"),
                "error": "无法访问: " + str(e)
            }
    else:
        return {
            "name": name,
            "type": "unknown",
            "path": relative_path.replace("\\", "/"),
            "error": "未知文件类型"
        }

# 创建FastAPI应用
app = FastAPI(title="文件目录树API", description="提供文件目录树结构的API服务")

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/get_file_tree")
async def get_file_tree(
    path: str = Query("", description="要获取树结构的目录路径，留空表示当前目录"),
    max_depth: int = Query(3, description="最大递归深度，默认为3", ge=1, le=10),
    include_files: bool = Query(True, description="是否包含文件，默认为True")
):
    """获取指定路径的文件目录树结构"""
    # 检查是否有默认路径环境变量
    default_path = os.environ.get("DEFAULT_PATH", "")
    
    try:
        # 如果未提供路径，则使用默认路径或当前目录
        if not path:
            base_path = default_path or os.getcwd()
        else:
            # 确保路径存在
            base_path = os.path.abspath(path)
        
        if not os.path.exists(base_path):
            raise HTTPException(status_code=404, detail=f"路径不存在: {base_path}")
        
        # 获取文件树结构
        tree = build_tree(base_path, base_path, max_depth, include_files)
        
        # 添加元数据
        result = {
            "status": "success",
            "meta": {
                "base_path": base_path,
                "max_depth": max_depth,
                "include_files": include_files,
                "timestamp": datetime.now().isoformat()
            },
            "tree": tree
        }
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理请求时出错: {str(e)}")

# 提供静态文件访问（用于访问前端页面）
app.mount("/", StaticFiles(directory=".", html=True), name="static")

def check_dependencies():
    """检查必要的依赖包是否已安装"""
    try:
        import fastapi
        import uvicorn
        return True
    except ImportError as e:
        print(f"错误: 缺少必要的依赖包: {e}")
        print("请先安装依赖: pip install fastapi uvicorn")
        return False

def check_files():
    """检查必要的文件是否存在"""
    html_file = Path("file_tree.html")
    
    if not html_file.exists():
        print(f"错误: 找不到HTML文件 {html_file}")
        return False
    
    return True

def main():
    """主函数，直接启动服务器，不带参数，不在后台运行"""
    # 设置默认配置
    host = '0.0.0.0'
    port = 8000
    
    # 检查依赖和文件
    if not check_dependencies() or not check_files():
        sys.exit(1)
    
    # 打印启动信息
    host_display = 'localhost' if host == '0.0.0.0' else host
    print(f"\n文件目录树展示系统启动中...")
    print(f"服务器地址: http://{host_display}:{port}")
    print(f"前端页面: http://{host_display}:{port}/file_tree.html")
    print("\n按 Ctrl+C 停止服务器\n")
    
    # 启动服务器（不使用reload=True，确保不在后台运行）
    import uvicorn
    uvicorn.run(app, host=host, port=port, reload=False)

if __name__ == "__main__":
    main()