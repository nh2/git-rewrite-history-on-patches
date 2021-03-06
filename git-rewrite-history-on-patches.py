#!/usr/bin/env python3

# Script to replace words in a range of recent git commits.
# See README for details.

import re
import sys

# Put your replacements in here; they are run in order.
# The replacement looks only at a single line.
replacements = [
  ('floor', 'level'),
  ('Floor', 'Level'),
  ('levelMarker', 'floorMarker'),
  ('LevelMarker', 'FloorMarker'),
  ('level marker', 'floor marker'),
  ('levelPlan', 'floorPlan'),
  ('LevelPlan', 'FloorPlan'),
  ('levelplan', 'floorplan'),
  ('level plan', 'floor plan'),
  ('Level Plan', 'Floor Plan'),
  ('Math.level', 'Math.floor'),
]

def do_replacements(s):
  did_replace = False
  for (old, new) in replacements:
    if not did_replace and old in line:
      did_replace = True
    s = s.replace(old, new)
  return (s, did_replace)


files = sys.argv[1:]

# The algorithm:
#
# * Walk each diff line.
# * Run the replacement on each '+' line.
# * Remembering changes:
#   If we replace `+a` -> `+b`, we also have to replace
#   `-a` -> `-b` and ` a` -> ` b` (context hunks) so that subsequent
#   patches don't conflict.

# TODO Currently the algorithm is crude and not perfect because
#      replacement are remembered just by line contents, independent
#      from (1) in which file they occur and (2) where in the file
#      they occur.
#      (1) could be fixed by tracking which files the changes were made
#      by parsing the diff,
#      (2) would be more difficult to fix; we'd have to rememer exactly
#      which line is at which line number in which file.
replaced_additions = {}


for file in files:
  lines = open(file).readlines()
  for i, line in enumerate(lines):
    new_line = line
    did_replace = False
    if not line.startswith('---') and not line.startswith('+++'):
      # Additions
      if line.startswith('+'):
        new_line, did_replace = do_replacements(line)

        if did_replace:
          replaced_additions[line[1:]] = new_line[1:] # chop off '+'

      # Deletions
      if line.startswith('-') and line[1:] in replaced_additions: # chop off '-'
        new_line = '-' + replaced_additions[line[1:]]
        did_replace = True

    # Hunk contexts
    if line.startswith(' ') and line[1:] in replaced_additions: # chop off ' '
      new_line = ' ' + replaced_additions[line[1:]]
      did_replace = True

    lines[i] = new_line

    if did_replace:
      print(line, end='')
      print(new_line, end='')
      print()

  open(file+'.new', 'w').writelines(lines)
