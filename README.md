# 小红书爬虫服务

基于 FastAPI + Playwright 的小红书采集服务，支持：
- 关键词搜索采集
- 详情抓取
- 评论抓取
- 导出 Excel

## 目录
- `app/` 主应用代码
- `data/exports/` 导出文件目录
- `requirements.txt` Python 依赖

## 快速启动

1. 安装依赖

```bash
pip install -r requirements.txt
playwright install chromium
```

2. 启动服务

```bash
python -m uvicorn app.main:app --port 8005
```

3. 打开接口文档

- http://127.0.0.1:8005/docs

## 采集接口

- 路径：`POST /xhs/crawl`
- 请求体参数：
  - `keyword`：搜索关键词（例如：咖啡）
  - `page_count`：采集页数
  - `page_size`：每页数量
  - `sort`：排序方式（默认 `general`）
  - `need_detail`：是否抓详情
  - `need_comments`：是否抓评论
  - `comment_limit`：评论数量上限
  - `need_export`：是否导出文件

请求示例：

```json
{
  "keyword": "咖啡",
  "page_count": 1,
  "page_size": 3,
  "sort": "general",
  "need_detail": true,
  "need_comments": false,
  "comment_limit": 5,
  "need_export": true
}
```

## 导出文件

导出结果默认保存到：
- `data/exports/`

## 说明

仅用于学习与测试，请遵守目标平台服务条款与相关法律法规。
