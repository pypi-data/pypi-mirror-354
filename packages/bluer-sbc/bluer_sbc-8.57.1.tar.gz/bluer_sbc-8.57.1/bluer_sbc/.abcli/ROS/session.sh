#! /usr/bin/env bash

function bluer_sbc_ROS_session() {
    local options=$2
    local do_dryrun=$(bluer_ai_option_int "$options" dryrun 0)
    local do_upload=$(bluer_ai_option_int "$options" upload 1)

    bluer_ai_log "@sbc.ROS: session @ $abcli_object_name started ..."

    bluer_objects_mlflow_tags_set \
        $abcli_object_name \
        session,ROS,host=$abcli_hostname,$BLUER_SBC_SESSION_OBJECT_TAGS

    bluer_ai_eval dryrun=$do_dryrun \
        python3 -m bluer_sbc.ROS \
        ${task}_session \
        "${@:3}"
    local status="$?"

    [[ "$do_upload" == 1 ]] &&
        bluer_objects_upload - $abcli_object_name

    bluer_ai_log "@sbc.ROS: session ended."

    return $status
}
