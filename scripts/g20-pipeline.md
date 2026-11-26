# G20 样例采集与转换

两份交接样例在团队仓库的 `fixtures/`。C 可以直接使用 `documents.sample.jsonl` 测试导入及重复导入，`publishedAt` 允许为 null。

A 在单独的 AIHOT 副本里运行采集。已验证的上游提交是 `5ffe226dd2da32672de4b8290507a6631ae2e992`。下方假设两个仓库在同一级目录。从团队仓库根目录运行。

```bash
git clone https://github.com/KKKKhazix/AIHOT.git ../AIHOT
git -C ../AIHOT checkout 5ffe226dd2da32672de4b8290507a6631ae2e992
git -C ../AIHOT apply ../g20-news-agent/scripts/remove-body-minimum.patch
cp scripts/g20-collect.ts ../AIHOT/scripts/
(cd ../AIHOT && npm ci && node scripts/g20-collect.ts --output ../g20-news-agent/fixtures/raw.sample.jsonl)
```

采集脚本针对新华网短讯和外交部通稿两个固定地址。若环境触发公网地址拦截，可手动保存两篇原页为 `xinhua.html` 和 `mfa.html`，然后给采集命令加上 `--html-dir <目录>`。本次样例使用真实网页 HTML 离线验证。

B 在团队仓库根目录运行 `node scripts/g20-documents.ts`（Node.js 24），读取原始样例并生成标准 JSONL。C 直接使用仓库中的样例时无需部署 AIHOT。
