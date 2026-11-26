import { mkdir, readFile, rename, rm, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { randomUUID } from 'node:crypto';
import { parseArgs } from 'node:util';
import { load } from 'cheerio';
import { readable } from '../packages/backend/src/content/extract.ts';
import { guardedFetch, requireOk } from '../packages/backend/src/lib/http-fetch.ts';

const samples = [
  {
    id: 'xinhua',
    url: 'https://www.news.cn/world/20261030/d5665a61eecb43eba27905a37358b390/c.html',
    source: '新华网',
    titleSelector: 'h1 .title',
    dateSelector: '.mheader .info',
    bodySelector: '#detailContent',
  },
  {
    id: 'mfa',
    url: 'https://www.mfa.gov.cn/web/zyxw/202511/t20251124_11758564.shtml',
    source: '外交部',
    titleSelector: 'h1',
    dateSelector: '.time',
    bodySelector: '.TRS_UEDITOR',
  },
];

const { values } = parseArgs({ options: {
  'html-dir': { type: 'string' },
  output: { type: 'string', default: 'fixtures/raw.sample.jsonl' },
} });

const records = [];
for (const sample of samples) {
  try {
    const html = values['html-dir']
      ? await readFile(join(values['html-dir'], sample.id + '.html'), 'utf8')
      : requireOk(await guardedFetch(sample.url), sample.id).text();
    const $ = load(html);
    const title = $(sample.titleSelector).first().text().trim();
    const summary = $('meta[name="description" i]').first().attr('content')?.trim() || null;
    const article = $(sample.bodySelector).first().html();
    if (!title || !article) throw new Error('Page layout did not match the article selectors');

    const page = load('<!doctype html><html><head><title></title></head><body><article></article></body></html>');
    page('title').text(title);
    page('article').html(article);
    const body = readable(page.html(), sample.url);
    if (!body) throw new Error('AIHOT returned no body. Check the HTML and the minimum-length patch.');

    const date = $(sample.dateSelector).text().match(/[0-9]{4}-[0-9]{2}-[0-9]{2}\s+[0-9]{2}:[0-9]{2}(?::[0-9]{2})?/)?.[0];
    const publicationTime = date ? date.replace(/\s+/, 'T') + (date.trim().length === 16 ? ':00' : '') + '+08:00' : null;
    const parsedTime = publicationTime ? Date.parse(publicationTime) : NaN;
    records.push({
      url: sample.url,
      source: sample.source,
      publicationTime: Number.isFinite(parsedTime) ? publicationTime : null,
      publishedAt: Number.isFinite(parsedTime) ? new Date(parsedTime).toISOString() : null,
      title,
      summary,
      body,
    });
  } catch (error) {
    throw new Error(`收集 ${sample.id} 失败（${sample.url}）`, { cause: error });
  }
}
await mkdir(dirname(values.output), { recursive: true });
const temporary = values.output + '.' + randomUUID() + '.tmp';
try {
  await writeFile(temporary, records.map(record => JSON.stringify(record)).join('\n') + '\n');
  await rename(temporary, values.output);
} finally {
  await rm(temporary, { force: true });
}
console.log(`写入 ${records.length} 条记录到 ${values.output}`);
