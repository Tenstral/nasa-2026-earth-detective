target_file = "v3/gldas_multi_model_processor.py"
c = open(target_file, "r", encoding="utf-8").read()
bad_str = 'plt.suptitle("Bengal Basin Multi-Model Storage Partitioning: GRACE vs GLDAS (Noah 2.1, VIC 2.1, CLSM 2.2)\n"\n                 "PRELIMINARY — Team Tenstral | NASA Space Apps Challenge 2026", fontsize=12, fontweight="bold")'
good_str = 'plt.suptitle("Bengal Basin Multi-Model Storage Partitioning: GRACE vs GLDAS (Noah 2.1, VIC 2.1, CLSM 2.2)\\nPRELIMINARY — Team Tenstral | NASA Space Apps Challenge 2026", fontsize=12, fontweight="bold")'
c = c.replace(bad_str, good_str)
open(target_file, "w", encoding="utf-8").write(c)
print("Suptitle fixed")
