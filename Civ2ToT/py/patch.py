"""
This patch for Civ 2 ToT v.1.1 unifies two patches, adapted for this game:

1) "attitude" patch for Civ2 MGE [https://forums.civfanatics.com/threads/civ-2-mge-ai-aggressiveness-patch.509103/]

2) my own patch "Preventing mass betrayal after 1 AD" for Civ 1 [https://civilization.fandom.com/wiki/Cheating_(Civ1)]

Placed at .\Civ2ToT\py\patch.py at launch it replaces civ2.exe with patched version,
meanwhile making a copy of the oriignal version as civ2.orig.
civ2.orig file is used as a reference for further repatching.

This patch has been made to make AI more rational and adequately peaceful.
This is 24th February, 2022. Say no to war. #SupportUkraine #UnitedForUkraine
"""

import re
from os.path import join as pj
from os.path import exists
from shutil import copyfile as cp

CIV2_EXEC = 'civ2.exe'
CIV2_BASE = 'civ2.orig'

p = lambda fn: pj('..', fn)

ce = p(CIV2_EXEC)
cb = p(CIV2_BASE)

if not exists(cb):
	cp(ce, cb)
	
with open(cb, 'rb') as f:
	cnt = bytearray(f.read())

cmds = [
	{		
		're': b'\xE8\x53...\x83\xC4\x0C',
		'pos_start': 0,
		'pos_finish': 0,
		'offset': 0,
		'length': 8,
		'replace': [0x90] * 8
	},
	{
		're': b'\x0F\xBF\x05....\x3D\xC8\x00\x00\x00\x0F\x8E',
		'pos_start': 0,
		'pos_finish': 0,
		'offset': 8,
		'length': 2,
		'replace': [0xff, 0x7f]
	},
]

for cmd in cmds:	
	patterns = [p for p in re.finditer(cmd['re'], cnt)][cmd['pos_start']:cmd['pos_finish'] + 1]
	for pattern in patterns:
		replace = cmd['replace'][:]
		stpt = pattern.span()[0] + cmd['offset']
		fnpt = stpt + cmd['length']
		for pt in range(stpt, fnpt):
			cnt[pt] = replace.pop(0)

with open(ce, 'wb') as f:
	f.write(cnt)
