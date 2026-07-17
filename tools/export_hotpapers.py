"""Export only the fields displayed by the static Paper Signal page."""
import json
from pathlib import Path

SOURCE=Path(r"C:\Users\chenx\Desktop\ai1\20260717_hotpapers\workspaces\ACL-2026-main\papers.json")
TARGET=Path(__file__).resolve().parents[1]/"paper-signal"/"data"/"acl2026.json"
ALLOWED={"full_title","title_similarity","doi","arxiv_id","openreview_id"}
def verified(items):return[x for x in(items or[])if x.get("evidence")in ALLOWED and str(x.get("url","")).startswith("https://huggingface.co/")]
def export(p):
 r=p.get("result")or{};i=r.get("identity")or{};m=r.get("metrics")or{};g=m.get("github");hf=m.get("huggingface")or{}
 if not g or g.get("evidence")not in ALLOWED or not str(g.get("url","")).startswith("https://github.com/"):g=None
 return{"id":p.get("id"),"title":p.get("title"),"conference":p.get("conference"),"presentation_types":p.get("presentation_types")or[],"collected_at":r.get("collected_at"),"authors":i.get("authors")or[],"published":i.get("published"),"venue":i.get("venue"),"doi":i.get("doi"),"arxiv_id":i.get("arxiv_id"),"pdf_url":i.get("pdf_url"),"semantic_scholar_url":i.get("semantic_scholar_url"),"semantic_scholar_search_url":i.get("semantic_scholar_search_url"),"citations":m.get("citations"),"citation_status":m.get("citation_status"),"citation_sources":m.get("citation_sources")or[],"influential_citations":m.get("influential_citations"),"github":g,"huggingface_models":verified((hf.get("models")or{}).get("items")),"huggingface_datasets":verified((hf.get("datasets")or{}).get("items")),"scores":r.get("scores")or{},"score_note":r.get("score_note")}
papers=json.loads(SOURCE.read_text(encoding="utf-8"));TARGET.parent.mkdir(parents=True,exist_ok=True);TARGET.write_text(json.dumps([export(p)for p in papers],ensure_ascii=False,separators=(",",":")),encoding="utf-8");print(f"Exported {len(papers)} papers ({TARGET.stat().st_size:,} bytes)")
