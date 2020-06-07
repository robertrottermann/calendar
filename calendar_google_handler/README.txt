calendar_google_handler
-----------------------

git@github.com:robertrottermann/calendar.git

This module should create odoo-events from google calendar entries.
Depending on the calendar, different types of events should be created.
Also visibility of the events depends from what google calendar they where created.
Ideally when an event is created within odoo, it the corresponding google calendar
should be updated.

At the time-being there are the following Calendars:

CALENDARS = [
    '1 Öffentliche Veranstaltungen',
    '2 Interne Notizen',
    '3 Privatvermietungen',
    '4 Vorreservation',
    '6 BT Admin',
    '7 Tagesschule',
]
They are distinguished by the google-calendars “summary” field.
The list of calendars should be configurable

To link a google calendar entry to an odoo event, some fields are created:

   google_calendar_name = fields.Char() # summary field of the related google calendar
   google_calendar_id   = fields.Char() # id of the realted google calendar
   google_calendar_link = fields.Char() # html link of the google event


An event CAN have an owner. This is a res_users.id of a user, that can edit the event.
So we need also a one2many or one2one field ??? added to the event


