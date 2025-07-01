# 文件夹上传系统

## 项目概述

这是一个基于Web的文件夹上传系统，允许用户通过浏览器选择或拖拽整个文件夹进行上传。系统由前端HTML页面和后端FastAPI服务组成，支持现代浏览器（Chrome、Firefox、Edge等）的文件夹上传功能。

## 功能特点

- **文件夹整体上传**：支持选择或拖拽整个文件夹进行上传，保留原始目录结构
- **进度显示**：实时显示上传进度和状态信息
- **文件列表预览**：上传前显示所选文件的列表和大小
- **错误处理**：完善的错误处理和用户提示
- **取消上传**：支持中途取消上传操作
- **超时处理**：自动处理长时间未响应的请求
- **跨域支持**：支持跨域请求，方便开发和部署

## 技术实现

### 前端实现 (dir_upload_demo.html)

前端使用纯HTML、CSS和JavaScript实现，不依赖任何外部框架。

#### 关键技术点：

1. **文件夹选择**：使用`webkitdirectory`和`directory`属性实现文件夹选择
   ```html
   <input type="file" id="fileInput" webkitdirectory directory multiple>
   ```

2. **拖放功能**：实现拖放区域，支持文件夹拖放上传
   ```javascript
   dropZone.addEventListener('drop', (e) => {
       // 处理拖放的文件夹
   });
   ```

3. **路径处理**：收集文件的相对路径，并作为JSON字符串发送给后端
   ```javascript
   const pathsArray = filesToUpload.map(file => file.webkitRelativePath || file.name);
   const pathsJson = JSON.stringify(pathsArray);
   formData.append('paths', pathsJson);
   ```

4. **进度监控**：使用XMLHttpRequest的upload.progress事件监控上传进度
   ```javascript
   xhr.upload.addEventListener('progress', (event) => {
       if (event.lengthComputable) {
           const percentComplete = Math.round((event.loaded / event.total) * 100);
           // 更新进度条
       }
   });
   ```

5. **错误处理**：完善的错误处理机制，包括网络错误、服务器错误和超时处理
   ```javascript
   xhr.onerror = function() {
       statusDiv.textContent = '网络错误，请检查服务器连接';
       resetUploadState();
   };
   
   xhr.timeout = 120000; // 2分钟超时
   xhr.ontimeout = function() {
       statusDiv.textContent = '请求超时，请检查网络连接或服务器状态';
       resetUploadState();
   };
   ```

### 后端实现 (dir_upload_main.py)

后端使用Python的FastAPI框架实现，提供文件上传和静态文件服务功能。

#### 关键技术点：

1. **跨域支持**：配置CORS中间件，允许跨域请求
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
       expose_headers=["*"],
   )
   ```

2. **文件上传处理**：接收前端发送的文件和路径信息
   ```python
   @app.post("/upload")
   async def upload_folder(files: List[UploadFile] = File(...), paths: str = Form(None)):
       # 处理上传的文件
   ```

3. **路径解析**：将前端发送的JSON路径字符串解析为Python列表
   ```python
   if paths:
       try:
           import json
           if paths.startswith('[') and paths.endswith(']'):
               path_list = json.loads(paths)
           else:
               path_list = [paths]  # 单个路径
       except Exception as e:
           print(f"解析路径信息失败: {str(e)}")
           path_list = []
   ```

4. **文件保存**：按照原始目录结构保存上传的文件
   ```python
   # 构建完整保存路径
   full_path = Path(UPLOAD_DIR) / relative_path
   
   # 确保目录存在
   full_path.parent.mkdir(parents=True, exist_ok=True)
   
   # 保存文件
   with open(full_path, "wb") as buffer:
       # 使用分块写入以支持大文件
       while content := await file.read(1024 * 1024):  # 1MB chunks
           buffer.write(content)
   ```

5. **静态文件服务**：提供静态文件访问，用于访问前端页面
   ```python
   app.mount("/", StaticFiles(directory=".", html=True), name="static")
   ```

## 使用方法

### 启动服务器

1. 确保已安装Python 3.7+和必要的依赖包：
   ```bash
   pip install fastapi uvicorn python-multipart
   ```

2. 运行后端服务器：
   ```bash
   python dir_upload_main.py
   ```

3. 服务器将在 http://localhost:8000 启动

### 使用前端页面

1. 在浏览器中访问 http://localhost:8000/dir_upload_demo.html

2. 点击"选择文件夹"按钮或将文件夹拖放到指定区域

3. 查看选中的文件列表，确认无误后点击"开始上传"按钮

4. 上传过程中可以查看进度条和状态信息，也可以点击"取消上传"按钮中断上传

5. 上传完成后，文件将保存在服务器的`uploads`目录中，保持原始目录结构

## 注意事项

1. **浏览器兼容性**：该功能依赖于现代浏览器的`webkitdirectory`属性，确保使用最新版本的Chrome、Firefox或Edge浏览器

2. **文件大小限制**：默认情况下，FastAPI对上传文件大小没有限制，但可能受到服务器配置的影响

3. **安全性考虑**：
   - 生产环境中应限制CORS的`allow_origins`为特定域名
   - 考虑添加身份验证和授权机制
   - 限制上传文件的类型和大小
   - 实施防止恶意文件上传的措施

4. **性能优化**：
   - 对于大文件或大量文件的上传，考虑使用分块上传或队列处理
   - 可以添加文件压缩功能减少传输数据量

## 扩展与改进

1. **用户认证**：添加用户登录和权限控制

2. **文件管理**：添加上传历史、文件列表和删除功能

3. **文件预览**：支持常见文件类型的在线预览

4. **断点续传**：实现大文件的断点续传功能

5. **多语言支持**：添加国际化支持

6. **移动端适配**：优化移动设备的用户体验

## 技术支持

如有问题或建议，请提交Issue或联系开发团队。