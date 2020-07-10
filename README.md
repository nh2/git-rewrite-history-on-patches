# git-rewrite-history-on-patches

Script to replace words in a range of recent git commits.

Works by:

* exporting the range using `git format-patch`
* doing search-and-replace on the .patch files (that's what this script does)
* re-importing the patches using `git am`.

## Example usage

To replace some words (defined in the script) in the last 9 commits on `mybranch`:

```sh
git checkout mybranch
git branch mybranch-backup # always first make a backup!
```

```sh
# Clean up stuff from previous iterations to get the replacements right
git am --abort
rm -rf patches
git reset --hard mybranch-backup

# Run
git format-patch --output-directory patches mybranch~9
./git-rewrite-history-on-patches.py patches/*.patch
git reset --hard mybranch~9
git am --ignore-whitespace patches/*.patch.new
```

If a patch doesn't apply, you can check whether it was rewritten correctly using a diff-tool, e.g.

```sh
meld patches/0001*
```
