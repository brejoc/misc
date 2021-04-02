## 🛑️ ATTENTION 🛑️

This project moved to [brejoc/teampulls](https://github.com/brejoc/teampulls).



# What is it?

This little script lists you all of the pull requests for a list of users from a list of repositories. On top of that every pull requests that is older than 14 days is printed in red.

# Get started

In order to use open_prs.py follow these steps:

## Create the virtualenv
```
$ virtualenv -p <path-to-python3> sandbox3
$ . ./sandbox3/bin/activate
(sandbox3) $ pip install -r requirements.txt
```

## Edit the settings file

Please take a look at `open_prs.toml`. There you'll have to add the users and repositories you are interested in. The Github API token can either also be set in this settings file or via the environment variable `GITHUB_TOKEN_GALAXY`.

## Start the script

At first you'll have to switch to the virtualenv again if you haven't done so already: `. ./sandbox3/bin/activate`

Now you can execute the script:

<img src="https://raw.githubusercontent.com/brejoc/misc/master/SUSE/open_prs/doc/screenshot1.png" />
