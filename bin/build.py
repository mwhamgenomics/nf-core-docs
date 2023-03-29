import os
import shutil
import json
import glob
import subprocess
import requests
import datetime
import argparse

a = argparse.ArgumentParser()
a.add_argument('repo_dir', help='Directory containing an nf-core template pipeline to build docs from')
a.add_argument('gh_org', help='GitHub organisation/user this pipeline is under')
a.add_argument('gh_name', help='Name of the pipeline GitHub project')
args = a.parse_args()

original_dir = os.getcwd()
os.chdir(args.repo_dir)
tags = subprocess.check_output(['git', 'tag']).decode().strip().split('\n')
current_tag = subprocess.check_output(['git', 'tag', '--points-at', 'HEAD']).decode().strip()

data = requests.get(
    'https://api.github.com/repos/%s/%s' % (args.gh_org, args.gh_name)
).json()

releases = [
    {
        'tag_name': tag,
        'published_at': datetime.datetime.strptime(
            subprocess.check_output(
                ['git', 'log', tag, '--date=format:%Y-%m-%d %H:%M:%S']
            ).decode().strip().split('\n')[2],
            '%Y-%m-%d %H:%M:%S'
        )
    }
    for tag in subprocess.check_output(['git', 'tag']).decode().strip().split('\n') if tag
]

releases.append({'tag_name': 'dev', 'published_at': str(datetime.datetime.now())})

doc_files = [
    f for f in glob.glob('docs/*.md')
    if 'README' not in f
]

with open('modules.json') as f:
    modules = json.load(f)    

if 'nf-core/modules' in modules['repos']:
    if 'modules' in modules['repos']['nf-core/modules']:
        modules = list(modules['repos']['nf-core/modules']['modules'])
    else:
        modules = list(modules['repos']['nf-core/modules'])
elif 'https://github.com/nf-core/modules.git' in modules['repos']:
    modules = list(modules['repos']['https://github.com/nf-core/modules.git']['modules']['nf-core'])
else:
    modules = []
    
modules = [m.replace('/', '_') for m in modules]

data['releases'] = releases
data['open_pr_count'] = len(
    requests.get(
        'https://api.github.com/repos/%s/%s/pulls?state=open' % (args.gh_org, args.gh_name)
    ).json()
)
data['contributors'] = [
    {'name': c['login'], 'count': c['contributions']}
    for c in requests.get('https://api.github.com/repos/%s/%s/contributors' % (args.gh_org, args.gh_name)).json()
    if c['login'] != 'nf-core-bot'
]
data['md_files'] = doc_files
data['current_tag'] = current_tag or 'dev'

os.chdir(original_dir)

os.makedirs('public/images', exist_ok=True)
image_dir = os.path.join(args.repo_dir, 'docs', 'images')
if os.path.isdir(image_dir):
    for img in os.listdir(image_dir):
        shutil.copy(os.path.join(image_dir, img), 'public/images')

with open('public/pipeline_info.json', 'w') as f:
    json.dump(data, f, indent=4)

# npm install astro
# cp ../nf-co.re/astro.config.mjs .
# cp ../nf-co.re/tsconfig.json .

# cache = {}
# with open('public/pipelines.json') as f:
#    pipelines_json = json.load(f)
   
# # go through the releases of each pipeline and get the files which are needed for the pipeline pages
#         release['doc_files'].append('README.md')
#         release['doc_files'].append('nextflow_schema.json')
#         version = release['tag_name']
#         for f in release['doc_files']:
#             cache_key = '%s/%s/%s' % (pipeline['name'], version, f)
#             is_cached = len(cache.get(cache_key, [])) > 0
#             if not is_cached:
#                 data = requests.get('https://api.github.com/repos/%s/%s/contents/%s?ref=%s' % (pipeline['owner']['login'], pipeline['name'], f, version)).json()
#                 content = base64.b64decode(data['content']).decode()
#                 if f.endswith('.md'):
#                     parent_directory = '/'.join(f.split('/')[:-1])

#                 # add github url to image links in markdown, e.g. ![MultiQC - FastQC sequence counts plot](images/mqc_fastqc_counts.png)
#                 content = re.sub(
#                     r'!\[([^\]]+)\]\(([^\)]+)\)',
#                     lambda match: '![%s](https://raw.githubusercontent.com/%s/%s/%s/%s/%s)' % (
#                         match.group(1), pipeline['owner']['login'], pipeline['name'], version, parent_directory, match.group(2)
#                     ),
#                     content
#                 )

#                 # add github url to html img tags in markdown
#                 content = re.sub(
#                     r'<img ([^>]+) src="([^"]+)" ([^>]+)>',
#                     lambda match: '<img %s src="https://raw.githubusercontent.com/%s/%s/%s/%s/%s" %s>' % (
#                         match.group(1), pipeline['owner']['login'], pipeline['name'], version, parent_directory, match.group(2), match.group(3),
#                     ),
#                     content
#                 )
#                 # remove github warning and everything before from docs
#                 content = re.sub(r'.*## :warning: ', '', content, flags=re.DOTALL)
                
#                 # remove blockquote ending in "files._" from the start of the document
#                 content = re.sub(r'.+files\._', '', content)
                
#                 # cleanup heading
#                 content = content.replace('# %s/%s: ' % (pipeline['owner']['login'], pipeline['name']), '# ')
                
#                 # remove everything before introduction
#                 content = re.sub(r'.*# Introduction', '', content, flags=re.DOTALL)
              
#             cache[cache_key] = content

