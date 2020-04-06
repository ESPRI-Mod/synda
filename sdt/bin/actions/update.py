import sdcache


def run(args):
    print_stderr("Retrieving parameters from ESGF...")
    sdcache.run(reload=True, host=args.index_host, project=args.project)
    print_stderr("Parameters are up-to-date.")
