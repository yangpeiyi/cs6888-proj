In this example, We'll be testing pydotplus. Its modified source code is stored in ./pydotplus_modified_source_code, and We included 202 .dot files as seeds in ./dots
All commands are to be run under the project directory, unless specified.

0.install all python packages listed in requirments.txt and graphviz by runnning:
pip install -r requirements.txt
apt install graphviz

1. Modify source code of pydotplus
Find out where your pydotplus is installed by running:
pip show pydotplus
For example:
/home/ubuntu/.local/lib/python3.8/site-packages.
Replace all .py files in /home/ubuntu/.local/lib/python3.8/site-packages/pydotplus with the .py files provides in pydotplus_modified_source_code. 
There are 4 .py files in total in pydotplus. We'll ignore __init__.py and version.py in the following steps, because they are not essential.

2. Generte call graph by running:
pyan3 {path to pydotplus}/pydotplus/graphviz.py {path to pydotplus}/pydotplus/parser.py --uses --no-defines --colored --grouped --annotated --dot > pydotplus.dot
For example:
pyan3 /home/ubuntu/.local/lib/python3.8/site-packages/pydotplus/graphviz.py /home/ubuntu/.local/lib/python3.8/site-packages/pydotplus/parser.py --uses --no-defines --colored --grouped --annotated --dot > pydotplus.dot

2. for each .py file in the source code, generate a coverage files (.xml)
mkdir xmls
coverage run --branch {path to pydotplus}/pydotplus/graphviz.py
coverage xml
mv coverage.xml graphviz.xml && mv graphviz.xml ./xmls
coverage run --branch {path to pydotplus}/pydotplus/parser.py
coverage xml
mv coverage.xml parser.xml && mv parser.xml ./xmls

For example:
mkdir xmls
coverage run --branch /home/ubuntu/.local/lib/python3.8/site-packages/pydotplus/graphviz.py
coverage xml
mv coverage.xml graphviz.xml && mv graphviz.xml ./xmls
coverage run --branch /home/ubuntu/.local/lib/python3.8/site-packages/pydotplus/parser.py
coverage xml
mv coverage.xml parser.xml && mv parser.xml ./xmls

3. generate trace for each seed by running:
python3 generate_trace.py

4. Top/Our Approach: process trace files, and put top N% seeds into its coresponding folder (N_top_seeds)
Modify calculate_seed_scores.py, replace line 4-5 accordingly and run:
python3 calculate_seed_scores.py

5. Peach Set: For each seed, calculate its coverage, then sort and put top N% seeds into its coresponding folder (N_peach_seeds)
Modify peach_calculate_coverage.py, replace line 13 accordingly and run:
python3 peach_calculate_coverage.py

6. Random Set & Comparison
A driver, pydouplus_main.py for the fuzzor has already been provided. 
Finally, compare the 3 algorithms by running the fuzzor for 30s with N varying from 10 to 90, and write the results into top_peach_random_results.txt by runnning:
bash run.sh

7. If you would like to test other programs, the "## pydotplus config" section in each .py files needs to be modified accordingly.

8. How to read top_peach_random_results.txt

10                                                          -> 10% seeds used
['top/10_top_seeds']                                        -> using Top 
#0 READ units: 20
#1 NEW     cov: 0 corp: 20 exec/s: 7 rss: 64.6484375 MB 
#2 NEW     cov: 1910 corp: 21 exec/s: 58 rss: 64.78515625 MB
#3 NEW     cov: 1959 corp: 22 exec/s: 12 rss: 64.9921875 MB
....
#69 NEW     cov: 2101 corp: 32 exec/s: 10 rss: 73.7109375 MB
#73 NEW     cov: 2103 corp: 33 exec/s: 9 rss: 73.7109375 MB -> at last round of fuzzing, coverage reach 2103, before decting a crash
  subgraph cluster1 {                                       -> crash found
                     ^
Expected "}", found '{'  (at char 206), (line:13, col:21)
    struct3 [shape=record,label="hello\nworld\n\
....
ValueError: not enough values to unpack (expected 2, got 1)
crash was written to crash-faa763633c916e68576c6e5576bd3a7d2f72674e39102d7749a3efbb98ddc577
