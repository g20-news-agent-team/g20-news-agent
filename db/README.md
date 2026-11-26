# G20 统一资料库开发库

使用 PostgreSQL 17 或 18、Python 3.14 和 uv。在可连接的 PostgreSQL 实例上用一个独立的开发库 `g20_dev` 进行导入验收。

## 建库与导入

从仓库根目录运行。使用部署机的数据库账号和连接地址，将实际连接串设置在本机环境变量 `G20_DATABASE_URL` 中。

```bash
createdb g20_dev
export G20_DATABASE_URL='postgresql://USER:PASSWORD@127.0.0.1:5432/g20_dev'
uv sync --project db --locked
uv run --project db --locked alembic -c db/alembic.ini upgrade head
uv run --project db --locked python db/import_documents.py
uv run --project db --locked python db/import_documents.py
```

使用团队 AIHOT Compose 的 PostgreSQL 时，可在其部署目录用 `docker compose -p g20-aihot exec -T db createdb -U aihot g20_dev` 建库。连接脚本可在 PostgreSQL 可访问的本地环境或同一 Docker 网络中运行。PowerShell 中用 `$env:G20_DATABASE_URL = 'postgresql://USER:PASSWORD@HOST:PORT/g20_dev'` 设置连接串。

导入脚本默认读取 `fixtures/documents.sample.jsonl` 和 `vendor/g20-sources.json`。可指定另一个标准 JSONL 文件，也可用 `--sources` 指定同格式的信源目录。

- `sources` 沿用信源目录中的 ID。现有样例中的「外交部」「新华网」会映射到对应信源。
- `documents` 使用来源 ID 和标准化的原文链接作为唯一键，`url` 接收转换脚本产出的规范链接。重复导入沿用资料 UUID。同一链接补到全文时，可以用全文补全原有摘要记录。
- `publishedAt` 和 `fetchedAt` 接收带时区的 ISO 日期时间或空值。导入会保留输入提供的 `originalUrl`、`publisher`、`author`、`sourceLabel` 和 `section`。
- 样例中的 `type` 写入 `suggested_type`。资料入库时处于待复核状态，确认后填写 `document_type`、`classification_reason`，并将 `review_status` 更新为 `confirmed`。

## 验收查询

在 `g20_dev` 中执行。对空库导入样例两遍，首次新增 2 条，第二次新增或补全 0 条，验收记录数和 ID 保持一致。

```sql
SELECT count(*) FROM documents;

SELECT id, source_id, title, content_text, original_url, suggested_type, review_status
FROM documents
ORDER BY source_id, canonical_url;

SELECT id, title, content_text, original_url
FROM documents
WHERE document_type = 'official_release' AND review_status = 'confirmed';
```
