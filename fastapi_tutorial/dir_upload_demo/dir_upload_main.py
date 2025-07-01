import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
from pathlib import Path

app = FastAPI()

# test pass, trae debug
# 前端可以实现浏览器上传文件夹的功能，主要通过 HTML5 的 webkitdirectory 属性实现（现代浏览器均支持，包括非 WebKit 内核的浏览器如 Firefox/Edge）。以下是具体实现和后台接收的文件结构
# 允许跨域请求（方便开发）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],  # 允许前端访问所有响应头
)

# 创建上传目录
UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

@app.post("/upload")
async def upload_folder(files: List[UploadFile] = File(...), paths: str = Form(None)):
    saved_count = 0
    
    # 打印接收到的请求信息，用于调试
    print(f"接收到上传请求")
    print(f"接收到 {len(files)} 个文件")
    print(f"接收到的路径信息: {paths}")
    
    # 打印文件信息
    for i, file in enumerate(files):
        print(f"文件 {i}: 名称={file.filename}, 大小={file.size if hasattr(file, 'size') else '未知'}, 内容类型={file.content_type}")
    
    # 如果paths是字符串，尝试解析为JSON
    path_list = []
    if paths:
        try:
            import json
            if paths.startswith('[') and paths.endswith(']'):
                path_list = json.loads(paths)
                print(f"成功解析JSON路径列表，包含 {len(path_list)} 个路径")
            else:
                path_list = [paths]  # 单个路径
                print(f"使用单个路径: {paths}")
        except Exception as e:
            print(f"解析路径信息失败: {str(e)}")
            print(f"原始路径字符串: '{paths}'")
            path_list = []
    
    # 打印解析后的路径信息
    print(f"解析后的路径列表: {path_list}")
    
    # 清空上传目录（可选，根据需求调整）
    shutil.rmtree(UPLOAD_DIR, ignore_errors=True)
    Path(UPLOAD_DIR).mkdir(exist_ok=True)
    
    # 确保文件和路径数量一致
    if len(path_list) > 0 and len(files) != len(path_list):
        print(f"警告: 文件数量 ({len(files)}) 与路径数量 ({len(path_list)}) 不匹配")
    
    # 处理文件上传
    for i, file in enumerate(files):
        try:
            # 获取相对路径
            relative_path = path_list[i] if i < len(path_list) else file.filename
            print(f"处理文件 {i}: {file.filename}, 使用路径: {relative_path}")
            
            # 构建完整保存路径
            full_path = Path(UPLOAD_DIR) / relative_path
            
            # 确保目录存在
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 保存文件
            with open(full_path, "wb") as buffer:
                # 使用分块写入以支持大文件
                while content := await file.read(1024 * 1024):  # 1MB chunks
                    buffer.write(content)
            
            saved_count += 1
            print(f"成功保存文件: {full_path}")
        except Exception as e:
            # 记录错误但继续处理其他文件
            print(f"保存文件 {file.filename} 时出错: {str(e)}")
    
    # 构建响应数据
    response_data = {
        "message": "文件夹上传处理完成",
        "saved_files": saved_count,
        "total_files": len(files),
        "upload_dir": os.path.abspath(UPLOAD_DIR)
    }
    
    # 记录响应信息
    print(f"返回响应: {response_data}")
    
    return response_data

# 提供静态文件访问（用于访问前端页面）
app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)