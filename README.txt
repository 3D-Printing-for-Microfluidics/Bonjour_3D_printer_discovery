
bonjour_service:		
	Broadcasts device information over mDNS
	(installed on all printers)

bonjour_js_server:	
	Discovers all broadcast devices and exposes current information with a json api
	(installed on always on raspberry pi server)

frontend_javascript:	
	javascript code that displays information fetched from bonjour_js_server's api
	(on wiki page)