import subprocess

def file_prefix(prog):
  return '{}-s{:02}e{:02}-{}'.format(
    prog['brand'],
    prog['series'],
    prog['episode'],
    prog['episode_title']
  )
  pass

def get_iplayer(prog, output_dir):
  subprocess.call([
    '/usr/bin/get-iplayer',
    '--type' ,'tv',
    '--pid', prog['pid'],
    '--file-prefix', file_prefix(prog),
    '--output', output_dir,
  ])
