# ELECTRO-HOBBY-3D-UPDATER: requirements

This register is the single source of the state of each capability: `STATUS.md` and the README files cite it and never state a state that it does not. A state is one of `planned`, `prototype`, `implemented` and `validated`. `validated` means that a person has run the capability on a real machine and the evidence of the manifest says `bench` or `field`; nothing here is validated, because the runs that the maintainer made by hand on his own computer are not tied to a test that anybody can repeat, so no row is marked from memory.

The register has 34 requirements: 29 implemented, 1 prototype, 4 planned and 0 validated. By progress: 29 done, 1 partial, 0 pending and 4 blocked. High coverage is not proof of correctness, so each row says how it is checked: the test that names it, and what it shows.

## How to read the register

* **ID:** `EHUP-NNN`, never reused and never renumbered; a new capability takes the next number.
* **State:** `implemented` is code that is complete and tested on a computer, `prototype` is part of the capability, `planned` is not written.
* **Progress:** `done`, `partial`, `pending` (can be written without hardware) or `blocked` (waits for hardware or for another program of the suite).
* **Evidence:** `simulator` when the test runs against a fake process runner in place of the four updaters, `host-test` when it checks a calculation, a reader or a screen-less piece, `none` when nothing is written yet.
* **Test:** the acceptance criterion: `file::name` is the test `name` of `tests/file.py`; a name with a slash, such as `tools/file::name`, is the path from the root without the extension. The test must exist. For a capability that is not written the cell says `planned:` and the name of the test that will show it; the day that test exists, the row must change.
* **Limits:** what is not done or not proven; a row that is `partial` or `blocked` always says it.

The check is `tests/test_requirements.py`: it reads this table, finds each test and fails when a state, a test or a count does not agree.

## Dispatching to the updaters

| ID | Requirement | State | Progress | Evidence | Test | Limits |
|---|---|---|---|---|---|---|
| EHUP-001 | The registry holds exactly the four ecosystems of the family. | implemented | done | host-test | `test_main::test_ecosystems_registry_has_exactly_the_four_real_ecosystems` | - |
| EHUP-002 | `status` for one ecosystem runs the own module of that updater. | implemented | done | host-test | `test_main::test_status_for_one_ecosystem_runs_that_ecosystems_own_cli_module` | Against a fake runner; `status` has also run by hand on three ecosystems. |
| EHUP-003 | `--offline` is forwarded to the updater. | implemented | done | host-test | `test_main::test_status_offline_forwards_the_flag_to_the_sub_updater` | - |
| EHUP-004 | `status --ecosystem all` runs every ecosystem once and prints them in a fixed order. | implemented | done | host-test | `test_main::test_status_all_runs_every_ecosystem_once_and_prints_them_in_order` | - |
| EHUP-005 | The four checks of `status --ecosystem all` run at the same time. | implemented | done | host-test | `test_main::test_status_all_really_runs_the_four_at_the_same_time` | - |
| EHUP-006 | One failed ecosystem does not stop the others and is reported. | implemented | done | host-test | `test_main::test_status_all_never_stops_at_the_first_failure_and_reports_it` | - |
| EHUP-007 | `install` needs exactly one ecosystem and one project name. | implemented | done | host-test | `test_main::test_install_requires_exactly_one_project_name_and_one_ecosystem` | - |
| EHUP-008 | `update` goes to the right ecosystem with the project name. | implemented | done | host-test | `test_main::test_update_dispatches_to_the_right_ecosystem_with_the_project_name` | Against a fake runner; `update` has not been run for real. |
| EHUP-009 | `install` and `update` refuse `--ecosystem all`. | implemented | done | host-test | `test_main::test_install_and_update_reject_ecosystem_all` | - |
| EHUP-010 | A failing updater passes its own exit code on. | implemented | done | host-test | `test_main::test_a_real_failing_sub_updater_call_propagates_its_own_exit_code` | - |
| EHUP-011 | A project name that looks like an option is refused and nothing runs. | implemented | done | host-test | `test_main::test_a_project_name_that_looks_like_an_option_is_refused_and_nothing_runs` | - |
| EHUP-012 | The names of real repositories are accepted. | implemented | done | host-test | `test_main::test_the_names_of_real_repositories_are_accepted` | - |
| EHUP-013 | The workspace is the parent folder of the tool when it is not given, and it is always forwarded. | implemented | done | host-test | `test_main::test_workspace_defaults_to_this_projects_own_parent_directory_when_not_given` | - |
| EHUP-014 | No build is forwarded to every ecosystem, and a preview only where the updater has one. | implemented | done | host-test | `test_pins::test_preview_is_forwarded_only_where_the_updater_has_it` | - |

## Time limits

| ID | Requirement | State | Progress | Evidence | Test | Limits |
|---|---|---|---|---|---|---|
| EHUP-015 | An updater that hangs is stopped with a clear message. | implemented | done | host-test | `test_main::test_a_sub_updater_that_hangs_is_stopped_with_a_clear_message` | - |
| EHUP-016 | A run that times out stops the processes it started too. | implemented | done | host-test | `test_tree_timeout_and_bump::test_a_run_that_times_out_stops_the_processes_it_started_too` | - |
| EHUP-017 | A timeout of zero means no limit. | implemented | done | host-test | `test_main::test_a_zero_timeout_means_no_limit` | - |

## Versions and pins

| ID | Requirement | State | Progress | Evidence | Test | Limits |
|---|---|---|---|---|---|---|
| EHUP-018 | `versions` reports the installed versions and flags an updater that is behind GitHub. | implemented | done | host-test | `test_main::test_versions_reports_installed_and_flags_an_updater_behind_github` | - |
| EHUP-019 | `versions --offline` never contacts GitHub. | implemented | done | host-test | `test_main::test_versions_offline_never_contacts_github` | - |
| EHUP-020 | A version with fewer numbers is padded with zeros, so 0.8.0 is not behind 0.8.0.0. | implemented | done | host-test | `test_versions_padding::test_an_installed_0_8_0_is_not_behind_a_latest_0_8_0_0` | - |
| EHUP-021 | The pins of this very project are all read with their version. | implemented | done | host-test | `test_pins::test_the_pins_of_this_very_project_are_all_read` | - |
| EHUP-022 | A pin is behind only when a higher tag exists, and the pins command exits 2 then. | implemented | done | host-test | `test_pins::test_the_pins_command_exits_2_when_one_is_behind_and_0_otherwise` | - |
| EHUP-023 | A pin by an abbreviated commit is said and fails the strict check. | implemented | done | host-test | `test_pins::test_check_pins_strict_fails_for_an_abbreviated_commit` | - |
| EHUP-024 | The CI script never fails without a network and fails on a late pin only when strict. | implemented | done | host-test | `test_pins::test_the_ci_script_fails_on_a_late_pin_only_with_strict` | - |

## Window and languages

| ID | Requirement | State | Progress | Evidence | Test | Limits |
|---|---|---|---|---|---|---|
| EHUP-025 | With no arguments the window opens and with arguments the command line is used. | implemented | done | host-test | `test_main::test_without_arguments_the_window_is_opened_and_with_arguments_the_cli_is_used` | - |
| EHUP-026 | Every text of the window exists in the eight languages. | implemented | done | host-test | `test_main::test_the_window_texts_exist_in_all_eight_languages` | - |
| EHUP-027 | The placeholders of a text are the same in every language. | implemented | done | host-test | `test_more::test_the_placeholders_are_the_same_in_every_language_of_a_key` | - |
| EHUP-028 | The Portuguese is the one of Portugal. | implemented | done | host-test | `test_more::test_the_portuguese_is_the_one_of_portugal_where_it_differs_from_the_brazilian_one` | - |
| EHUP-029 | The log of the window is changed only on the window thread. | prototype | partial | host-test | `test_main::test_the_window_log_is_changed_only_on_the_window_thread` | The window is tested for its texts and its thread rules; nobody has looked at it on a screen on every system. |
| EHUP-030 | The runtime version is the version of the package. | implemented | done | host-test | `test_main::test_the_runtime_version_matches_the_one_of_the_package` | - |

## Not written yet

| ID | Requirement | State | Progress | Evidence | Test | Limits |
|---|---|---|---|---|---|---|
| EHUP-031 | `update` is run for real against a real checkout and the project is updated. | planned | blocked | none | `planned:real_update::an_update_runs_for_real_against_a_real_checkout` | Needs a real checkout and a person who accepts the confirmation of the updater. |
| EHUP-032 | The hand-over to the EH3D updater is run through this tool against a real checkout. | planned | blocked | none | `planned:real_eh3d::the_eh3d_updater_is_run_through_the_dispatcher_on_a_real_checkout` | Needs a real checkout of the EH3D repositories. |
| EHUP-033 | The window is looked at on a screen on each system and matches its reference picture. | planned | blocked | none | `planned:window_screen::the_window_matches_the_reference_picture` | Needs a person at a screen on each system. |
| EHUP-034 | The updater of A.R.M.O.R. is updated from this tool without breaking its installation. | planned | blocked | none | `planned:self_update::the_armor_updater_updates_without_breaking` | Waits for that updater to update itself safely. |
