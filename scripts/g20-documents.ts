import { createHash, randomUUID } from 'node:crypto';
import { mkdir, readFile, rename, rm, writeFile } from 'node:fs/promises';
import { dirname } from 'node:path';

type RawRecord = {
  url?: string;
  title?: string;
  source?: string;
  publishedAt?: string | null;
  summary?: string | null;
  body?: { text?: string | null } | null;
};

const [input = 'fixtures/raw.sample.jsonl', output = 'fixtures/documents.sample.jsonl'] = process.argv.slice(2);
const lines = (await readFile(input, 'utf8')).replace(/^\uFEFF/, '').split(/\r?\n/);
const documents = new Map<string, { contentKind: string }>();
for (const [index, line] of lines.entries()) {
  if (!line.trim()) continue;
  try {
    const raw: RawRecord = JSON.parse(line);
    const title = raw.title?.trim();
    const source = raw.source?.trim();
    if (!raw.url || !title || !source) throw new Error('缺少 URL、标题或来源');
    const url = new URL(raw.url);
    if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password) throw new Error('无效原文 URL');
    url.hash = '';
    for (const key of [...url.searchParams.keys()]) {
      if (/^utm_/i.test(key)) url.searchParams.delete(key);
    }
    const canonicalUrl = url.href;
    const fullText = raw.body?.text?.trim() || '';
    const summary = raw.summary?.trim() || '';
    const text = fullText || summary;
    // Some pages put their headline in the description meta tag.
    if (!text || (!fullText && text.replace(/\s/g, '') === title.replace(/\s/g, ''))) throw new Error('缺少正文或有效摘要');
    const time = raw.publishedAt ? Date.parse(raw.publishedAt) : NaN;
    const official = /(^|\.)mfa\.gov\.cn$/.test(url.hostname);
    const document = {
      id: createHash('sha256').update(canonicalUrl).digest('hex'),
      url: canonicalUrl,
      title,
      text,
      contentKind: fullText ? 'full_text' : 'summary',
      type: official ? 'official_release' : 'news_report',
      source,
      publishedAt: Number.isFinite(time) ? new Date(time).toISOString() : null,
    };
    const previous = documents.get(canonicalUrl);
    if (!previous || (previous.contentKind === 'summary' && fullText)) documents.set(canonicalUrl, document);
  } catch (error) {
    throw new Error(`${input} 第 ${index + 1} 行转换失败`, { cause: error });
  }
}
if (!documents.size) throw new Error('输入文件没有记录');
await mkdir(dirname(output), { recursive: true });
const temporary = output + '.' + randomUUID() + '.tmp';
try {
  await writeFile(temporary, [...documents.values()].map(document => JSON.stringify(document)).join('\n') + '\n');
  await rename(temporary, output);
} finally {
  await rm(temporary, { force: true });
}
console.log(`写入 ${documents.size} 条记录到 ${output}`);
