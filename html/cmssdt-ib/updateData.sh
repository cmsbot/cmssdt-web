#!/usr/bin/env bash
rm -fr ./html/data/
rm -fr /tmp/cms-io
git clone --depth 1 https://github.com/cms-sw/cms-sw.github.io/ /tmp/cms-io
mv /tmp/cms-io/_data/* ./SDT/html/data/
