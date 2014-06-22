#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import bencode
import random
import string
import sys
from os import path
from bencode import BTFailure


def random_string():
    r = ''.join(
        random.choice(
            string.ascii_uppercase +
            string.digits) for x in range(6))
    return r


def trash_useless(data):  # dump useless info
    keys = [
        'publisher-url',
        'publisher',
        'publisher-url.utf-8',
        'publisher.utf-8',
        'name.utf-8',]
    for k in keys:
        if k in data['info']:
            data['info'].pop(k)
    if 'comment' in data:
        data.pop('comment')
    return data

# differents see
# https://wiki.theory.org/BitTorrentSpecification#Info_Dictionary


def single_file(info):
    dot_index = info['name'].rfind(".")  # find the last . in the file
    if dot_index != -1:
        # random file name
        info['name'] = random_string() + info['name'][dot_index:]
    return info


def multi_file(info):
    info['name'] = random_string()
    for i in info['files']:
        if 'path' in i:
            i['path'] = short_and_random(i)
        if 'path.utf-8' in i:
            i.pop('path.utf-8')
    return info


def short_and_random(item):
    # the file is the last one of a path list
    dot_index = item['path'][-1].rfind(".")
    if dot_index != -1:
        # no more folder just file
        return [random_string() + item['path'][-1][dot_index:]]


def lu_torrent(torrent):
    try:
        decoded_data = bencode.bdecode(torrent.read())
        old_info = decoded_data['info']
    except BTFailure:
        print "error, not a valid torrent."
    else:
        if 'files' in old_info:
            decoded_data['info'] = multi_file(old_info)
        else:
            decoded_data['info'] = single_file(old_info)
        split_path = path.split(path.abspath(sys.argv[1]))
        new_torrent = open(path.join(split_path[0], 'new_' + split_path[1]), "wb")
        new_torrent.write(bencode.bencode(trash_useless(decoded_data)))
        new_torrent.close()
        torrent.close()

if __name__ == '__main__':
    try:
        old_torrent = open(sys.argv[1], "rb")
    except IOError:
        print "error, can not open torrent file."
    else:
        lu_torrent(old_torrent)