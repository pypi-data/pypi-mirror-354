'''
 --- Get Archive Metadata ---
  - Extract data from archive files
  - Copied from elastic_scrapers/scraper_code
'''

import logging

logger = logging.getLogger(__name__)
from ceda_flight_pipeline.utils import logstream
logger.addHandler(logstream)
logger.propagate = False

from ceda_flight_pipeline.utils import jsonWrite

def addList(item,id):
    buffer = []
    try:
        if type(item[id]) != list:
            buffer = [item[id]]
        else:
            buffer = item[id]
    except:
        pass
    return buffer

class FlightConverter:
    def __init__(self, rootdir):
        
        self.rootdir = rootdir
        self.collection_dict = {}
        self.outdir = 'flight_catalog'

        self.scores = {}

    def convert(self):

        self.findFilesRecursive(self.rootdir, 0)

        #self.createCollections()
        #self.createCatalog()

        for score in sorted(self.scores.keys()):
            print(score, self.scores[score])

    def findFilesRecursive(self, directory, r):
        files = os.listdir(directory)
        print('Found {} items'.format(len(files)))
        for idx, f in enumerate(files):
            if r > 0:
                print(' -- ',end='')
            print(idx+1, len(files), f)
            if os.path.isdir(directory + '/' + f):
                self.findFilesRecursive(directory + '/' + f,1)
            else:
                if f.endswith('.json'):
                    filename = directory + '/' + f
                    fileout = f
                    self.convertFile(filename, fileout)

    def convertFile(self, filename, fileout):
        f = open(filename,'r')
        content = json.load(f)
        f.close()

        score = 0
        flight = content["_source"]

        id = filename.split('_flight_info')[0].split('/')[-1]

        try:
            org = flight["misc"]["organisation"]
        except:
            org = flight["file"]["path"].split('/')[2]

        if type(org) == list:
            org = '-'.join(org)

        try:
            pi = flight["misc"]["crew"]["principle"]
        except:
            try:
                pi = flight["misc"]["pi"]
            except:
                pi = ""
        
        if pi != '':
            score += 1

        try:
            airc = flight["misc"]["aircraft"]
        except:
            airc = ""
        
        if airc != "":
                score += 1

        variables = addList(flight["misc"],"variables")

        if variables != "" and variables != []:
            score += 1
        
        location = addList(flight["misc"],"location")

        if location != "" and location != []:
            score += 1

        try:
            platform = flight["misc"]["platform"]
        except:
            platform = ""

        if platform != "":
            score += 1

        instruments = addList(flight["misc"],"instruments")

        if instruments != "" and instruments != []:
            score += 1

        try:
            pcode = flight["misc"]["pcode"]
        except:
            pcode = id

        try:
            alt = flight["misc"]["altitude"]
        except:
            alt = ""

        if alt != "":
            score += 1

        stac_content = {
            "id": id,
            "type" : "Feature",
            "stac_version": "1.0.0",
            "stac_extensions":[""],

            "es_id":content["_id"],

            "description_path":flight["file"]["path"],

            "collection":org,

            "geometry": flight["spatial"]["geometries"],
            "properties":{
                "data_format":flight["data_format"]["format"],
                "start_datetime":flight["temporal"]["start_time"],
                "end_datetime": flight["temporal"]["end_time"],
                "flight_num":flight["misc"]["flight_num"],
                "pcode": pcode,
                "aircraft": airc,
                "altitude":alt,
                "variables": variables,
                "location": location,
                "platform": platform,
                "instruments": instruments,
                "principle": pi
            },
            "assets":{},
            "links":[]
        }

        coords = flight["spatial"]["geometries"]["display"]["coordinates"]
        non_emp = -1
        try:
            is_ne = False
            while not is_ne:
                non_emp += 1
                if len(coords[non_emp]) != 0:
                    is_ne = True

            if len(coords[non_emp]) == 2: # Line String
                coords_lat = np.array(coords)[:,0]
                coords_lon = np.array(coords)[:,1]
            else:
                stac_content["geometry"]["display"]["type"] = "MultiLineString"

                coords_lat = np.array(coords[non_emp])[:,0]
                coords_lon = np.array(coords[non_emp])[:,1]

                for x in range(non_emp+1,len(coords)):
                    cline = coords[x]
                    if len(cline) > 0:
                        cline_lat = np.array(cline)[:,0]
                        cline_lon = np.array(cline)[:,1]

                        coords_lat = np.concatenate((coords_lat, cline_lat))
                        coords_lon = np.concatenate((coords_lon, cline_lon))

        except KeyError:
            print('Issue')
            x=input()
        latmax = np.max(coords_lat)
        latmin = np.min(coords_lat)
        lonmax = np.max(coords_lon)
        lonmin = np.min(coords_lon)


        try:
            orgmeta = self.collection_dict[org]
            orgmeta['items'].append(id)

            if latmin < orgmeta['spatial_minmax'][0]:
                orgmeta['spatial_minmax'][0] = latmin
            if latmax > orgmeta['spatial_minmax'][1]:
                orgmeta['spatial_minmax'][1] = latmax
            if lonmin < orgmeta['spatial_minmax'][2]:
                orgmeta['spatial_minmax'][2] = lonmin
            if lonmax > orgmeta['spatial_minmax'][3]:
                orgmeta['spatial_minmax'][3] = lonmax

            tmin = [flight["temporal"]["start_time"], orgmeta['temporal_minmax'][0]]
            tmax = [flight["temporal"]["end_time"], orgmeta['temporal_minmax'][1]]

            orgmeta['temporal_minmax'] = [
                sorted(tmin)[0],
                sorted(tmax)[1]
            ]

            self.collection_dict[org] = orgmeta

        except KeyError:
            self.collection_dict[org] = {
                'items':[id],
                'spatial_minmax':[latmin, latmax, lonmin, lonmax], # min_lat ... max_lon
                'temporal_minmax':[
                    flight["temporal"]["start_time"],
                    flight["temporal"]["end_time"]
                    ]
            }

        try:
            self.scores[str(score)] += 1
        except:
            self.scores[str(score)] = 1

        jsonWrite('{}/collections/items/'.format(self.outdir), fileout, stac_content)

    def createCollections(self):

        for org in self.collection_dict.keys():

            orgmeta = self.collection_dict[org]

            desc = '{} Flight Collection'.format(org)
            cfile = "collections/{}.json".format(org)

            ## Build Links

            collection_links = [{
                    "rel":"self",
                    "href":cfile,
                    "type":"application/json",
                    "title":org
                }
            ]
            for id in orgmeta['items']:
                collection_links.append({
                    "rel":"item",
                    "href":"items/{}_flight_info.json".format(id), # Filename
                    "type":"application/json",
                    "title":id
                })

            collection = {
                "id":org,
                "type": "Collection",
                "stac_extensions": [
                    ""
                ],
                "stac_version":"1.0.0",
                "description": desc,
                "title": org,
                "providers": [],
                "extent": {
                    "spatial": {"bbox":[orgmeta['spatial_minmax']]},
                    "temporal":{"interval":[orgmeta['temporal_minmax']]}
                },
                "license":"", # Find this
                "summaries":{},
                "links":collection_links
            }

            jsonWrite(self.outdir,cfile, collection)

    def createCatalog(self):

        catalog_links = [
            {
                "rel":"self",
                "href":"./flight_catalog.json",
                "type":"application/json",
                "title":"Flight Catalog"
            }
        ]

        for org in self.collection_dict.keys():
            catalog_links.append({
                "rel":"child",
                "href":"collections/{}.json".format(org), # Filename
                "type":"application/json",
                "title":org
            })

        catalog = {
            "id":"Flight_Catalog",
            "type":"Catalog",
            "stac_version":"1.6.1",
            "stac_extensions":[""],
            "title":"Flight Catalog",
            "description": "Full catalog of flights for CEDA flight finder",
            "links":catalog_links
        }

        jsonWrite(self.outdir,"flight_catalog", catalog)

