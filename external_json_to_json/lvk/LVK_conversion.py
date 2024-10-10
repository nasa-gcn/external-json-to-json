alert_types = ["INITIAL", "UPDATE", "RETRACTION"]

def parse_lvc_json(lvc_json):
    schema_json = {"$schema" : "https://gcn.nasa.gov/schema/main/gcn/notices/lvk/alert.schema.json"}

    if lvc_json['alert_type'] in alert_types:
        schema_json['alert_type'] = lvc_json['alert_type'].lower()
    else:
        schema_json['alert_type']= None
    
    schema_json['alert_datetime'] = lvc_json['time_created']

    id = lvc_json['superevent_id']
    schema_json['id'] = [id]

    if schema_json['alert_type'] != 'retraction':
        schema_json['trigger_time'] = lvc_json['event']['time']

        schema_json['far'] = lvc_json['event']['far']
        schema_json['significant'] = lvc_json['event']['significant']

        detector_status = {}
        for detector in lvc_json['event']['instruments']:
            detector_status[detector] = 'triggered'

        schema_json['detector_status'] = detector_status

        schema_json['healpix_file'] = lvc_json['event']['skymap']
        schema_json['healpix_url'] = f"https://gracedb.ligo.org/api/superevents/{id}/files/bayestar.multiorder.fits,0"

        schema_json['search'] = lvc_json['event']['search']
        group = lvc_json['event']['group']
        schema_json['group'] = group
        schema_json['pipeline'] = lvc_json['event']['pipeline']


        if group == "Burst":
            schema_json['duration'] = lvc_json['event']['duration']
            schema_json['central_frequency'] = lvc_json['event']['central_frequency']
        else:
            schema_json['duration'] = None
            schema_json['central_frequency'] = None

        schema_json['properties'] = lvc_json['event']['properties']
        schema_json['classification'] = lvc_json['event']['classification']

    schema_json['external_coincidence'] = lvc_json['external_coinc']
    
    return schema_json
