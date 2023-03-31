---
title: PRL Library
---

This repo is a fork of the [Chirpy Theme](https://img.shields.io/gem/v/jekyll-theme-chirpy) by [cotes2020](https://img.shields.io/github/license/cotes2020/chirpy-starter.svg?color=blue)

# Pipeline

1. Hired writer submits summary to google form; auto saved to a google sheet
2. A script in `operations/library/` pushes from the google sheet to our RDS
3. Another script in `operations/library/` pulls from the RDS and generates local markdown files formatted in the way the Chirpy theme and Jekyll are expecting.
4. This repo is deployed as a github pages site, which is embedded in an iframe on our wordpress website.

![visualization of pipeline](pipeline.png)

