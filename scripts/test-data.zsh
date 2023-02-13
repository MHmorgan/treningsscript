#!/usr/bin/env zsh
# vim: expandtab:

alias run='python app'

if [[ ! -f db.sqlite ]]; then
    run initdb
fi

run exercises new 'Dips' 'Bodyweight' Push
run exercises new 'Pullup, vektapparat' 'Each Arm' Pull
run exercises new 'Squats' 'Bodyweight' Legs
run exercises new 'Utfall' Bodyweight Legs

run exercises entry Dips 2023-01-01 6 6 6 -r 1
run exercises entry Utfall 2023-01-02 8 8 8 8 -r 2
run exercises entry Squats 2023-01-02 8 8 8 8 -r 1 -w 80
