from datetime import datetime, timedelta
import json
import logging
import os
import re
import pandas as pd
import time

from tabulate import tabulate

from nemo_library.features.focus import focusMoveAttributeBefore
from nemo_library.features.migman_database import MigManDatabaseLoad
from nemo_library.features.nemo_persistence_api import (
    createImportedColumns,
    createReports,
    createRules,
    getImportedColumns,
    getProjectID,
)
from nemo_library.features.nemo_persistence_api import createProjects
from nemo_library.features.nemo_report_api import LoadReport
from nemo_library.model.imported_column import ImportedColumn
from nemo_library.model.migman import MigMan
from nemo_library.model.project import Project
from nemo_library.model.report import Report
from nemo_library.model.rule import Rule
from nemo_library.utils.config import Config
from nemo_library.features.fileingestion import ReUploadDataFrame
from nemo_library.utils.migmanutils import (
    get_mig_man_field,
    get_migman_fields,
    get_migman_mandatory_fields,
    get_migman_postfixes,
    get_migman_project_list,
    getProjectName,
    is_migman_project_existing,
    DUPLICATE_CHECK_FIELDS,
)
from nemo_library.utils.utils import (
    get_internal_name,
    log_error,
)
from nemo_library.features.import_configuration import ImportConfigurations
from rapidfuzz import process, fuzz

__all__ = ["MigManLoadData"]


def MigManLoadData(
    config: Config,
    deficiency_mining_only: bool = False,
    fuzzy_matching: bool = True,
) -> None:
    """
    Main function to load data for MigMan projects.

    This function retrieves the configuration, checks for the existence of projects in the database,
    and processes data files for each project and its associated postfixes. If the project or columns
    are not defined in NEMO, they are created. Data is then uploaded, and deficiency mining reports
    are updated.

    Args:
        config (Config): Configuration object containing MigMan settings.

    Raises:
        ValueError: If a project is not found in the database.
    """
    # get configuration
    local_project_directory = config.get_migman_local_project_directory()
    multi_projects = config.get_migman_multi_projects()
    projects = get_migman_project_list(config)

    database = MigManDatabaseLoad()
    for project in projects:

        # check for project in database
        if not is_migman_project_existing(database, project):
            raise ValueError(f"project '{project}' not found in database")

        # get list of postfixes
        postfixes = get_migman_postfixes(database, project)

        # init project
        multi_projects_list = (
            (multi_projects[project] if project in multi_projects else None)
            if multi_projects
            else None
        )
        if multi_projects_list:
            for addon in multi_projects_list:
                for postfix in postfixes:
                    _load_data(
                        config,
                        database,
                        local_project_directory,
                        project,
                        addon,
                        postfix,
                        deficiency_mining_only,
                        fuzzy_matching,
                    )
        else:
            for postfix in postfixes:
                _load_data(
                    config,
                    database,
                    local_project_directory,
                    project,
                    None,
                    postfix,
                    deficiency_mining_only,
                    fuzzy_matching,
                )


def _load_data(
    config: Config,
    database: list[MigMan],
    local_project_directory: str,
    project: str,
    addon: str,
    postfix: str,
    deficiency_mining_only: bool = False,
    fuzzy_matching: bool = True,
) -> None:
    """
    Loads data for a specific project, addon, and postfix.

    This function checks for the existence of the data file, validates its contents,
    and uploads it to NEMO. It also creates missing columns and updates deficiency
    mining reports.

    Args:
        config (Config): Configuration object.
        database (list[MigMan]): List of MigMan database entries.
        local_project_directory (str): Path to the local project directory.
        project (str): Name of the project.
        addon (str): Addon name (optional).
        postfix (str): Postfix for the project.
    """
    # check for file first
    project_name = getProjectName(project, addon, postfix)
    file_name = os.path.join(
        local_project_directory,
        "srcdata",
        f"{project_name}.csv",
    )

    if os.path.exists(file_name):
        logging.info(
            f"File '{file_name}' for '{project}', addon '{addon}', postfix '{postfix}' found"
        )

        # does project exist? if not, create it
        new_project = False
        projectid = getProjectID(config, project_name)
        if not projectid:
            if deficiency_mining_only:
                log_error(
                    f"Project '{project_name}' not found in NEMO. Cannot run deficiency mining only mode."
                )
            new_project = True
            logging.info(f"Project not found in NEMO. Create it...")
            createProjects(
                config=config,
                projects=[
                    Project(
                        displayName=project_name,
                        description=f"Data Model for Mig Man table '{project}'",
                    )
                ],
            )

        # check whether file is newer than uploaded data
        time_stamp_file = datetime.fromtimestamp(os.path.getmtime(file_name)).strftime(
            "%d.%m.%Y %H:%M:%S"
        )
        if not new_project:
            df = LoadReport(
                config=config,
                projectname=project_name,
                report_name="static information",
            )
            if deficiency_mining_only:
                if df["TIMESTAMP_FILE"].iloc[0] != time_stamp_file:
                    log_error(
                        f"Project '{project_name}' is not up to date. Cannot run deficiency mining only mode."
                    )
            else:
                if df["TIMESTAMP_FILE"].iloc[0] == time_stamp_file:
                    logging.info(
                        f"file and data in NEMO has the same time stamp ('{time_stamp_file}'). Ignore this file"
                    )
                    return

        # read the file now and check the fields that are filled in that file
        datadf = pd.read_csv(
            file_name,
            sep=";",
            dtype=str,
        )

        # drop all columns that are totally empty
        columns_to_drop = datadf.columns[datadf.isna().all()]
        datadf_cleaned = datadf.drop(columns=columns_to_drop)
        if not columns_to_drop.empty:
            logging.info(
                f"totally empty columns removed. Here is the list {json.dumps(columns_to_drop.to_list(),indent=2)}"
            )

        # reconcile migman columns with columns from import file
        columns_migman = get_migman_fields(database, project, postfix)
        for col in datadf_cleaned.columns:
            if not col in columns_migman:
                log_error(
                    f"file {file_name} contains column '{col}' that is not defined in MigMan Template"
                )

        # check mandatory fields
        mandatoryfields = get_migman_mandatory_fields(database, project, postfix)
        for field in mandatoryfields:
            if not field in datadf_cleaned.columns:
                raise ValueError(
                    f"file {file_name} is missing mandatory field '{field}'"
                )

        ics_nemo = getImportedColumns(config, project_name)
        ics_import_names = [ic.importName for ic in ics_nemo]

        new_columns = []
        for col in datadf_cleaned.columns:

            # column already defined in nemo? if not, create it
            if not col in ics_import_names:
                logging.info(
                    f"column '{col}' not found in project {project_name}. Create it."
                )

                col_migman = get_mig_man_field(
                    database, project, postfix, columns_migman.index(col) + 1
                )

                if not col_migman:
                    log_error(
                        f"could nof find record in migman database for project '{project}', postfix '{postfix}' and index {columns_migman.index(col) + 1}"
                    )

                # Convert JSON data to a list of tuples
                table_data = [
                    (key, value if value else "<None>")
                    for key, value in col_migman.to_dict().items()
                ]

                # Print the table
                description = tabulate(
                    table_data,
                    headers=["Field", "Value"],
                    tablefmt="plain",
                    maxcolwidths=[35, 30],
                )
                new_columns.append(
                    ImportedColumn(
                        displayName=col_migman.nemo_display_name,
                        importName=col_migman.nemo_import_name,
                        internalName=col_migman.nemo_internal_name,
                        description=description,
                        dataType="string",
                        order=f"{(columns_migman.index(col) + 1):03}",
                    )
                )

        # check for duplicate columns
        if fuzzy_matching and project_name in DUPLICATE_CHECK_FIELDS:

            # it might happen that not every column defined in DUPLICATE_CHECK_FIELDS is present in the file
            doub_cols = [
                x
                for x in DUPLICATE_CHECK_FIELDS[project_name]
                if x in datadf_cleaned.columns
            ]

            # if there are no columns to check, we do not need to create the column
            if doub_cols:

                logging.info(
                    f"Project {project_name} has {len(doub_cols)} columns for duplicate check: {', '.join(doub_cols)}"
                )

                # Create a cleaned string for duplicate check from multiple columns
                datadf_cleaned["duplicate_check"] = (
                    datadf_cleaned[doub_cols]
                    .fillna("")  # replace NaN with empty string
                    .astype(str)
                    .apply(lambda x: " | ".join(x), axis=1)
                    .str.lower()  # normalize case
                    .apply(lambda s: re.sub(r"\s+", " ", s))  # normalize whitespace
                    .apply(
                        lambda s: re.sub(r"(\s*\|\s*)+", " | ", s)
                    )  # normalize separator spacing
                    .str.strip(" |")  # remove leading/trailing pipes and spaces
                )

                # Extract list of values to compare
                duplicate_values = datadf_cleaned["duplicate_check"].tolist()

                # check for duplicates now using fuzzy matching
                # Initialize result lists
                best_matches = []
                match_scores = []

                start_time = time.time()
                total = len(duplicate_values)

                # Loop over each value and find its best fuzzy match (excluding itself)
                for i, value in enumerate(duplicate_values):
                    if i % 100 == 0 and i > 0:
                        elapsed = time.time() - start_time
                        avg_time_per_item = elapsed / i
                        remaining = total - i
                        eta_seconds = avg_time_per_item * remaining
                        eta_time = datetime.now() + timedelta(seconds=eta_seconds)

                        logging.info(
                            f"Processing fuzzy match for value {i + 1}/{total} "
                            f"(ETA: {eta_time.strftime('%Y-%m-%d %H:%M:%S')})"
                        )

                    match = process.extractOne(
                        value,
                        duplicate_values[:i]
                        + duplicate_values[i + 1 :],  # exclude self
                        scorer=fuzz.token_sort_ratio,
                    )

                    if match:
                        best_matches.append(match[0])  # matched string
                        match_scores.append(match[1])  # similarity score
                    else:
                        best_matches.append(None)
                        match_scores.append(None)

                # Add the fuzzy match results to the original DataFrame
                datadf_cleaned["fuzzy_match_partner"] = best_matches
                datadf_cleaned["fuzzy_match_score"] = match_scores

                # Optional: add a boolean flag for likely duplicates based on a score threshold
                datadf_cleaned["is_potential_duplicate"] = (
                    datadf_cleaned["fuzzy_match_score"] >= 90
                )

        if new_columns:
            if deficiency_mining_only:
                log_error(
                    f"Project '{project_name}' has {len(new_columns)} new columns that are not defined in NEMO. Cannot run deficiency mining only mode."
                )
                return
            logging.info(
                f"Project {project_name} has {len(new_columns)} new columns that are not defined in NEMO. Create them now."
            )
            # create new columns in NEMO
            createImportedColumns(
                config=config,
                projectname=project_name,
                importedcolumns=new_columns,
            )

            # move columns into the right order
            logging.info(
                f"Project {project_name} has {len(new_columns)} new columns that are not defined in NEMO. Move them into the right order."
            )
            last_col = None
            for col in sorted(new_columns, key=lambda x: x.order, reverse=True):
                logging.info(
                    f"Move column {col.displayName} ({col.internalName}) into the right order"
                )
                focusMoveAttributeBefore(
                    config=config,
                    projectname=project_name,
                    sourceInternalName=col.internalName,
                    targetInternalName=last_col,
                )
                last_col = col.internalName

        # now we have created all columns in NEMO. Upload data
        if not deficiency_mining_only:
            datadf_cleaned["timestamp_file"] = time_stamp_file
            ReUploadDataFrame(
                config=config,
                projectname=project_name,
                df=datadf_cleaned,
                update_project_settings=False,
                version=3,
                datasource_ids=[{"key": "datasource_id", "value": project_name}],
                import_configuration=ImportConfigurations(
                    skip_first_rows=1,
                    record_delimiter="\n",
                    field_delimiter=";",
                    optionally_enclosed_by='"',
                    escape_character="\\",
                ),
            )

            _update_static_report(config=config, project_name=project_name)

        # if there are new columns, update all reports
        if deficiency_mining_only or new_columns:
            _update_deficiency_mining(
                config=config,
                project_name=project_name,
                postfix=postfix,
                columns_in_file=datadf_cleaned.columns,
                database=database,
            )
    else:
        logging.info(f"File {file_name} for project {project_name} not found")


def _update_static_report(
    config: Config,
    project_name: str,
) -> None:
    """
    Updates the static information report for a project.

    This report contains the latest timestamp of the uploaded file.

    Args:
        config (Config): Configuration object.
        project_name (str): Name of the project.
    """
    sql_query = """
SELECT  
    MAX(timestamp_file) AS timestamp_file
FROM 
    $schema.$table
WHERE
    not timestamp_file = 'timestamp_file'
"""
    createReports(
        config=config,
        projectname=project_name,
        reports=[
            Report(
                displayName="static information",
                querySyntax=sql_query,
                internalName="static_information",
                description="return static information",
            )
        ],
    )


def _update_deficiency_mining(
    config: Config,
    project_name: str,
    postfix: str,
    columns_in_file: list[str],
    database: list[MigMan],
) -> None:
    """
    Updates deficiency mining reports and rules for a project.

    This function generates column-specific and global deficiency mining reports
    based on the data file and MigMan database definitions.

    Args:
        config (Config): Configuration object.
        project_name (str): Name of the project.
        postfix (str): Postfix for the project.
        columns_in_file (list[str]): List of columns in the data file.
        database (list[MigMan]): List of MigMan database entries.
    """
    logging.info(
        f"Update deficiency mining reports and rules for project {project_name}"
    )

    # create column specific fragments
    frags_checked = []
    frags_msg = []
    joins = {}
    migman_fields = [
        x
        for x in database
        if x.project == project_name
        and x.postfix == postfix
        and x.nemo_import_name in columns_in_file
    ]
    for migman_field in migman_fields:

        frag_check = []
        frag_msg = []

        # data type specific checks
        match migman_field.desc_section_data_type.lower():
            case "character":
                # Parse format to get maximum length
                match = re.search(r"x\((\d+)\)", migman_field.desc_section_format)
                field_length = (
                    int(match.group(1))
                    if match
                    else len(migman_field.desc_section_format)
                )
                frag_check.append(
                    f"LENGTH({migman_field.nemo_internal_name}) > {field_length}"
                )
                frag_msg.append(
                    f"{migman_field.nemo_display_name} exceeds field length (max {field_length} digits)"
                )

            case "integer" | "decimal":
                format_str = migman_field.desc_section_format
                value = migman_field.nemo_internal_name

                # STEP 1: Handle optional minus sign based on format
                has_leading_minus = format_str.startswith("-")
                has_trailing_minus = format_str.endswith("-")
                minus_allowed = has_leading_minus or has_trailing_minus

                if not minus_allowed:
                    frag_check.append(f"INSTR({value}, '-') > 0")
                    frag_msg.append(
                        f"{migman_field.nemo_display_name} must not contain a minus sign (expected format: {format_str})"
                    )
                else:
                    if has_leading_minus:
                        frag_check.append(
                            f"(INSTR({value}, '-') > 0 AND LEFT({value}, 1) != '-')"
                        )
                        frag_msg.append(
                            f"{migman_field.nemo_display_name} must have minus sign only at the beginning if present (expected format: {format_str})"
                        )
                    elif has_trailing_minus:
                        frag_check.append(
                            f"(INSTR({value}, '-') > 0 AND RIGHT({value}, 1) != '-')"
                        )
                        frag_msg.append(
                            f"{migman_field.nemo_display_name} must have minus sign only at the end if present (expected format: {format_str})"
                        )

                # Clean value for further analysis
                value_stripped = f"REPLACE({value}, '-', '')"

                # STEP 2: Check allowed number of decimal places
                if "." in format_str:
                    decimals_allowed = sum(
                        1 for c in format_str.split(".")[1].lower() if c in ("z", "9")
                    )
                else:
                    decimals_allowed = 0

                if decimals_allowed == 0:
                    frag_check.append(f"INSTR({value_stripped}, ',') > 0")
                    frag_msg.append(
                        f"{migman_field.nemo_display_name} must not contain decimal places (expected format: {format_str})"
                    )
                else:
                    frag_check.append(
                        f"""LOCATE(',', {value_stripped}) > 0 AND 
                            LENGTH(RIGHT(
                                {value_stripped},
                                LENGTH({value_stripped}) - LOCATE(',', {value_stripped})
                            )) > {decimals_allowed}"""
                    )
                    frag_msg.append(
                        f"{migman_field.nemo_display_name} has too many decimal places (maximum {decimals_allowed} allowed; expected format: {format_str})"
                    )

                # STEP 3: Check number of digits before the decimal comma (excluding thousands separators)
                format_clean = format_str.replace("-", "")
                integer_format_part = format_clean.split(".")[0]
                digits_before_comma = sum(
                    1 for c in integer_format_part.lower() if c in ("z", "9")
                )

                cleaned = f"REPLACE(REPLACE(REPLACE({value_stripped}, ' ', ''), '.', ''), ',', '')"

                frag_check.append(
                    f"""LENGTH(
                        CASE 
                            WHEN LOCATE(',', {value_stripped}) > 0 
                            THEN LEFT({cleaned}, LOCATE(',', {value_stripped}) - 1)
                            ELSE {cleaned}
                        END
                    ) > {digits_before_comma}"""
                )
                frag_msg.append(
                    f"{migman_field.nemo_display_name} has too many digits before the decimal point (maximum {digits_before_comma} allowed; expected format: {format_str})"
                )

                # STEP 4: Check if the value matches a valid German number format
                # Format accepted: optional minus, digits with optional thousands separators (.), and optional decimal part (with comma)
                frag_check.append(
                    f"""NOT REPLACE({value}, '-', '') 
                    LIKE_REGEXPR('^[-]?([[:digit:]]+|[[:digit:]]{{1,3}}(\\.[[:digit:]]{{3}})*)(,[[:digit:]]+)?$')"""
                )
                frag_msg.append(
                    f"{migman_field.nemo_display_name} is not a valid number (expected German format, e.g. 1.234,56; format: {format_str})"
                )

            case "date":
                pattern = "^(0[1-9]|[1-2][0-9]|3[0-1])\\.(0[1-9]|1[0-2])\\.([0-9]{4})$"

                frag_check.append(
                    f"NOT {migman_field.nemo_internal_name} LIKE_REGEXPR('{pattern}')"
                )
                frag_msg.append(f"{migman_field.nemo_display_name} is not a valid date")

        # special fields

        if "mail" in migman_field.nemo_internal_name:
            frag_check.append(
                f"NOT {migman_field.nemo_internal_name} LIKE_REGEXPR('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{{2,}}$')"
            )
            frag_msg.append(f"{migman_field.nemo_display_name} is not a valid email")

        # VAT_ID
        if "s_ustid_ustid" in migman_field.nemo_internal_name:
            joins[migman_field.nemo_internal_name] = {"CLASSIFICATION": "VAT_ID"}
            frag_check.append(
                f"(genius_{migman_field.nemo_internal_name}.STATUS IS NOT NULL AND genius_{migman_field.nemo_internal_name}.STATUS = 'check')"
            )
            frag_msg.append(
                f"genius analysis: ' || genius_{migman_field.nemo_internal_name}.STATUS_MESSAGE || '"
            )
        # URL
        elif "s_adresse_homepage" in migman_field.nemo_internal_name:
            joins[migman_field.nemo_internal_name] = {"CLASSIFICATION": "URL"}
            frag_check.append(
                f"(genius_{migman_field.nemo_internal_name}.STATUS IS NOT NULL AND genius_{migman_field.nemo_internal_name}.STATUS = 'check')"
            )
            frag_msg.append(
                f"genius analysis: ' || genius_{migman_field.nemo_internal_name}.STATUS_MESSAGE || '"
            )

        # now build deficiency mining report for this column (if there are checks)
        if frag_check:

            # save checks and messages for total report
            frags_checked.extend(frag_check)
            frags_msg.extend(frag_msg)
            sorted_columns = [
                f'{migman_field.nemo_internal_name} AS "{migman_field.nemo_display_name}"'
            ] + [
                f'{other_field.nemo_internal_name} AS "{other_field.nemo_display_name}"'
                for other_field in database
                if other_field.project == project_name
                and other_field.postfix == postfix
                and other_field.index != migman_field.index
                and other_field.nemo_import_name in columns_in_file
            ]

            # case statements for messages and dm report
            case_statement_specific = " ||\n\t".join(
                [
                    f"CASE\n\t\tWHEN {check}\n\t\tTHEN CHAR(10) || '{msg}'\n\t\tELSE ''\n\tEND"
                    for check, msg in zip(frag_check, frag_msg)
                ]
            )

            status_conditions = " OR ".join(frag_check)

            sql_statement = f"""SELECT
\tCASE 
\t\tWHEN {status_conditions} THEN 'check'
\tELSE 'ok'
\tEND AS STATUS
\t,LTRIM({case_statement_specific},CHAR(10)) AS DEFICIENCY_MININNG_MESSAGE
\t,{',\n\t'.join(sorted_columns)}
FROM
\t$schema.$table
"""
            if migman_field.nemo_internal_name in joins:
                sql_statement += f"""LEFT JOIN
\t$schema.SHARED_NAIGENT genius_{migman_field.nemo_internal_name}
ON  
\t    genius_{migman_field.nemo_internal_name}.CLASSIFICATION = '{joins[migman_field.nemo_internal_name]["CLASSIFICATION"]}'
\tAND genius_{migman_field.nemo_internal_name}.VALUE          = {migman_field.nemo_internal_name}
"""

            # create the report
            report_display_name = f"(DEFICIENCIES) {migman_field.index:03} {migman_field.nemo_display_name}"
            report_internal_name = get_internal_name(report_display_name)

            createReports(
                config=config,
                projectname=project_name,
                reports=[
                    Report(
                        displayName=report_display_name,
                        internalName=report_internal_name,
                        querySyntax=sql_statement,
                        description=f"Deficiency Mining Report for column '{migman_field.nemo_display_name}' in project '{project_name}'",
                    )
                ],
            )

            createRules(
                config=config,
                projectname=project_name,
                rules=[
                    Rule(
                        displayName=f"DM_{migman_field.index:03}: {migman_field.nemo_display_name}",
                        ruleSourceInternalName=report_internal_name,
                        ruleGroup="02 Columns",
                        description=f"Deficiency Mining Rule for column '{migman_field.nemo_display_name}' in project '{project_name}'",
                    )
                ],
            )

        logging.info(
            f"project: {project_name}, column: {migman_field.nemo_display_name}: {len(frag_check)} frags added"
        )

    # now setup global dm report and rule
    case_statement_specific, status_conditions = _create_dm_rule_global(
        config=config,
        project_name=project_name,
        postfix=postfix,
        columns_in_file=columns_in_file,
        database=database,
        frags_checked=frags_checked,
        frags_msg=frags_msg,
        sorted_columns=sorted_columns,
        joins=joins,
    )

    # create report for mig man
    _create_report_for_migman(
        config=config,
        project_name=project_name,
        postfix=postfix,
        columns_in_file=columns_in_file,
        database=database,
        case_statement_specific=case_statement_specific,
        status_conditions=status_conditions,
        joins=joins,
    )

    # create report for the customer containing all errors
    _create_report_for_customer(
        config=config,
        project_name=project_name,
        postfix=postfix,
        columns_in_file=columns_in_file,
        database=database,
        case_statement_specific=case_statement_specific,
        status_conditions=status_conditions,
        joins=joins,
    )

    logging.info(f"Project {project_name}: {len(frags_checked)} checks implemented...")
    return len(frags_checked)


def _create_dm_rule_global(
    config: Config,
    project_name: str,
    postfix: str,
    columns_in_file: list[str],
    database: list[MigMan],
    frags_checked: list[str],
    frags_msg: list[str],
    sorted_columns: list[str],
    joins: dict[str, dict[str, str]],
) -> (str, str):  # type: ignore
    """
    Creates a global deficiency mining rule and report for a project.

    Args:
        config (Config): Configuration object.
        project_name (str): Name of the project.
        postfix (str): Postfix for the project.
        columns_in_file (list[str]): List of columns in the data file.
        database (list[MigMan]): List of MigMan database entries.
        frags_checked (list[str]): List of condition fragments for checks.
        frags_msg (list[str]): List of messages corresponding to checks.
        sorted_columns (list[str]): List of sorted columns for the report.
        joins (dict[str, dict[str, str]]): Join conditions for the report.

    Returns:
        tuple: Case statement and status conditions for the global rule.
    """
    # case statements for messages and dm report
    case_statement_specific = " ||\n\t".join(
        [
            f"CASE\n\t\tWHEN {check}\n\t\tTHEN  CHAR(10) || '{msg}'\n\t\tELSE ''\n\tEND"
            for check, msg in zip(frags_checked, frags_msg)
        ]
    )

    status_conditions = " OR ".join(frags_checked)

    sql_statement = f"""WITH CTEDefMining AS (
    SELECT
\t\t{',\n\t\t'.join([x.nemo_internal_name for x in database if x.project == project_name and x.postfix == postfix and x.nemo_display_name in columns_in_file])}
        ,LTRIM({case_statement_specific},CHAR(10)) AS DEFICIENCY_MININNG_MESSAGE
        ,CASE 
            WHEN {status_conditions} THEN 'check'
            ELSE 'ok'
        END AS STATUS
    FROM
        $schema.$table"""

    for join in joins:
        sql_statement += f"""
LEFT JOIN
\t$schema.SHARED_NAIGENT genius_{join}
ON  
\t    genius_{join}.CLASSIFICATION = '{joins[join]["CLASSIFICATION"]}'
\tAND genius_{join}.VALUE          = {join}"""

    sql_statement += f"""       
)
SELECT
      Status
    , DEFICIENCY_MININNG_MESSAGE
    , {',\n\t'.join(sorted_columns)}
FROM 
    CTEDefMining"""

    # create the report
    report_display_name = f"(DEFICIENCIES) GLOBAL"
    report_internal_name = get_internal_name(report_display_name)

    createReports(
        config=config,
        projectname=project_name,
        reports=[
            Report(
                displayName=report_display_name,
                internalName=report_internal_name,
                querySyntax=sql_statement,
                description=f"Deficiency Mining Report for  project '{project_name}'",
            )
        ],
    )

    createRules(
        config=config,
        projectname=project_name,
        rules=[
            Rule(
                displayName="Global",
                ruleSourceInternalName=report_internal_name,
                ruleGroup="01 Global",
                description=f"Deficiency Mining Rule for project '{project_name}'",
            )
        ],
    )

    return case_statement_specific, status_conditions


def _create_report_for_migman(
    config: Config,
    project_name: str,
    postfix: str,
    columns_in_file: list[str],
    database: list[MigMan],
    case_statement_specific: str,
    status_conditions: str,
    joins: dict[str, dict[str, str]],
) -> None:
    """
    Creates a report for MigMan containing valid data.

    Args:
        config (Config): Configuration object.
        project_name (str): Name of the project.
        postfix (str): Postfix for the project.
        columns_in_file (list[str]): List of columns in the data file.
        database (list[MigMan]): List of MigMan database entries.
        case_statement_specific (str): Case statement for deficiency messages.
        status_conditions (str): Conditions for status checks.
        joins (dict[str, dict[str, str]]): Join conditions for the report.
    """
    sql_statement = f"""WITH CTEDefMining AS (
    SELECT
        {',\n\t\t'.join([x.nemo_internal_name for x in database if x.project == project_name and x.postfix == postfix and x.nemo_display_name in columns_in_file])}
        ,LTRIM({case_statement_specific},CHAR(10)) AS DEFICIENCY_MININNG_MESSAGE
        ,CASE 
            WHEN {status_conditions} THEN 'check'
            ELSE 'ok'
        END AS STATUS
    FROM
        $schema.$table"""

    for join in joins:
        sql_statement += f"""
LEFT JOIN
\t$schema.SHARED_NAIGENT genius_{join}
ON  
\t    genius_{join}.CLASSIFICATION = '{joins[join]["CLASSIFICATION"]}'
\tAND genius_{join}.VALUE          = {join}"""

    sql_statement += f"""       
)
SELECT
    {',\n\t'.join([f"{x.nemo_internal_name} as \"{x.header_section_label}\"" for x in database if x.project == project_name and x.postfix == postfix and x.nemo_display_name in columns_in_file])}
FROM 
    CTEDefMining
WHERE
    STATUS = 'ok'
    """

    # create the report
    report_display_name = f"(MigMan) All records with no message"
    report_internal_name = get_internal_name(report_display_name)

    createReports(
        config=config,
        projectname=project_name,
        reports=[
            Report(
                displayName=report_display_name,
                internalName=report_internal_name,
                querySyntax=sql_statement,
                description=f"MigMan export with valid data for project '{project_name}'",
            )
        ],
    )


def _create_report_for_customer(
    config: Config,
    project_name: str,
    postfix: str,
    columns_in_file: list[str],
    database: list[MigMan],
    case_statement_specific: str,
    status_conditions: str,
    joins: dict[str, dict[str, str]],
) -> None:
    """
    Creates a report for customers containing invalid data.

    Args:
        config (Config): Configuration object.
        project_name (str): Name of the project.
        postfix (str): Postfix for the project.
        columns_in_file (list[str]): List of columns in the data file.
        database (list[MigMan]): List of MigMan database entries.
        case_statement_specific (str): Case statement for deficiency messages.
        status_conditions (str): Conditions for status checks.
        joins (dict[str, dict[str, str]]): Join conditions for the report.
    """
    sql_statement = f"""WITH CTEDefMining AS (
    SELECT
        {',\n\t\t'.join([x.nemo_internal_name for x in database if x.project == project_name and x.postfix == postfix and x.nemo_display_name in columns_in_file])}
        ,LTRIM({case_statement_specific},CHAR(10)) AS DEFICIENCY_MININNG_MESSAGE
        ,CASE 
            WHEN {status_conditions} THEN 'check'
            ELSE 'ok'
        END AS STATUS
    FROM
        $schema.$table"""

    for join in joins:
        sql_statement += f"""
LEFT JOIN
\t$schema.SHARED_NAIGENT genius_{join}
ON  
\t    genius_{join}.CLASSIFICATION = '{joins[join]["CLASSIFICATION"]}'
\tAND genius_{join}.VALUE          = {join}"""

    sql_statement += f"""       
)
SELECT
    DEFICIENCY_MININNG_MESSAGE,
    {',\n\t'.join([f"{x.nemo_internal_name} as \"{x.header_section_label}\"" for x in database if x.project == project_name and x.postfix == postfix and x.nemo_display_name in columns_in_file])}
FROM 
    CTEDefMining
WHERE
    STATUS <> 'ok'
"""

    # create the report
    report_display_name = f"(Customer) All records with message"
    report_internal_name = get_internal_name(report_display_name)

    createReports(
        config=config,
        projectname=project_name,
        reports=[
            Report(
                displayName=report_display_name,
                internalName=report_internal_name,
                querySyntax=sql_statement,
                description=f"export invalid data for project '{project_name}'",
            )
        ],
    )
