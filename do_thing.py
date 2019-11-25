import subprocess
import datetime
import os
import pytz

COMPARES = {
    "prd": ("master", "remotes/origin/stg"),
    "stg": ("master", "remotes/origin/stg"),
    "tst": ("remotes/origin/tst", "remotes/origin/stg")
}

os.environ["TZ"] = "UTC"


def get_git_diff_by_branch(from_branch, to_branch):
    output = subprocess.run(["git", "diff", "--name-status", "{}..{}".format(from_branch, to_branch)], stdout=subprocess.PIPE)
    output_data = output.stdout.decode("utf-8")
    output_data_lines = output_data.splitlines()
    out_lines_transform = map(lambda val: val.split("\t"), output_data_lines)
    print(list(out_lines_transform))


def get_git_file_modified_time(git_object):
    output = subprocess.run(["git", "log", "-1", "--format=\"%ad\"", "--", git_object], stdout=subprocess.PIPE)
    output_data = output.stdout.decode("utf-8").replace("\"", "").strip()
    print(output_data)
    parsed_date = datetime.datetime.strptime(output_data, "%a %b %d %H:%M:%S %Y %z")
    parsed_utc_date = parsed_date.astimezone(pytz.timezone("utc"))
    return parsed_utc_date


def get_git_diff_by_file_time(files_loc):
    output = subprocess.run(["git", "ls-tree", "-r", "--name-only", "remotes/origin/master", files_loc], stdout=subprocess.PIPE)
    output_data = output.stdout.decode("utf-8")
    print(output_data)
    data_lines = output_data.splitlines()
    data_lines_with_time = map(lambda val: (val, get_git_file_modified_time(val)), data_lines)
    return data_lines_with_time


def reduce_to_changes_less_than(files, interval_seconds=600):
    utc_now = datetime.datetime.utcnow().astimezone(pytz.timezone("utc"))

    def lambda_func(val):
        time_delta = utc_now - val[1]
        print(time_delta.seconds)

        if time_delta.seconds <= interval_seconds:
            return True
        else:
            return False

    return filter(lambda_func, files)


def map_changes_to_string(files):
    just_files = map(lambda val: val[0], files)
    return just_files


x = get_git_diff_by_file_time("tables")
y = reduce_to_changes_less_than(x)
print(list(y))
