import os
import zipfile



def zipdir(ziph, path, exclude=None):
    nlist = ziph.namelist()

    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            rel_dir = os.path.relpath(root, path)
            rel_file = os.path.join(rel_dir, file)
            abs_file = os.path.join(root, file)

            dirn = os.path.dirname(abs_file)

            if '__pycache__' in abs_file or '.log' in abs_file or (exclude and dirn in exclude):
                continue

            ziph.write(abs_file, rel_file)


# zip modules
for module_name in os.listdir('modules'):
    if module_name.startswith('__'):
        continue

    zipf = zipfile.ZipFile('mod.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(zipf, os.path.join('modules', module_name))
    zipf.close()
    os.replace('mod.zip', f'eme/_tools/modules/{module_name}.zip')

# zip main bundle:
for bundle_type in os.listdir('bundles'):

    zipf = zipfile.ZipFile('base.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(zipf, os.path.join('bundles', bundle_type))
    zipf.close()
    os.replace('base.zip', f'eme/_tools/content/_eme_bundle_{bundle_type}.zip')

try:
    os.remove('mod.zip')
    os.remove('base.zip')
except:
    pass
