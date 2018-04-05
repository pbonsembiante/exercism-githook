# Exercism GitHook

This is a very simple hook to submit [exercism](http://exercism.io) challenges
on git commit.

It will process on the [pre-commit](https://git-scm.com/docs/githooks#_pre_commit)
hook provided bit git submitting any exercism challenge individually.

## Requirements

* [exercism-cli](http://exercism.io/clients/cli)
* [git](http://git-scm.com)
* A few considerations on the git repository containing the exercism challenges

## Installing

In the meantime, the hook can be installed manually, in a per-repository bases,
placing the pre-commit.py file in this repo into `.git/hooks` and dropping
the `.py` extension out of it.

### Unix-like systems

An install script is provided to automatically install the hook in the right place!

```
git clone https://github.com/pbonsembiante/exercism-githook
cd exercism-githook
chmod +x install.sh
./install.sh
```

### Windows

I'll provide a similar batch scripts to automatically install the hook soon.

## Usage

Once installed the hook will trigger before the `git commit` is executed
preventing the commit if there are any errors submitting the files to `exercism`

To prevent the hook from executing add `--no-verify` to the `git commit` command.
This will prevent the hook execution completely making the commit proceed as usual.


**_TODO: Provide output samples_**

## Licence

This code is released under [The GNU General Public License v3](./COPYING)
