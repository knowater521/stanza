"""
Tests for the run_pipeline.py script, also serves as integration test
"""

import re
import subprocess

from datetime import datetime
from tests import *

DOWNLOAD_TEST_DIR = f'{TEST_WORKING_DIR}/download'
FR_MODELS_DOWNLOAD_DIR = f'{DOWNLOAD_TEST_DIR}/{FR_SHORTHAND}_models'

RUN_PIPELINE_TEST_LANGUAGES = [AR_SHORTHAND, DE_SHORTHAND, FR_SHORTHAND, KK_SHORTHAND, KO_SHORTHAND]


def test_all_langs():
    for lang_shorthand in RUN_PIPELINE_TEST_LANGUAGES:
        run_pipeline_for_lang(lang_shorthand)


def run_pipeline_for_lang(lang_shorthand):
    input_file = f'{TEST_WORKING_DIR}/in/{lang_shorthand}.test.txt'
    output_file = f'{TEST_WORKING_DIR}/out/{lang_shorthand}.test.txt.out'
    gold_output_file = f'{TEST_WORKING_DIR}/out/{lang_shorthand}.test.txt.out.gold'
    download_dir = f'{DOWNLOAD_TEST_DIR}/{lang_shorthand}_models'
    # check input files present
    assert os.path.exists(input_file), f'Missing test input file: {input_file}'
    assert os.path.exists(gold_output_file), f'Missing test gold output file: {gold_output_file}'
    # verify models not downloaded and output file doesn't exist
    safe_rm(output_file)
    safe_rm(download_dir)
    # run french pipeline command and check results
    pipeline_cmd = \
        f"python -m stanfordnlp.run_pipeline -l fr -d {download_dir} --force-download -o {output_file} " \
        f"{input_file}"
    subprocess.call(pipeline_cmd, shell=True)
    # cleanup
    # log this test run's final output
    if os.path.exists(output_file):
        curr_timestamp = re.sub(' ', '-', str(datetime.now()))
        os.rename(output_file, f'{output_file}-{curr_timestamp}')
    safe_rm(download_dir)
    assert open(gold_output_file).read() == open(f'{output_file}-{curr_timestamp}').read(), \
        f'Test failure: output does not match gold'
