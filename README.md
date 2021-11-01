# CTF Writeups

This is a collection of writeups for various CTFs, formatted using [The Hacker CTF Theme](https://github.com/Nissen96/hacker-ctf-theme). Using this theme makes it very easy to write new writeups:

*Run the script -> Write in markdown -> Push commit -> The site is generated automatically*

The site is running [here](https://Nissen96.github.io)

*Some useful snippets for markdown included in the template project:*

| Prefix       | Description                                        |
|:-------------|:---------------------------------------------------|
| cmdbashdown  | To add a code block with bash prompt and download  |
| cmdbash      | To add a code block with bash prompt               |
| cmdotherdown | To add a code block with other prompt and download |
| cmdother     | To add a code block with other prompt              |
| down         | Downloadable code                                  |
| linenum      | Code block with line numbers                       |
| linenumdown  | Downloadable code with line numbers                |


## Usage

1. Open a new terminal window in VS Code
2. Run `python scripts/writeup_gen.py` and fill in the details. The script generates the required writeup files and asset directory for the CTF
3. Write the writeups in markdown and push the commits to your repo

To preview changes locally:

1. Run `gem install bundler` and `bundle install` once to install dependencies
2. Run `bundle exec jekyll serve` to start a preview server with hot reloading
3. Visit [`localhost:4000`](http://localhost:4000)` to preview changes.