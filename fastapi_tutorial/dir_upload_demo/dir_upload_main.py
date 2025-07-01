import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
from pathlib import Path

app = FastAPI()

# 允许跨域请求（方便开发）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建上传目录
UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

@app.post("/upload")
async def upload_folder(files: List[UploadFile] = File(...)):
    saved_count = 0
    
    # 清空上传目录（可选，根据需求调整）
    shutil.rmtree(UPLOAD_DIR, ignore_errors=True)
    Path(UPLOAD_DIR).mkdir(exist_ok=True)
    
    for file in files:
        try:
            # 获取文件相对路径（前端通过webkitRelativePath设置）
            relative_path = file.filename
            
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
        except Exception as e:
            # 记录错误但继续处理其他文件
            print(f"保存文件 {file.filename} 时出错: {str(e)}")
    
    return {
        "message": "文件夹上传处理完成",
        "saved_files": saved_count,
        "total_files": len(files),
        "upload_dir": os.path.abspath(UPLOAD_DIR)
    }

# 提供静态文件访问（用于访问前端页面）
app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)