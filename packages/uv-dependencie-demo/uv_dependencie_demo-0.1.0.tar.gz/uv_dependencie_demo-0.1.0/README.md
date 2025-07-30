## uv文档
1. https://docs.astral.sh/uv/reference/cli/#uv

## 新建一个uv项目
1. uv init uv_dependencie_demo  项目初始化
2. cd uv_dependencie_demo  进入项目目录
3. uv add "fastapi"  添加依赖包，内容会出现在pyproject.toml的dependencies中
4. pip install "fastapi"  安装依赖包
5. 对于步骤3和4，如果使用pycharm，引入依赖时，直接通过pycharm添加，会安装和添加到pyproject.toml的dependencies中


## 已有uv项目安装依赖
1. 怎么命令安装pyproject.toml的dependencies中依赖
   uv sync
2. 补充说明 
   虚拟环境要求：uv sync 会自动关联当前目录的虚拟环境（如 .venv），无需手动激活。
   依赖解析：uv 会解析 pyproject.toml 的依赖树，并下载/安装所有依赖及其子依赖。
   替代方案：若需类似 pip install -r requirements.txt 的行为，可使用 uv pip install -r requirements.txt，但直接使用 pyproject.toml 更符合现代 Python 项目规范。


## uv项目启动
1. uv run main.py


## uv使用详细流程
使用 `uv` 管理 Python 项目的详细流程如下，结合示例说明关键步骤：

---

### 1. **初始化项目**
在项目根目录运行以下命令：
```bash
uv init
```
- **作用**：生成 `pyproject.toml` 和 `.venv` 虚拟环境目录。
- **输出示例**：
  ```toml
  [project]
  name = "my-project"
  version = "0.1.0"
  dependencies = []
  ```

---

### 2. **添加依赖**
使用 `uv add` 安装包并自动更新 `pyproject.toml` 和 `uv.lock`：
```bash
uv add fastapi uvicorn
```
- **效果**：`pyproject.toml` 中 `dependencies` 列表新增 `fastapi` 和 `uvicorn`。
- **可选依赖**：添加测试依赖时使用 `--extra`：
  ```bash
  uv add --extra test pytest
  ```
  这会在 `pyproject.toml` 中生成：
  ```toml
  [project.optional-dependencies]
  test = ["pytest"]
  ```

---

### 3. **运行命令**
通过 `uv run` 在隔离环境中执行脚本或命令：
```bash
uv run python main.py
```
- **自动同步**：`uv` 会先验证 `uv.lock` 是否与 `pyproject.toml` 同步，并确保虚拟环境已安装所有依赖 <sub index="1" url="https://docs.astral.sh/uv/guides/projects/" title="Working on projects | uv - Astral Docs" snippet="## Running commandsuv run can be used to run arbitrary scripts or commands in your project environment.Prior to every uv run invocation, uv will verify that the lockfile is up-to-date with thepyproject.toml, and that the environment is up-to-date with the lockfile, keeping your projectin-sync without the need for manual intervention. uv run guarantees that your command is run in aconsistent, locked environment."></sub><sub index="2" url="https://docs.astral.sh/uv/concepts/projects/run/" title="Running commands in projects - uv - Astral Docs" snippet="# Running commands in projectsWhen working on a project, it is installed into the virtual environment at .venv. This environmentis isolated from the current shell by default, so invocations that require the project, e.g.,python -c &quot;import example&quot;, will fail. Instead, use uv run to run commands in the projectenvironment:When using run, uv will ensure that the project environment is up-to-date before running the givencommand."></sub>。
- **示例**：运行 FastAPI 应用：
  ```bash
  uv run uvicorn main:app --reload
  ```

---

### 4. **管理虚拟环境**
- **手动激活环境**（非必需）：
  ```bash
  source .venv/bin/activate  # Linux/macOS
  .venv\Scripts\activate     # Windows
  ```
- **强制同步依赖**：
  ```bash
  uv sync
  uv sync --extra test       # 安装可选依赖
  ```

---

### 5. **项目结构示例**
最终目录结构如下：
```
my-project/
├── .venv/                # 虚拟环境
├── pyproject.toml        # 项目配置
├── uv.lock               # 依赖锁文件
├── main.py               # 主程序文件
└── tests/                # 测试目录
    └── test_main.py
```

---

### 6. **常见问题与解决方案**
#### **Q1: Windows 路径报错（ModuleNotFoundError）**
- **原因**：脚本路径使用反斜杠 `\` 导致模块导入失败 <sub index="5" url="https://github.com/astral-sh/uv/issues/12270" title="`uv run --project` doesn't allow resolving module imports on windows" snippet="https://avatars.githubusercontent.com/u/31117813?u=f968ae19cd2c47801eb32affa786576fddf6d668&amp;v=4&amp;size=80## Description### SummaryIn my python project, I have a scripts folder where I keep various utilities that need to import code from the main app folder. When running it on macOS, I just use uv run scripts/test.py --project . and everything works as expected. On my windows system, when I try uv run scripts\test.py --project . i get the following error : ModuleNotFoundError: No module named 'app'.I tried using an absolute path instead and various tricks to make it work, and also using the --folder argument instead, but nothing helps. Am I misunderstanding something or is this a bug ?"></sub>。
- **解决**：确保 `sys.path` 包含项目根目录，或使用正斜杠 `/`：
  ```bash
  uv run python scripts/test.py
  ```

#### **Q2: 依赖冲突**
- **现象**：安装依赖时提示 `no solution found`。
- **解决**：升级/降级依赖版本，或使用 `--upgrade-package`：
  ```bash
  uv lock --upgrade-package numpy
  ```

---

### 7. **完整示例：创建并运行 FastAPI 项目**
1. **初始化项目**：
   ```bash
   uv init
   ```
2. **添加依赖**：
   ```bash
   uv add fastapi uvicorn
   ```
3. **编写 `main.py`**：
   ```python
   from fastapi import FastAPI
   app = FastAPI()
   @app.get("/")
   def read_root():
       return {"Hello": "World"}
   ```
4. **启动服务**：
   ```bash
   uv run uvicorn main:app --reload
   ```
5. **访问**：浏览器打开 `http://127.0.0.1:8000`。

---

### 8. **高级用法：构建可分发包**
1. **配置 `pyproject.toml` 的构建系统**：
   ```toml
   [build-system]
   requires = ["setuptools"]
   build-backend = "setuptools.build_meta"
   ```
2. **构建 wheel 包**：
   ```bash
   uv build --wheel
   ```

通过上述流程，可高效管理 Python 项目的依赖、环境和运行逻辑。
