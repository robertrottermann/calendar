# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class calendar_google_handler(models.Model):
#     _name = 'calendar_google_handler.calendar_google_handler'
#     _description = 'calendar_google_handler.calendar_google_handler'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

# -*- coding: utf-8 -*-


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        TIME_FIELDS_IN_EVENT = ['start', 'stop',
                                'start_datetime', 'stop_datetime']
        result = super(CalendarEvent, self).read(fields, load)
        data = []
        tz = self.env.context and self.env.context.get('tz')
        if tz:
            tz = pytz.timezone(tz)
        for record in result:
            id_pair = str(record['id']).split('-')
            if (not record.get('allday')
                    and isinstance(record['id'], (str))
                    and tz and len(id_pair) > 1):
                delta = self.get_time_dst_delta(int(id_pair[0]), tz, record)
                if not delta:
                    data.append(record)
                    continue
                for field in TIME_FIELDS_IN_EVENT:
                    if field in record and record[field]:
                        record[field] = api_fields.Datetime.to_string(
                            api_fields.Datetime.from_string(
                                record[field]) + delta)
            data.append(record)
        return data

    @api.model
    def get_time_dst_delta(self, idx, tz, record):
        master_id = self.browse(idx)
        master_dst = tz.localize(api_fields.Datetime.from_string(
            master_id.start_datetime)).dst()
        current_dst = tz.localize(datetime.strptime(
            record['id'].split('-')[1], '%Y%m%d%H%M%S')).dst()
        delta = False
        if master_dst and not current_dst:
            delta = timedelta(hours=1)
        elif not master_dst and current_dst:
            delta = timedelta(hours=-1)
        return delta
