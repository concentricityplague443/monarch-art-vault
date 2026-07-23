#!/usr/bin/env python3
import argparse, csv, hashlib, json, mimetypes, shutil
from datetime import datetime, timezone
from pathlib import Path

def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024), b''): h.update(block)
    return h.hexdigest()

def image_data(path):
    out={'pixel_width':None,'pixel_height':None,'exif_capture_date':None}
    try:
        from PIL import Image, ExifTags
        with Image.open(path) as im:
            out['pixel_width'],out['pixel_height']=im.size
            exif=im.getexif()
            lookup={v:k for k,v in ExifTags.TAGS.items()}
            dt=exif.get(lookup.get('DateTimeOriginal')) or exif.get(lookup.get('DateTime'))
            out['exif_capture_date']=str(dt) if dt else None
    except Exception: pass
    return out

def main():
    p=argparse.ArgumentParser(description='Create a non-destructive Monarch Art Vault inventory.')
    p.add_argument('source'); p.add_argument('--managed-root',default='ArtLibrary'); p.add_argument('--run-id',default=None)
    args=p.parse_args(); source=Path(args.source).resolve(); root=Path(args.managed_root).resolve()
    run=args.run_id or 'RUN-'+datetime.now().strftime('%Y%m%d-%H%M%S')
    archive=root/'01_Archive_Originals'/str(datetime.now().year)/run; catalog=root/'02_Catalog'; reports=root/'99_Reports'
    archive.mkdir(parents=True,exist_ok=True); catalog.mkdir(parents=True,exist_ok=True); reports.mkdir(parents=True,exist_ok=True)
    files=[x for x in source.rglob('*') if x.is_file()] if source.is_dir() else [source]
    seen={}; rows=[]
    for i,path in enumerate(files,1):
        digest=sha256(path); rel=path.name if source.is_file() else str(path.relative_to(source))
        dest=archive/rel; dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists(): shutil.copy2(path,dest)
        rec={'asset_id':f'AST-{datetime.now().year}-{i:04d}','run_id':run,'source_path':str(path),'archived_path':str(dest),'filename':path.name,'bytes':path.stat().st_size,'mime_type':mimetypes.guess_type(path.name)[0] or 'application/octet-stream','sha256':digest,'classification':'exact_duplicate' if digest in seen else 'unique','canonical_asset_id':seen.get(digest),'ingested_at':datetime.now(timezone.utc).isoformat(),**image_data(path)}
        seen.setdefault(digest,rec['asset_id']); rows.append(rec)
    manifest=reports/f'{run}_source-manifest.json'; manifest.write_text(json.dumps(rows,indent=2))
    csv_path=catalog/f'{run}_inventory.csv'
    with csv_path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys() if rows else ['asset_id']); w.writeheader(); w.writerows(rows)
    print(json.dumps({'run_id':run,'assets':len(rows),'exact_duplicates':sum(x['classification']=='exact_duplicate' for x in rows),'manifest':str(manifest),'inventory':str(csv_path)},indent=2))
if __name__=='__main__': main()
