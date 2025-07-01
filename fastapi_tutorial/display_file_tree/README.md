# 文件目录树展示系统

## 项目概述

这是一个基于Web的文件目录树展示系统，允许用户通过浏览器查看服务器上的文件目录结构，效果类似Linux系统下的`tree`命令。系统由后端FastAPI服务和前端HTML页面组成，支持可交互的树状结构展示，包括展开/折叠目录、显示文件大小和路径等功能。该系统设计轻量化，无需外部依赖库（除了FastAPI和Uvicorn），易于部署和使用。

## 功能特点

- **树状结构展示**：以树状结构直观展示文件目录层级，清晰呈现目录和文件的层次关系
- **可交互操作**：支持展开/折叠目录、一键展开/折叠全部，提升用户体验
- **自定义参数**：可指定目录路径、最大递归深度、是否包含文件，灵活控制展示内容
- **文件信息展示**：显示文件大小（自动格式化为KB/MB/GB）、相对路径等信息
- **错误处理**：完善的错误处理和用户提示，包括权限不足、路径不存在等异常情况
- **响应式设计**：使用现代CSS技术，适配不同屏幕尺寸的设备
- **跨域支持**：配置CORS中间件，支持跨域请求，方便开发和部署
- **统计信息**：显示目录和文件数量、加载耗时等统计信息
- **无外部依赖**：前端纯HTML/CSS/JavaScript实现，无需引入第三方框架

## 技术实现

### 后端实现 (file_tree_api.py)

后端使用Python的FastAPI框架实现，提供文件目录树数据和静态文件服务功能。整个后端设计遵循RESTful API设计原则，采用模块化结构，便于维护和扩展。

#### 关键技术点：

1. **API接口设计**：提供`/get_file_tree`接口，支持路径、深度和文件包含选项参数
   ```python
   @app.get("/get_file_tree")
   async def get_file_tree(
       path: str = Query("", description="要获取树结构的目录路径，留空表示当前目录"),
       max_depth: int = Query(3, description="最大递归深度，默认为3", ge=1, le=10),
       include_files: bool = Query(True, description="是否包含文件，默认为True")
   ):
       # 获取文件树结构
   ```

2. **递归构建树结构**：使用递归算法构建目录树结构，支持深度限制
   ```python
   def build_tree(base_path: str, current_path: str, max_depth: int = 3, include_files: bool = True, current_depth: int = 0) -> Dict[str, Any]:
       # 递归构建文件树结构
       # 先处理目录，再处理文件，确保目录在前
       # 支持最大深度限制，超过深度时返回标记
   ```

3. **文件大小格式化**：自动将字节大小转换为人类可读格式
   ```python
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
   ```

4. **全面的错误处理**：处理各种异常情况，包括路径不存在、权限不足、跨驱动器访问等
   ```python
   # 处理权限错误
   except PermissionError:
       return {
           "name": name,
           "type": "directory",
           "path": relative_path.replace("\\", "/"),
           "error": "权限不足",
           "children": []
       }
   # 处理其他IO错误
   except (PermissionError, OSError) as e:
       return {
           "name": name,
           "type": "file",
           "path": relative_path.replace("\\", "/"),
           "error": "无法访问: " + str(e)
       }
   # API错误处理
   except Exception as e:
       raise HTTPException(status_code=500, detail=f"处理请求时出错: {str(e)}")
   ```

5. **跨域支持**：配置CORS中间件，允许跨域请求，便于前后端分离开发
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # 在生产环境中应该限制为特定域名
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
       expose_headers=["*"],
   )
   ```

6. **静态文件服务**：提供静态文件访问，用于访问前端页面，简化部署
   ```python
   app.mount("/", StaticFiles(directory=".", html=True), name="static")
   ```

7. **依赖检查与启动优化**：启动前检查必要依赖和文件，确保系统正常运行
   ```python
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
   ```

8. **元数据添加**：API响应中包含元数据，便于前端处理和调试
   ```python
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
   ```

### 前端实现 (file_tree.html)

前端使用纯HTML、CSS和JavaScript实现，不依赖任何外部框架，采用现代Web技术和最佳实践，确保良好的用户体验和性能。

#### 关键技术点：

1. **树状结构渲染**：使用嵌套的UL/LI元素实现树状结构，递归处理目录和文件
   ```javascript
   function renderTree(node, container) {
       if (!node) return;
       
       const ul = document.createElement('ul');
       
       // 如果是根节点，不创建li
       if (container === fileTree) {
           renderChildren(node, ul);
           container.appendChild(ul);
       } else {
           const li = document.createElement('li');
           
           if (node.type === 'directory') {
               // 目录节点处理
               // ...
           } else if (node.type === 'file') {
               // 文件节点处理
               // ...
           }
           
           container.appendChild(li);
       }
   }
   ```

2. **交互功能**：实现目录的展开/折叠功能，以及一键展开/折叠全部
   ```javascript
   // 添加折叠/展开事件
   function addToggleEvents() {
       const carets = document.querySelectorAll('.caret');
       carets.forEach(caret => {
           caret.addEventListener('click', function() {
               this.classList.toggle('caret-down');
               const directory = this.parentElement.querySelector('.directory');
               if (directory) directory.classList.toggle('open');
               const nested = this.parentElement.querySelector('.nested');
               if (nested) nested.classList.toggle('active');
           });
       });
   }
   
   // 展开全部按钮
   expandAllBtn.addEventListener('click', () => {
       const carets = document.querySelectorAll('.caret');
       carets.forEach(caret => {
           caret.classList.add('caret-down');
           const directory = caret.parentElement.querySelector('.directory');
           if (directory) directory.classList.add('open');
           const nested = caret.parentElement.querySelector('.nested');
           if (nested) nested.classList.add('active');
       });
   });
   ```

3. **API调用与错误处理**：使用Fetch API调用后端接口获取数据，包含完整的错误处理和加载状态管理
   ```javascript
   // 获取文件树数据
   function fetchFileTree() {
       const path = pathInput.value.trim();
       const maxDepth = depthInput.value;
       const includeFiles = includeFilesCheckbox.checked;
       
       // 显示加载中
       loading.style.display = 'block';
       error.style.display = 'none';
       statusBar.style.display = 'none';
       fileTree.innerHTML = '';
       
       // 禁用按钮，防止重复点击
       fetchBtn.disabled = true;
       fetchBtn.textContent = '加载中...';
       
       // 记录开始时间（用于计算耗时）
       const startTime = new Date();
       
       // 构建API URL
       const apiUrl = `/get_file_tree?path=${encodeURIComponent(path)}&max_depth=${maxDepth}&include_files=${includeFiles}`;
       
       // 发送请求
       fetch(apiUrl)
           .then(response => {
               if (!response.ok) {
                   return response.json().then(err => {
                       throw new Error(err.detail || '获取文件树失败');
                   });
               }
               return response.json();
           })
           .then(data => {
               // 处理成功响应
               // ...
           })
           .catch(err => {
               // 显示错误信息
               loading.style.display = 'none';
               error.style.display = 'block';
               error.textContent = `错误: ${err.message}`;
           })
           .finally(() => {
               // 恢复按钮状态
               fetchBtn.disabled = false;
               fetchBtn.textContent = '获取目录树';
           });
   }
   ```

4. **统计信息计算**：递归计算文件和目录数量，显示加载耗时等统计信息
   ```javascript
   // 递归计算文件和目录数量
   function countItems(node) {
       if (!node) return;
       if (node.type === 'file') {
           fileCount++;
       } else if (node.type === 'directory') {
           dirCount++;
           if (node.children) {
               node.children.forEach(countItems);
           }
       }
   }
   
   // 显示状态信息
   statusBar.style.display = 'block';
   statusBar.innerHTML = `
       <strong>统计信息:</strong> 
       ${dirCount} 个目录, 
       ${fileCount} 个文件, 
       加载耗时: ${timeElapsed.toFixed(2)}秒
   `;
   ```

5. **文件大小格式化**：前端也实现了文件大小的格式化显示
   ```javascript
   // 格式化文件大小
   function formatFileSize(bytes) {
       if (bytes === 0) return '0 Bytes';
       const k = 1024;
       const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
       const i = Math.floor(Math.log(bytes) / Math.log(k));
       return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
   }
   ```

6. **CSS动画与视觉效果**：使用CSS动画增强用户体验，如加载动画、展开/折叠动画
   ```css
   .loading::after {
       content: "";
       animation: dots 1.5s infinite;
   }
   @keyframes dots {
       0% { content: ""; }
       25% { content: "."; }
       50% { content: ".."; }
       75% { content: "..."; }
       100% { content: ""; }
   }
   ```

7. **响应式设计**：使用Flexbox和媒体查询实现响应式布局，适配不同屏幕尺寸
   ```css
   .controls {
       display: flex;
       gap: 15px;
       margin-bottom: 20px;
       flex-wrap: wrap;
   }
   .input-group {
       flex: 1;
       min-width: 200px;
   }
   ```

8. **直观的文件和目录图标**：使用Unicode字符作为图标，区分文件和目录
   ```css
   .tree .file::before {
       content: "📄";
       margin-right: 6px;
   }
   .tree .directory::before {
       content: "📁";
       margin-right: 6px;
   }
   .tree .directory.open::before {
       content: "📂";
   }
   ```

## 使用方法

### 安装与启动

1. 确保已安装Python 3.7+和必要的依赖包：
   ```bash
   pip install fastapi uvicorn
   ```

2. 运行后端服务器：
   ```bash
   python file_tree_api.py
   ```
   启动成功后，会看到类似以下输出：
   ```
   检查依赖项...
   检查文件...
   启动服务器...
   服务器已启动，请访问: http://localhost:8000
   ```

3. 在浏览器中访问：http://localhost:8000

### 使用界面

1. **输入目录路径**：在"目录路径"输入框中输入要查看的目录的完整路径
   - Windows示例：`C:\Users\username\Documents` 或 `C:/Users/username/Documents`
   - Linux/Mac示例：`/home/username/documents`

2. **设置最大深度**：在"最大深度"输入框中设置遍历的最大层级（默认为3）
   - 设置为1只显示顶级目录和文件
   - 设置为较大的值可以查看更深层次的目录结构

3. **包含文件选项**：勾选"包含文件"复选框可以显示文件，取消勾选则只显示目录

4. **获取目录树**：点击"获取目录树"按钮开始加载目录结构

5. **交互操作**：
   - 点击目录前的箭头图标可以展开或折叠该目录
   - 点击"展开全部"按钮可以一键展开所有目录
   - 点击"折叠全部"按钮可以一键折叠所有目录

6. **查看统计信息**：加载完成后，页面底部会显示统计信息，包括目录数量、文件数量和加载耗时

## 注意事项

- **性能考虑**：对于大型目录，建议设置较小的最大深度值（3-5），以避免性能问题和浏览器卡顿

- **路径格式**：
  - Windows系统中，路径可以使用正斜杠(/)或反斜杠(\)，但使用反斜杠时需要转义（如`C:\Users`）
  - Linux/Mac系统中，使用正斜杠(/)作为路径分隔符

- **权限问题**：
  - 确保应用有足够的权限访问指定的目录，否则会显示权限错误
  - 某些系统目录可能需要管理员/root权限才能访问

- **错误处理**：
  - 如果输入的路径不存在，系统会显示相应的错误信息
  - 如果遇到权限问题，会显示"权限被拒绝"的错误
  - 如果目录结构过大导致加载超时，可以尝试减小最大深度值

- **服务器地址**：
  - 默认情况下，服务器绑定到`localhost`，只能在本机访问
  - 如需在局域网内访问，可以修改`file_tree_api.py`中的`host`参数为`0.0.0.0`

## 扩展与改进

1. **文件操作**：添加文件上传、下载、删除等功能

2. **搜索功能**：添加文件和目录搜索功能

3. **文件预览**：支持常见文件类型的在线预览

4. **权限控制**：添加用户登录和权限控制

5. **主题切换**：支持明暗主题切换

6. **性能优化**：对于大型目录结构，实现懒加载或虚拟滚动

## 技术支持

如有问题或建议，请提交Issue或联系开发团队。