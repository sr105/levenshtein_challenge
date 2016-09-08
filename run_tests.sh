CMD=./levenshtein.py3
for i in `seq 1 5`; do
    diff -q <(${CMD} tests/input${i}) tests/output${i} >/dev/null 2>&1
    [ $? -eq 0 ] && result="PASS" || result="FAIL"
    printf "%2d: %s\n" $i $result
done
