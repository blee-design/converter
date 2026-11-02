#
# Regular cron jobs for the converter package.
#
0 4	* * *	root	[ -x /usr/bin/converter_maintenance ] && /usr/bin/converter_maintenance
