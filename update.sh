#!/bin/sh

echo "commit message: "
# shellcheck disable=SC2162
read commit_message

git add .
git commit -am "$commit_message"
git push

cd ~/.local/share/rhythmbox/plugins/rythmbox-id3-lyrics-support
git pull

pkill rhythmbox
rhythmbox -D src
