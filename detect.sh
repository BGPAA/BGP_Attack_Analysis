if [ $# -eq 0 ] || [ $1 == '-h' ]; then
    printf "=== USAGE :\n\n   Execution on specific file :\n./detect.sh <zipped MRT_file_path>\n\n   Download and execution of the newest update from RIPE :\n./detect.sh -new\n\n   Execution and generate graph of all.routes.json :\n./detect.sh (-new | <mrt_file.gz>) -graph\n\n   Execution on a given time window (time format = 'YYYY-mm-DD_HH:MM', data will be downloaded from RIPE) and generate graph :\n./detect.sh -timewindow <start_time> <end_time>\n\nTo start loading the job automatically after each 5min update from RIPE, and store results in 'archives', add this to your crontab :\n*/5 * * * * ./detect.sh -new\n\n===\n"
    exit 0

elif [ $1 == '-timewindow' ]; then
    if [ $# -eq 3 ]; then
        source tabi-master/ve-tabi/bin/activate
        # python script to retrieve data from RIPE and compute all json files from TaBi.
        python timewindow.py $2 $3
        printf "EXECUTION : done. Check results in 'output' folder.\n"
        mv output/no_name/all.routes.json.gz archives/$(date '+%Y-%m-%d_%H:%M:%S')_timewindow_routes.json.gz
        mv output/no_name/all.hijacks.json.gz archives/$(date '+%Y-%m-%d_%H:%M:%S')_timewindow_hijacks.json.gz
        python graph-master/route_graph_complex.py output/no_name/all.routes.json output/no_name/all.hijacks.json
        rm -f output/no_name/*.json
	deactivate
        exit 0
    else
        printf "Wrong arguments. Time format = 'YYYY-mm-DD_HH:MM'. Usage :\n./detect.sh -timewindow <start_time> <end_time>\n"
        exit 1
    fi

elif [ $1 == '-new' ] || test -f "$1"; then
    source tabi-master/ve-tabi/bin/activate
    log="output/log.txt"
    cur="output/current_mrt_file"
    # MAX STORED EXEC SET TO 3456 (6 days of compute, ~2Go). Change the '+x' below if needed
    if ! [ $(ls archives | tail +3457) -z ]; then
        cd archives && ls | tail -n +3457 | xargs rm
        cd ..
    fi
    rm -f output/no_name/*.json
    rm -f output/no_name/*.gz
    rm -f output/graph.png
    echo " " > $log
    echo " " > $cur
    if [ $1 == '-new' ]; then
        python download_newest.py
        file=tabi-master/input/rrc21/$(ls -t tabi-master/input/rrc21/ | head -1)
        gzip -dkc $file > $cur
    else
        gzip -dkc $1 > $cur
    fi
    ./mabo-master/mabo dump "$cur" > "$log" & tabi -d -f -j8 rrc21 output/ "$log"
    rm -f output/log.txt
    deactivate
    printf "EXECUTION : done. Check results in 'output' folder.\n"
    cp output/no_name/all.routes.json.gz archives/$(date '+%Y-%m-%d_%H:%M:%S')_routes.json.gz
    cp output/no_name/all.hijacks.json.gz archives/$(date '+%Y-%m-%d_%H:%M:%S')_hijacks.json.gz

    #python3 alerting/alert_discord.py
    printf "ALERTING : discord bot displayed the detected hijacks.\n"

    if ! [ -z "$2" ] && [ $2 == '-graph' ]; then
        source tabi-master/ve-tabi/bin/activate
	gzip -dk output/no_name/all.routes.json.gz
        gzip -dk output/no_name/all.hijacks.json.gz
        python graph-master/route_graph_complex.py output/no_name/all.routes.json output/no_name/all.hijacks.json
	rm -f output/no_name/*.json
	deactivate
    fi
    exit 0
else
    printf "No such file: '$1'. Please enter a valid file path.\n"
fi
exit 1
