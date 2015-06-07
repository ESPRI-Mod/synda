##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

# Parse wget output to get more informations about the error

# notes
#  - this script is only intended to be sourced by sdget.sh script
#    (can't run on it's own, as no shebang included)
#  - sample parsed data available here => doc/WGET_403_FORBIDEN__2
#  - TODO: maybe use "case" and "esac" with wildchar to match HTTP code
#    this way, you don't depend on language variation
#    example: *403*) ...
#




# This gives something like:
#
# HTTP request sent, awaiting response... 302 Moved Temporarily
# HTTP request sent, awaiting response... 302 Moved Temporarily
# HTTP request sent, awaiting response... 403 Forbidden
#
http_response_code_list=`echo "$wget_stderr" | grep "^HTTP"`

# if some wget version, we have many messages all in one line, like this:
#
#  HTTP request sent, awaiting response... 403 Forbidden
#
# in that case, we remove the un-interesting prefix
#
http_response_code_list=`echo "$http_response_code_list" | sed -e 's/HTTP request sent, awaiting response... //g'`

# if some wget version, we have wget messages on separate line, like:
#
#  HTTP request sent, awaiting response... 
#  403 Forbidden
#
# in that case, we remove the un-interesting line
#
http_response_code_list=`echo "$http_response_code_list" | grep -v '^HTTP request sent, awaiting response... $'`

# count how many HTTP response we have
#
#
nbr=`echo "$http_response_code_list" | wc -l`

if [ $nbr -eq 3 ]; then
    # it means we were redirected to the ORP, then we get redirected on the datanode, then if failed

    # split
    #
    #
    data1_http_response_code=`echo "$http_response_code_list" | head -n 1`
    orp_http_response_code=`echo "$http_response_code_list" | head -n 2 | tail -n 1`
    data2_http_response_code=`echo "$http_response_code_list" | tail -n 1`

    # print
    if [ "x$DEBUG" = "xyes" ]; then
        echo $data1_http_response_code
        echo $orp_http_response_code
        echo $data2_http_response_code
    fi

    # wget / get_data.sh error mapping
    if [ "x$data2_http_response_code" = "x403 Forbidden" ]; then
        wget_error_status_from_parsing=20
    elif [ "x$data2_http_response_code" = "x200 OK" ]; then
        wget_error_status_from_parsing=0
    elif [ "x$data2_http_response_code" = "xRead error (Connection timed out) in headers." ]; then
        wget_error_status_from_parsing=21
    elif [ "x$data2_http_response_code" = "xRead error (Connection reset by peer) in headers." ]; then
        wget_error_status_from_parsing=28
    else
        wget_error_status_from_parsing=24

        msg "DEB001" "DEBUG BEGIN ($wget_error_status_from_parsing,$*)"     >> $debug_file
        echo "$wget_stderr"                                                 >> $debug_file
        msg "DEB002" "DEBUG END"                                            >> $debug_file
    fi

elif [ $nbr -eq 1 ]; then
    # it means it failed on the first HTTP request and no redirect occured

    data1_http_response_code=$http_response_code_list

    if [ "x$data1_http_response_code" = "x403 Forbidden" ]; then
        wget_error_status_from_parsing=22
    elif [ "x$data1_http_response_code" = "xRead error (Connection timed out) in headers." ]; then
        wget_error_status_from_parsing=25
    elif [ "x$data1_http_response_code" = "x200 OK" ]; then
        # this case happens !!
        # seems that sometime, there is no redirect to ORP at all !!
        # the file can be accessed directly, without security check..

        wget_error_status_from_parsing=0
    else
        wget_error_status_from_parsing=23

        msg "DEB003" "DEBUG BEGIN ($wget_error_status_from_parsing,$*)"  >> $debug_file
        echo "$wget_stderr"                                              >> $debug_file
        msg "DEB004" "DEBUG END"                                         >> $debug_file
    fi

elif [ $nbr -eq 2 ]; then
    # it means we were redirected to the ORP, then it failed on the ORP (and we never get redirected on the datanode)

    wget_error_status_from_parsing=26

    msg "DEB005" "DEBUG BEGIN ($wget_error_status_from_parsing,$*)"  >> $debug_file
    echo "$wget_stderr"                                              >> $debug_file
    msg "DEB006" "DEBUG END"                                         >> $debug_file

else
    # we shouldn't be here

    wget_error_status_from_parsing=27

    msg "DEB007" "DEBUG BEGIN ($wget_error_status_from_parsing,$*)"  >> $debug_file
    echo "$wget_stderr"                                              >> $debug_file
    msg "DEB008" "DEBUG END"                                         >> $debug_file

fi
