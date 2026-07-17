#!/bin/bash
# Deep extraction of the canonical-action / semantic-convergence layer
OUT=semantic_layer_bundle
rm -rf $OUT && mkdir -p $OUT

echo "=== 1. Every file that touches the semantic layer ===" | tee $OUT/00_map.txt
grep -rln "canonical_action\|semantic_convergence\|canonical\b\|normalize\|evidence\[" \
  --include="*.py" . 2>/dev/null \
  | grep -v "venv\|__pycache__\|\.bak\|broken\|node_modules" \
  | tee -a $OUT/00_map.txt

echo "" >> $OUT/00_map.txt
echo "=== 2. Where canonical values are PRODUCED (writes) vs CONSUMED (reads) ===" >> $OUT/00_map.txt
grep -rn "canonical.*=" --include="*.py" pv_runtime/ pv_runtime_v2/ core_engine/ 2>/dev/null \
  | grep -v "venv\|__pycache__\|==" | head -40 >> $OUT/00_map.txt

echo "" >> $OUT/00_map.txt
echo "=== 3. Interfaces of the core semantic files ===" >> $OUT/00_map.txt
for f in intent_schema.py intent_binding.py intent_hash.py signal_schema.py \
         control_plane_normalize.py drift_detection_fixed.py \
         unstructured_intent_demo.py; do
  echo "--- $f ---" >> $OUT/00_map.txt
  grep -n "^def \|^class \|^    def " $f 2>/dev/null >> $OUT/00_map.txt
done

echo "" >> $OUT/00_map.txt
echo "=== 4. The EAV / convergence engine itself ===" >> $OUT/00_map.txt
find pv_runtime pv_runtime_v2 core_engine -name "*.py" 2>/dev/null \
  | xargs grep -ln "convergence\|canonical" 2>/dev/null >> $OUT/00_map.txt

# 5. Copy the actual sources (small files only, skip junk)
for f in $(grep -rln "canonical\|convergence\|normalize" --include="*.py" \
    intent_schema.py intent_binding.py intent_hash.py signal_schema.py \
    control_plane_normalize.py drift_detection_fixed.py \
    pv_runtime/ pv_runtime_v2/ core_engine/ 2>/dev/null \
    | grep -v "venv\|__pycache__\|\.bak\|broken" | sort -u); do
  size=$(wc -c < "$f" 2>/dev/null || echo 999999)
  if [ "$size" -lt 60000 ]; then
    mkdir -p "$OUT/$(dirname $f)"
    cp "$f" "$OUT/$f"
  fi
done

# 6. Include one real EAV output for ground truth
head -c 20000 decision_receipts.log > $OUT/sample_receipts.log 2>/dev/null

tar --exclude='.git' -czf semantic_layer_bundle.tar.gz $OUT
echo ""
echo "DONE: semantic_layer_bundle.tar.gz ($(du -h semantic_layer_bundle.tar.gz | cut -f1))"
echo "Files captured: $(find $OUT -name '*.py' | wc -l)"
echo "Upload semantic_layer_bundle.tar.gz to Claude for the deep review."
