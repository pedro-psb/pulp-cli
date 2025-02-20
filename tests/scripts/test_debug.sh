#!/bin/bash

# shellcheck source=tests/scripts/config.source
. "$(dirname "$(realpath "$0")")"/config.source

expect_succ pulp debug has-plugin --name "core" --max-version "4.0"
expect_succ pulp debug openapi spec
expect_succ pulp debug openapi operation-ids
expect_succ pulp debug openapi operation --id tasks_list
