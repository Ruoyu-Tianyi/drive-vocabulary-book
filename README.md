# 云端词汇本 · Drive Vocabulary Book

**本地运行 AI，Google Drive 保存并同步词汇与学习记录。** 面向两台私人电脑使用，支持为法律、金融等课程创建独立单词本。

基于 **[Eric Zhou 的 Vocabulary Notebook](https://github.com/Eric-Zhou-0302/vocabulary-notebook)** 开发，保留原项目提交历史与 MIT 版权声明。原项目提供 FastAPI、React、AI 补全、FSRS 复习及导出；本项目扩展云同步、多单词本、逐次复习记录与冲突合并。[来源说明](NOTICE) · [原 README](docs/UPSTREAM_README.md) · [MIT License](LICENSE)

## 功能

- 创建、重命名单词本与填写课程说明；相同拼写可在法律、金融本中保留不同释义。
- 按当前单词本搜索、筛选日期、复习与导出，也可跨本浏览。
- 本机 Ollama 参考课程领域补全音标、中文释义和例句；手动内容不会被 AI 覆盖。
- FSRS 间隔复习，保留每次评分、复习次数、遗忘次数与到期时间。
- 两种 Google Drive 同步方式，离线修改后自动合并。
- 完整 JSON 备份恢复，兼容原项目的 `words.json`。
- 保留原项目的主题、快捷键、闪卡与 PDF/CSV/JSON 导出。

## Windows 快速启动

安装 [Python 3.10+](https://www.python.org/downloads/)，然后：

```powershell
git clone https://github.com/Ruoyu-Tianyi/drive-vocabulary-book.git
cd drive-vocabulary-book
.\start.bat
```

首次运行自动创建虚拟环境并安装依赖。前端构建产物已包含在仓库中，日常使用不需要 Node.js。浏览器访问 **http://127.0.0.1:1400**。

已安装依赖可直接运行 `.venv\Scripts\python.exe app.py`。升级后安装新依赖：`powershell -ExecutionPolicy Bypass -File .\start.ps1 -Install`。

macOS / Linux：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## 本地 AI

安装并启动 [Ollama](https://ollama.com/)，下载适合本机的模型，例如：

```bash
ollama pull qwen3:8b
ollama serve
```

Ollama 桌面程序已运行时无需再执行 `ollama serve`。默认模型为 `qwen3:8b`，可复制 `config.json.example` 为 `config.json` 修改模型名称。未启动 AI 时仍可保存、手动编辑、同步和复习；之后点击“补全缺失”即可补全。

此版本限定 AI 使用本机 HTTP 地址，移除了云端 DeepSeek 调用。模型、配置和令牌不上传到词库。

## 同步方式一：Drive 桌面同步文件夹（推荐）

无需 Google Cloud 项目和 OAuth 客户端。

1. 两台电脑安装[桌面版 Google Drive](https://support.google.com/drive/answer/10838124?hl=zh-Hans)，登录同一个私人账号。
2. 在“我的云端硬盘”新建专用文件夹，例如 `Drive Vocabulary Book`，将它设为“可离线使用”。
3. 进入“同步与备份”，填写本机绝对路径，例如 `G:\我的云端硬盘\Drive Vocabulary Book`，点击“连接同步文件夹”。第二台电脑选择**同一个云端文件夹**，本机盘符可以不同。
4. 各自在本机运行程序。应用默认每 30 秒读取并合并变更。

**“待写入文件夹为 0”表示变更已交给 Drive 桌面版；实际上传/下载由桌面版完成。关闭电脑前还应确认 Drive 的同步状态为已完成。** 另一台电脑收到文件后，应用下一轮自动合并。

两台电脑的程序目录、模型、`.venv`、`.secrets` 和 `words.json` 分别留在本机。云端目录只保存 `library.json` 身份标识及不可变的 `vocabulary-*.json` 变更文件。不要将整个项目或 `.secrets` 放入同步目录，不要手动编辑/删除变更文件。

ChatGPT 的 Drive 插件可帮助聊天读写文件，这个独立应用不依赖 ChatGPT 持续运行，也不读取或导出聊天插件的授权令牌。[OpenAI 插件授权说明](https://developers.openai.com/plugins/build/auth)

## 同步方式二：Drive API 直连（可选）

适合不安装 Drive 桌面版的电脑。与文件夹方式二选一，在设置中断开后可切换。

1. 在 [Google Cloud](https://console.cloud.google.com/apis/library/drive.googleapis.com) 创建项目并启用 Google Drive API。
2. 配置 OAuth 同意屏幕，个人测试时把自己的账号加入测试用户。
3. 创建 **桌面应用** OAuth 客户端，下载 JSON。
4. 在设置中导入 JSON，点击“连接 Google Drive”→“继续 Google 授权”。
5. 两台电脑使用**同一客户端 JSON、同一 Google 账号**各自授权，不要复制 `token.json`。

只申请 `drive.appdata` 权限，数据存于应用专属的隐藏 `appDataFolder`，不出现在普通 Drive 文件列表，也不访问其他文件。[Google 文档](https://developers.google.com/workspace/drive/api/guides/appdata)

授权采用本机回调、随机 state 和 PKCE。令牌仅保存在 `.secrets/token.json`。Google 测试应用的授权可能按 Google 发布状态/策略失效；应用会保留离线修改并提示重新授权。账户空间、API 配额和网络仍适用。

## 两台电脑如何合并

```text
电脑 A：本地界面 → 原子保存缓存 → 追加变更文件
                                   ↕ Google Drive
电脑 B：本地界面 ← 合并并重算 FSRS ← 读取变更文件
```

- 不用整份词库覆盖云端。每个变更有独立 ID，重试、重启和重复传输不会重复评分。
- 不同字段的编辑同时保留。同一字段同时编辑，按 Lamport 时钟、设备 ID、操作 ID 的固定顺序选择一致结果，不以电脑墙上时间决定先后。
- 每次复习是独立事件，按时间与事件 ID 排序重算 FSRS，两台电脑的评分均保留。请保持系统时钟正确。
- 删除优先于旧设备的编辑和评分，避免单词复活。重新添加会生成新 ID。
- 同步为最终一致，两个设备同时写入后，下一轮读取收敛；尚未上传的修改不会出现在另一台电脑。
- 两台电脑离线分别新建同一拼写时，保留两条独立记录，避免误合并课程含义与学习记录。同步后可检查并删除重复项。
- 当前不自动压缩历史或清理删除标记，以支持长期离线设备。适合私人词库，变更文件会随使用增长。

## 备份、迁移与恢复

“同步与备份”里的**完整备份**包含全部单词本、字段变更、删除标记和每次复习事件。导入时合并，不覆盖现有数据，也保留删除标记。

从原项目迁移：导入原 `words.json`，或首次启动前复制到本项目根目录。旧 FSRS 状态作为基线保留；旧版本未记录的逐次评分无法补造。自动迁移前保留 `words.json.legacy.bak`。原格式导入时，已有 ID 跳过。

单词列表的 JSON/CSV/PDF 导出只含当前筛选结果，需要全部历史时请用设置中的完整备份。本地每 10 分钟另存 `words.json.bak`。损坏文件会保留并停止读取，不会用空词库覆盖云端。

## 配置与安全

```json
{
  "provider": "ollama",
  "ollama": {"url": "http://127.0.0.1:11434/api/generate", "model": "qwen3:8b"},
  "srs": {"daily_new_limit": 20},
  "sync": {"interval_seconds": 30, "credentials_dir": ".secrets"}
}
```

只监听 `127.0.0.1:1400`，限制 Host 与修改请求来源；不用于公开部署。一个本地缓存只允许一个进程打开。真实配置、词库、备份和令牌被 Git 忽略。同步文件为 JSON，文件夹模式沿用文件夹的现有共享权限，请使用私人文件夹。

测试可用 `VOCAB_DATA_FILE` 指定独立本地缓存。不要把个人词库、令牌或完整备份提交到公共仓库。

## 开发与验证

```bash
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest -q
cd frontend
npm ci
npm run build
```

前端修改后必须重新构建。上游误提交的 `node_modules` 已从版本管理移除。测试覆盖双设备编辑与复习合并、删除、离线重试、文件夹重启、Drive HTTP 模拟及备份恢复。真实 API 直连需要自己的 Google OAuth 客户端。

核心扩展：`sync_storage.py`（变更与 FSRS 重放）、`drive_sync.py`（文件夹、Drive API、OAuth）、`instance_lock.py`（本地单进程保护）、`frontend/src/Books.jsx` 和 `frontend/src/pages/Settings.jsx`。
