# 云端词汇本 · Drive Vocabulary Book

**本机运行词汇本，DeepSeek API 补全，Google Drive 同步词汇与学习记录。** 支持将新电脑作为日常主力、旧电脑作为备用，按法律、金融等课程创建独立单词本。

基于 **[Eric Zhou 的 Vocabulary Notebook](https://github.com/Eric-Zhou-0302/vocabulary-notebook)** 开发，保留原项目提交历史与 MIT 版权声明。原项目提供 FastAPI、React、AI 补全、FSRS 复习及导出；本项目扩展云同步、多单词本、逐次复习记录与冲突合并。[来源说明](NOTICE) · [原 README](docs/UPSTREAM_README.md) · [MIT License](LICENSE)

## Agent 安装提示词

在另一台电脑把下面整段复制给可操作本机的 Agent 即可。常规安装直接使用仓库附带的前端，无需 Node.js、Ollama 或模型文件。API Key 在该电脑的设置页输入。

```text
请在这台私人电脑上直接安装并配置“云端词汇本”，将这台电脑作为我的日常主力机。

GitHub 仓库：https://github.com/Ruoyu-Tianyi/drive-vocabulary-book
请先读取最新 README 和适用的 AGENTS.md，然后实际执行安装，不要只给我步骤。

1. 检查操作系统、Git 和 Python 3.10+。缺少时通过官方渠道安装；遇到系统权限、登录或安装条款时说明需要我完成的具体步骤。Windows 默认使用 D:\000_Workspace\云端词汇本；D 盘不可用则使用用户 Documents 下的 drive-vocabulary-book。本程序放在本地非同步目录。
2. 克隆上述仓库的 main 分支。如果已存在这个项目，先检查工作区与远程，保留已有词库、配置和未提交修改，安全更新，不执行强制重置或覆盖。
3. 创建项目独立 .venv 并安装 requirements.txt。使用已包含的 frontend/dist，常规安装无需 Node.js。此版本使用 DeepSeek API，不安装 Ollama 或下载模型。
4. 检查是否已有 DEEPSEEK_API_KEY。没有时先启动应用，引导我在“同步与备份 → DeepSeek API 词汇补全”中自己输入 Key；不要让我把 Key 贴到聊天、命令行参数或仓库。默认模型 deepseek-flash，可按我的账号可用模型调整。Key 只留本机，各电脑分别配置，不复制另一台的 .secrets 或令牌。
5. 优先检测已安装并登录的 Google Drive 桌面版，找到同一 Google 账号已有的“我的云端硬盘/Drive Vocabulary Book”文件夹。等待该文件夹完整下载并设为可离线使用，然后通过设置页连接它在本机的绝对路径。不同电脑的盘符可以不同。不要另建同名空词库，不要覆盖或清空云端 library.json / vocabulary-*.json。如果 Drive 尚未登录或尚未出现已有文件夹，只暂停这项并告诉我需要完成的登录/等待步骤，继续其他安装工作。
6. 启动词汇本，访问 http://127.0.0.1:1400，确认已有“法律英语”“金融英语”等单词本从云端恢复。同步采用双向合并，新电脑作为主力不需要清空或禁用旧电脑。保留两台各自的 words.json 本地缓存。
7. 检查 /api/health、/api/sync/status 和浏览器错误。Key 未配置时应标记为待配置，仍能手动保存和同步。连接检测不发送收费的生成请求；需要测试真实词汇补全时，使用我指定的一个词验证，保留我的正式词汇与学习进度。没有 Key 时不要声称真实 DeepSeek 调用已通过。
8. 完成后告诉我本机安装目录、启动方式、Drive 路径、当前 AI 配置状态、检查结果及任何仍需我处理的事项。默认无需创建远程部署、开机自启或推送任何个人数据。
```

## 功能

- 创建、重命名单词本与填写课程说明；相同拼写可在法律、金融本中保留不同释义。
- 按当前单词本搜索、筛选日期、复习与导出，也可跨本浏览。
- DeepSeek API 参考课程领域补全音标、中文释义和例句；手动内容不会被 AI 覆盖。
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

## DeepSeek API 配置

从 [DeepSeek 平台](https://platform.deepseek.com/api_keys) 创建 API Key，在“同步与备份 → DeepSeek API 词汇补全”填写并保存。Key 写入本机 `.secrets/deepseek.json`，页面不回显，且不进入 Drive 或 Git。每台电脑各自配置；修改后立即生效。

也支持启动进程的环境变量 `DEEPSEEK_API_KEY`、`DEEPSEEK_MODEL`。优先级为环境变量 > 本机设置页 > `config.json`。`config.json.example` 可复制为 `config.json`，示例中的空 Key 不影响启动。

默认使用当前官方模型名 `deepseek-flash`，请求 `https://api.deepseek.com/chat/completions`，采用 JSON Output 并关闭深度思考。可在设置页填写其他账号可用模型。[官方接入说明](https://api-docs.deepseek.com/) · [JSON 输出](https://api-docs.deepseek.com/guides/json_mode/) · [思考开关](https://api-docs.deepseek.com/guides/thinking_mode/)

补全会把当前单词与单词本的领域说明发送给 DeepSeek，并按其 API 规则计费；不会上传整本词库或复习历史。连接检查通过 `GET /models` 完成，不生成词汇。没有 Key、断网、鉴权失败或额度不足时，手动保存、同步和已有词汇复习仍可用；恢复后点击“补全缺失”。从旧 Ollama 版本更新时会在内存中切换到 DeepSeek，保留原有同步与复习配置。

## 同步方式一：Drive 桌面同步文件夹（推荐）

无需 Google Cloud 项目和 OAuth 客户端。

1. 两台电脑安装[桌面版 Google Drive](https://support.google.com/drive/answer/10838124?hl=zh-Hans)，登录同一个私人账号。
2. 在“我的云端硬盘”新建专用文件夹，例如 `Drive Vocabulary Book`，将它设为“可离线使用”。
3. 进入“同步与备份”，填写本机绝对路径，例如 `G:\我的云端硬盘\Drive Vocabulary Book`，点击“连接同步文件夹”。第二台电脑选择**同一个云端文件夹**，本机盘符可以不同。
4. 各自在本机运行程序。应用默认每 30 秒读取并合并变更。

**“待写入文件夹为 0”表示变更已交给 Drive 桌面版；实际上传/下载由桌面版完成。关闭电脑前还应确认 Drive 的同步状态为已完成。** 另一台电脑收到文件后，应用下一轮自动合并。

两台电脑的程序目录、`.venv`、`.secrets` 和 `words.json` 分别留在本机。云端目录只保存 `library.json` 身份标识及不可变的 `vocabulary-*.json` 变更文件。不要将整个项目或 `.secrets` 放入同步目录，不要手动编辑/删除变更文件。

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
  "provider": "deepseek",
  "deepseek": {"model": "deepseek-flash", "api_key": ""},
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
