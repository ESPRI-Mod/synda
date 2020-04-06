import sdremoteparam, sdutils, sdproxy_ra


def run(args):
    # currently, mode (list or show) is determined by
    # parameter existency. This may change in the future
    # as it may be useful to list variable based on filter
    # (e.g. list variable long name only for obs4MIPs
    # project, etc..). To do that, we will need to
    # add an 'action' argument (i.e. list and show).
    #
    action = 'show' if len(args.parameter) > 0 else 'list'

    if action == 'list':

        if args.long_name:
            facet = 'variable_long_name'
        elif args.short_name:
            facet = 'variable'
        elif args.standard_name:
            facet = 'cf_standard_name'
        else:
            # no options set by user

            facet = 'variable_long_name'  # default

        params = sdremoteparam.run(pname=facet, dry_run=args.dry_run)

        if not args.dry_run:

            # This try/except block is to prevent
            # IOError: [Errno 32] Broken pipe
            # Other way to prevent it is to ignore SIGPIPE
            # More info at
            # http://stackoverflow.com/questions/14207708/ioerror-errno-32-broken-pipe-python
            try:

                # TODO: func for code below
                items = params.get(facet)
                for item in items:
                    print(item.name)

            except:
                pass

    elif action == 'show':

        # We do not use inference here, instead we use
        # search-api 'query' feature to do the job.
        #
        query = sdutils.parameter_to_query(args.parameter)
        file_ = sdproxy_ra.get_one_file(query=query, dry_run=args.dry_run)

        if not args.dry_run:

            if file_ is None:

                print('Variable not found.')

            else:

                print('short name:       ', file_['variable'][0])
                print('standard name:    ', file_['cf_standard_name'][0])
                print('long name:        ', file_['variable_long_name'][0])
                print('unit:             ', file_['variable_units'][0])
