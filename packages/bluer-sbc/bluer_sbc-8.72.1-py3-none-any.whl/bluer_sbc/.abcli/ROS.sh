#! /usr/bin/env bash

function bluer_sbc_ROS() {
    local task=$1

    local function_name=bluer_sbc_ROS_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    python3 -m bluer_sbc.ROS "$@"
}

bluer_ai_source_caller_suffix_path /ROS
