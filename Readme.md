# nf-core docs

This repo is part of a project to make it possible to build [nf-core](https://nf-co.re/)-styled
documentation for community pipelines that follow the [nf-core template](https://nf-co.re/tools/#creating-a-new-pipeline),
independently of the system for building documentation for published pipelines on the nf-core
website.


## About this project

This repo uses [Astro](https://astro.build), a static site builder/publisher. The build process
consists of:

- Query the GitHub API for metadata on releases, users, etc
- Copy pipeline/docs/images to public/, where Astro can access and server them
- Cache the contents of the .md doc files
- Build via the layout and component files, and serve

Underneath, this uses components from the nf-core website, stripped down to remove unneeded features.


## Usage

This project requires [nodejs](https://nodejs.org). To set up:

    $ npm install
    $ python bin/build.py path/to/repo gh-repo-owner gh-repo-name
    $ npm run build-cache path/to/repo

You can then run a local test server with either of:

    $ npm run start
    $ npm run preview

Or you can build it into a static site at `dist/` with:

    $ npm run build

## Roadmap

- Make it possible to build any documentation mini-site without overwriting the caches
- Figure out how to keep this repo in sync with the layout and styling of the nf-core website
- Make sure the markdown rendering works with documentation written in RTL and other non-Latin scripts
- Figure out how to use Actions to publish to GitHub pages
