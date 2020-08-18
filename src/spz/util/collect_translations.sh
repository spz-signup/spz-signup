#!/usr/bin/env sh

pybabel extract -F i18n.build/babel.conf -o i18n.build/messages.pot .
# pybabel init -i i18n.build/messages.pot -d i18n.build -l en
pybabel update -i i18n.build/messages.pot -d i18n.build
pybabel compile -d i18n.build
