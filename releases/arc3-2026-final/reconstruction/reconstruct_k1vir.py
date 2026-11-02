"""Reconstruct the exact submitted K1+VIR script from an authorized source carrier.

Uses only SQLite, ZIP and source-text operations. Does not import or execute the
reconstructed carrier, deserialize pickle objects, start serving or play games.
"""
from pathlib import Path
import argparse, base64, hashlib, io, json, sqlite3, zipfile, zlib

def digest(data):
    return hashlib.sha256(data).hexdigest()

def reconstruct(source_sqlite, output, resources=None):
    root=Path(resources) if resources else Path(__file__).resolve().parent
    plan=json.loads((root/'K1VIR_source_edits.json').read_text())
    target=Path(output)
    if target.exists():
        raise FileExistsError(f'Output already exists: {target}')
    uri=Path(source_sqlite).resolve().as_uri()+'?mode=ro'
    with sqlite3.connect(uri,uri=True) as db:
        row=db.execute('SELECT zip_bytes FROM source_payload WHERE id=1').fetchone()
    if row is None:
        raise ValueError('Missing source_payload.id=1')
    payload=row[0]
    if digest(payload)!=plan['source_zip_sha256']:
        raise ValueError('Source ZIP SHA-256 differs from the pinned carrier')
    template=(root/'K1VIR_carrier.py.template').read_text()
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        for f in plan['files']:
            raw=archive.read(f['path'])
            if digest(raw)!=f['base_sha256']:
                raise ValueError('Base source hash mismatch: '+f['path'])
            lines=raw.decode().splitlines(keepends=True)
            for edit in reversed(f['edits']):
                start=edit['start'];count=edit['delete']
                lines[start:start+count]=edit['insert'].splitlines(keepends=True)
            rebuilt=''.join(lines).encode()
            if digest(rebuilt)!=f['target_sha256']:
                raise ValueError('Reconstructed source hash mismatch: '+f['path'])
            encoded=base64.b64encode(zlib.compress(rebuilt,9)).decode()
            if template.count(f['placeholder'])!=1:
                raise ValueError('Missing or ambiguous template placeholder')
            template=template.replace(f['placeholder'],encoded)
    result=template.encode()
    if digest(result)!=plan['original_carrier_sha256']:
        raise ValueError('Reconstructed carrier differs from the submitted script')
    target.write_bytes(result)
    return dict(size_bytes=len(result),sha256=digest(result),source_verified=True,
                generated_carrier_executed=False)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-sqlite',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    print(json.dumps(reconstruct(args.source_sqlite,args.output)))

