#! /usr/bin/env node
import Cache from 'file-system-cache';
import { readFileSync, readdirSync, statSync } from 'fs';
import { execSync } from 'child_process';
import path from 'path';

if (process.argv.length < 3) {
  console.log('Usage: node build-cache.js <pipeline_project_dir> [--force]');
  process.exit(0)
}

// get current path
const __dirname = path.resolve();

const cache = Cache.default({
  basePath: './.cache',
  ns: 'nf-core',
});

function walkDir(dir) {
  let files = [];
  for (const f of readdirSync(dir)) {
      const stat = statSync(`${dir}/${f}`);
      if (stat.isDirectory()) {
          files = files.concat(walkDir(`${dir}/${f}`));
      } else {
          files.push(`${dir}/${f}`);
      }
  }
  return files;
}

// check for `--force` flag
const buildDir = process.argv.filter(a => a != '--force')[2]

const buildCache = async () => {
  const pipelineJson = readFileSync(path.join(__dirname, 'pipeline_info.json'));
  const pipeline = JSON.parse(pipelineJson);

  const owner = pipeline.owner.login;
  const doc_files = walkDir(path.join(buildDir, 'docs'));
  doc_files.push(path.join(buildDir, 'README.md')); // add the top-level README to the cache
  doc_files.push(path.join(buildDir, 'nextflow_schema.json')); // add the nextflow_schema.json to the cache

  for (const f of doc_files) {
    const splitF = f.split('/');
    const cache_key = splitF.slice(1, splitF.length).join('/');
    console.log('Caching ', cache_key);
    let content = readFileSync(f, {encoding: 'utf-8'});
    if (f.endsWith('.md')) {
      const parent_directory = f.split('/').slice(0, -1).join('/');
      // add github url to image links in markdown
      // content = content.replaceAll(/!\[(.*?)\]\((.*?)\)/g, (match, p1, p2) => {
      //   return `![${p1}](https://raw.githubusercontent.com/${owner}/${pipeline.name}/${version}/${parent_directory}/${p2})`;
      // });
      // add github url to html img tags in markdown
      // content = content.replaceAll(/<img(.*?)src="(.*?)"/g, (match, p1, p2) => {
      //   return `<img${p1}src="https://raw.githubusercontent.com/${owner}/${pipeline.name}/${version}/${parent_directory}/${p2}"`;
      // });
      // remove github warning and everything before from docs
      content = content.replace(/(.*?)(## :warning:)(.*?)(\n)/s, '');
      // remove blockquote ending in "files._" from the start of the document
      content = content.replace(/(.*?)(files\._)/s, '');
      // cleanup heading
      content = content.replace(`# ${owner}/${pipeline.name}: `, '# ');
      // remove everything before introduction
      content = content.replace(/.*?# Introduction/gs, '## Introduction');
    }
    cache.set(cache_key, content);
  }
};
buildCache();
