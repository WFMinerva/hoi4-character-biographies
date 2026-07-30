from common import ROOT, load_json
s=load_json(ROOT/'audit/baselines/baseline_summary.json')
print('v130e baseline')
print('lite:',s['lite_zip'])
print('full:',s['full_zip'])
print('comparison:',s['normalized_comparison'])
