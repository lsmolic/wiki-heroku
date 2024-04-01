#!/usr/bin/env sh

_() {
  while getopts u:a:f: flag
  do
    case "${flag}" in
        u) USERNAME=${OPTARG};;
        a) ACCESS_TOKEN=${OPTARG};;
        y) YEAR=${OPTARG};;
        m) MONTH=${OPTARG};;
        d) DAY=${OPTARG};;
    esac
  done
  [ -z "$USERNAME" ] && exit 1
  [ -z "$ACCESS_TOKEN" ] && exit 1  
  [ -z $MONTH ] && exit 1
  [ -z $DAY ] && exit 1
  [ -z $YEAR ] && exit 1

  tr -dc A-Za-z0-9 </dev/urandom | head -c 13; echo \
    >README.md
  git add .
  GIT_AUTHOR_DATE="${YEAR}-${MONTH}-${DAY}T18:00:00" \
    GIT_COMMITTER_DATE="${YEAR}-${MONTH}-${DAY}T18:00:00" \
    git commit -m "${YEAR}-${MONTH}-${DAY}"
  #git remote add origin "https://${ACCESS_TOKEN}@github.com/${USERNAME}/${YEAR}.git"
  #git branch -M main
  #git push -u origin main -f
  #cd ..
  #rm -rf "${YEAR}"
  #echo
  echo "Cool, check your profile now: https://github.com/${USERNAME}"
} && _

unset -f _
