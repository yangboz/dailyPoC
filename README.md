# dailyPoC
daily Proof of concept by coding with AI 每日AI原型验证

concept：

1. 应用功能设计

核心功能（理想的）

AI 技能学习模块：
提供 AI 基础知识、机器学习、深度学习等课程。
每个课程包含视频、文档和练习题。
代码实践环境：
提供在线的 Python 代码编辑器，支持运行 AI 相关代码（如 TensorFlow、PyTorch）。
AI 助手：
基于 DeepSeek API 的智能助手，回答用户问题，提供学习建议。
学习进度跟踪：
记录用户的学习进度和成绩。
社区互动：
用户可以在社区中提问、分享经验和参与讨论。

于是以每日AI tips为MVP起步

2. 技术栈

前端：HTML5、CSS、JavaScript（React 或 Vue.js 可选）。
后端：Python（Flask 或 FastAPI）。
AI 服务：DeepSeek API 或其他国内 AI 平台。
数据库：MySQL 或 MongoDB（存储用户数据和学习记录）。
部署：Nginx + Gunicorn（后端），Vercel 或阿里云（前端）。
3. 前端实现

以下是一个简单的 HTML5 前端页面，包含学习模块和AI TIPS 生成及接收。

