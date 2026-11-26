# 仓库内置的 AIHOT 采集

`aihot-source.tar.gz` 包含 AIHOT 上游提交 `5ffe226dd2da32672de4b8290507a6631ae2e992` 的源码、MIT 许可证、本地正文门槛改动及 G20 采集脚本。

在团队仓库根目录用 Node.js 24.22.1 或更新版本运行：

```bash
bash vendor/run-aihot.sh
node scripts/g20-documents.ts
```

运行脚本将源码解压到临时目录，安装锁定的 npm 依赖并用两个固定文章地址生成 `fixtures/raw.sample.jsonl`，无需克隆另一份仓库或部署 AIHOT。需要离线解析网页时，可使用 `bash vendor/run-aihot.sh --html-dir /path/to/pages`，目录内放置 `xinhua.html`、`mfa.html`。首次安装 npm 依赖需要网络或本地缓存。
