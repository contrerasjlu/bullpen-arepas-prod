

	$(document).ready(function() {
	
		$('#calendar').fullCalendar({

			// THIS KEY WON'T WORK IN PRODUCTION!!!
			// To make your own Google API key, follow the directions here:
			// http://fullcalendar.io/docs/google_calendar/
			googleCalendarApiKey: 'AIzaSyC8Q7U0x2aqOQl4OrCcXPxUxeNTwdHe_PM',
		
			// US Holidays
			events: 'jocmyk@gmail.com',
			
			eventClick: function(event) {
				// opens events in a popup window
				window.open(event.url, 'gcalevent', 'width=700,height=600');
				return false;
			},
			
			loading: function(bool) {
				$('#loading').toggle(bool);
			}
			
		});
		
	});