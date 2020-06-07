# -*- coding: utf-8 -*-

import pytz
from datetime import datetime, timedelta
from odoo import api, models, fields as api_fields

"""
a typical google event:
-----------------------
[events[0]
{'kind': 'calendar#event',
 'etag': '"3182958133483000"',
 'id': 'fhra33tjs4rab4fui9v0lamegk',
 'status': 'confirmed',
 'htmlLink': 'https://www.google.com/calendar/event?eid=ZmhyYTMzdGpzNHJhYjRmdWk5djBsYW1lZ2sgcm9iZXJ0QHJlZGNvci5jaA',
 'created': '2020-06-06T11:08:35.000Z',
 'updated': '2020-06-07T07:53:38.090Z',
 'summary': 'Fuss-Wasch-Zeremonie',
 'creator': {'email': 'robert@redcor.ch',
             'displayName': 'robert rottermann',
             'self': True},
 'organizer': {'email': 'robert@redcor.ch',
               'displayName': 'robert rottermann',
               'self': True},
 'start': {'dateTime': '2020-06-07T10:00:00+02:00', 'timeZone': 'UTC'},
 'end': {'dateTime': '2020-06-07T13:00:00+02:00', 'timeZone': 'UTC'},
 'visibility': 'public',
 'iCalUID': 'fhra33tjs4rab4fui9v0lamegk@google.com',
 'sequence': 0,
 'attendees': [{'email': 'robert@redo2oo.ch',
                'displayName': 'Robert Rottermann',
                'responseStatus': 'accepted'},
               {'email': 'info@breitsch-traeff.ch',
                'displayName': 'Administrator',
                'responseStatus': 'accepted'}],
 'hangoutLink': 'https://meet.google.com/cpq-jssy-fhs',
 'conferenceData': {'createRequest': {'requestId': 'p8jntak5lit3ke4770b7tr1vu4',
                                      'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                                      'status': {'statusCode': 'success'}},
                    'entryPoints': [{'entryPointType': 'video',
                                     'uri': 'https://meet.google.com/cpq-jssy-fhs',
                                     'label': 'meet.google.com/cpq-jssy-fhs'},
                                    {'regionCode': 'US',
                                     'entryPointType': 'phone',
                                     'uri': 'tel:+1-563-538-1087',
                                     'label': '+1 563-538-1087',
                                     'pin': '892036486'}],
                    'conferenceSolution': {'key': {'type': 'hangoutsMeet'},
                                           'name': 'Google Meet',
                                           'iconUri': 'https://lh5.googleusercontent.com/proxy/bWvYBOb7O03a7HK5iKNEAPoUNPEXH1CHZjuOkiqxHx8OtyVn9sZ6Ktl8hfqBNQUUbCDg6T2unnsHx7RSkCyhrKgHcdoosAW8POQJm_ZEvZU9ZfAE7mZIBGr_tDlF8Z_rSzXcjTffVXg3M46v'},
                    'conferenceId': 'cpq-jssy-fhs',
                    'signature': 'ADR/mfMiP3E3rOtYHpJazlA+HQt2'},
 'reminders': {'useDefault': False}}

"""

from cal import get_events_for_summary, CALENDARS

class CalendarGoogleHandler(models.Model):
    _name = 'calendar_google_handler.calendar_google_handler'
    _description = 'calendar_google_handler.calendar_google_handler'

    _inherit = 'event.event'

    google_calendar_name = fields.Char() # summary field of the related google calendar
    google_calendar_id   = fields.Char() # id of the realted google calendar
    google_calendar_link = fields.Char() # html link of the google event
    # an event can have an owner. Then this owner is allowed to edit it
    owner_ids = fields.One2many(
        string='Event Owner',
        comodel_name='res.users',
        inverse_name='inverse_field',  # <---------------- please fix
    )

    def create_event(self, event):
        """create an odoo event, set values according the evnt

        Args:
            event (dict): a dictionary describing a google event
        """
        pass

    def sync_events(self, which_one='all'):
        """ reach out to google to get a list of upcomming events
            and create odoo events for them

        Args:
            which_one (str, optional): a comma separated list of calendars to updat. Defaults to 'all'.
        """
        if which_one == 'all':
            for calendar in CALENDARS:
                events = get_events_for_summary(calendar)
                for event in events:
                    self.create_event(evnt)