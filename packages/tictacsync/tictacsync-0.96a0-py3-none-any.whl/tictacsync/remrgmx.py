def is_video(f):
    # True if name as video extension
    name_ext = f.split('.')
    if len(name_ext) != 2:
        return False
    name, ext = name_ext
    return ext.lower() in video_extensions

# def find_ISO_vids_pairs(top):
#     # top is 
vids = []
ISOs = []
for (root,dirs,files) in os.walk(Path('.'), topdown=True):
    for d in dirs:
        if d[-4:] == '_ISO':
            ISOs.append(Path(root)/d)
    for f in files:
        if is_video(f):
            vids.append(Path(root)/f)        
for pair in list(itertools.product(vids, ISOs)):
    # print(pair)
    matches = []
    vid, ISO = pair
    vidname, ext = vid.name.split('.')
    if vidname == ISO.name[:-4]:
        matches.append(pair)
    # print(vidname, ISO.name[:-4])
    # return matches
