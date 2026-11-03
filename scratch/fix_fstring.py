p = "v3/imerg_daily_extremes_pipeline.py"
c = open(p, "r", encoding="utf-8").read()
c = c.replace('md = f"""# GPM IMERG', 'md = """# GPM IMERG')
open(p, "w", encoding="utf-8").write(c)
print("Updated successfully")
