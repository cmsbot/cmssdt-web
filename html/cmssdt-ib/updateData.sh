#!/usr/bin/env bash
rm -fr ./data/
svn checkout https://github.com/cms-sw/cms-sw.github.io/trunk/_data
mv ./_data ./data/
