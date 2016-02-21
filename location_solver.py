from utils.www_location_finder import LocationLookup
from utils.language_processor import find_chunk
from db_api.db_loc import LocCacheDB
import logging

logger = logging.getLogger(__name__)

class locationSolve:

    def __init__(self):
        self.loc_cache = LocCacheDB()
        self.loc_lookup = LocationLookup()
        pass

    def loc_solve_chooser(self,fc,postgq,ip):

        res = ''
        for (w,t) in postgq:
            if t == 'PRP' and w == 'I':
                data = self.loc_cache.get_ip_loc(ip)
                if not data:
                    logger.debug('querying www for %s' %ip)
                    data = self.loc_lookup.get_location_by_ip(ip)
                    if isinstance(data, dict):
                        data['qry'] = ip
                        logger.info('adding %s location to db' %ip )
                        self.loc_cache.insert_ip_loc(data)
                if data:    
                    if data['status'] == 'success':
                        res += 'city: ' + data.get('city','NA')+'\r\n<BR>'
                        res += 'region: '+ data.get('regionName','NA')+'\r\n<BR>'
                        res += 'country: ' + data.get('country','NA')+'\r\n<BR>'
                        #res += 'zip: ' + data.get('zip','NA')+'<BR>'
                        res += 'timezone: '+data.get('timezone','NA')+'\r\n<BR>'
                        #res += 'lat: '+ str(data['loc'][0])
                        #res += ',lon: '+ str(data['loc'][1])+'\r\n<BR>'

                    elif data['status'] == 'fail':
                        res += data.get('message','NA')
                else:
                    res += 'could not find your location'
            elif t == 'PRP' and w.lower() == 'you':
                res += 'I wish to be everywhere, but I am no where'

        if not res:
            srch_trm = find_chunk(postgq,'DCHUNK: <W.*><V.*><DT>*{<V.*>*<RB.*>*<JJ.*>*<N.*>*<RB>*}')
            data = ''
            if srch_trm:
                data = self.loc_cache.get_str_loc(srch_trm.lower())
            if srch_trm and not data:
                logger.debug('querying www for %s' %srch_trm.lower() )
                data = self.loc_lookup.get_location_by_str(srch_trm)
                if isinstance(data, dict):
                    data['qry'] = srch_trm.lower()
                    logger.info('adding %s to location db' %srch_trm.lower())
                    self.loc_cache.insert_str_loc(data)
            if data:
                res = data['display_name']
        if not res:    
            res = 'I do not have the location data yet'
        return res    

